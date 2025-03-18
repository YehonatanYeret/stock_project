using Microsoft.AspNetCore.Mvc;
using Server.Data;
using Server.Models;
using Microsoft.EntityFrameworkCore;
using Server.Gateways.Interfaces;
using Server.Models.Domain;
using Server.Models.DTOs.Commands;
using Server.Utils;

namespace Server.Controllers.Commands;

[Route("api/transaction/command")]
[ApiController]
public class TransactionCommandController : Controller
{
    private readonly StockContext _context;
    private readonly IStocksGateway _polygonGateway;

    public TransactionCommandController(StockContext context, IStocksGateway polygonGateway)
    {
        _context = context;
        _polygonGateway = polygonGateway;
    }

    // POST: api/transaction/command/sell
    [HttpPost("sell")]
    public async Task<ActionResult> Sell([FromBody] SellRequest model)
    {
        if (model.HoldingId == 0 || model.Quantity == 0)
        {
            return BadRequest(new { message = "HoldingId and Quantity are required." });
        }

        try
        {
            // Find the holding by HoldingId
            Holding? holding = await _context.Holdings
                .FirstOrDefaultAsync(h => h.Id == model.HoldingId);

            if (holding is null)
            {
                return BadRequest(new { message = "Holding not found." });
            }

            // Check if the user has enough shares to sell
            if (holding.Quantity < model.Quantity)
            {
                return BadRequest(new { message = "Not enough shares to sell." });
            }

            // Fetch current price from Polygon API using the PolygonGateway
            decimal currentPrice = await _polygonGateway.GetSellPriceAsync(holding.Symbol, model.SellDate);

            // Calculate profit/loss
            decimal profitLoss = (currentPrice - holding.BuyPrice) * model.Quantity;

            // Update the holding quantity
            holding.Quantity -= model.Quantity;

            // If the holding quantity becomes 0, remove it from the holdings
            if (holding.Quantity == 0)
            {
                _context.Holdings.Remove(holding);
            }

            // Log the trade in the Trades table as a sell
            var trade = new Trade
            {
                UserId = holding.UserId,
                Symbol = holding.Symbol,
                Date = model.SellDate,
                Type = Enums.historyType.Sell,
                Quantity = model.Quantity,
                Price = currentPrice
            };

            _context.Trades.Add(trade);

            // Update the user's profit and portfolio value
            User user = _context.Users.FirstOrDefault(u => u.Id == holding.UserId)!;

            // The profit/loss is added to the user's profit and the portfolio value is updated by the amount of the sale
            user.Profit += profitLoss;
            user.CashBalance = PortfolioValueUtils.CalculatePortfolioValue(user.CashBalance, currentPrice * model.Quantity);

            await _context.SaveChangesAsync();

            return Ok(new { message = "Sell trade completed successfully.", profitLoss });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { message = $"An error occurred during sell transaction: {ex.Message}" });
        }
    }


    // POST: api/transaction/command/buy
    [HttpPost("buy")]
    public async Task<ActionResult> Buy([FromBody] BuyRequest model)
    {
        if (string.IsNullOrWhiteSpace(model.Symbol) || model.Quantity <= 0)
        {
            return BadRequest(new { message = "Symbol and Quantity are required." });
        }

        try
        {
            // Fetch the current stock price from Polygon API
            decimal currentPrice = await _polygonGateway.GetSellPriceAsync(model.Symbol, model.BuyDate);

            User? user = _context.Users.FirstOrDefault(u => u.Id == model.UserId);
            if (user is null)
            {
                return BadRequest(new { message = "User not found." });
            }

            // Check if the user has enough funds to buy and update the portfolio value
            decimal cost = model.Quantity * currentPrice;
            user.CashBalance = PortfolioValueUtils.CalculatePortfolioValue(user.CashBalance, -cost);


            // Find existing holding for the user and stock
            Holding? holding = await _context.Holdings
                .FirstOrDefaultAsync(h => h.UserId == model.UserId && h.Symbol == model.Symbol);

            if (holding is not null)
            {
                // Update existing holding (average buy price)
                decimal totalCost = holding.Quantity * holding.BuyPrice + cost;
                holding.Quantity += model.Quantity;
                holding.BuyPrice = totalCost / holding.Quantity; // New average price
            }
            else
            {
                // Create new holding
                holding = new Holding
                {
                    UserId = model.UserId,
                    Symbol = model.Symbol,
                    Quantity = model.Quantity,
                    BuyPrice = currentPrice
                };
                _context.Holdings.Add(holding);
            }

            // Log the trade in the Trades table as a buy
            var trade = new Trade
            {
                UserId = model.UserId,
                Symbol = model.Symbol,
                Date = model.BuyDate,
                Type = Enums.historyType.Buy,
                Quantity = model.Quantity,
                Price = currentPrice
            };

            _context.Trades.Add(trade);

            await _context.SaveChangesAsync();

            return Ok(new { message = "Buy trade completed successfully.", holdingId = holding.Id });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { message = $"An error occurred during buy transaction: {ex.Message}" });
        }
    }

}
