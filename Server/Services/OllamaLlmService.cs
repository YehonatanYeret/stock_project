using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Server.IServices;
using Server.Models;
using Server.Models.DTOs.Queries;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace Server.Services;

public class OllamaLlmService : ILlmService
{
    private readonly ILogger<OllamaLlmService> _logger;
    private readonly HttpClient _httpClient;
    private readonly PdfEmbeddingOptions _options;

    public OllamaLlmService(
        ILogger<OllamaLlmService> logger,
        HttpClient httpClient,
        IOptions<PdfEmbeddingOptions> options)
    {
        _logger = logger;
        _httpClient = httpClient;
        _options = options.Value;
    }

    public async Task<string> GenerateAnswerAsync(string query, string context)
    {
        string prompt = $"Context:\n{context}\n\nQuestion: {query}\nProvide a direct and precise answer, without additional explanations in the minimum words as you can\nAnswer:";
        return await InvokeLlmAsync(prompt);
    }

    private async Task<string> InvokeLlmAsync(string prompt)
    {
        var requestBody = new
        {
            model = _options.ModelName,
            prompt = prompt,
            stream = false
        };

        var response = await _httpClient.PostAsJsonAsync($"{_options.OllamaApiUrl}/generate", requestBody);
        response.EnsureSuccessStatusCode();

        var responseObj = await response.Content.ReadFromJsonAsync<OllamaGenerateResponse>();
        return responseObj.Response;
    }
}