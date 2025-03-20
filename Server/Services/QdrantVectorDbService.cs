using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Server.IServices;
using Server.Models;
using Server.Models.DTOs.Queries;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Net.Http.Json;
using System.Threading.Tasks;

namespace Server.Services;

public class QdrantVectorDbService : IVectorDbService
{
    private readonly ILogger<QdrantVectorDbService> _logger;
    private readonly HttpClient _httpClient;
    private readonly PdfEmbeddingOptions _options;
    private readonly IEmbeddingService _embeddingService;

    public QdrantVectorDbService(
        ILogger<QdrantVectorDbService> logger,
        HttpClient httpClient,
        IOptions<PdfEmbeddingOptions> options,
        IEmbeddingService embeddingService)
    {
        _logger = logger;
        _httpClient = httpClient;
        _options = options.Value;
        _embeddingService = embeddingService;
    }

    public async Task<bool> CollectionExistsAsync()
    {
        try
        {
            var response = await _httpClient.GetAsync(
                $"http://{_options.QdrantHost}:{_options.QdrantPort}/collections/{_options.CollectionName}");
            return response.IsSuccessStatusCode;
        }
        catch
        {
            return false;
        }
    }

    public async Task CreateCollectionAsync()
    {
        _logger.LogInformation("Creating Qdrant collection...");

        var createRequest = new
        {
            vectors = new
            {
                size = _options.EmbeddingDim,
                distance = "Cosine"
            }
        };

        var response = await _httpClient.PutAsJsonAsync(
            $"http://{_options.QdrantHost}:{_options.QdrantPort}/collections/{_options.CollectionName}",
            createRequest
        );

        response.EnsureSuccessStatusCode();
        _logger.LogInformation("Collection created successfully");
    }

    public async Task<bool> HasEmbeddingsAsync()
    {
        try
        {
            var countRequest = new { exact = true };

            var response = await _httpClient.PostAsJsonAsync(
                $"http://{_options.QdrantHost}:{_options.QdrantPort}/collections/{_options.CollectionName}/points/count",
                countRequest
            );

            if (!response.IsSuccessStatusCode)
                return false;

            var result = await response.Content.ReadFromJsonAsync<CountResponse>();
            return result.Result.Count > 0;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error checking if collection has embeddings");
            return false;
        }
    }

    private class CountResponse
    {
        public CountResult Result { get; set; }

        public class CountResult
        {
            public int Count { get; set; }
        }
    }

    public async Task StoreEmbeddingsAsync(List<string> chunks)
    {
        _logger.LogInformation("Computing embeddings and storing in Qdrant...");

        // Process chunks in batches to avoid overwhelming the system
        int batchSize = 10;
        for (int i = 0; i < chunks.Count; i += batchSize)
        {
            var batchChunks = chunks.Skip(i).Take(batchSize).ToList();
            var pointsToUpsert = new List<object>();

            for (int j = 0; j < batchChunks.Count; j++)
            {
                var chunk = batchChunks[j];
                var vector = await _embeddingService.EmbedTextAsync(chunk);

                pointsToUpsert.Add(new
                {
                    id = i + j,
                    vector = vector,
                    payload = new { text = chunk }
                });
            }

            var upsertRequest = new
            {
                points = pointsToUpsert
            };

            var response = await _httpClient.PutAsJsonAsync(
                $"http://{_options.QdrantHost}:{_options.QdrantPort}/collections/{_options.CollectionName}/points",
                upsertRequest
            );

            response.EnsureSuccessStatusCode();
            _logger.LogInformation($"Processed batch {i / batchSize + 1} of {Math.Ceiling((double)chunks.Count / batchSize)}");
        }

        _logger.LogInformation("Embeddings stored successfully.");
    }

    public async Task<List<string>> SearchSimilarTextAsync(string query)
    {
        var queryVector = await _embeddingService.EmbedTextAsync(query);

        var searchRequest = new
        {
            vector = queryVector,
            limit = _options.TopK,
            with_payload = true
        };

        var response = await _httpClient.PostAsJsonAsync(
            $"http://{_options.QdrantHost}:{_options.QdrantPort}/collections/{_options.CollectionName}/points/search",
            searchRequest
        );

        response.EnsureSuccessStatusCode();

        var searchResults = await response.Content.ReadFromJsonAsync<QdrantSearchResponse>();

        if (searchResults?.Result == null)
        {
            _logger.LogWarning("Search results or result list is null.");
            return new List<string>();
        }

        return searchResults.Result
            .Where(hit => hit.Payload != null)
            .Select(hit => hit.Payload.Text)
            .ToList();
    }
}
