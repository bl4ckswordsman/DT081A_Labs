import numpy as np
from L1_2_1 import img, img_resampled, img_requantized

def calculate_psnr(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return float('inf')
    max_pixel = 255.0
    psnr = 20 * np.log10(max_pixel / np.sqrt(mse))
    return psnr

# Calculate PSNR for resampled and requantized images
psnr_resampled = calculate_psnr(img, img_resampled)
psnr_requantized = calculate_psnr(img, img_requantized)
print(f"PSNR for resampled image: {psnr_resampled:.2f} dB")
print(f"PSNR for requantized image: {psnr_requantized:.2f} dB")

## 1. Which process (resampling or requantization) introduces more distortion
##    according to the PSNR values?
## 2. How well do the PSNR values correlate with your visual perception of
##    image quality?
## 3. Audio Processing
## 4. Research the Structural Similarity Index (SSIM) as an alternative to
##    PSNR. How does SSIM address some of the limitations of PSNR?
## 5. Implement the SSIM metric and compare its results with PSNR for your
##    processed images. Discuss the differences in how these metrics
##    evaluate image quality.
