using Microsoft.Extensions.Configuration;
using Server.Gateways.Interfaces;
using System;
using System.Net.Http;
using System.Threading.Tasks;
using Newtonsoft.Json.Linq;

namespace Server.Gateways.Implementations
{
    public class PolygonGateway : IPolygonGateway
    {
        private readonly string _polygonApiKey;

        // Constructor to initialize the Polygon API key from app settings
        public PolygonGateway(IConfiguration configuration)
        {
            _polygonApiKey = configuration["ApiKeys:polygon"]
                             ?? throw new InvalidOperationException("Polygon API key is missing from configuration.");
        }

        /// <summary>
        /// This method fetches the closing price for the given ticker symbol on a specific date.
        /// </summary>
        /// <param name="ticker">The stock ticker symbol</param>
        /// <param name="date">The date to fetch the closing price for</param>
        /// <returns>The closing price for the given ticker on the specified date</returns>
        public async Task<decimal> GetSellPriceAsync(string ticker, DateTime date)
        {
            string url = $"https://api.polygon.io/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={_polygonApiKey}";
            Console.WriteLine($"Fetching data from: {url}");

            using (var client = new HttpClient())
            {
                HttpResponseMessage response = await client.GetAsync(url);

                if (!response.IsSuccessStatusCode)
                {
                    throw new InvalidOperationException($"Error fetching data from Polygon API. Status: {response.StatusCode}");
                }

                var jsonResponse = await response.Content.ReadAsStringAsync();
                var json = JObject.Parse(jsonResponse);
                Console.WriteLine($"API Response: {json}");

                if (json["results"] is JArray results && results.Count > 0)
                {
                    decimal closePrice = results[0]["c"]?.Value<decimal>() ?? throw new InvalidOperationException("Closing price not found.");
                    return closePrice;
                }

                throw new InvalidOperationException("No results found in API response.");
            }
        }

        /// <summary>
        /// This method fetches the aggregate data for the given ticker symbol from the Polygon API.
        /// </summary>
        /// <param name="ticker">The stock ticker symbol</param>
        /// <param name="startDate">The start date for the data range</param>
        /// <param name="endDate">The end date for the data range</param>
        /// <returns>A JSON string containing the aggregate data for the given ticker symbol</returns>
        public async Task<string> GetAggregateDataAsync(string ticker, string startDate, string endDate)
        {
            // Construct the URL to get data from the Polygon API
            string url = $"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{startDate}/{endDate}?apiKey={_polygonApiKey}";

            using (var client = new HttpClient())
            {
                // Send the GET request to the Polygon API
                HttpResponseMessage response = await client.GetAsync(url);

                if (response.IsSuccessStatusCode)
                {
                    // Read the response as JSON string
                    var jsonResponse = await response.Content.ReadAsStringAsync();
                    return jsonResponse;
                }
                else
                {
                    // Handle errors by returning a failure message (or you can throw an exception)
                    return $"Error fetching data from Polygon API. Status: {response.StatusCode}";
                }
            }
        }
    }
}
