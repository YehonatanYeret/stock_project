using Microsoft.EntityFrameworkCore;
using Server.Models.Domain;


namespace Server.Data;

/// <summary>
/// Represents the database context for the FamilyLink application.
/// </summary>
/// <param name="options"> The options to be used by the context. </param>
public class StockContext(DbContextOptions<StockContext> options) : DbContext(options)
{
    // dbsets for the models
    public DbSet<User> Users { get; set; } = default!;
    public DbSet<Log> Logs { get; set; } = default!;

    /// <summary>
    /// When the model is created, the configurations for the models are applied.
    /// </summary>
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {

        // call the base method to complete the model creation for each model
        base.OnModelCreating(modelBuilder);
    }

}
