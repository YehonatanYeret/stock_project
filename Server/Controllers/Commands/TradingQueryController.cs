//using Microsoft.AspNetCore.Mvc;
//using MediatR;
//using Server.DTOs;
//using Server.Queries;
//using System.Collections.Generic;
//using System.Threading.Tasks;

//namespace Server.Controllers;

//[Route("api/trading/query")]
//[ApiController]
//public class TradingQueryController : ControllerBase
//{
//    private readonly IMediator _mediator;

//    public TradingQueryController(IMediator mediator)
//    {
//        _mediator = mediator;
//    }

//    /// <summary>
//    /// Get all holdings for a specific user.
//    /// </summary>
//    [HttpGet("holdings/{userId}")]
//    public async Task<ActionResult<List<HoldingDto>>> GetUserHoldings(int userId)
//    {
//        var query = new GetUserHoldingsQuery(userId);
//        var result = await _mediator.Send(query);
//        return Ok(result);
//    }

//    /// <summary>
//    /// Get all trade history for a specific user.
//    /// </summary>
//    [HttpGet("trades/{userId}")]
//    public async Task<ActionResult<List<TradeDto>>> GetUserTrades(int userId)
//    {
//        var query = new GetUserTradesQuery(userId);
//        var result = await _mediator.Send(query);
//        return Ok(result);
//    }
//}
