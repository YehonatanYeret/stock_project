using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json.Linq;
using Server.Gateways.Interfaces;
using System;
using System.Threading.Tasks;

namespace Server.Controllers.Queries
{
    [Route("api/transaction/query")]
    [ApiController]
    public class TransactionQueryController : ControllerBase
    {
        private readonly IStocksGateway _polygonGateway;

        public TransactionQueryController(IStocksGateway polygonGateway)
        {
            _polygonGateway = polygonGateway;
        }

        /// <summary>
        /// Gets aggregate stock data for a given ticker symbol and date range.
        /// </summary>
        /// <param name="ticker">The ticker symbol</param>
        /// <param name="startDate">The start date of the date range</param>
        /// <param name="endDate">The end date of the date range</param>
        /// <returns>Aggregate data for the given ticker symbol and date range</returns>
        [HttpGet("getDetails")]
        public async Task<ActionResult> GetAggregateData(string ticker, string startDate, string endDate)
        {
            try
            {
                // Validate input parameters
                if (string.IsNullOrWhiteSpace(ticker) || string.IsNullOrWhiteSpace(startDate) || string.IsNullOrWhiteSpace(endDate))
                {
                    return BadRequest("Ticker, startDate, and endDate are required.");
                }

                // Fetch data in parallel
                var aggregateDataTask = _polygonGateway.GetAggregateDataAsync(ticker, startDate, endDate);
                var metadataTask = _polygonGateway.GetTickerMetadataAsync(ticker);

                await Task.WhenAll(aggregateDataTask, metadataTask);

                var aggregateData = await aggregateDataTask;
                var metadata = await metadataTask;

                // Handle cases where the ticker is invalid or data is missing
                if (aggregateData == null || aggregateData["queryCount"]?.Value<int>() == 0)
                {
                    return NotFound(new { message = $"Ticker '{ticker}' not found." });
                }

                if (metadata == null)
                {
                    return NotFound(new { message = $"Metadata for ticker '{ticker}' not found." });
                }

                // Fetch image only if a logo URL exists
                string imageBase64 = await _polygonGateway.GetTickerImageBase64Async(metadata.Logo, ticker);

                // Build response
                var response = new
                {
                    metadata.Ticker,
                    metadata.Name,
                    metadata.Description,
                    LogoBase64 = imageBase64,
                    AggregateData = aggregateData?.ToString(Newtonsoft.Json.Formatting.None)
                };
                return Ok(response);
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Error in GetAggregateData: {ex.Message}");
                return StatusCode(500, new { message = "An internal error occurred.", error = ex.Message });
            }
        }
    }
}
