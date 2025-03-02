
namespace Server.Models;


public class Holding
{
    public string Symbol { get; set; }
    public int Quantity { get; set; }
    public decimal BuyPrice { get; set; }
    public decimal CurrentPrice { get; set; }
    public decimal DailyChange { get; set; }
    public decimal ProfitLoss { get; set; }
    public string MarketCap { get; set; }   
    public decimal PeRatio { get; set; }
}
