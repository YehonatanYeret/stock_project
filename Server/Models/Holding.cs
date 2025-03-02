using System.ComponentModel.DataAnnotations;

namespace Server.Models;


public class Holding
{
    [Key]
    public int Id { get; set; }
    public required int UserId { get; set; }
    public required string Symbol { get; set; }
    public int Quantity { get; set; }
    public decimal BuyPrice { get; set; }
    public decimal CurrentPrice { get; set; }
    public decimal DailyChange { get; set; }
    public decimal ProfitLoss { get; set; }
    public required string MarketCap { get; set; }
    public decimal PeRatio { get; set; }
}
