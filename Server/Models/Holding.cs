using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Server.Models;


public class Holding
{
    [Key]
    public int Id { get; set; }

    [ForeignKey("User")]
    public required int UserId { get; set; }
    public required string Symbol { get; set; }
    public int Quantity { get; set; }
    public decimal BuyPrice { get; set; }
}
