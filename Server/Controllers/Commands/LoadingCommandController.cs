using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Gateways.Interfaces;
using Server.Models.Domain;
using Server.Models.DTOs.Commands;

namespace Server.Controllers.Commands;

[Route("api/[controller]/command")]
[ApiController]
public class LoadingCommandController : Controller
{
    private readonly StockContext _context;

    public LoadingCommandController(StockContext context)
    {
        _context = context;
    }

    // POST: api/loading/command/sell
    [HttpPost("load/{userId}")]
    public async Task<ActionResult> Load(int userId, int amount)
    {
        User? user = await _context.Users.FirstOrDefaultAsync(u => u.Id == userId);
        if (user == null)
        {
            return BadRequest(new { message = "User not found." });
        }
        user.PortfolioValue += amount;
        await _context.SaveChangesAsync();
        return Ok(new { message = "Successfully loaded funds." });
    }
}
