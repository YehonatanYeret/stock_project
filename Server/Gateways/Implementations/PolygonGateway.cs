using Newtonsoft.Json.Linq;
using Server.Gateways.Interfaces;
using Server.Models.DTOs;

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

        public async Task<string> GetAggregateDataAsync(string ticker, string startDate, string endDate)
        {
            var endpoint = $"/v2/aggs/ticker/{ticker}/range/1/day/{startDate}/{endDate}?apiKey={_polygonApiKey}";

            try
            {
                return await SendRequestAsync(endpoint);
            }
            catch (HttpRequestException ex)
            {
                return $"Error fetching data from Polygon API: {ex.Message}";
            }
        }

        public async Task<TickerMetadataDto> GetTickerMetadataAsync(string ticker)
        {
            var endpoint = $"/v3/reference/tickers/{ticker}?apiKey={_polygonApiKey}";

            var response = await SendRequestAsync(endpoint);
            var json = JObject.Parse(response);

            if (json["results"] is not null)
            {
                var result = json["results"];
                return new TickerMetadataDto
                {
                    Ticker = result["ticker"]?.Value<string>(),
                    Name = result["name"]?.Value<string>(),
                    Exchange = result["primary_exchange"]?.Value<string>(),
                    Industry = result["industry"]?.Value<string>(),
                    Logo = result["logo"]?.Value<string>()
                };
            }

            throw new InvalidOperationException("No results found in API response.");
        }

        public async Task<string> GetTickerImageUrlAsync(string ticker)
        {
            try
            {
                var metadata = await GetTickerMetadataAsync(ticker);
                return !string.IsNullOrEmpty(metadata?.Logo)
                    ? metadata.Logo
                    : GetDefaultLogoUrl(ticker);
            }
            catch (Exception)
            {
                return GetDefaultLogoUrl(ticker);
            }
        }

        private static string GetDefaultLogoUrl(string ticker)
        {
            // Implementation for a default logo based on ticker
            return $"https://your-default-logo-service.com/logo/{ticker}.png";
        }

        private async Task<string> SendRequestAsync(string endpoint)
        {
            var url = $"{BaseUrl}{endpoint}";
            var response = await _httpClient.GetAsync(url);

            response.EnsureSuccessStatusCode();

            return await response.Content.ReadAsStringAsync();
        }
    }
}