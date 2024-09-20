#LAB 1 - 1.2
import numpy as np
import matplotlib.pyplot as plt

def generate_signal(t):
    return np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 20 * t)

t = np.linspace(0, 1, 1000)
signal = generate_signal(t)

# Compute DFT
fft_result = np.fft.fft(signal)
freqs = np.fft.fftfreq(len(t), t[1] - t[0])

# Plot
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, signal)
plt.title('Time Domain')
plt.subplot(2, 1, 2)
plt.plot(freqs[:len(freqs)//2], np.abs(fft_result)[:len(freqs)//2])
plt.title('Frequency Domain')
plt.xlabel('Frequency (Hz)')
plt.tight_layout()
plt.show()
