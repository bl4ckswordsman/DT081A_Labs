import numpy as np
import matplotlib.pyplot as plt

# Time vector
t = np.linspace(0, 1, 1000)

# Generate signals
sine_wave = np.sin(2 * np.pi * 10 * t)
square_wave = np.sign(np.sin(2 * np.pi * 5 * t))

# Plot signals
# plt.figure(figsize=(12, 6))
# plt.subplot(2, 1, 1)
# plt.plot(t, sine_wave)
# plt.title('Sine Wave')
#
# plt.subplot(2, 1, 2)
# plt.plot(t, square_wave)
# plt.title('Square Wave')
# plt.tight_layout()
# plt.show()

######################
# L1.1
#
## 1. Modify the code to create a sawtooth wave.
#    Describe the mathematical function you used.

sawtooth_wave = 2 * (t * 5 - np.floor(0.5 + t * 5))
# This function creates a sawtooth wave by:
# 1. Multiplying time t by frequency (5 Hz)
# 2. Subtracting the floor of (t*5 + 0.5) to create periodic ramps
# 3. Multiplying by 2 to scale the amplitude to [-1, 1]

# Plot signals
plt.figure(figsize=(12, 6))
plt.title('L1.1 (1) - Sawtooth wave')
plt.plot(t, sawtooth_wave)
plt.show()

## 2. Change the frequency of the sine wave to 20 Hz.
##    How does this affect the plot?
#    Changing the frequency to 20 Hz doubles the number of cycles,
#    making the waveform appear more compressed horizontally.
sine_wave_2 = np.sin(2 * np.pi * 20 * t)

plt.figure(figsize=(12, 6))
plt.plot(t, sine_wave, label='10 Hz')
plt.plot(t, sine_wave_2, label='20 Hz')
plt.title('L1.1 (2) - Sine Wave with f=20 Hz')
plt.xlim(0, 0.2)  # Set x-axis range from 0 to 0.2 seconds
plt.xlabel('Time (s)')
plt.legend()
plt.show()

## 3. What happens to the square wave if you change the sign function
##    to np.ceil(np.sin(2 * np.pi * 5 * t)) * 2 - 1 ? Explain why.

square_wave2 = np.ceil(np.sin(2 * np.pi * 5 * t)) * 2 - 1

# The original square wave transitions symmetrically between +1 and -1,
# while the modified square wave using np.ceil stays at +1 for a
# longer portion of the cycle, switching to -1 abruptly. This
# difference occurs because np.ceil rounds up the sine values,
# extending the time spent at the positive level.

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t, square_wave)
plt.title('L1.1 (3) - Square Wave')

plt.subplot(2, 1, 2)
plt.plot(t, square_wave2)
plt.title('L1.1 (3) - New Square Wave')

plt.tight_layout()
plt.show()

## 4. Create a composite signal by adding the sine wave and square wave
##    together. Plot this new signal and describe its characteristics.

composite_signal = sine_wave + square_wave

# "The composite signal shows:
# 1. A distorted sine-like shape
# 2. Amplitude range of approximately -2 to +2
# 3. Dominant higher frequency from the sine wave
# 4. Sharp transitions from the square wave
# 5. Visible 'beats' due to frequency interference"


plt.figure(figsize=(12, 6))
plt.plot(t, composite_signal)
plt.title('L1.1 (4) - Composite Signal (Sine + Square)')
plt.xlabel('Time (s)')
plt.ylabel('Amplitude')
plt.grid(True)
plt.show()

## 5. How might understanding different signal types be useful in
## real-world applications? Provide an example.

# Understanding signal types is crucial in medical devices:

# - Sine waves in ECG machines to detect heart rhythms
# - Square waves in pacemakers to regulate heartbeats
# - Sawtooth waves in nerve stimulators for pain management

# This knowledge enables engineers to design precise, effective medical
#  equipment for diagnosis and treatment.
