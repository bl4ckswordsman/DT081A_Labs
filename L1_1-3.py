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

## 2. Increase the sampling rate to 25 Hz. How does this affect the sampled
##    signal's representation of the original signal?

## 3. Set the signal frequency to 20 Hz and the sampling rate to 30 Hz.
##    Describe and explain the resulting aliasing effect.

## 4. Create a function that demonstrates the "wagon-wheel effect" by sampling
##    a high-frequency sinusoid at a much lower rate. Plot the original and
##    sampled signals, and explain the visual effect.

## 5. Describe a real-world scenario where understanding aliasing is crucial.
