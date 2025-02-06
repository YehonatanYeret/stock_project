using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;
using Server.Models;

namespace Server.Data;

// Configuration for the User entity
public class UserConfiguration : IEntityTypeConfiguration<User>
{
    public void Configure(EntityTypeBuilder<User> builder)
    {
        // primary key
        builder.HasKey(u => u.Id);

        // name: required
        builder.Property(u => u.Email)
               .IsRequired();

        // password: required, max length 20
        builder.Property(u => u.HashPassword)
                .IsRequired();

    }
}
