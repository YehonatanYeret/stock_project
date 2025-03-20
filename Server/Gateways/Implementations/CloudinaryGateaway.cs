using CloudinaryDotNet;
using CloudinaryDotNet.Actions;
using Microsoft.Extensions.Configuration;
using Server.Gateways.Interfaces;

namespace Server.Gateways.Implementations
{
    public class CloudinaryGateway : IImageGateaway

    {
        private readonly Cloudinary _cloudinary;

        public CloudinaryGateway(IConfiguration configuration)
        {
            _cloudinary = new Cloudinary(configuration["ApiKeys:cloudinary"]);
            _cloudinary.Api.Secure = true;
        }

        /// <summary>
        /// Upload an image to Cloudinary and return the URL.
        /// </summary>
        public async Task<ImageUploadResult> UploadImageAsync(string imageUrl, string fileName)
        {
            var uploadParams = new ImageUploadParams
            {
                File = new FileDescription(imageUrl),
                PublicId=fileName,
                UniqueFilename = false,
                Overwrite = true
            };

            return await _cloudinary.UploadAsync(uploadParams);
        }

        /// <summary>
        /// Retrieve an image URL from Cloudinary using the public ID.
        /// </summary>
        public string? GetImageUrl(string publicId)
        {
            try
            {
                var getResourceParams = new GetResourceParams(publicId);
                var getResourceResult = _cloudinary.GetResource(getResourceParams);
                Console.WriteLine(getResourceResult.SecureUrl);
                return getResourceResult?.SecureUrl;
            }
            catch
            {
                return null; // Image not found in Cloudinary
            }
        }
    }
}
