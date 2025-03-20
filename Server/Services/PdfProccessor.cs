using System.Text;
using System.Text.RegularExpressions;
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
        StringBuilder textBuilder = new StringBuilder();

        try
        {
            using PdfReader pdfReader = new PdfReader(pdfPath);
            using PdfDocument pdfDoc = new PdfDocument(pdfReader);

            _logger.LogInformation($"PDF contains {pdfDoc.GetNumberOfPages()} pages.");

            // Process each page of the PDF
            for (int pageNumber = 1; pageNumber <= pdfDoc.GetNumberOfPages(); pageNumber++)
            {
                _logger.LogInformation($"Extracting text from page {pageNumber}.");

                // Use LocationTextExtractionStrategy for optimal text order preservation
                ITextExtractionStrategy strategy = new LocationTextExtractionStrategy();
                string pageText = PdfTextExtractor.GetTextFromPage(pdfDoc.GetPage(pageNumber), strategy);

                if (!string.IsNullOrEmpty(pageText))
                {
                    // Clean and process the extracted text from the page
                    pageText = CleanupText(pageText);
                    textBuilder.AppendLine(pageText);
                    textBuilder.AppendLine(); // Add an empty line between pages
                }
            }

            // Final text processing
            string finalText = textBuilder.ToString();
            finalText = NormalizeWhitespace(finalText);
            finalText = FixEncodingIssues(finalText);

            return finalText;
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, $"Error while extracting text from PDF: {pdfPath}");
            throw;
        }
    }

    private string CleanupText(string text)
    {
        if (string.IsNullOrEmpty(text))
            return text;

        // Remove any null characters from the text
        text = text.Replace('\u0000', ' ');

        // ניתן להוסיף כאן תיקונים נוספים לבעיות קידוד במידת הצורך

        return text;
    }

    private string NormalizeWhitespace(string text)
    {
        if (string.IsNullOrEmpty(text))
            return text;

        // Replace multiple spaces with a single space
        text = Regex.Replace(text, @"\s+", " ");
        // Replace multiple newlines with at most two consecutive newlines
        text = Regex.Replace(text, @"\n{3,}", "\n\n");

        return text.Trim();
    }

    private string FixEncodingIssues(string text)
    {
        if (string.IsNullOrEmpty(text))
            return text;

        // Remove Unicode replacement characters
        text = text.Replace("\uFFFD", "");

        // Remove extraneous question marks that may appear near Hebrew characters
        text = Regex.Replace(text, @"\?(?=\s*[\u0590-\u05FF])", "");
        text = Regex.Replace(text, @"(?<=[\u0590-\u05FF]\s*)\?", "");

        // Remove question marks that appear between words
        text = Regex.Replace(text, @"(\w)\?(\w)", "$1$2");

        // General clean-up for repeated question marks
        text = Regex.Replace(text, @"\?\?+", "?");

        return text;
    }

    public List<string> SplitText(string text, int chunkSize, int chunkOverlap)
    {
        _logger.LogInformation("Splitting text into semantically meaningful chunks.");
        List<string> chunks = new List<string>();

        // Split the text into paragraphs using empty lines as delimiters
        string[] paragraphs = Regex.Split(text, @"(?<=\n)\s*\n");
        StringBuilder currentChunk = new StringBuilder();

        foreach (string paragraph in paragraphs)
        {
            string trimmedParagraph = paragraph.Trim();
            if (string.IsNullOrEmpty(trimmedParagraph))
                continue;

            // If the paragraph itself is larger than the chunk size, split it further
            if (trimmedParagraph.Length > chunkSize)
            {
                if (currentChunk.Length > 0)
                {
                    chunks.Add(currentChunk.ToString().Trim());
                    currentChunk.Clear();
                }

                SplitLargeParagraph(trimmedParagraph, chunkSize, chunkOverlap, chunks);
            }
            else if (currentChunk.Length + trimmedParagraph.Length + 1 > chunkSize)
            {
                // If adding the paragraph exceeds the chunk size, save the current chunk and start a new one
                chunks.Add(currentChunk.ToString().Trim());
                currentChunk.Clear();
                currentChunk.AppendLine(trimmedParagraph);
            }
            else
            {
                // Otherwise, append the paragraph to the current chunk
                if (currentChunk.Length > 0)
                    currentChunk.AppendLine();

                currentChunk.AppendLine(trimmedParagraph);
            }
        }

        // Add any remaining text as a final chunk
        if (currentChunk.Length > 0)
        {
            chunks.Add(currentChunk.ToString().Trim());
        }

        _logger.LogInformation($"Text split into {chunks.Count} chunks.");
        return chunks;
    }

    private void SplitLargeParagraph(string paragraph, int chunkSize, int chunkOverlap, List<string> chunks)
    {
        // Split the paragraph into sentences
        string[] sentences = Regex.Split(paragraph, @"(?<=[.!?])\s+");
        StringBuilder currentChunk = new StringBuilder();

        foreach (string sentence in sentences)
        {
            if (string.IsNullOrWhiteSpace(sentence))
                continue;

            // If a single sentence is too long, split it further
            if (sentence.Length > chunkSize)
            {
                if (currentChunk.Length > 0)
                {
                    chunks.Add(currentChunk.ToString().Trim());
                    currentChunk.Clear();
                }

                int startIndex = 0;
                while (startIndex < sentence.Length)
                {
                    int length = Math.Min(chunkSize, sentence.Length - startIndex);

                    // Avoid cutting in the middle of a word
                    if (startIndex + length < sentence.Length && !char.IsWhiteSpace(sentence[startIndex + length]))
                    {
                        int lastSpace = sentence.LastIndexOf(' ', startIndex + length, length);
                        if (lastSpace > startIndex)
                        {
                            length = lastSpace - startIndex;
                        }
                    }

                    string part = sentence.Substring(startIndex, length).Trim();
                    if (!string.IsNullOrEmpty(part))
                    {
                        chunks.Add(part);
                    }

                    startIndex += length;

                    // Apply overlap for the next chunk if possible
                    if (chunkOverlap < length)
                    {
                        startIndex -= chunkOverlap;
                    }
                }
            }
            else if (currentChunk.Length + sentence.Length + 1 > chunkSize)
            {
                chunks.Add(currentChunk.ToString().Trim());
                currentChunk.Clear();
                currentChunk.Append(sentence);
            }
            else
            {
                if (currentChunk.Length > 0)
                    currentChunk.Append(" ");
                currentChunk.Append(sentence);
            }
        }

        if (currentChunk.Length > 0)
        {
            chunks.Add(currentChunk.ToString().Trim());
        }
    }
}
