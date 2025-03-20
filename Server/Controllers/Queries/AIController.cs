//using Microsoft.AspNetCore.Mvc;
//using Microsoft.Extensions.Logging;
//using System;
//using System.Collections.Generic;
//using System.IO;
//using System.Linq;
//using System.Net.Http;
//using System.Text;
//using System.Threading.Tasks;
//using System.Net.Http.Json;
//using iText.Kernel.Pdf;
//using iText.Kernel.Pdf.Canvas.Parser;
//using iText.Kernel.Pdf.Canvas.Parser.Listener;

//namespace Server.Controllers;

//[ApiController]
//[Route("api/[controller]")]
//public class PdfEmbeddingController : ControllerBase
//{
//    private readonly ILogger<PdfEmbeddingController> _logger;
//    private readonly HttpClient _httpClient;
//    private readonly IWebHostEnvironment _environment;

//    // Constants
//    private const string QdrantHost = "localhost";
//    private const int QdrantPort = 6333;
//    private const string CollectionName = "pdf_vectors2";
//    private const int EmbeddingDim = 2048;
//    private const string PdfFileName = "MI_PDF_Economic_Dynamics_2025_10_Key_Trends_and_Forecasts.pdf";
//    private const int TopK = 5; // Number of top results to retrieve
//    private const int ChunkSize = 1500;
//    private const int ChunkOverlap = 150;
//    private const string OllamaApiUrl = "http://localhost:11434/api";
//    private const string ModelName = "gemma:2b";

//    public PdfEmbeddingController(ILogger<PdfEmbeddingController> logger, HttpClient httpClient, IWebHostEnvironment environment)
//    {
//        _logger = logger;
//        _httpClient = httpClient;
//        _environment = environment;
//    }

//    [HttpPost("process-pdf")]
//    public async Task<IActionResult> ProcessPdf()
//    {
//        try
//        {
//            // Get the full path to the PDF file
//            string pdfPath = GetPdfFilePath();

//            if (!System.IO.File.Exists(pdfPath))
//            {
//                return NotFound($"PDF file not found at: {pdfPath}");
//            }

//            _logger.LogInformation($"Processing PDF at path: {pdfPath}");
//            string text = ExtractTextFromPdf(pdfPath);
//            List<string> chunks = SplitText(text, ChunkSize, ChunkOverlap);

//            // Check if collection exists
//            bool collectionExists = await CollectionExistsAsync();

//            if (!collectionExists)
//            {
//                await CreateCollectionAsync();
//                await StoreEmbeddingsAsync(chunks);
//                _logger.LogInformation("PDF processed and embeddings stored successfully.");
//            }
//            else
//            {
//                _logger.LogInformation("Collection already exists. Checking if we need to update...");
//                // You may implement logic to check if the PDF has changed and update if needed
//                // For simplicity, we'll assume we need to update
//                await StoreEmbeddingsAsync(chunks);
//                _logger.LogInformation("Embeddings updated successfully.");
//            }

//            return Ok("PDF processed successfully");
//        }
//        catch (Exception ex)
//        {
//            _logger.LogError(ex, "Error processing PDF");
//            return StatusCode(500, $"Error processing PDF: {ex.Message}");
//        }
//    }

//    [HttpGet("answer")]
//    public async Task<IActionResult> AnswerQuery([FromQuery] string query)
//    {
//        try
//        {
//            if (string.IsNullOrEmpty(query))
//            {
//                return BadRequest("Query is required");
//            }

//            string response = await AnswerQueryAsync(query);
//            return Ok(new { answer = response });
//        }
//        catch (Exception ex)
//        {
//            _logger.LogError(ex, "Error answering query");
//            return StatusCode(500, $"Error answering query: {ex.Message}");
//        }
//    }

//    private string GetPdfFilePath()
//    {
//        // Log the environment paths
//        _logger.LogInformation($"ContentRootPath: {_environment.ContentRootPath}");
//        _logger.LogInformation($"WebRootPath: {_environment.WebRootPath}");

//        // Check if the environment paths are null
//        if (string.IsNullOrEmpty(_environment.ContentRootPath))
//        {
//            throw new InvalidOperationException("ContentRootPath is null or empty.");
//        }

