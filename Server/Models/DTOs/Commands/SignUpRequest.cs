namespace Server.Models.DTOs.Commands;

public class SignUpRequest
{
    public required string Email { get; set; }
    public required string Password { get; set; }
    public required string Name { get; set; }
}
