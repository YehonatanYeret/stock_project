using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Gateways.Interfaces;
using Server.Models.Domain;
using Server.Models.DTOs.Queries;

namespace Server.Controllers;

[Route("api/trading/query")]
[ApiController]
public class TradingQueryController : ControllerBase
{
    private readonly StockContext _context;
    private readonly IStocksGateway _polygonGateway;

    public TradingQueryController(StockContext context, IStocksGateway polygonGateway)
    {
        _context = context;
        _polygonGateway = polygonGateway;
    }

    /// <summary>
    /// Get all holdings for a specific user.
    /// </summary>
    [HttpGet("holdings/{userId}")]
    public async Task<ActionResult<List<HoldingDto>>> GetUserHoldings(int userId)
    {
        var holdings = await _context.Holdings
            .Where(h => h.UserId == userId)
            .ToListAsync();

        if (!holdings.Any())
        {
            return NotFound(new { message = "No holdings found for this user." });
        }

        var holdingsDto = new List<HoldingDto>();

        foreach (var holding in holdings)
        {
            holdingsDto.Add(await CalculateHoldingDto(holding));
        }

        return Ok(holdingsDto);
    }

    /// <summary>
    /// Get all trade history for a specific user.
    /// </summary>
    [HttpGet("trades/{userId}")]
    public async Task<ActionResult<List<TradingDto>>> GetUserTrades(int userId)
    {
        var trades = await _context.Trades
            .Where(t => t.UserId == userId)
            .Select(t => new TradingDto
            {
                Symbol = t.Symbol,
                Date = t.Date,
                Type = t.Type,
                Quantity = t.Quantity,
                Price = t.Price
            })
            .ToListAsync();

        if (!trades.Any())
        {
            return NotFound(new { message = "No trades found for this user." });
        }

        return Ok(trades);
    }

    /// <summary>
    /// Helper method to calculate HoldingDto from Holding entity.
    /// </summary>
    private async Task<HoldingDto> CalculateHoldingDto(Holding holding)
    {
        decimal currentPrice = await _polygonGateway.GetSellPriceAsync(holding.Symbol) ?? 0;
        decimal totalValue = holding.Quantity * currentPrice;
        decimal totalGain = (currentPrice - holding.BuyPrice) * holding.Quantity;
        decimal totalGainPercentage = holding.BuyPrice > 0 ? (totalGain / (holding.BuyPrice * holding.Quantity)) * 100 : 0;

        return new HoldingDto
        {
            Id = holding.Id,
            Symbol = holding.Symbol,
            Quantity = holding.Quantity,
            CurrentPrice = currentPrice,
            TotalValue = totalValue,
            TotalGain = totalGain,
            TotalGainPercentage = totalGainPercentage
        };
    }

    /// <summary>
    /// return the amount of cashbalace for a specific user
    /// </summary>
    [HttpGet("cashbalance/{userId}")]
    public async Task<ActionResult<decimal>> GetCashBalance(int userId)
    {
        var user = await _context.Users
            .FirstOrDefaultAsync(u => u.Id == userId);
        if (user is null)
        {
            return NotFound(new { message = "User not found." });
        }
        Console.WriteLine(user.CashBalance);
        return Ok(user.CashBalance);
    }

    ///<summary>
    ///return the profit and loss for a specific user
    /// </summary>
    [HttpGet("profit/{userId}")]
    public async Task<ActionResult<decimal>> GetProfit(int userId)
    {
        var user = await _context.Users
            .FirstOrDefaultAsync(u => u.Id == userId);
        if (user is null)
        {
            return NotFound(new { message = "User not found." });
        }
        return Ok(user.Profit);
    }
}
