using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Server.Models.Domain;


/// <summary>
/// this class represent the holding of a user. the user can have multiple holdings
/// </summary>
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
