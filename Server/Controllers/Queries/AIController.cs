using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using Microsoft.Extensions.Options;
using Server.IServices;
using Server.Models;
using Server.Models.DTOs.Queries;
using System;
using System.IO;
using System.Threading.Tasks;

namespace Server.Controllers.Queries;

[ApiController]
[Route("api/[controller]/query")]
public class AIController : ControllerBase
{
    private readonly ILogger<AIController> _logger;
    private readonly IWebHostEnvironment _environment;
    private readonly PdfEmbeddingOptions _options;
    private readonly IPdfProcessor _pdfProcessor;
    private readonly IVectorDbService _vectorDbService;
    private readonly ILlmService _llmService;

    public AIController(
        ILogger<AIController> logger,
        IWebHostEnvironment environment,
        IOptions<PdfEmbeddingOptions> options,
        IPdfProcessor pdfProcessor,
        IVectorDbService vectorDbService,
        ILlmService llmService)
    {
        _logger = logger;
        _environment = environment;
        _options = options.Value;
        _pdfProcessor = pdfProcessor;
        _vectorDbService = vectorDbService;
        _llmService = llmService;
    }

    [HttpPost("process-pdf")]
    public async Task<IActionResult> ProcessPdf()
    {
        try
        {
            // Get the full path to the PDF file
            string pdfPath = GetPdfFilePath();

            if (!System.IO.File.Exists(pdfPath))
            {
                return NotFound($"PDF file not found at: {pdfPath}");
            }

            _logger.LogInformation($"Processing PDF at path: {pdfPath}");

            // Check if collection exists
            bool collectionExists = await _vectorDbService.CollectionExistsAsync();

            if (!collectionExists)
            {
                await _vectorDbService.CreateCollectionAsync();
                // Process PDF and store embeddings
                await ProcessAndStoreEmbeddings(pdfPath);
                _logger.LogInformation("PDF processed and embeddings stored successfully.");
            }
            else
            {
                // Check if the collection already has embeddings
                bool hasEmbeddings = await _vectorDbService.HasEmbeddingsAsync();

                if (!hasEmbeddings)
                {
                    // Only process PDF if there are no embeddings
                    await ProcessAndStoreEmbeddings(pdfPath);
                    _logger.LogInformation("PDF processed and embeddings stored successfully.");
                }
                else
                {
                    _logger.LogInformation("Collection already has embeddings. Skipping processing.");
                }
            }

            return Ok("PDF processing complete");
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error processing PDF");
            return StatusCode(500, $"Error processing PDF: {ex.Message}");
        }
    }

    private async Task ProcessAndStoreEmbeddings(string pdfPath)
    {
        string text = _pdfProcessor.ExtractTextFromPdf(pdfPath);
        var chunks = _pdfProcessor.SplitText(text, _options.ChunkSize, _options.ChunkOverlap);
        await _vectorDbService.StoreEmbeddingsAsync(chunks);
    }

    [HttpGet("response")]
    public async Task<IActionResult> AnswerQuery([FromQuery] string query)
    {
        try
        {
            if (string.IsNullOrEmpty(query))
            {
                return BadRequest("Query is required");
            }

            var context = await _vectorDbService.SearchSimilarTextAsync(query);
            string contextText = string.Join("\n", context);
            string response = await _llmService.GenerateAnswerAsync(query, contextText);

            return Ok(response);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error answering query");
            return StatusCode(500, $"Error answering query: {ex.Message}");
        }
    }

    private string GetPdfFilePath()
    {
        // Log the environment paths
        _logger.LogInformation($"ContentRootPath: {_environment.ContentRootPath}");
        _logger.LogInformation($"WebRootPath: {_environment.WebRootPath}");

        // Check if the environment paths are null
        if (string.IsNullOrEmpty(_environment.ContentRootPath))
        {
            throw new InvalidOperationException("ContentRootPath is null or empty.");
        }

        // Try multiple possible locations for the PDF file
        string[] possibleLocations = new[]
        {
            // 1. Content Root Path (where the application is running)
            Path.Combine(_environment.ContentRootPath, _options.PdfFileName),
            
            // 2. One level up from Content Root
            Path.Combine(Directory.GetParent(_environment.ContentRootPath)?.FullName ?? string.Empty, _options.PdfFileName),
            
            // 3. In a "Data" or "Files" subdirectory
            Path.Combine(_environment.ContentRootPath, "Data", _options.PdfFileName),
            Path.Combine(_environment.ContentRootPath, "Files", _options.PdfFileName),
            
            // 4. In wwwroot if it's a web application
            _environment.WebRootPath != null ? Path.Combine(_environment.WebRootPath, _options.PdfFileName) : string.Empty,
            
            // 5. Absolute path (in case it was specified)
            _options.PdfFileName
        };

        // Log all the paths we're checking
        _logger.LogInformation("Checking for PDF file in the following locations:");
        foreach (var path in possibleLocations)
        {
            _logger.LogInformation($"- {path}");
            if (!string.IsNullOrEmpty(path) && System.IO.File.Exists(path))
            {
                _logger.LogInformation($"Found PDF at: {path}");
                return path;
            }
        }

        // If no file is found, return the default path (which will result in a proper error)
        _logger.LogWarning($"PDF file not found in any expected location. Using default path: {possibleLocations[0]}");
        return possibleLocations[0];
    }
}
