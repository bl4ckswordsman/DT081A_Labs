#LAB 1 - 2.2
import numpy as np
import matplotlib.pyplot as plt
from L1_2_1 import img, img_resampled, img_requantized, load_image, resample_image, requantize_image, image_url
from skimage.metrics import structural_similarity as ssim

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

# PSNR for resampled image: 31.73 dB
# PSNR for requantized image: 29.21 dB
# The requantization process introduces more distortion than the resampling.

## 2. How well do the PSNR values correlate with your visual perception of
##    image quality?

# By my visual perception, the PSNR seem misleading. The requantized image
# looks better than the resampled image.

## 3. Create a function that calculates PSNR for different resampling
##    factors and bits per pixel. Plot these results and discuss the
##    trade-offs between compression and quality.

# Observations:
# - Higher resampling factors (more compression) result in lower PSNR (quality)
# - Diminishing returns in PSNR improvement beyond 4-5 bits per pixel
# - Factor 2 offers a good balance between compression and quality
# - Factors 4 and 8 show significant quality loss, especially at lower bpp

def calculate_psnr_for_factors_and_bpp(image, factors, bpp_values):
    results = {}
    for factor in factors:
        for bpp in bpp_values:
            resampled = resample_image(image, factor)
            requantized = requantize_image(resampled, bpp)
            psnr = calculate_psnr(image, requantized)
            results[(factor, bpp)] = psnr
    return results

def plot_psnr_results(results, factors, bpp_values):
    fig, ax = plt.subplots(figsize=(10, 6))

    for factor in factors:
        psnr_values = [results[(factor, bpp)] for bpp in bpp_values]
        ax.plot(bpp_values, psnr_values, marker='o', label=f'Factor {factor}')

    ax.set_xlabel('Bits per Pixel')
    ax.set_ylabel('PSNR (dB)')
    ax.set_title('PSNR vs. Compression')
    ax.legend()
    ax.grid(True)
    plt.show()

# Load the image
img = load_image(image_url)

# Define factors and bpp values to test
factors = [1, 2, 4, 8]
bpp_values = [1, 2, 3, 4, 5, 6, 7, 8]

# Calculate PSNR for different combinations
results = calculate_psnr_for_factors_and_bpp(img, factors, bpp_values)

# Plot the results
plot_psnr_results(results, factors, bpp_values)

## 4. Research the Structural Similarity Index (SSIM) as an alternative
##    to PSNR. How does SSIM address some of the limitations of PSNR?

# SSIM improves on PSNR by:
# 1. Considering structural information humans are sensitive to
# 2. Analyzing local image regions
# 3. Evaluating luminance, contrast, and structure separately
# 4. Correlating better with human perception
# 5. Handling various distortions more effectively
# 6. Being less sensitive to uniform changes that don't affect perceived quality

## 5. Implement the SSIM metric and compare its results with PSNR for
##    your processed images. Discuss the differences in how these metrics
##    evaluate image quality.

# PSNR for resampled image: 31.73 dB
# PSNR for requantized image: 29.21 dB
# SSIM for resampled image: 0.6297
# SSIM for requantized image: 0.8667

# Comparison of SSIM and PSNR results:
# - SSIM shows higher quality for requantized image (0.8667) vs resampled (0.6297)
# - PSNR indicates higher quality for resampled image (31.73 dB) vs requantized (29.21 dB)
# - SSIM aligns better with visual perception, suggesting requantization preserves
#   structure better
# - Both metrics show quality improving with higher bpp, but SSIM curve flattens earlier
# - SSIM differentiates more between resampling factors at higher bpp
# - SSIM may be more reliable for perceptual quality assessment in this context

def calculate_ssim(original, compressed):
    return ssim(original, compressed, data_range=original.max() - original.min())

# Calculate SSIM for resampled and requantized images
ssim_resampled = calculate_ssim(img, img_resampled)
ssim_requantized = calculate_ssim(img, img_requantized)

print(f"PSNR for resampled image: {psnr_resampled:.2f} dB")
print(f"PSNR for requantized image: {psnr_requantized:.2f} dB")
print(f"SSIM for resampled image: {ssim_resampled:.4f}")
print(f"SSIM for requantized image: {ssim_requantized:.4f}")

# Now let's create a function to calculate both PSNR and SSIM for different factors and bpp
def calculate_metrics_for_factors_and_bpp(image, factors, bpp_values):
    results = {}
    for factor in factors:
        for bpp in bpp_values:
            resampled = resample_image(image, factor)
            requantized = requantize_image(resampled, bpp)
            psnr = calculate_psnr(image, requantized)
            ssim_value = calculate_ssim(image, requantized)
            results[(factor, bpp)] = (psnr, ssim_value)
    return results

# Calculate metrics
results = calculate_metrics_for_factors_and_bpp(img, factors, bpp_values)

# Plot the results
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

for factor in factors:
    psnr_values = [results[(factor, bpp)][0] for bpp in bpp_values]
    ssim_values = [results[(factor, bpp)][1] for bpp in bpp_values]
    ax1.plot(bpp_values, psnr_values, marker='o', label=f'Factor {factor}')
    ax2.plot(bpp_values, ssim_values, marker='o', label=f'Factor {factor}')

ax1.set_xlabel('Bits per Pixel')
ax1.set_ylabel('PSNR (dB)')
ax1.set_title('PSNR vs. Compression')
ax1.legend()
ax1.grid(True)

ax2.set_xlabel('Bits per Pixel')
ax2.set_ylabel('SSIM')
ax2.set_title('SSIM vs. Compression')
ax2.legend()
ax2.grid(True)

plt.tight_layout()
plt.show()
