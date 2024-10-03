import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import requests
from io import BytesIO
import sounddevice as sd
from matplotlib.widgets import Button


# Audio URL
audio_url = "https://github.com/parisjava/wav-piano-sound/raw/master/wav/a1.wav" # Piano sound
audio_url2 = "https://www.pacdv.com/sounds/ambience_sounds/rain_2.wav" # Rain
audio_url3 = "https://www.pacdv.com/sounds/voices/can-you-keep-a-secret.wav" # Speech

def load_and_analyze_audio(url):
    response = requests.get(url)
    samplerate, data = wavfile.read(BytesIO(response.content))

    # Ensure data is mono
    if len(data.shape) > 1:
        data = data[:, 0]

    # Normalize data
    data = data / np.max(np.abs(data))

    #### Analyze only the first half second ####
    half_second_samples = int(samplerate * 0.5)
    data = data[:half_second_samples]

    # Time array
    time = np.arange(0, len(data)) / samplerate

    # Compute Fourier Transform
    n = len(data)
    fft_result = np.fft.fft(data)
    freqs = np.fft.fftfreq(n, 1/samplerate)

    # Plot waveform, frequency spectrum, and spectrogram
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 15))

    # Time domain plot
    ax1.plot(time, data)
    ax1.set_title('Audio Waveform')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Amplitude')

    # Frequency domain plot
    ax2.plot(freqs[:n//2], np.abs(fft_result[:n//2]))
    ax2.set_title('Frequency Spectrum')
    ax2.set_xlabel('Frequency (Hz)')
    ax2.set_ylabel('Magnitude')

    # Spectrogram
    ax3.specgram(data, Fs=samplerate, NFFT=1024, noverlap=512)
    ax3.set_title('Spectrogram')
    ax3.set_xlabel('Time (s)')
    ax3.set_ylabel('Frequency (Hz)')
    plt.tight_layout()

    # Function to play sound when button is pressed
    def play_sound(event):
        sd.play(data, samplerate)

    # Add play button
    ax_button = plt.axes([0.81, 0.01, 0.1, 0.05])
    button = Button(ax_button, 'Play')
    button.on_clicked(play_sound)
    plt.show()

# Analyze audio
load_and_analyze_audio(audio_url3)

# In Debian, had to run:
# sudo apt-get update
# sudo apt-get install libportaudio2 libportaudiocpp0 portaudio19-dev


## 1. What is the duration of the audio clip? What is its highest frequency component?

# Duration: 0.5 s
# Highest frequency component: 219 Hz (Magnitude of 2350)


## 2. Describe the main features you observe in the spectrogram. What do the bright
##    areas represent?

# The vertical axis represents frequency, ranging from 0 to 20,000 Hz.
# Brighter areas represent higher amplitudes or louder sounds at those frequencies.
# The spectrogram shows distinct horizontal lines, indicating harmonic frequencies.


## 3. Modify the code to analyze only the first half second of the audio. How does
##    this change the frequency spectrum?

# The audio sample was already just about 0.5 seconds long (a bit longer), but now
# a small portion of the end is cut.


## 4. Try using different audio files by changing the audio_url . You can find a
##    variety of sound effects and audio samples at# https://www.pacdv.com/sounds/.
##    How do the waveform, frequency spectrum, and spectrogram differ for different
##    types of audio (e.g., music, speech, environmental sounds)?


## 5. Implement a function to downsample the audio (reduce the sampling rate). How
##  does this affect the audio quality and the frequency spectrum?
##   At what point does aliasing become noticeable?

# The waveform, frequency spectrum, and spectrogram differ significantly for various
#  types of audio:
# - Speech: The waveform is less periodic, the frequency spectrum has peaks
#   corresponding to formants, and the spectrogram shows varying frequency bands
#   representing different phonemes.
# - Environmental sounds: The waveform is more random, the frequency spectrum is
#   more continuous without distinct peaks, and the spectrogram shows a more diffuse
#   pattern with less defined frequency bands.


## 6. Research and briefly describe a common audio processing technique (e.g., noise
##  reduction, pitch shifting, time stretching). How might this technique be
## implemented using the concepts you've learned in this lab?

# **Noise Reduction:**
# Noise reduction removes unwanted noise from an audio signal. A common method is
# spectral subtraction, where the noise spectrum is estimated and subtracted from
# the noisy signal's spectrum.

# **Implementation:**
# 1. Estimate the noise spectrum.
# 2. Compute the Fourier Transform of the noisy signal.
# 3. Subtract the noise spectrum from the noisy signal's spectrum.
# 4. Apply the inverse Fourier Transform to get the denoised signal.


def noise_reduction(noisy_signal, noise_estimate):
    noisy_fft = np.fft.fft(noisy_signal)
    noise_fft = np.fft.fft(noise_estimate)
    denoised_fft = noisy_fft - noise_fft
    denoised_signal = np.fft.ifft(denoised_fft)
    return np.real(denoised_signal)

# Example usage
# noisy_signal = data  # Noisy signal
# noise_estimate = data[:1000]  # Noise estimate
# denoised_signal = noise_reduction(noisy_signal, noise_estimate)
# sd.play(denoised_signal, samplerate)


# This uses Fourier Transform concepts to reduce noise in an audio signal.
