using System.ComponentModel.DataAnnotations;

namespace Server.Models;

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

}