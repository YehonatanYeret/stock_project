using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models.Domain;
using Server.Models.DTOs.Queries;
using Server.Utils;
using System.Threading.Tasks;

namespace Server.Controllers.Queries
{
    [Route("api/auth/query")]
    [ApiController]
    public class AuthQueryController : ControllerBase
    {
        private readonly StockContext _context;

        public AuthQueryController(StockContext context)
        {
            _context = context;
        }

        // POST: api/auth/signin
        [HttpPost("signin")]
        public async Task<ActionResult<object>> SignIn([FromBody] SignInRequest model)
        {
            if (string.IsNullOrWhiteSpace(model.Email) || string.IsNullOrWhiteSpace(model.Password))
            {
                return BadRequest(new { message = "Email and password are required." });
            }

            try
            {
                var user = await _context.Users
                    .AsNoTracking()
                    .FirstOrDefaultAsync(u => u.Email == model.Email);

                if (user == null || !HashUtils.VerifyPassword(model.Password, user.HashPassword))
                {
                    return Unauthorized(new { message = "Invalid credentials." });
                }

                return Ok(new { userId = user.Id, message = "User logged in successfully." });
            }
            catch
            {
                return StatusCode(500, new { message = "An error occurred during sign in." });
            }
        }
    }
}