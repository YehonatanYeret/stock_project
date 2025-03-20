using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Gateways.Interfaces;
using Server.Models;
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
    /// Get all holdings for a specific user reconstructed from trade logs.
    /// </summary>
    [HttpGet("holdings/{userId}")]
    public async Task<ActionResult<List<HoldingDto>>> GetUserHoldings(int userId)
    {
        var trades = await _context.Logs
            .Where(t => t.UserId == userId)
            .OrderBy(t => t.Date) // Ensure chronological order
            .ToListAsync();

        if (!trades.Any())
        {
            return NotFound(new { message = "No trades found for this user." });
        }

        var holdings = trades
            .GroupBy(t => t.Symbol)
            .Select(g =>
            {
                var symbol = g.Key;
                var totalQuantity = 0m;
                var totalCost = 0m;

                foreach (var trade in g)
                {
                    if (trade.Type == Enums.historyType.Buy)
                    {
                        totalQuantity += trade.Quantity;
                        totalCost += trade.Quantity * trade.Price;
                    }
                    else if (trade.Type == Enums.historyType.Sell)
                    {
                        totalQuantity -= trade.Quantity;
                        totalCost -= trade.Quantity * trade.Price; // Not used for cost basis, but useful for tracking
                    }
                }

                var averageBuyPrice = totalQuantity > 0 ? totalCost / totalQuantity : 0;

                return new
                {
                    Symbol = symbol,
                    Quantity = totalQuantity,
                    BuyPrice = averageBuyPrice
                };
            })
            .Where(h => h.Quantity > 0) // Filter out fully sold stocks
            .ToList();

        var holdingsDto = new List<HoldingDto>();

        foreach (var holding in holdings)
        {
            holdingsDto.Add(await CalculateHoldingDto(holding.Symbol, holding.Quantity, holding.BuyPrice));
        }

        return Ok(holdingsDto);
    }

    /// <summary>
    /// Helper method to calculate HoldingDto from trade logs.
    /// </summary>
    private async Task<HoldingDto> CalculateHoldingDto(string symbol, decimal quantity, decimal buyPrice)
    {
        decimal currentPrice = await _polygonGateway.GetSellPriceAsync(symbol) ?? 0;
        decimal totalValue = quantity * currentPrice;
        decimal totalGain = (currentPrice - buyPrice) * quantity;
        decimal totalGainPercentage = buyPrice > 0 ? (totalGain / (buyPrice * quantity)) * 100 : 0;

        return new HoldingDto
        {
            Symbol = symbol,
            Quantity = quantity,
            CurrentPrice = currentPrice,
            TotalValue = totalValue,
            TotalGain = totalGain,
            TotalGainPercentage = totalGainPercentage
        };
    }

    /// <summary>
    /// Get all trade history for a specific user.
    /// </summary>
    [HttpGet("trades/{userId}")]
    public async Task<ActionResult<List<TradingDto>>> GetUserTrades(int userId)
    {
        var trades = await _context.Logs
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
    /// Returns the cash balance for a specific user.
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
        return Ok(user.CashBalance);
    }

    /// <summary>
    /// Returns the profit and loss for a specific user.
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
