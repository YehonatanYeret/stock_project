namespace Server.Models.DTOs.Commands;

public class TransactionRequest
{
    public required string Ticker { get; set; }
    public decimal Quantity { get; set; }
    public DateTime Date { get; set; } = DateTime.UtcNow;
}
