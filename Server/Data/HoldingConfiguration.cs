namespace Server.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Server.Models;


public class HoldingConfiguration : IEntityTypeConfiguration<Holding>
{
    public void Configure(EntityTypeBuilder<Holding> builder)
    {
        builder.HasKey(h => h.Id);

        builder.Property(h => h.UserId)
            .IsRequired();

        builder.Property(h => h.Symbol)
            .IsRequired();

        builder.Property(h => h.Quantity)
            .IsRequired();

        builder.Property(h => h.BuyPrice)
            .IsRequired();
    }
}
