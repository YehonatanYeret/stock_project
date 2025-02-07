using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using Server.Data;
using Server.Models;
using System.Security.Cryptography;

namespace Server.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class AccountController : ControllerBase
    {
        private readonly StockContext _context;

        public AccountController(StockContext context)
        {
            _context = context;
        }

        // POST: api/account/signup
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
                model.HashPassword = HashPassword(plainPassword);

                _context.Users.Add(model);
                await _context.SaveChangesAsync();

                return Ok(new { userId = model.Id, message = "User registered successfully." });
            }
            catch (Exception)
            {
                return StatusCode(500, new { message = "An error occurred during registration." });
            }
        }

        // POST: api/account/signin
        [HttpPost("signin")]
        public async Task<ActionResult<object>> SignIn([FromBody] User model)
        {
            try
            {
                if (!ModelState.IsValid)
                {
                    var error = ModelState.Values
                        .SelectMany(v => v.Errors)
                        .FirstOrDefault()?.ErrorMessage;
                    return BadRequest(new { message = error ?? "Invalid login data." });
                }

                var user = await _context.Users
                    .FirstOrDefaultAsync(u => u.Email == model.Email);

                if (user == null)
                {
                    return Unauthorized(new { message = "Invalid credentials." });
                }

                if (VerifyPassword(model.HashPassword, user.HashPassword))
                {
                    return Ok(new { userId = user.Id, message = "User logged in successfully." });
                }

                return Unauthorized(new { message = "Invalid credentials." });
            }
            catch (Exception)
            {
                return StatusCode(500, new { message = "An error occurred during sign in." });
            }
        }

        private static string HashPassword(string password)
        {
            byte[] salt = new byte[16];
            using (var rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(salt);
            }

            using (var pbkdf2 = new Rfc2898DeriveBytes(password, salt, 100000, HashAlgorithmName.SHA256))
            {
                byte[] hash = pbkdf2.GetBytes(32);
                byte[] hashBytes = new byte[salt.Length + hash.Length];
                Array.Copy(salt, 0, hashBytes, 0, salt.Length);
                Array.Copy(hash, 0, hashBytes, salt.Length, hash.Length);
                return Convert.ToBase64String(hashBytes);
            }
        }

        private static bool VerifyPassword(string enteredPassword, string storedHash)
        {
            try
            {
                byte[] hashBytes = Convert.FromBase64String(storedHash);
                byte[] salt = new byte[16];
                Array.Copy(hashBytes, 0, salt, 0, salt.Length);

                using (var pbkdf2 = new Rfc2898DeriveBytes(enteredPassword, salt, 100000, HashAlgorithmName.SHA256))
                {
                    byte[] hash = pbkdf2.GetBytes(32);
                    for (int i = 0; i < hash.Length; i++)
                    {
                        if (hashBytes[salt.Length + i] != hash[i])
                        {
                            return false;
                        }
                    }
                }
                return true;
            }
            catch
            {
                return false;
            }
        }
    }
}