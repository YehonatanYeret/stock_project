using Microsoft.AspNetCore.Mvc;
using Server.Gateways.Implementations;
using Server.Gateways.Interfaces;

namespace Server.Controllers.Queries
{
    [Route("api/transaction/query")]
    [ApiController]
    public class TransactionQueryController : ControllerBase
    {
        private readonly IPolygonGateway _polygonGateway;

        public TransactionQueryController(IPolygonGateway polygonGateway)
        {
            _polygonGateway = polygonGateway;
        }

        /// <summary>
        /// the method will get the aggregate data for a given ticker symbol and date range
        /// </summary>
        /// <param name="ticker">the ticker symbol</param>
        /// <param name="startDate"> the start date of the date range</param>
        /// <param name="endDate"> the end date of the date range</param>
        /// <returns> the aggregate data for the given ticker symbol and date range</returns>
        [HttpGet("getDetails")]
        public async Task<ActionResult> GetAggregateData(string ticker, string startDate, string endDate)
        {
            if (string.IsNullOrEmpty(ticker) || string.IsNullOrEmpty(startDate) || string.IsNullOrEmpty(endDate))
            {
                return BadRequest("Ticker, startDate, and endDate are required.");
            }

            var result = await _polygonGateway.GetAggregateDataAsync(ticker, startDate, endDate);
            return Ok(result);
        }
    }
}
