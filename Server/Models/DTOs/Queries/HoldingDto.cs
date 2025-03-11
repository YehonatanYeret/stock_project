namespace Server.Models.DTOs.Queries;

public class HoldingDto
{
    public int Id { get; set; }
    public required string Symbol { get; set; }
    public int Quantity { get; set; }
    public decimal CurrentPrice { get; set; }
    public decimal TotalValue { get; set; }
    public decimal TotalGain { get; set; }
    public decimal TotalGainPercentage { get; set; }

}
