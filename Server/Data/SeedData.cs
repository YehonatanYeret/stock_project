using Server.Models;
using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography;

namespace Server.Data
{
    public static class SeedData
    {
        public static void Initialize(IServiceProvider serviceProvider)
        {
            using (var context = new StockContext(
                       serviceProvider.GetRequiredService<
                           DbContextOptions<StockContext>>()))
            {
                if (context == null || context.Users == null)
                {
                    throw new ArgumentNullException("Null UserContext");
                }

                // Check if data already exists
                if (!context.Users.Any())
                {
                    // Add users
                    var users = new List<User>
                        {
                            new User { Email = "yeretyn@gmail.com", HashPassword = HashPassword("123456") },
                            new User { Email = "manoy@gmail.com", HashPassword = HashPassword("123456") },
                        };

                    context.Users.AddRange(users);
                    context.SaveChanges();
                    Console.WriteLine("Seeded Users");
                }

                if (!context.Holdings.Any())
                {
                    // Add holdings
                    var holdings = new List<Holding>
                    {
                        new Holding { UserId = 1, Symbol = "AAPL", Quantity = 10, MarketCap = "2T", PeRatio = 30 },
                        new Holding { UserId = 1, Symbol = "GOOGL", Quantity = 5, MarketCap = "2T", PeRatio = 30 },
                        new Holding { UserId = 2, Symbol = "TSLA", Quantity = 20, MarketCap = "2T", PeRatio = 30 },
                        new Holding { UserId = 2, Symbol = "AMZN", Quantity = 15, MarketCap = "2T", PeRatio = 30 },
                    };
                    context.Holdings.AddRange(holdings);
                    context.SaveChanges();
                    Console.WriteLine("Seeded Holdings");
                }

                if (!context.Trades.Any())
                {
                    // Add trades
                    var trades = new List<Trade>
                        {
                            new Trade {Symbol = "AAPL", Date = DateTime.Now, Type = "Buy", Quantity = 10, Price = 100, Fees = 1 },
                            new Trade {Symbol = "GOOGL", Date = DateTime.Now, Type = "Buy", Quantity = 5, Price = 200, Fees = 1 },
                            new Trade {Symbol = "TSLA", Date = DateTime.Now, Type = "Buy", Quantity = 20, Price = 300, Fees = 1 },
                            new Trade {Symbol = "AMZN", Date = DateTime.Now, Type = "Buy", Quantity = 15, Price = 400, Fees = 1 },
                        };
                    context.Trades.AddRange(trades);
                    context.SaveChanges();
                    Console.WriteLine("Seeded Trades");
                }
            }
        }

        // Hash a password using PBKDF2
        private static string HashPassword(string password)
        {
            // Generate a cryptographic salt
            byte[] salt = new byte[16]; // Salt size of 16 bytes
            using (var rng = RandomNumberGenerator.Create())
            {
                rng.GetBytes(salt); // Generate a random salt
            }

            // Use PBKDF2 with SHA256 to hash the password
            using (var pbkdf2 = new Rfc2898DeriveBytes(password, salt, 100000, HashAlgorithmName.SHA256))
            {
                byte[] hash = pbkdf2.GetBytes(32); // Hash length of 32 bytes

                // Combine salt and hash for storage
                byte[] hashBytes = new byte[salt.Length + hash.Length];
                Array.Copy(salt, 0, hashBytes, 0, salt.Length);
                Array.Copy(hash, 0, hashBytes, salt.Length, hash.Length);

                // Return the result as a base64 string to store in the DB
                return Convert.ToBase64String(hashBytes);
            }
        }
    }
}
