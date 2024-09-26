#LAB 1 - 1.2
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal as sig


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

## 1. What frequencies are present in the signal? How can you identify them from
##    the frequency domain plot?
#  Frequencies present: 10 Hz and 20 Hz. These appear as peaks in the frequency
#  domain plot.

## 2. Modify the generate_signal function to include a 30 Hz component. How does
##    this change the frequency domain representation?

# This change will:
# - Add a third peak at 30 Hz in the frequency domain plot
# - The new peak will be smaller than the 10 Hz and 20 Hz peaks due to its lower
#   amplitude (0.25)
# - The overall frequency spectrum will now show three distinct components


def generate_signal2(t):
    return np.sin(2 * np.pi * 10 * t) + 0.5 * np.sin(2 * np.pi * 20 * t) + 0.25 * np.sin(2 * np.pi * 30 * t)

signal2 = generate_signal2(t)

# Compute DFT
fft_result2 = np.fft.fft(signal2)
freqs2 = np.fft.fftfreq(len(t), t[1] - t[0])

# Plot
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, signal2)
plt.title('Time Domain')
plt.subplot(2, 1, 2)
plt.plot(freqs2[:len(freqs2)//2], np.abs(fft_result2)[:len(freqs2)//2])
plt.title('Frequency Domain')
plt.xlabel('Frequency (Hz)')
plt.tight_layout()
plt.show()

## 3. What happens to the frequency domain plot if you add random noise to the
##    signal? Implement this and explain your observations.

# Generate signal with noise
noise_amplitude = 0.2
noisy_signal = signal + noise_amplitude * np.random.randn(len(t))

# Compute DFT for noisy signal
fft_result_noisy = np.fft.fft(noisy_signal)

# Plot
plt.figure(figsize=(12, 9))
plt.subplot(3, 1, 1)
plt.plot(t, noisy_signal)
plt.title('Time Domain (Noisy Signal)')
plt.subplot(3, 1, 2)
plt.plot(freqs[:len(freqs)//2], np.abs(fft_result)[:len(freqs)//2])
plt.title('Frequency Domain (Original Signal)')
plt.subplot(3, 1, 3)
plt.plot(freqs[:len(freqs)//2], np.abs(fft_result_noisy)[:len(freqs)//2])
plt.title('Frequency Domain (Noisy Signal)')
plt.xlabel('Frequency (Hz)')
plt.tight_layout()
plt.show()

# - Time domain: Signal appears noisier.
# - Frequency domain:
#    - Main peaks still visible
#    - Raised noise floor across all frequencies
#    - Random fluctuations throughout spectrum
# - Decreased SNR, potentially obscuring weaker frequency components.
# This shows noise's impact on signal representation and the importance of
# noise reduction in signal processing.



## 4. Create a function that generates a signal with a frequency that changes
##    over time (e.g., a chirp signal). Plot this signal in both time and
##    frequency domains and explain what you observe.

def chirp_signal(t, f0, f1):
    return np.sin(2 * np.pi * (f0 * t + (f1 - f0) * t**2 / (2 * len(t))))

t_chirp = np.linspace(0, 1, 1000)
chirp = chirp_signal(t_chirp, 10, 50)  # Frequency changes from 10 Hz to 50 Hz

# Compute STFT
f, t_stft, Zxx = sig.stft(chirp, fs=1000, nperseg=256)

plt.figure(figsize=(12, 8))
plt.subplot(2, 1, 1)
plt.plot(t_chirp, chirp)
plt.title('Time Domain - Chirp Signal')
plt.xlabel('Time [sec]')
plt.ylabel('Amplitude')

plt.subplot(2, 1, 2)
plt.pcolormesh(t_stft, f, 10 * np.log10(np.abs(Zxx)), shading='gouraud', cmap='viridis')
plt.title('Frequency Domain - Spectrogram')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.colorbar(label='Magnitude (dB)')
plt.tight_layout()
plt.show()

# Observations:
# 1. Time domain: Frequency increases over time, visible as compressed waves.
# 2. Frequency domain: Shows increasing frequency as an upward slope in the spectrogram.
# 3. The spectrogram clearly visualizes how the signal's frequency changes with time.


## 5. Describe a practical application where understanding the frequency domain
##    of a signal is important.

# Audio processing is a key application where frequency domain analysis is crucial.
#  It enables:
# 1. Sound equalization
# 2. Instrument identification
# 3. Noise reduction
# 4. Music genre classification
# 5. Voice recognition
# 6. Audio compression (e.g., MP3)

# These applications rely on breaking down complex audio signals into their frequency
#  components, revealing insights not apparent in the time domain.
