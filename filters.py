from numpy.fft import fft, fftfreq, ifft
import numpy as np

def bandpass(signal, sample_rate, minfreq, maxfreq):
  F = fft(signal)
  f = fftfreq(len(F), 1.0/sample_rate)

  F_filtered = np.array([_bandpass(x, freq, minfreq, maxfreq) for x, freq in zip(F, f)])
  f_filtered = ifft(F_filtered)

  return f_filtered  

def _bandpass(x,freq,minfreq,maxfreq):
  if abs(freq) >= maxfreq or abs(freq) <= minfreq:
    return 0
  return x 

def squelch(signal):
  amplitudes = np.log10(numpy.abs(f_filtered))
  threshold = np.median(signal_amplitudes)
  a_filtered = np.array([_squelch(x, amplitude, threshold) for x, amplitude in zip(signal, amplitudes)])

  return a_filtered 

def _squelch(x, amplitude, threshold):
  if abs(amplitude) <= threshold:
    return 0
  return x
