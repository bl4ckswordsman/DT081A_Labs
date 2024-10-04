#LAB 1 - 2.1
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import requests
from io import BytesIO

# Image URL
image_url = "https://upload.wikimedia.org/wikipedia/en/7/7d/Lenna_%28test_image%29.png"

def load_image(url):
    response = requests.get(url)
    return np.array(Image.open(BytesIO(response.content)).convert('L'))

def resample_image(image, factor):
    small = image[::factor, ::factor]
    return np.repeat(np.repeat(small, factor, axis=0), factor, axis=1)

def requantize_image(image, bpp):
    levels = 2**bpp
    return np.floor(image / (256/levels)) * (256/levels)

# Load image
img = load_image(image_url)
# Process image
factor = 4
bpp = 4

img_resampled = resample_image(img, factor)
img_requantized = requantize_image(img, bpp)

plt.figure(figsize=(15, 5))
plt.subplot(131), plt.imshow(img, cmap='gray'), plt.title('Original') # type: ignore
plt.subplot(132), plt.imshow(img_resampled, cmap='gray'), plt.title(f'Resampled (factor {factor})') # type: ignore
plt.subplot(133), plt.imshow(img_requantized, cmap='gray'), plt.title(f'Requantized ({bpp} bpp)') # type: ignore
plt.savefig('processed_image.png')
plt.show()

## 1. How does the resampling factor affect the image quality? At what factor
##    does the distortion become apparent?

# Function to display multiple resampled images
def display_resampled_images(image, factors):
    n = len(factors) + 1
    fig, axes = plt.subplots(1, n, figsize=(5*n, 5))

    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original')

    for i, factor in enumerate(factors, 1):
        resampled = resample_image(image, factor)
        axes[i].imshow(resampled, cmap='gray')
        axes[i].set_title(f'Factor {factor}')

    plt.tight_layout()
    plt.show()

# Display resampled images with different factors
factors = [2, 4, 8, 16]
display_resampled_images(img, factors)

# Observations:
# 1. As the resampling factor increases, image quality decreases.
# 2. Distortion becomes noticeable at factor 4, with loss of fine details.
# 3. At factor 8 and above, the image is significantly pixelated and degraded.
# 4. The exact point of noticeable distortion may vary depending on image
#  content and viewer perception.


## 2. What is the characteristic of the distortion introduced by resampling?
##    How does it differ from the distortion introduced by requantization?

# Resampling distortion:
# - Introduces pixelation and loss of fine details
# - Maintains overall contrast and brightness
# Requantization distortion:
# - Causes banding or posterization
# - Reduces number of gray levels, creating abrupt tonal transitions
# Key differences:
# - Resampling affects spatial resolution; requantization affects tonal
#   resolution
# - Resampling creates a blocky appearance; requantization creates a banded
#   look
# - Resampling loses detail; requantization simplifies tonal gradients


## 3. How few bits per pixel can be used in requantization before the image
##    distortion becomes apparent?

def display_requantized_images(image, bpp_values):
    n = len(bpp_values) + 1
    fig, axes = plt.subplots(1, n, figsize=(5*n, 5))

    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original (8 bpp)')

    for i, bpp in enumerate(bpp_values, 1):
        requantized = requantize_image(image, bpp)
        axes[i].imshow(requantized, cmap='gray')
        axes[i].set_title(f'{bpp} bpp')

    plt.tight_layout()
    plt.show()

# Display requantized images with different bpp
bpp_values = [7, 6, 5, 4, 3, 2, 1]
display_requantized_images(img, bpp_values)

# Observations:
# - Distortion becomes noticeable at 5-6 bpp
# - At 4 bpp, banding effects are clearly visible
# - 3 bpp and below show severe degradation
# - The exact point of noticeable distortion may vary depending on image
#   content and viewer perception


## 4. Implement a function that applies both resampling and requantization
##    to the image. Experiment with different combinations of factors and
##    bits per pixel. What combination gives the best balance between
##    compression and visual quality?

def resample_and_requantize(image, factor, bpp):
    resampled = resample_image(image, factor)
    return requantize_image(resampled, bpp)

