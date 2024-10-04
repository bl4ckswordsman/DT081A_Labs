#LAB 1 - 2.3
import numpy as np
import matplotlib.pyplot as plt
from L1_2_1 import img
from L1_2_2 import calculate_psnr

def add_noise(image, std_dev):
    noise = np.random.normal(0, std_dev, image.shape)
    noisy_image = image + noise
    return np.clip(noisy_image, 0, 255).astype(np.uint8)

std_devs = np.linspace(0, 50, 20)
psnr_values = []
for std_dev in std_devs:
    noisy_img = add_noise(img, std_dev)
    psnr = calculate_psnr(img, noisy_img)
    psnr_values.append(psnr)

plt.plot(std_devs, psnr_values)
plt.xlabel('Standard Deviation of Added Noise')
plt.ylabel('PSNR (dB)')
plt.title('PSNR vs. Noise Level')
plt.show()

# Display noisy image at a specific noise level
std_dev_display = 7
noisy_img_display = add_noise(img, std_dev_display)
plt.figure(figsize=(10, 5))
plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Original')
plt.subplot(122), plt.imshow(noisy_img_display, cmap='gray'), plt.title(f'Noisy (std dev = {std_dev_display})')
plt.show()


## 1. At what PSNR value does the noise start to become visibly apparent in
##    the image?

# The noise starts to become visibly apparent around a PSNR of 34.19 (std dev value of 5.0).

def display_noise_levels(image, std_devs):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()

    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original')

    for i, std_dev in enumerate(std_devs, 1):
        noisy_img = add_noise(image, std_dev)
        psnr = calculate_psnr(image, noisy_img)
        axes[i].imshow(noisy_img, cmap='gray')
        axes[i].set_title(f'Std Dev: {std_dev:.2f}\nPSNR: {psnr:.2f} dB')

    plt.tight_layout()
    plt.show()

# Display images with different noise levels
noise_levels = [150, 500, 900, 1500, 2000]
# noise_levels = [5, 10, 20, 30, 50]
display_noise_levels(img, noise_levels)

## 2. How does this PSNR threshold compare to the often-cited 30-50 dB range
##    for acceptable image quality?

# The PSNR threshold of 34.19 dB where noise becomes visibly apparent is within
#  the often-cited range of 30-50 dB for acceptable image quality.

## 3. At what noise level (standard deviation) does the image become
##    unrecognizable? What is the corresponding PSNR?

# The image becomes unrecognizable at a noise level of approximately 500 (PSNR = 27.89).

## 4. Implement a simple noise reduction technique, such as a median filter
##    or Gaussian blur. Apply this to the noisy images and compare the PSNR
##    values before and after noise reduction. Discuss the effectiveness and
##    limitations of this simple denoising approach.

from scipy.ndimage import gaussian_filter

def apply_gaussian_blur(image, sigma):
    return gaussian_filter(image, sigma=sigma)

# Compare original noisy image with Gaussian blurred version
std_dev_noise = 20
noisy_img = add_noise(img, std_dev_noise)
blurred_img = apply_gaussian_blur(noisy_img, sigma=2)

psnr_noisy = calculate_psnr(img, noisy_img)
psnr_blurred = calculate_psnr(img, blurred_img)

plt.figure(figsize=(15, 5))
plt.subplot(131), plt.imshow(img, cmap='gray'), plt.title('Original')
plt.subplot(132), plt.imshow(noisy_img, cmap='gray'), plt.title(f'Noisy (PSNR: {psnr_noisy:.2f} dB)')
plt.subplot(133), plt.imshow(blurred_img, cmap='gray'), plt.title(f'Blurred (PSNR: {psnr_blurred:.2f} dB)')
plt.tight_layout()
plt.show()

print(f"PSNR before denoising: {psnr_noisy:.2f} dB")
print(f"PSNR after denoising: {psnr_blurred:.2f} dB")

# Effectiveness and limitations discussion:
# Gaussian blur effectively reduces noise, improving PSNR.
# However, it also blurs edges and fine details.
# It works well for uniform noise but may struggle with
# preserving important image features.
#
# PSNR before denoising: 28.70 dB
# PSNR after denoising: 32.22 dB

## 5. Research and briefly describe an advanced noise reduction technique.
##    How does it improve upon simpler methods?

"""
Non-Local Means (NLM) Denoising:
- Advanced algorithm that averages similar patches across the entire image
- Improves upon simpler methods by:
  1. Better preserving fine details and edges
  2. Adapting to local image structure
  3. Using non-local information
  4. Handling various noise types effectively

For more details, see: https://doi.org/10.1109/ICIP.2005.1530033
"""
