using Server.Models;
using Microsoft.EntityFrameworkCore;
using Server.Utils;
using Server.Models.Domain;

namespace Server.Data;

public static class SeedData
{
    public static void Initialize(IServiceProvider serviceProvider)
    {
        using (var context = new StockContext(
                   serviceProvider.GetRequiredService<
                       DbContextOptions<StockContext>>()))
        {
            if (context == null || context.Users == null || context.Logs == null)
            {
                throw new ArgumentNullException("Null UserContext");
            }

            // ✅ Seed Users
            if (!context.Users.Any())
            {
                var users = new List<User>
                {
                    new User { Name = "Yehonatan", Email = "yeretyn@gmail.com", HashPassword = HashUtils.HashPassword("123456") },
                    new User { Name = "Maor", Email = "manoy@gmail.com", HashPassword = HashUtils.HashPassword("123456") },
                };

                context.Users.AddRange(users);
                context.SaveChanges();
                Console.WriteLine("✅ Seeded Users");
            }

            // ✅ Seed Trades (Over a Year with Buys & Sells)
            if (!context.Logs.Any())
            {
                var logs = new List<Log>
                {
                    // Yehonatan (User 1)
                    new Log { UserId = 1, Symbol = "AAPL", Date = DateTime.Now.AddMonths(-12), Type = Enums.historyType.Buy, Quantity = 10, Price = 150 },
                    new Log { UserId = 1, Symbol = "GOOGL", Date = DateTime.Now.AddMonths(-10), Type = Enums.historyType.Buy, Quantity = 5, Price = 2500 },
                    new Log { UserId = 1, Symbol = "AAPL", Date = DateTime.Now.AddMonths(-8), Type = Enums.historyType.Sell, Quantity = 5, Price = 180 },
                    new Log { UserId = 1, Symbol = "GOOGL", Date = DateTime.Now.AddMonths(-5), Type = Enums.historyType.Sell, Quantity = 2, Price = 2600 },
                    new Log { UserId = 1, Symbol = "AAPL", Date = DateTime.Now.AddMonths(-3), Type = Enums.historyType.Buy, Quantity = 10, Price = 170 },
                        
                    // Maor (User 2)
                    new Log { UserId = 2, Symbol = "TSLA", Date = DateTime.Now.AddMonths(-11), Type = Enums.historyType.Buy, Quantity = 5, Price = 700 },
                    new Log { UserId = 2, Symbol = "AMZN", Date = DateTime.Now.AddMonths(-9), Type = Enums.historyType.Buy, Quantity = 3, Price = 3200 },
                    new Log { UserId = 2, Symbol = "TSLA", Date = DateTime.Now.AddMonths(-7), Type = Enums.historyType.Sell, Quantity = 2, Price = 750 },
                    new Log { UserId = 2, Symbol = "AMZN", Date = DateTime.Now.AddMonths(-6), Type = Enums.historyType.Sell, Quantity = 1, Price = 3400 },
                    new Log { UserId = 2, Symbol = "TSLA", Date = DateTime.Now.AddMonths(-2), Type = Enums.historyType.Buy, Quantity = 3, Price = 720 },
                };

                context.Logs.AddRange(logs);
                context.SaveChanges();
                Console.WriteLine("✅ Seeded Trades");
            }
        }
    }
}
