using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models.Domain;
using Server.Models.DTOs;

namespace Server.Controllers.Commands
{
    [Route("api/[controller]")]
    [ApiController]
    public class CashBalanceController : ControllerBase
    {
        private readonly StockContext _context;

        public CashBalanceController(StockContext context)
        {
            _context = context;
        }

        // POST: api/withdraw
        [HttpPost("withdraw")]
        public async Task<ActionResult> Withdraw([FromBody] ChangeCashBalance model)
        {
            if (model.Amount <= 0)
            {
                return BadRequest(new { message = "Amount is required." });
            }
            try
            {
                // Find the user by UserId
                User? user = await _context.Users
                    .FirstOrDefaultAsync(u => u.Id == model.UserId);
                if (user is null)
                {
                    return BadRequest(new { message = "User not found." });
                }
                // Check if the user has enough cash to withdraw
                if (user.CashBalance < model.Amount)
                {
                    return BadRequest(new { message = "Not enough cash to withdraw." });
                }
                // Update the user's cash balance
                user.CashBalance -= model.Amount;
                await _context.SaveChangesAsync();
                return Ok(new { message = "Withdrawal successful." });
            }
            catch
            {
                return BadRequest(new { message = "Failed to withdraw cash." });
            }
        }

        // POST: api/deposit
        [HttpPost("deposit")]
        public async Task<ActionResult> Deposit([FromBody] ChangeCashBalance model)
        {
            if (model.Amount <= 0)
            {
                return BadRequest(new { message = "Amount is required." });
            }
            try
            {
                // Find the user by UserId
                User? user = await _context.Users
                    .FirstOrDefaultAsync(u => u.Id == model.UserId);
                if (user is null)
                {
                    return BadRequest(new { message = "User not found." });
                }
                // Update the user's cash balance
                user.CashBalance += model.Amount;
                await _context.SaveChangesAsync();
                return Ok(new { message = "Deposit successful." });
            }
            catch
            {
                return BadRequest(new { message = "Failed to deposit cash." });
            }
        }
    }
}
