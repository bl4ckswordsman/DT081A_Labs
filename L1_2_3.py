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
std_dev_display = 25
noisy_img_display = add_noise(img, std_dev_display)
plt.figure(figsize=(10, 5))
plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Original')
plt.subplot(122), plt.imshow(noisy_img_display, cmap='gray'), plt.title(f'Noisy (std dev = {std_dev_display})')
plt.show()
