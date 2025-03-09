using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
namespace Server.Models.Domain;

public class Trade
{
    [Key]
    public int Id { get; set; }

    [ForeignKey("User")]
    public required int UserId { get; set; }
    public required string Symbol { get; set; }
    public required DateTime Date { get; set; }
    public Enums.historyType Type { get; set; }
    public int Quantity { get; set; }
    public decimal Price { get; set; }
}
