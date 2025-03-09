namespace Server.Gateways.Interfaces
{
    public interface IPolygonGateway
    {
        //Task<decimal> GetStockPriceAsync(string symbol);
        Task<string> GetAggregateDataAsync(string ticker, string startDate, string endDate);

        Task<decimal> GetSellPriceAsync(string ticker, DateTime date);
    }
}