//        // Try multiple possible locations for the PDF file
//        string[] possibleLocations = new[]
//        {
//        // 1. Content Root Path (where the application is running)
//        Path.Combine(_environment.ContentRootPath, PdfFileName),
        
//        // 2. One level up from Content Root
//        Path.Combine(Directory.GetParent(_environment.ContentRootPath)?.FullName ?? string.Empty, PdfFileName),
        
//        // 3. In a "Data" or "Files" subdirectory
//        Path.Combine(_environment.ContentRootPath, "Data", PdfFileName),
//        Path.Combine(_environment.ContentRootPath, "Files", PdfFileName),
        
//        // 4. In wwwroot if it's a web application
//        _environment.WebRootPath != null ? Path.Combine(_environment.WebRootPath, PdfFileName) : string.Empty,
        
//        // 5. Absolute path (in case it was specified)
//        PdfFileName
//    };

//        // Log all the paths we're checking
//        _logger.LogInformation("Checking for PDF file in the following locations:");
//        foreach (var path in possibleLocations)
//        {
//            _logger.LogInformation($"- {path}");
//            if (!string.IsNullOrEmpty(path) && System.IO.File.Exists(path))
//            {
//                _logger.LogInformation($"Found PDF at: {path}");
//                return path;
//            }
//        }

//        // If no file is found, return the default path (which will result in a proper error)
//        _logger.LogWarning($"PDF file not found in any expected location. Using default path: {possibleLocations[0]}");
//        return possibleLocations[0];
//    }


//    private string ExtractTextFromPdf(string pdfPath)
//    {
//        _logger.LogInformation($"Extracting text from PDF: {pdfPath}");
//        StringBuilder text = new StringBuilder();

//        try
//        {
//            using (PdfReader pdfReader = new PdfReader(pdfPath))
//            using (PdfDocument pdfDoc = new PdfDocument(pdfReader))
//            {
//                _logger.LogInformation($"PDF has {pdfDoc.GetNumberOfPages()} pages");
//                for (int i = 1; i <= pdfDoc.GetNumberOfPages(); i++)
//                {
//                    _logger.LogInformation($"Extracting text from page {i}");
//                    ITextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
//                    string pageText = PdfTextExtractor.GetTextFromPage(pdfDoc.GetPage(i), strategy);
//                    if (!string.IsNullOrEmpty(pageText))
//                    {
//                        text.AppendLine(pageText);
//                    }
//                }
//            }
//        }
//        catch (Exception ex)
//        {
//            _logger.LogError(ex, $"Error extracting text from PDF: {pdfPath}");
//            throw;
//        }

//        return text.ToString();
//    }

//    private List<string> SplitText(string text, int chunkSize, int chunkOverlap)
//    {
//        _logger.LogInformation("Splitting text into chunks");
//        var chunks = new List<string>();

//        // Simple implementation of text splitting
//        int startIndex = 0;
//        while (startIndex < text.Length)
//        {
//            int length = Math.Min(chunkSize, text.Length - startIndex);
//            if (length > 0)
//            {
//                chunks.Add(text.Substring(startIndex, length));
//            }
//            startIndex += chunkSize - chunkOverlap;
//            if (startIndex >= text.Length) break;
//        }

//        _logger.LogInformation($"Split text into {chunks.Count} chunks");
//        return chunks;
//    }

//    private async Task<bool> CollectionExistsAsync()
//    {
//        try
//        {
//            var response = await _httpClient.GetAsync($"http://{QdrantHost}:{QdrantPort}/collections/{CollectionName}");
//            return response.IsSuccessStatusCode;
//        }
//        catch
//        {
//            return false;
//        }
//    }

//    private async Task CreateCollectionAsync()
//    {
//        _logger.LogInformation("Creating Qdrant collection...");

//        var createRequest = new
//        {
//            vectors = new
//            {
//                size = EmbeddingDim,
//                distance = "Cosine"
//            }
//        };

//        var response = await _httpClient.PutAsJsonAsync(
//            $"http://{QdrantHost}:{QdrantPort}/collections/{CollectionName}",
//            createRequest
//        );

