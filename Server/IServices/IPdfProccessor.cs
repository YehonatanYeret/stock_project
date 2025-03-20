using System.Collections.Generic;
using System.Threading.Tasks;

namespace Server.IServices
{
    public interface IPdfProcessor
    {
        string ExtractTextFromPdf(string pdfPath);
        List<string> SplitText(string text, int chunkSize, int chunkOverlap);
    }
}
