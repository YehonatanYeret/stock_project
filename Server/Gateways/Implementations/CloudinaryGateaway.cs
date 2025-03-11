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
        public async Task<string> UploadImageAsync(IFormFile file)
        {
            using (var stream = file.OpenReadStream())
            {
                var uploadParams = new ImageUploadParams
                {
                    File = new FileDescription(file.FileName, stream),
                    UseFilename = true,
                    UniqueFilename = false,
                    Overwrite = true

                };

                var uploadResult = await _cloudinary.UploadAsync(uploadParams);
                return uploadResult.SecureUrl.AbsoluteUri;
            }
        }

        /// <summary>
        /// Retrieve an image URL from Cloudinary using the public ID.
        /// </summary>
        public string GetImageUrl(string publicId)
        {
            return _cloudinary.Api.UrlImgUp.Secure(true).BuildUrl(publicId);
        }
    }
}
