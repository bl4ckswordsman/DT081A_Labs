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


## 5. Modify the code to implement a more advanced resampling method, such
##  as bicubic interpolation. Compare the results with the simple
##  resampling method used initially. Discuss the trade-offs between
##  image quality and computational complexity.


## 6. Try using different images by changing the image_url . You can find
##  a variety of test images at the USC-SIPI Image Database
## (http://sipi.usc.edu/database/). How do the effects of resampling and
##  requantization vary for different types of images (e.g., portraits,
##  textures, aerial photos)?