def display_processed_images(image, combinations):
    n = len(combinations) + 1
    fig, axes = plt.subplots(1, n, figsize=(5*n, 5))

    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original')

    for i, (factor, bpp) in enumerate(combinations, 1):
        processed = resample_and_requantize(image, factor, bpp)
        axes[i].imshow(processed, cmap='gray')
        axes[i].set_title(f'Factor {factor}, {bpp} bpp')

        # Calculate compression ratio
        original_size = image.shape[0] * image.shape[1] * 8  # 8 bpp original
        compressed_size = (image.shape[0] // factor) * (image.shape[1] // factor) * bpp
        compression_ratio = original_size / compressed_size
        axes[i].set_xlabel(f'Compression: {compression_ratio:.1f}x')

    plt.tight_layout()
    plt.show()

# Experiment with different combinations
combinations = [
    (2, 6), (2, 4), (4, 6), (4, 4), (8, 6), (8, 4)
]
display_processed_images(img, combinations)

# Observations:
# - Factor 2 with 6 bpp provides good balance between quality and compression
# - Factor 4 with 6 bpp offers higher compression with acceptable quality
# - Factor 8 introduces significant pixelation, even at 6 bpp
# - 4 bpp shows noticeable banding in all cases
# - The best balance depends on the specific use case and quality requirements
# - For general purpose, factor 2 or 4 with 6 bpp seems to offer a good
#   compromise



## 5. Modify the code to implement a more advanced resampling method, such
##  as bicubic interpolation. Compare the results with the simple
##  resampling method used initially. Discuss the trade-offs between
##  image quality and computational complexity.

from scipy import ndimage

def resample_bicubic(image, factor):
    new_shape = (image.shape[0] // factor, image.shape[1] // factor)
    return ndimage.zoom(image, 1/factor, order=3)

def compare_resampling_methods(image, factor):
    simple_resampled = resample_image(image, factor)
    bicubic_resampled = resample_bicubic(image, factor)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))

    axes[0].imshow(image, cmap='gray')
    axes[0].set_title('Original')

    axes[1].imshow(simple_resampled, cmap='gray')
    axes[1].set_title(f'Simple (factor {factor})')

    axes[2].imshow(bicubic_resampled, cmap='gray')
    axes[2].set_title(f'Bicubic (factor {factor})')

    plt.tight_layout()
    plt.show()

# Compare simple and bicubic resampling
compare_resampling_methods(img, 4)

# Measure execution time
import time

def measure_time(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start

simple_result, simple_time = measure_time(resample_image, img, 4)
bicubic_result, bicubic_time = measure_time(resample_bicubic, img, 4)

print(f"Simple resampling time: {simple_time:.4f} seconds")
print(f"Bicubic resampling time: {bicubic_time:.4f} seconds")

# Observations:
# 1. Image Quality:
#    - Bicubic interpolation produces smoother results with less pixelation
#    - Simple resampling creates a more blocky appearance
#    - Bicubic preserves more detail and edge information
#
# 2. Computational Complexity:
#    - Simple resampling is significantly faster
#    - Bicubic interpolation requires more computational resources
#
# 3. Trade-offs:
#    - Simple resampling is preferred for speed and low computational
#      resources
#    - Bicubic is better for higher quality output, especially for larger
#      factors
#    - The choice depends on the specific application requirements (speed vs.
#      quality)
#
# 4. Use cases:
#    - Simple: Real-time applications, preview generation
#    - Bicubic: Final image processing, high-quality downscaling


## 6. Try using different images by changing the image_url . You can find
##  a variety of test images at the USC-SIPI Image Database
## (http://sipi.usc.edu/database/). How do the effects of resampling and
##  requantization vary for different types of images (e.g., portraits,
##  textures, aerial photos)?

# The quantized images generally seem to have a better balance between compression and visual quality.
#  Whereas the resampled images are more pixelated and lose more detail.
# - Image with a person: Visble pixelation in the resampled image.
# - Grass texture: The requantized image looks more natural and less pixelated.
# - Aerial photo: The requantized image has unnoticeable quality loss without zooming in.
#   The resampled image is more pixelated.
# - Peppers: Heavy pixelation in the resampled image, while the requantized image looks better.

# List of local file paths
image_paths = [
    "images/male_portrait.tiff",
    "images/grass_texture.tiff",
    "images/sandiego_aerial.tiff",
    "images/peppers.tiff"
]

def load_local_image(path):
    return np.array(Image.open(path).convert('L'))

def process_and_display(path, factor, bpp):
    img = load_local_image(path)
    resampled = resample_image(img, factor)
    requantized = requantize_image(img, bpp)

    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].imshow(img, cmap='gray')
    axes[0].set_title('Original')
    axes[1].imshow(resampled, cmap='gray')
    axes[1].set_title(f'Resampled (factor {factor})')
    axes[2].imshow(requantized, cmap='gray')
    axes[2].set_title(f'Requantized ({bpp} bpp)')
    plt.tight_layout()
    plt.show()

# Process each image
for path in image_paths:
    process_and_display(path, factor=4, bpp=4)
