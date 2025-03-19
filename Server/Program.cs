using Microsoft.EntityFrameworkCore;
using MyApp.Controllers;
using Server.Data;
using Server.Gateways.Implementations;
using Server.Gateways.Interfaces;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllersWithViews();

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

builder.Services.AddScoped<IStocksGateway, PolygonGateway>();
builder.Services.AddScoped<IImageGateaway, CloudinaryGateway>();
builder.Services.AddHttpClient<ModelController>(client =>
{
    client.Timeout = Timeout.InfiniteTimeSpan;
});

builder.Services.AddDbContext<StockContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("StockContext")
    ?? throw new InvalidOperationException("No connection string found.")));

var app = builder.Build();

using (var scope = app.Services.CreateScope())
{
    var services = scope.ServiceProvider;
    SeedData.Initialize(services);
    var context = new StockContext(
               services.GetRequiredService<
                   DbContextOptions<StockContext>>());

}

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
}

app.UseAuthorization();

app.MapControllers();

app.Run();
