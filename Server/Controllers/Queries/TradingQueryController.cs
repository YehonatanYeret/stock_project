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
    private readonly IPolygonGateway _polygonGateway;

    public TradingQueryController(StockContext context, IPolygonGateway polygonGateway)
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
    /// Get a single holding by ID.
    /// </summary>
    [HttpGet("holding/{holdingId}")]
    public async Task<ActionResult<HoldingDto>> GetHoldingById(int holdingId)
    {
        var holding = await _context.Holdings.FirstOrDefaultAsync(h => h.Id == holdingId);

        if (holding == null)
        {
            return NotFound(new { message = "Holding not found." });
        }

        return Ok(await CalculateHoldingDto(holding));
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
    /// Get a single trade by ID.
    /// </summary>
    [HttpGet("trade/{tradeId}")]
    public async Task<ActionResult<TradingDto>> GetTradeById(int tradeId)
    {
        var trade = await _context.Trades
            .Where(t => t.Id == tradeId)
            .Select(t => new TradingDto
            {
                Symbol = t.Symbol,
                Date = t.Date,
                Type = t.Type,
                Quantity = t.Quantity,
                Price = t.Price
            })
            .FirstOrDefaultAsync();

        if (trade == null)
        {
            return NotFound(new { message = "Trade not found." });
        }

        return Ok(trade);
    }

    /// <summary>
    /// Helper method to calculate HoldingDto from Holding entity.
    /// </summary>
    private async Task<HoldingDto> CalculateHoldingDto(Holding holding)
    {
        decimal currentPrice = await _polygonGateway.GetSellPriceAsync(holding.Symbol, DateTime.UtcNow);
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
}
