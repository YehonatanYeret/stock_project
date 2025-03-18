using Newtonsoft.Json.Linq;
using Server.Models.DTOs;

namespace Server.Gateways.Interfaces
{
    public interface IStocksGateway
    {
        /// <summary>
        /// This method fetches the aggregate data for the given ticker symbol from the Polygon API.
        /// </summary>
        /// <param name="ticker">The stock ticker symbol</param>
        /// <param name="startDate">The start date for the data range</param>
        /// <param name="endDate">The end date for the data range</param>
        /// <returns>A JSON string containing the aggregate data for the given ticker symbol</returns>
        Task<JObject> GetAggregateDataAsync(string ticker, string startDate, string endDate);

        /// <summary>
        /// This method fetches the closing price for the given ticker symbol on a specific date.
        /// </summary>
        /// <param name="ticker">The stock ticker symbol</param>
        /// <param name="date">The date to fetch the closing price for</param>
        /// <returns>The closing price for the given ticker on the specified date</returns>
        Task<decimal?> GetSellPriceAsync(string ticker, DateTime date);

        /// <summary>
        /// This method fetches the metadata for the given ticker symbol from the Polygon API.
        /// </summary>
        /// <param name="ticker">the given ticker</param>
        /// <returns>the metadata</returns>
        Task<TickerMetadataDto> GetTickerMetadataAsync(string ticker);

        /// <summary>
        /// This method fetches the image URL for the given ticker symbol from the Polygon API.
        /// </summary>
        /// <param name="ticker">the given ticker</param>
        /// <returns>the url</returns>
        Task<string> GetTickerImageBase64Async(string imageUrl, string ticker);
    }
}
