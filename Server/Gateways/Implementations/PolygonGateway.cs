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
        private readonly IImageGateaway _cloudinaryGateway;
        private const string BaseUrl = "https://api.polygon.io";

        public PolygonGateway(IConfiguration configuration, IImageGateaway cloudinaryGateway)
        {
            _polygonApiKey = configuration["ApiKeys:polygon"]
                ?? throw new InvalidOperationException("Polygon API key is missing from configuration.");
            _httpClient = new HttpClient();
            _cloudinaryGateway = cloudinaryGateway;
        }

        public async Task<JObject?> GetAggregateDataAsync(string ticker, string startDate, string endDate)
        {
            var endpoint = $"/v2/aggs/ticker/{ticker}/range/1/day/{startDate}/{endDate}?apiKey={_polygonApiKey}";
            var response = await SendRequestAsync(endpoint);

            if (string.IsNullOrEmpty(response)) return null;

            var json = JObject.Parse(response);

            // Detect unrecognized ticker
            if (json["queryCount"]?.Value<int>() == 0 || json["resultsCount"]?.Value<int>() == 0)
            {
                return null;
            }

            return json;
        }

        public async Task<decimal?> GetSellPriceAsync(string ticker)
        {
            var endpoint = $"/v2/aggs/ticker/{ticker}/prev?adjusted=true&apiKey={_polygonApiKey}";
            var response = await SendRequestAsync(endpoint);
            if (string.IsNullOrEmpty(response)) return null;

            var json = JObject.Parse(response);

            if (json["results"] is JArray results && results.Count > 0)
            {
                return results[0]["c"]?.Value<decimal>();
            }

            return null; // Return null instead of throwing an exception
        }

        public async Task<TickerMetadataDto?> GetTickerMetadataAsync(string ticker)
        {
            var endpoint = $"/v3/reference/tickers/{ticker}?apiKey={_polygonApiKey}";
            var response = await SendRequestAsync(endpoint);

            if (string.IsNullOrEmpty(response)) return null;

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

            return null; // Return null if no data is found
        }
        public async Task<string> GetTickerImageBase64Async(string imageUrl, string ticker)
        {
            try
            {
                // 1️⃣ Check if image exists in Cloudinary
                var cloudinaryImageUrl = _cloudinaryGateway.GetImageUrl(ticker);

                if (!string.IsNullOrEmpty(cloudinaryImageUrl))
                {
                    var cloudinaryBytes = await FetchImageBytesAsync(cloudinaryImageUrl);
                    return Convert.ToBase64String(cloudinaryBytes);
                }

                // 2️⃣ If not in Cloudinary, fetch from Polygon
                if (!string.IsNullOrEmpty(imageUrl))
                {
                    imageUrl = imageUrl + $"?apiKey={_polygonApiKey}";
                    var imageBytes = await FetchImageBytesAsync(imageUrl);
                    await _cloudinaryGateway.UploadImageAsync(imageUrl, ticker);

                    // 4️⃣ Return the newly fetched image
                    return Convert.ToBase64String(imageBytes);
                }
            }
            catch (Exception)
            {
                // 5️⃣ If everything fails, return a default image
            }

            var defaultUrl = _cloudinaryGateway.GetImageUrl("default");
            var defaultImageBytes = await FetchImageBytesAsync(defaultUrl);
            return Convert.ToBase64String(defaultImageBytes);
        }

        private async Task<byte[]> FetchImageBytesAsync(string imageUrl)
        {
            var response = await _httpClient.GetAsync(imageUrl);
            if (response.IsSuccessStatusCode)
            {
                return await response.Content.ReadAsByteArrayAsync();
            }
            throw new HttpRequestException("Failed to fetch ticker image.");
        }

        private async Task<string?> SendRequestAsync(string endpoint)
        {
            try
            {
                var url = $"{BaseUrl}{endpoint}";
                var response = await _httpClient.GetAsync(url);

                if (!response.IsSuccessStatusCode)
                {
                    Console.WriteLine($"API Request Failed: {url} - {response.StatusCode}");
                    return null;
                }

                return await response.Content.ReadAsStringAsync();
            }
            catch (Exception ex)
            {
                Console.WriteLine($"API Request Exception: {ex.Message}");
                return null;
            }
        }
    }
}

