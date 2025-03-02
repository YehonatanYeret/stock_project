using System.ComponentModel.DataAnnotations;
namespace Server.Models;

public class Trade
{
    [Key]
    public int Id { get; set; }
    public required string Symbol { get; set; }
    public required DateTime Date { get; set; }
    public required string Type { get; set; }
    public int Quantity { get; set; }
    public decimal Price { get; set; }
    public decimal Fees { get; set; }
}
