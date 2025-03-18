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
            if (context == null || context.Users == null || context.Holdings == null || context.Trades == null)
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

            // ✅ Seed Holdings
            if (!context.Holdings.Any())
            {
                var holdings = new List<Holding>
                {
                    new Holding { UserId = 1, Symbol = "AAPL", Quantity = 15 },
                    new Holding { UserId = 1, Symbol = "GOOGL", Quantity = 10 },
                    new Holding { UserId = 2, Symbol = "TSLA", Quantity = 8 },
                    new Holding { UserId = 2, Symbol = "AMZN", Quantity = 5 },
                };

                context.Holdings.AddRange(holdings);
                context.SaveChanges();
                Console.WriteLine("✅ Seeded Holdings");
            }

            // ✅ Seed Trades (Over a Year with Buys & Sells)
            if (!context.Trades.Any())
            {
                var trades = new List<Trade>
                {
                    // Yehonatan (User 1)
                    new Trade { UserId = 1, Symbol = "AAPL", Date = DateTime.Now.AddMonths(-12), Type = Enums.historyType.Buy, Quantity = 10, Price = 150 },
                    new Trade { UserId = 1, Symbol = "GOOGL", Date = DateTime.Now.AddMonths(-10), Type = Enums.historyType.Buy, Quantity = 5, Price = 2500 },
                    new Trade { UserId = 1, Symbol = "AAPL", Date = DateTime.Now.AddMonths(-8), Type = Enums.historyType.Sell, Quantity = 5, Price = 180 },
                    new Trade { UserId = 1, Symbol = "GOOGL", Date = DateTime.Now.AddMonths(-5), Type = Enums.historyType.Sell, Quantity = 2, Price = 2600 },
                    new Trade { UserId = 1, Symbol = "AAPL", Date = DateTime.Now.AddMonths(-3), Type = Enums.historyType.Buy, Quantity = 10, Price = 170 },

                    // Maor (User 2)
                    new Trade { UserId = 2, Symbol = "TSLA", Date = DateTime.Now.AddMonths(-11), Type = Enums.historyType.Buy, Quantity = 5, Price = 700 },
                    new Trade { UserId = 2, Symbol = "AMZN", Date = DateTime.Now.AddMonths(-9), Type = Enums.historyType.Buy, Quantity = 3, Price = 3200 },
                    new Trade { UserId = 2, Symbol = "TSLA", Date = DateTime.Now.AddMonths(-7), Type = Enums.historyType.Sell, Quantity = 2, Price = 750 },
                    new Trade { UserId = 2, Symbol = "AMZN", Date = DateTime.Now.AddMonths(-6), Type = Enums.historyType.Sell, Quantity = 1, Price = 3400 },
                    new Trade { UserId = 2, Symbol = "TSLA", Date = DateTime.Now.AddMonths(-2), Type = Enums.historyType.Buy, Quantity = 3, Price = 720 },
                };

                context.Trades.AddRange(trades);
                context.SaveChanges();
                Console.WriteLine("✅ Seeded Trades");
            }
        }
    }
}
