using System.Threading.Tasks;

namespace Server.IServices;

public interface ILlmService
{
    Task<string> GenerateAnswerAsync(string query, string context);
}