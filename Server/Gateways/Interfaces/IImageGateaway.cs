using CloudinaryDotNet.Actions;

namespace Server.Gateways.Interfaces;

public interface IImageGateaway
{
    /// <summary>
    /// Upload an image to the cloud storage and return the URL.
    /// </summary>
    /// <param name="file">the file to uplaod</param>
    /// <returns></returns>
    public Task<ImageUploadResult> UploadImageAsync(string imageUrl, string fileName);
    /// <summary>
    /// Retrieve an image URL from the cloud storage using the public ID.
    /// </summary>
    /// <param name="publicId"></param>
    /// <returns></returns>
    public string? GetImageUrl(string publicId);
}
