
using System.Collections.Generic;

namespace Server.Models.DTOs.Queries;

public class OllamaEmbeddingResponse
{
    public List<float> Embedding { get; set; }
}

public class OllamaGenerateResponse
{
    public string Model { get; set; }
    public string Response { get; set; }
}

public class QdrantSearchResponse
{
    public List<SearchResult> Result { get; set; }
}

public class SearchResult
{
    public int Id { get; set; }
    public double Score { get; set; }
    public PayloadData Payload { get; set; }
}

public class PayloadData
{
    public string Text { get; set; }
}

public class QueryResponse
{
    public string Answer { get; set; }
}