namespace Server.Models.DTOs
{
    public class TickerMetadataDto
    {
        public required string Ticker { get; set; }
        public required string Name { get; set; }
        public required string Description { get; set; }
        public required string Logo { get; set; }
    }
}
