using System.Collections.Generic;
using System.Threading.Tasks;

namespace Server.IServices;

public interface IEmbeddingService
{
    Task<List<float>> EmbedTextAsync(string text);
}