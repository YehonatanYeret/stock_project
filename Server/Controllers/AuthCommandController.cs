using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models;
using Server.Utils;

namespace Server.Controllers
{
    [Route("api/auth/command")]
    [ApiController]
    public class AuthCommandController : ControllerBase
    {
        private readonly StockContext _context;

        public AuthCommandController(StockContext context)
        {
            _context = context;
        }

        // POST: api/auth/signup
        [HttpPost("signup")]
        public async Task<ActionResult<object>> SignUp([FromBody] User model)
        {
            try
            {
                if (!ModelState.IsValid)
                {
                    var error = ModelState.Values
                        .SelectMany(v => v.Errors)
                        .FirstOrDefault()?.ErrorMessage;
                    return BadRequest(new { message = error ?? "Invalid user data." });
                }

                var existingUser = await _context.Users
                    .FirstOrDefaultAsync(u => u.Email == model.Email);

                if (existingUser != null)
                {
                    return BadRequest(new { message = "Email is already in use." });
                }

                var plainPassword = model.HashPassword;
                model.HashPassword = HashUtils.HashPassword(plainPassword);

                _context.Users.Add(model);
                await _context.SaveChangesAsync();

                return Ok(new { userId = model.Id, message = "User registered successfully." });
            }
            catch (Exception)
            {
                return StatusCode(500, new { message = "An error occurred during registration." });
            }
        }

   }
}