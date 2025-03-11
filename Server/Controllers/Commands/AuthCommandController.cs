using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models.Domain;
using Server.Models.DTOs.Commands;
using Server.Utils;

namespace Server.Controllers.Commands;

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
    public async Task<ActionResult<object>> SignUp([FromBody] SignUpRequest model)
    {
        try
        {
            if (string.IsNullOrWhiteSpace(model.Email) || string.IsNullOrWhiteSpace(model.Password) || string.IsNullOrWhiteSpace(model.Name))
            {
                return BadRequest(new { message = "Email, password, and name are required." });
            }

            var existingUser = await _context.Users
                .FirstOrDefaultAsync(u => u.Email == model.Email);

            if (existingUser != null)
            {
                return BadRequest(new { message = "Email is already in use." });
            }

            User user = new User
            {
                Email = model.Email,
                HashPassword = HashUtils.HashPassword(model.Password),
                Name = model.Name,
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            return Ok(new { user, message = "User registered successfully." });
        }
        catch (Exception)
        {
            return StatusCode(500, new { message = "An error occurred during registration." });
        }
    }

}