using System.Collections.Generic;
using System.Threading.Tasks;

namespace Server.IServices;

public interface IVectorDbService
{
    Task<bool> CollectionExistsAsync();
    Task CreateCollectionAsync();
    Task StoreEmbeddingsAsync(List<string> chunks);
    Task<List<string>> SearchSimilarTextAsync(string query);
    Task<bool> HasEmbeddingsAsync();
}