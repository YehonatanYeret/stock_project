using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Configuration;
using Server.Data;
using System;
using System.Net.Http;
using System.Threading.Tasks;

namespace Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class TransactionController : ControllerBase
    {
        private readonly StockContext _context;
        private readonly string _polygonApiKey;

        public TransactionController(StockContext context, IConfiguration configuration)
        {
            _context = context ?? throw new ArgumentNullException(nameof(context));
            _polygonApiKey = configuration["ApiKeys:polygon"]
                             ?? throw new InvalidOperationException("Polygon API key is missing from configuration.");
        }

        // Get stock aggregate data based on ticker, start date, and end date
        [HttpGet("getDetails")]
        public async Task<ActionResult> GetAggregateData(string ticker, string startDate, string endDate)
        {
            if (string.IsNullOrEmpty(ticker) || string.IsNullOrEmpty(startDate) || string.IsNullOrEmpty(endDate))
            {
                return BadRequest("Ticker, startDate, and endDate are required.");
            }

            string url = $"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/{startDate}/{endDate}?apiKey={_polygonApiKey}";
            Console.WriteLine(url);
            using (var client = new HttpClient())
            {
                HttpResponseMessage response = await client.GetAsync(url);
                if (response.IsSuccessStatusCode)
                {
                    var jsonResponse = await response.Content.ReadAsStringAsync();
                    return Ok(jsonResponse);
                }
                else
                {
                    return StatusCode((int)response.StatusCode, "Error fetching data from Polygon API.");
                }
            }
        }
    }
}
