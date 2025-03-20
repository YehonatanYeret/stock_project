using Microsoft.Extensions.Logging;
using System;
using System.Collections.Generic;
using System.Text;
using iText.Kernel.Pdf;
using iText.Kernel.Pdf.Canvas.Parser;
using iText.Kernel.Pdf.Canvas.Parser.Listener;
using Server.IServices;

namespace Server.Services;

public class PdfProcessor : IPdfProcessor
{
    private readonly ILogger<PdfProcessor> _logger;

    public PdfProcessor(ILogger<PdfProcessor> logger)
    {
        _logger = logger;
    }

    public string ExtractTextFromPdf(string pdfPath)
    {
        _logger.LogInformation($"Extracting text from PDF: {pdfPath}");
        StringBuilder text = new StringBuilder();

        try
        {
            using (PdfReader pdfReader = new PdfReader(pdfPath))
            using (PdfDocument pdfDoc = new PdfDocument(pdfReader))
            {
                _logger.LogInformation($"PDF has {pdfDoc.GetNumberOfPages()} pages");
                for (int i = 1; i <= pdfDoc.GetNumberOfPages(); i++)
                {
                    _logger.LogInformation($"Extracting text from page {i}");
                    ITextExtractionStrategy strategy = new SimpleTextExtractionStrategy();
                    string pageText = PdfTextExtractor.GetTextFromPage(pdfDoc.GetPage(i), strategy);
                    if (!string.IsNullOrEmpty(pageText))
                    {
                        text.AppendLine(pageText);
                    }
                }
            }
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Error extracting text from PDF: {pdfPath}");
            throw;
        }

        return text.ToString();
    }

    public List<string> SplitText(string text, int chunkSize, int chunkOverlap)
    {
        _logger.LogInformation("Splitting text into chunks");
        var chunks = new List<string>();

        // Simple implementation of text splitting
        int startIndex = 0;
        while (startIndex < text.Length)
        {
            int length = Math.Min(chunkSize, text.Length - startIndex);
            if (length > 0)
            {
                chunks.Add(text.Substring(startIndex, length));
            }
            startIndex += chunkSize - chunkOverlap;
            if (startIndex >= text.Length) break;
        }

        _logger.LogInformation($"Split text into {chunks.Count} chunks");
        return chunks;
    }
}
