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


## 2. What is the characteristic of the distortion introduced by resampling?
##    How does it differ from the distortion introduced by requantization?


## 3. How few bits per pixel can be used in requantization before the image
##    distortion becomes apparent?


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
