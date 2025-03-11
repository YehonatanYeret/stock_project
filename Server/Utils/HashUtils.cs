using System.Security.Cryptography;

namespace Server.Utils;

/// <summary>
/// Provides utility methods for securely hashing and verifying passwords using PBKDF2 with SHA-256.
/// </summary>
public static class HashUtils
{
    /// <summary>
    /// Hashes a password using PBKDF2 with SHA-256 and a randomly generated salt.
    /// </summary>
    /// <param name="password">The plaintext password to be hashed.</param>
    /// <returns>
    /// A base64-encoded string containing the salt and hashed password.
    /// </returns>
    public static string HashPassword(string password)
    {
        // Generate a 16-byte salt
        byte[] salt = new byte[16];
        using (var rng = RandomNumberGenerator.Create())
        {
            rng.GetBytes(salt);
        }

        // Derive a 32-byte hash using PBKDF2 with SHA-256
        using (var pbkdf2 = new Rfc2898DeriveBytes(password, salt, 100000, HashAlgorithmName.SHA256))
        {
            byte[] hash = pbkdf2.GetBytes(32);

            // Combine salt and hash into a single array
            byte[] hashBytes = new byte[salt.Length + hash.Length];
            Array.Copy(salt, 0, hashBytes, 0, salt.Length);
            Array.Copy(hash, 0, hashBytes, salt.Length, hash.Length);

            // Convert to base64 for storage
            return Convert.ToBase64String(hashBytes);
        }
    }

    /// <summary>
    /// Verifies whether an entered password matches a stored hashed password.
    /// </summary>
    /// <param name="enteredPassword">The plaintext password entered by the user.</param>
    /// <param name="storedHash">The stored base64-encoded hash that includes the salt.</param>
    /// <returns>
    /// <c>true</c> if the entered password matches the stored hash; otherwise, <c>false</c>.
    /// </returns>
    public static bool VerifyPassword(string enteredPassword, string storedHash)
    {
        try
        {
            // Decode stored hash from base64
            byte[] hashBytes = Convert.FromBase64String(storedHash);

            // Extract the salt (first 16 bytes)
            byte[] salt = new byte[16];
            Array.Copy(hashBytes, 0, salt, 0, salt.Length);

            // Derive the hash using the extracted salt
            using (var pbkdf2 = new Rfc2898DeriveBytes(enteredPassword, salt, 100000, HashAlgorithmName.SHA256))
            {
                byte[] hash = pbkdf2.GetBytes(32);

                // Compare the stored hash with the newly generated hash
                for (int i = 0; i < hash.Length; i++)
                {
                    if (hashBytes[salt.Length + i] != hash[i])
                    {
                        return false; // Mismatch found
                    }
                }
            }
            return true; // Passwords match
        }
        catch
        {
            return false; // Handle invalid hash format or decoding errors
        }
    }
}