//        response.EnsureSuccessStatusCode();
//        _logger.LogInformation("Collection created successfully");
//    }

//    private async Task StoreEmbeddingsAsync(List<string> chunks)
//    {
//        _logger.LogInformation("Computing embeddings and storing in Qdrant...");

//        // Process chunks in batches to avoid overwhelming the system
//        int batchSize = 10;
//        for (int i = 0; i < chunks.Count; i += batchSize)
//        {
//            var batchChunks = chunks.Skip(i).Take(batchSize).ToList();
//            var pointsToUpsert = new List<object>();

//            for (int j = 0; j < batchChunks.Count; j++)
//            {
//                var chunk = batchChunks[j];
//                var vector = await EmbedTextAsync(chunk);

//                pointsToUpsert.Add(new
//                {
//                    id = i + j,
//                    vector = vector,
//                    payload = new { text = chunk }
//                });
//            }

//            var upsertRequest = new
//            {
//                points = pointsToUpsert
//            };

//            var response = await _httpClient.PutAsJsonAsync(
//                $"http://{QdrantHost}:{QdrantPort}/collections/{CollectionName}/points",
//                upsertRequest
//            );

//            response.EnsureSuccessStatusCode();
//            _logger.LogInformation($"Processed batch {i / batchSize + 1} of {Math.Ceiling((double)chunks.Count / batchSize)}");
//        }

//        _logger.LogInformation("Embeddings stored successfully.");
//    }

//    private async Task<List<float>> EmbedTextAsync(string text)
//    {
//        var requestBody = new
//        {
//            model = ModelName,
//            prompt = text
//        };

//        var response = await _httpClient.PostAsJsonAsync($"{OllamaApiUrl}/embeddings", requestBody);
//        response.EnsureSuccessStatusCode();

//        var responseObj = await response.Content.ReadFromJsonAsync<OllamaEmbeddingResponse>();
//        return responseObj.Embedding;
//    }

//    private async Task<List<string>> SearchSimilarTextAsync(string query)
//    {
//        var queryVector = await EmbedTextAsync(query);

//        var searchRequest = new
//        {
//            vector = queryVector,
//            limit = TopK
//        };

//        var response = await _httpClient.PostAsJsonAsync(
//            $"http://{QdrantHost}:{QdrantPort}/collections/{CollectionName}/points/search",
//            searchRequest
//        );

//        response.EnsureSuccessStatusCode();

//        var searchResults = await response.Content.ReadFromJsonAsync<QdrantSearchResponse>();

//        if (searchResults?.Result == null)
//        {
//            _logger.LogWarning("Search results or result list is null.");
//            return new List<string>();
//        }

//        return searchResults.Result
//            .Where(hit => hit.Payload != null)
//            .Select(hit => hit.Payload.Text)
//            .ToList();
//    }


//    private async Task<string> AnswerQueryAsync(string query)
//    {
//        var context = await SearchSimilarTextAsync(query);
//        string contextText = string.Join("\n", context);
//        string prompt = $"Context:\n{contextText}\n\nQuestion: {query}\nAnswer:";

//        return await InvokeLlmAsync(prompt);
//    }

//    private async Task<string> InvokeLlmAsync(string prompt)
//    {
//        var requestBody = new
//        {
//            model = ModelName,
//            prompt = prompt,
//            stream = false
//        };

//        var response = await _httpClient.PostAsJsonAsync($"{OllamaApiUrl}/generate", requestBody);
//        response.EnsureSuccessStatusCode();

//        var responseObj = await response.Content.ReadFromJsonAsync<OllamaGenerateResponse>();
//        return responseObj.Response;
//    }
//}

//// Classes for deserializing API responses
//public class OllamaEmbeddingResponse
//{
//    public List<float> Embedding { get; set; }
//}

//public class OllamaGenerateResponse
//{
//    public string Model { get; set; }
//    public string Response { get; set; }
//}

//public class QdrantSearchResponse
//{
//    public List<SearchResult> Result { get; set; }
//}

//public class SearchResult
//{
//    public int Id { get; set; }
//    public double Score { get; set; }
//    public PayloadData Payload { get; set; }
//}

//public class PayloadData
//{
//    public string Text { get; set; }
//}