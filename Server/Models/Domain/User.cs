using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace Server.Models.Domain;

public class User
{
    [Key]
    public int Id { get; set; }

    // required and in email format
    [Required, EmailAddress]
    public required string Email { get; set; }

    [Required]
    public required string HashPassword { get; set; }

    public required string Name { get; set; }

    [Column(TypeName = "decimal(18,2)")]  // Ensures proper precision in the database
    public decimal PortfolioValue { get; set; } = 0;

}