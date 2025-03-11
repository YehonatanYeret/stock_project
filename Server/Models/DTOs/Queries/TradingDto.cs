using System.ComponentModel.DataAnnotations.Schema;
using System.ComponentModel.DataAnnotations;

namespace Server.Models.DTOs.Queries;

public class TradingDto
{
    public required string Symbol { get; set; }
    public required DateTime Date { get; set; }
    public Enums.historyType Type { get; set; }
    public int Quantity { get; set; }
    public decimal Price { get; set; }
}