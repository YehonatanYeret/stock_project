namespace Server.Models.DTOs.Queries;


public class PdfEmbeddingOptions
{
    public string QdrantHost { get; set; } 
    public int QdrantPort { get; set; } 
    public string CollectionName { get; set; } 
    public int EmbeddingDim { get; set; } 
    public string PdfFileName { get; set; } 
    public int TopK { get; set; } 
    public int ChunkSize { get; set; } 
    public int ChunkOverlap { get; set; } 
    public string OllamaApiUrl { get; set; } 
    public string ModelName { get; set; } 

}
