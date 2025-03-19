using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
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
        private readonly ILogger<TransactionQueryController> _logger;

        public TransactionQueryController(IStocksGateway polygonGateway, ILogger<TransactionQueryController> logger)
        {
            _polygonGateway = polygonGateway ?? throw new ArgumentNullException(nameof(polygonGateway));
            _logger = logger ?? throw new ArgumentNullException(nameof(logger));
        }

        /// <summary>
        /// Gets aggregate stock data for a given ticker symbol and date range.
        /// </summary>
        /// <param name="ticker">The ticker symbol</param>
        /// <param name="startDate">The start date of the date range</param>
        /// <param name="endDate">The end date of the date range</param>
        /// <returns>Aggregate data for the given ticker symbol and date range</returns>
        [HttpGet("getDetails")]
        public async Task<IActionResult> GetAggregateData([FromQuery] string ticker, [FromQuery] string startDate, [FromQuery] string endDate)
        {
            if (string.IsNullOrWhiteSpace(ticker) || string.IsNullOrWhiteSpace(startDate) || string.IsNullOrWhiteSpace(endDate))
            {
                return BadRequest(new { message = "Ticker, startDate, and endDate are required." });
            }

            try
            {
                // Fetch data in parallel
                var aggregateDataTask = _polygonGateway.GetAggregateDataAsync(ticker, startDate, endDate);
                var metadataTask = _polygonGateway.GetTickerMetadataAsync(ticker);
                var currentPriceTask = _polygonGateway.GetSellPriceAsync(ticker);

                await Task.WhenAll(aggregateDataTask, metadataTask, currentPriceTask);

                var aggregateData = aggregateDataTask.Result;
                var metadata = metadataTask.Result;
                var currentPrice = currentPriceTask.Result;

                Console.WriteLine(currentPrice);

                // Validate responses
                if (aggregateData?["queryCount"]?.Value<int>() == 0)
                {
                    return NotFound(new { message = $"Ticker '{ticker}' not found." });
                }

                if (metadata == null)
                {
                    return NotFound(new { message = $"Metadata for ticker '{ticker}' not found." });
                }

                // Fetch image only if a logo URL exists
                var imageBase64 = string.IsNullOrWhiteSpace(metadata.Logo)
                    ? null
                    : await _polygonGateway.GetTickerImageBase64Async(metadata.Logo, ticker);

                // Build response
                var response = new
                {
                    metadata.Ticker,
                    metadata.Name,
                    metadata.Description,
                    LogoBase64 = imageBase64,
                    SellPrice = currentPrice,
                    AggregateData = aggregateData?.ToString(Newtonsoft.Json.Formatting.None)
                };

                return Ok(response);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error in GetAggregateData for ticker: {Ticker}", ticker);
                return StatusCode(500, new { message = "An internal error occurred.", error = ex.Message });
            }
        }
    }
}
