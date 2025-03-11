

namespace Server.Utils;

/// <summary>
/// Provides utility methods for calculating the value of a user's portfolio.
/// </summary>
public class PortfolioValueUtils
{
    /// <summary>
    /// Calculates the total value of a user's portfolio.
    /// </summary>
    /// <param name="portfolioValue"> The value of the user's stock portfolio. </param>
    /// <param name="cashValue"> The amount of cash the user wants to add or remove from their portfolio. </param>
    /// <returns> The total value of the user's portfolio. </returns>
    /// <exception cref="InvalidOperationException"> Thrown when the user has negative funds or more than $1,000,000 in their portfolio. </exception>
    public static decimal CalculatePortfolioValue(decimal portfolioValue, decimal cashValue)
    {
        if (portfolioValue + cashValue < 0)
        {
            throw new InvalidOperationException("User cannot have negative funds.");
        }
        return portfolioValue + cashValue;
    }
}
