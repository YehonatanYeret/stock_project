
namespace Server.Models;

public class Trade
{
    public string Date { get; set; }
    public string Symbol { get; set; }
    public string Type { get; set; }
    public int Quantity { get; set; }
    public decimal Price { get; set; }
    public decimal Fees { get; set; }
} 