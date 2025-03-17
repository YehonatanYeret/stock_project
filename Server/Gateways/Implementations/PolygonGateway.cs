using Newtonsoft.Json.Linq;
using Server.Gateways.Interfaces;
using Server.Models.DTOs;
using System.Text;

namespace Server.Gateways.Implementations
{
    public class PolygonGateway : IStocksGateway
    {
        private readonly string _polygonApiKey;
        private readonly HttpClient _httpClient;
        private const string BaseUrl = "https://api.polygon.io";

        public PolygonGateway(IConfiguration configuration)
        {
            _polygonApiKey = configuration["ApiKeys:polygon"]
                ?? throw new InvalidOperationException("Polygon API key is missing from configuration.");
            _httpClient = new HttpClient();
        }

        public async Task<string> GetAggregateDataAsync(string ticker, string startDate, string endDate)
        {
            var endpoint = $"/v2/aggs/ticker/{ticker}/range/1/day/{startDate}/{endDate}?apiKey={_polygonApiKey}";
            return await SendRequestAsync(endpoint);
        }

        public async Task<decimal> GetSellPriceAsync(string ticker, DateTime date)
        {
            var endpoint = $"/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={_polygonApiKey}";

            var response = await SendRequestAsync(endpoint);
            var json = JObject.Parse(response);

            if (json["results"] is JArray results && results.Count > 0)
            {
                return results[0]["c"]?.Value<decimal>()
                    ?? throw new InvalidOperationException("Closing price not found.");
            }

            throw new InvalidOperationException("No results found in API response.");
        }

        public async Task<TickerMetadataDto> GetTickerMetadataAsync(string ticker)
        {
            var endpoint = $"/v3/reference/tickers/{ticker}?apiKey={_polygonApiKey}";
            var response = await SendRequestAsync(endpoint);

            if (response == "")
                throw new InvalidOperationException("No results found in API response.");

            var json = JObject.Parse(response);

            if (json["results"] is not null)
            {
                var result = json["results"];
                return new TickerMetadataDto
                {
                    Ticker = result["ticker"]?.Value<string>() ?? string.Empty,
                    Name = result["name"]?.Value<string>() ?? string.Empty,
                    Description = result["description"]?.Value<string>() ?? string.Empty,
                    Logo = result["branding"]?["logo_url"]?.Value<string>() ?? string.Empty
                };
            }

            throw new InvalidOperationException("No results found in API response.");
        }

        /// <summary>
        /// Fetches the actual image bytes and converts them to Base64.
        /// If fetching fails, returns a default image.
        /// </summary>
        public async Task<string> GetTickerImageBase64Async(string ticker)
        {
            try
            {
                var metadata = await GetTickerMetadataAsync(ticker);
                var imageUrl = metadata?.Logo;

                if (!string.IsNullOrEmpty(imageUrl))
                {
                    var imageBytes = await FetchImageBytesAsync(imageUrl);
                    return Convert.ToBase64String(imageBytes); // Convert image to Base64
                }

                var defaultImageBytes = await FetchImageBytesAsync(GetDefaultLogoUrl());

                return Convert.ToBase64String(defaultImageBytes);
            }
            catch (Exception)
            {
                // If any error occurs, return the default placeholder image
            }
            return "";
        }

        /// <summary>
        /// Fetches image bytes from a given URL.
        /// </summary>
        private async Task<byte[]> FetchImageBytesAsync(string imageUrl)
        {
            var response = await _httpClient.GetAsync(imageUrl +$"?apiKey={_polygonApiKey}");

            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsByteArrayAsync();
            }

            throw new InvalidOperationException("Failed to fetch ticker image.");
        }

        /// <summary>
        /// Returns a default logo URL if no image is found.
        /// </summary>
        private string GetDefaultLogoUrl()
        {
            return "https://www.shutterstock.com/image-vector/no-image-available-picture-coming-600nw-2057829641.jpg";
        }

        private async Task<string> SendRequestAsync(string endpoint)
        {
            try
            {
                var url = $"{BaseUrl}{endpoint}";
                var response = await _httpClient.GetAsync(url);
                // If the status code is not successful, just return an empty string 
                if (!response.IsSuccessStatusCode)
                {
                    return string.Empty;
                }

                return await response.Content.ReadAsStringAsync();
            }
            catch
            {
                return string.Empty;
            }
        }
    }
}
