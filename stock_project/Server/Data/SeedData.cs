using Server.Models;
using Microsoft.EntityFrameworkCore;

namespace Server.Data;

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
                new User {Email = "yeret@gmail.com", HashPassword = "123" },
                new User {Email = "manoy@gmail.com", HashPassword = "123" },
            };

            context.Users.AddRange(users);
            context.SaveChanges();

        }
    }
}
