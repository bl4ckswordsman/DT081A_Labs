import numpy as np
import matplotlib.pyplot as plt

def generate_and_sample_signal(f, fs):
    t = np.linspace(0, 1, 1000)
    original = np.sin(2 * np.pi * f * t)
    t_sampled = np.arange(0, 1, 1/fs)
    sampled = np.sin(2 * np.pi * f * t_sampled)
    return t, original, t_sampled, sampled

f = 10 # Signal frequency
fs = 15 # Sampling frequency
t, original, t_sampled, sampled = generate_and_sample_signal(f, fs)

plt.figure(figsize=(12, 6))
plt.plot(t, original, label='Original')
plt.stem(t_sampled, sampled, 'r', label='Sampled')
plt.title(f'Signal ({f} Hz) sampled at {fs} Hz')
plt.legend()
plt.show()

## 1. What is the Nyquist rate for the given signal? Is the current sampling
##    rate sufficient?

# Nyquist rate = 2 * f = 2 * 10 Hz = 20 Hz
# The Nyquist rate for the 10 Hz signal is 20 Hz. The current sampling rate
# of 15 Hz is insufficient, as it's below the Nyquist rate. This can lead to
#  aliasing and inaccurate signal reconstruction.


## 2. Increase the sampling rate to 25 Hz. How does this affect the sampled
##    signal's representation of the original signal?

# Increased sampling rate
fs_new = 25  # New sampling frequency
t, original, t_sampled_new, sampled_new = generate_and_sample_signal(f, fs_new)

plt.figure(figsize=(12, 6))
plt.plot(t, original, label='Original')
plt.stem(t_sampled_new, sampled_new, 'r', label='Sampled')
plt.title(f'Signal ({f} Hz) sampled at {fs_new} Hz')
plt.legend()
plt.show()

# Observation:
# Increasing the sampling rate to 25 Hz improves signal representation. More
#  samples per cycle are captured, resulting in a more accurate reconstruction
#  of the original waveform and reducing the risk of aliasing.


## 3. Set the signal frequency to 20 Hz and the sampling rate to 30 Hz.
##    Describe and explain the resulting aliasing effect.

f_new = 20  # New signal frequency
fs_alias = 30  # Sampling frequency for aliasing demonstration
t, original, t_sampled_alias, sampled_alias = generate_and_sample_signal(f_new, fs_alias)

plt.figure(figsize=(12, 6))
plt.plot(t, original, label='Original')
plt.stem(t_sampled_alias, sampled_alias, 'r', label='Sampled')
plt.title(f'Signal ({f_new} Hz) sampled at {fs_alias} Hz')
plt.legend()
plt.show()

# Observation:
# With a 20 Hz signal sampled at 30 Hz, aliasing occurs. The sampled signal
#  appears as a lower frequency waveform, misrepresenting the original signal.
#  This happens because the sampling rate is below the Nyquist rate (40 Hz
#  for a 20 Hz signal), causing high-frequency components to be incorrectly
#  represented as lower frequencies.


## 4. Create a function that demonstrates the "wagon-wheel effect" by sampling
##    a high-frequency sinusoid at a much lower rate. Plot the original and
##    sampled signals, and explain the visual effect.

def wagon_wheel_effect(f_signal, f_sample, duration=1):
    t = np.linspace(0, duration, 10000)
    original = np.sin(2 * np.pi * f_signal * t)
    t_sampled = np.arange(0, duration, 1/f_sample)
    sampled = np.sin(2 * np.pi * f_signal * t_sampled)

    plt.figure(figsize=(12, 6))
    plt.plot(t, original, label='Original')
    plt.stem(t_sampled, sampled, 'r', label='Sampled', markerfmt='ro')
    plt.title(f'Wagon-wheel effect: {f_signal} Hz signal sampled at {f_sample} Hz')
    plt.legend()
    plt.show()

# Demonstrate the effect
wagon_wheel_effect(f_signal=10, f_sample=11)

# Explanation:
# The "wagon-wheel effect" occurs when a high-frequency signal is sampled
#  at a rate close to, but slightly different from, its frequency or a
#  multiple thereof. In this example, a 10 Hz signal sampled at 11 Hz
#  appears to move slowly in the opposite direction. This illusion
#  happens because the sampling captures the signal at slightly
#  different phases each cycle, creating the appearance of a slower,
#  reverse motion.


## 5. Describe a real-world scenario where understanding aliasing is crucial.

# Digital photography: In image sensors, aliasing can cause moiré patterns
#  when photographing fine, repetitive details like fabric textures or
#  architectural features. Understanding aliasing helps camera manufacturers
#  design anti-aliasing filters and guides photographers in choosing
#  appropriate shooting techniques to avoid these artifacts, ensuring higher
#  image quality.
