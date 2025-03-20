namespace Server.Models.DTOs.Queries;


public class PdfEmbeddingOptions
{
    public string QdrantHost { get; set; } = "localhost";
    public int QdrantPort { get; set; } = 6333;
    public string CollectionName { get; set; } = "pdf_vectors2";
    public int EmbeddingDim { get; set; } = 2048;
    public string PdfFileName { get; set; } = "MI_PDF_Economic_Dynamics_2025_10_Key_Trends_and_Forecasts.pdf";
    public int TopK { get; set; } = 5;
    public int ChunkSize { get; set; } = 1500;
    public int ChunkOverlap { get; set; } = 150;
    public string OllamaApiUrl { get; set; } = "http://localhost:11434/api";
    public string ModelName { get; set; } = "gemma:2b";

}
