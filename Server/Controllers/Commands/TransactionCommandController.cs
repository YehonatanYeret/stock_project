using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Gateways.Interfaces;
using Server.Models;
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
    [HttpPost("sell/{userId}")]
    public async Task<ActionResult> Sell(int userId, [FromBody] TransactionRequest model)
    {
        if (string.IsNullOrEmpty(model.Ticker) || model.Quantity <= 0)
        {
            return BadRequest(new { message = "Ticker and Quantity are required." });
        }

        try
        {
            // Get user's trade history for this stock
            var tradeHistory = await _context.Logs
                .Where(t => t.UserId == userId && t.Symbol == model.Ticker)
                .ToListAsync();

            if (!tradeHistory.Any())
            {
                return BadRequest(new { message = "No holdings found for this stock." });
            }

            // Calculate available shares
            decimal totalSharesOwned = tradeHistory
                .Where(t => t.Type == Enums.historyType.Buy)
                .Sum(t => t.Quantity) -
                tradeHistory
                .Where(t => t.Type == Enums.historyType.Sell)
                .Sum(t => t.Quantity);

            if (totalSharesOwned < model.Quantity)
            {
                return BadRequest(new { message = "Not enough shares to sell." });
            }

            // Fetch current price from Polygon API
            decimal? currentPrice = await _polygonGateway.GetSellPriceAsync(model.Ticker);
            if (currentPrice == null)
            {
                return BadRequest(new { message = "Stock not found or Api limit exceeded" });
            }

            // Calculate total cost of owned shares
            decimal totalBuyCost = tradeHistory
                .Where(t => t.Type == Enums.historyType.Buy)
                .Sum(t => t.Quantity * t.Price);

            decimal averageBuyPrice = totalSharesOwned > 0 ? totalBuyCost / totalSharesOwned : 0;
            decimal profitLoss = ((decimal)currentPrice - averageBuyPrice) * model.Quantity;

            // Log the sale
            var sellTrade = new Log
            {
                UserId = userId,
                Symbol = model.Ticker,
                Date = model.Date,
                Type = Enums.historyType.Sell,
                Quantity = model.Quantity,
                Price = (decimal)currentPrice
            };

            _context.Logs.Add(sellTrade);

            // Update user's cash balance and profit
            var user = await _context.Users.FirstOrDefaultAsync(u => u.Id == userId);
            if (user == null)
            {
                return BadRequest(new { message = "User not found." });
            }

            user.CashBalance += model.Quantity * (decimal)currentPrice;
            user.Profit += profitLoss;

            await _context.SaveChangesAsync();

            return Ok(new { message = "Sell trade completed successfully.", sellTrade });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { message = $"An error occurred during sell transaction: {ex.Message}" });
        }
    }

    // POST: api/transaction/command/buy
    [HttpPost("buy/{userId}")]
    public async Task<ActionResult> Buy(int userId, [FromBody] TransactionRequest model)
    {
        if (string.IsNullOrWhiteSpace(model.Ticker) || model.Quantity <= 0)
        {
            return BadRequest(new { message = "Ticker and Quantity are required." });
        }

        try
        {
            // Fetch the current stock price from Polygon API
            var currentPrice = await _polygonGateway.GetSellPriceAsync(model.Ticker);
            if(currentPrice == null)
            {
                return BadRequest(new { message = "Stock not found or Api limit exceeded" });
            }

            // Fetch user
            var user = await _context.Users.FirstOrDefaultAsync(u => u.Id == userId);
            if (user == null)
            {
                return BadRequest(new { message = "User not found." });
            }

            // Check if user has enough funds
            decimal totalCost = model.Quantity * (decimal)currentPrice;
            if (user.CashBalance < totalCost)
            {
                return BadRequest(new { message = "Insufficient funds." });
            }

            // Deduct cash balance
            user.CashBalance -= totalCost;

            // Log the buy trade
            var buyTrade = new Log
            {
                UserId = userId,
                Symbol = model.Ticker,
                Date = model.Date,
                Type = Enums.historyType.Buy,
                Quantity = model.Quantity,
                Price = (decimal)currentPrice
            };

            _context.Logs.Add(buyTrade);
            await _context.SaveChangesAsync();

            return Ok(new { message = "Buy trade completed successfully.", buyTrade });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { message = $"An error occurred during buy transaction: {ex.Message}" });
        }
    }
}
