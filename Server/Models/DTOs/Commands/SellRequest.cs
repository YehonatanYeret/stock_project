namespace Server.Models.DTOs.Commands;

public class SellRequest
{
    public int HoldingId { get; set; }
    public int Quantity { get; set; }
    public DateTime SellDate { get; set; } = DateTime.UtcNow;
}
