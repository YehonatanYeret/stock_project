using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;

namespace MyApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class ModelController : ControllerBase
    {
        private readonly HttpClient _httpClient;

        // Constructor that initializes the HttpClient
        public ModelController(IHttpClientFactory httpClientFactory)
        {
            _httpClient = httpClientFactory.CreateClient(nameof(ModelController));
        }

        // API endpoint to send the question to the model
        [HttpPost("ask")]
        public async Task<IActionResult> AskModel([FromBody] AskRequest request)
        {
            // Define the API URL for the model running in Docker
            var apiUrl = "http://localhost:11434/api/generate";

            // Create the request payload (including the question and model name)
            var data = new
            {
                prompt = request.Question,
                model = "tinyllama",
                stream = false // Set to false to get a complete response
            };

            // Convert the request data to JSON and set the content type to "application/json"
            var content = new StringContent(JsonConvert.SerializeObject(data), Encoding.UTF8, "application/json");

            // Send the request to the model API
            var response = await _httpClient.PostAsync(apiUrl, content);

            if (response.IsSuccessStatusCode)
            {
                // Read the response body from the model API
                var responseBody = await response.Content.ReadAsStringAsync();

                // Deserialize the JSON response to extract the model's output
                var modelResponse = JsonConvert.DeserializeObject<ModelResponse>(responseBody);

                // Return the model's output to the client
                return Ok(new { Answer = modelResponse.Response });
            }
            else
            {
                // Handle error response from the API
                return StatusCode((int)response.StatusCode, "Error calling model API");
            }
        }
    }

    // Request model for receiving the user's question
    public class AskRequest
    {
        public string Question { get; set; }
    }

    // Response model to deserialize the API response
    public class ModelResponse
    {
        // Field to extract the response text from the model API
        [JsonProperty("response")]
        public string Response { get; set; }
    }
}
