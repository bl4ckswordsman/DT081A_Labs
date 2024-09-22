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
