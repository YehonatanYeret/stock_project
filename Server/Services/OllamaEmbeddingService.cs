using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Server.IServices;
using Server.Models;
using Server.Models.DTOs.Queries;
using System.Collections.Generic;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace Server.Services;

public class OllamaEmbeddingService : IEmbeddingService
{
    private readonly ILogger<OllamaEmbeddingService> _logger;
    private readonly HttpClient _httpClient;
    private readonly PdfEmbeddingOptions _options;

    public OllamaEmbeddingService(
        ILogger<OllamaEmbeddingService> logger,
        HttpClient httpClient,
        IOptions<PdfEmbeddingOptions> options)
    {
        _logger = logger;
        _httpClient = httpClient;
        _options = options.Value;
    }

    public async Task<List<float>> EmbedTextAsync(string text)
    {
        var requestBody = new
        {
            model = _options.ModelName,
            prompt = text
        };

        var response = await _httpClient.PostAsJsonAsync($"{_options.OllamaApiUrl}/embeddings", requestBody);
        response.EnsureSuccessStatusCode();

        var responseObj = await response.Content.ReadFromJsonAsync<OllamaEmbeddingResponse>();
        return responseObj.Embedding;
    }
}