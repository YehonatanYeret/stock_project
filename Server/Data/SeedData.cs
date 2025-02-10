using Server.Models;
using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography;
using System.Text;

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
                if (context.Users.Any())
                {
                    return; // DB has been seeded
                }

                // Add users
                var users = new List<User>
                {
                    new User { Email = "yeret@gmail.com", HashPassword = HashPassword("123456") },
                    new User { Email = "manoy@gmail.com", HashPassword = HashPassword("123456") },
                };

                context.Users.AddRange(users);
                context.SaveChanges();
                System.Console.WriteLine("Seeded Users");
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
                Console.WriteLine(Convert.ToBase64String(hashBytes));
                Console.WriteLine(hashBytes);
                return Convert.ToBase64String(hashBytes);
            }
        }
    }
}
