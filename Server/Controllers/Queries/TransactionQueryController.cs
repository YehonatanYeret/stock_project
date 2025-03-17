using Microsoft.AspNetCore.Mvc;
using Server.Gateways.Implementations;
using Server.Gateways.Interfaces;

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
        /// the method will get the aggregate data for a given ticker symbol and date range
        /// </summary>
        /// <param name="ticker">the ticker symbol</param>
        /// <param name="startDate"> the start date of the date range</param>
        /// <param name="endDate"> the end date of the date range</param>
        /// <returns> the aggregate data for the given ticker symbol and date range</returns>
        [HttpGet("getDetails")]
        public async Task<ActionResult> GetAggregateData(string ticker, string startDate, string endDate)
        {
            try
            {
                if (string.IsNullOrEmpty(ticker) || string.IsNullOrEmpty(startDate) || string.IsNullOrEmpty(endDate))
                {
                    return BadRequest("Ticker, startDate, and endDate are required.");
                }

                var aggregateDataTask = _polygonGateway.GetAggregateDataAsync(ticker, startDate, endDate);
                var metadataTask = _polygonGateway.GetTickerMetadataAsync(ticker);
                var imageBase64Task = _polygonGateway.GetTickerImageBase64Async(ticker); // Fetch actual image bytes as Base64

                await Task.WhenAll(aggregateDataTask, metadataTask, imageBase64Task);

                var aggregateData = await aggregateDataTask;
                var metadata = await metadataTask;
                var imageBase64 = await imageBase64Task;

                var response = new
                {
                    Ticker = metadata.Ticker,
                    Name = metadata.Name,
                    Description = metadata.Description,
                    LogoBase64 = imageBase64, // Embed image in Base64 format
                    AggregateData = aggregateData
                };

                return Ok(response);
            }
            catch
            {
                return BadRequest("Failed to fetch data.");
            }
        }
    }
}
