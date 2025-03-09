using System.ComponentModel.DataAnnotations;

namespace Server.Models.DTOs.Queries;

public class SignInRequest
{
    [EmailAddress]
    public required string Email { get; set; }

    public required string Password { get; set; }
}
