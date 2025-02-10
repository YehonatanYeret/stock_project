using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Newtonsoft.Json;
using Server.Data;
using Server.Models;
using System.Security.Cryptography;
using Microsoft.Extensions.Configuration;

namespace Server.Controllers;

[Route("api/[controller]")]
[ApiController]
public class TransactionController : ControllerBase
{
    private readonly StockContext _context;
    private readonly string _polygonApiKey;

    public TransactionController(StockContext context, IConfiguration configuration)
    {
        if (context == null)
            throw new ArgumentNullException(nameof(context));

        if (configuration == null)
            throw new ArgumentNullException(nameof(configuration));

        _context = context;
        _polygonApiKey = configuration["ApiKeys:polygon"]
                         ?? throw new InvalidOperationException("Polygon API key is missing from configuration.");
    }



    // Consider storing this securely (e.g., in web.config or appsettings.json)

    // Example action to get aggregate data
    [HttpGet("transaction")]
    public async Task<ActionResult> GetAggregateData(string ticker)
    {
        // Build the API URL
        // For instance, this retrieves 1-day aggregates for a given date range
        string url = $"https://api.polygon.io/v2/aggs/ticker/{ticker}/range/1/day/2024-10-10/2025-01-01?apiKey={_polygonApiKey}";
        Console.WriteLine(ticker);
        using (var client = new HttpClient())
        {
            HttpResponseMessage response = await client.GetAsync(url);
            if (response.IsSuccessStatusCode)
            {
                // Read and deserialize the JSON response
                var jsonResponse = await response.Content.ReadAsStringAsync();
                return Ok(jsonResponse);
            }
            else
                return StatusCode(500, "Error");
        }
    }
}