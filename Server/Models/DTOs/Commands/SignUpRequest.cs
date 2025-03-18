using System.ComponentModel.DataAnnotations;

namespace Server.Models.DTOs.Commands;

public class SignUpRequest
{
    [EmailAddress]
    public required string Email { get; set; }
    public required string Password { get; set; }
    public required string Name { get; set; }
}
