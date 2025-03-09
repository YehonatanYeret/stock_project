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

            // seed the users if there are none
            if (!context.Users.Any())
            {
                // Add users
                var users = new List<User>
                    {
                        new User {Name = "Yehonatan", Email = "yeretyn@gmail.com", HashPassword = HashUtils.HashPassword("123456") },
                        new User {Name = "Maor", Email = "manoy@gmail.com", HashPassword = HashUtils.HashPassword("123456") },
                    };

                context.Users.AddRange(users);
                context.SaveChanges();
                Console.WriteLine("Seeded Users");
            }

            // seed the holdings if there are none
            if (!context.Holdings.Any())
            {
                // Add holdings
                var holdings = new List<Holding>
                {
                    new Holding { UserId = 1, Symbol = "AAPL", Quantity = 10},
                    new Holding { UserId = 1, Symbol = "GOOGL", Quantity = 5},
                    new Holding { UserId = 2, Symbol = "TSLA", Quantity = 20},
                    new Holding { UserId = 2, Symbol = "AMZN", Quantity = 15},
                };
                context.Holdings.AddRange(holdings);
                context.SaveChanges();
                Console.WriteLine("Seeded Holdings");
            }

            // seed the trades if there are none
            if (!context.Trades.Any())
            {
                // Add trades
                var trades = new List<Trade>
                    {
                        new Trade { UserId = 1, Symbol = "AAPL", Date = DateTime.Now, Type = Enums.historyType.Buy, Quantity = 10, Price = 100},
                        new Trade { UserId = 1, Symbol = "GOOGL", Date = DateTime.Now, Type = Enums.historyType.Buy, Quantity = 5, Price = 200},
                        new Trade { UserId = 1, Symbol = "TSLA", Date = DateTime.Now, Type = Enums.historyType.Sell, Quantity = 20, Price = 300},
                        new Trade { UserId = 2, Symbol = "AMZN", Date = DateTime.Now, Type = Enums.historyType.Buy, Quantity = 15, Price = 400},
                    };
                context.Trades.AddRange(trades);
                context.SaveChanges();
                Console.WriteLine("Seeded Trades");
            }
        }
    }
}
