namespace Server.Models.DTOs.Commands;

public class BuyRequest
{
    public int UserId { get; set; }
    public required string Symbol { get; set; }
    public int Quantity { get; set; }
    public DateTime BuyDate { get; set; } = DateTime.UtcNow;
}
