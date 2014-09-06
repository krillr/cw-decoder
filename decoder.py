from scipy.io import wavfile
import numpy as np, Levenshtein

import filters, utils

MORSE_FREQUENCY = 600

class Decoder:
  def __init__(self, fn, options):
    if isinstance(fn, tuple):
      self.sample_rate, self.signal = fn
    else:
      self.sample_rate, self.signal = wavfile.read(fn)
    self.options = options

    self.message = []
    self.remainder = ''

  def process(self):
    self.segment_size = int(self.options['segment_seconds'] * self.sample_rate)
    self.chunk_size = int(self.options['chunk_seconds'] * self.sample_rate)
    for chunk_start in range(0, len(self.signal), self.chunk_size):
      chunk = self.signal[chunk_start:chunk_start+self.chunk_size]
      filtered_chunk = self.filter_signal(chunk)
      samples = self.sample_signal(filtered_chunk)
      groups = self.group_samples(samples)

      tones = [x[1] for x in groups if x[0]]
      pauses = [x[1] for x in groups if not x[0]]

      self.tonetype = np.mean(tones)
      self.charbreak = np.mean(pauses) + np.std(pauses)*0.5
      self.wordbreak = np.mean([x for x in pauses if x > self.charbreak])

      self.message += self.predict(groups)
    if self.remainder and self.remainder in utils.CODEBOOK:
      self.message.append(self.remainder)

  def message_as_string(self):
    return ''.join(utils.CODEBOOK[x] for x in self.message if x in utils.CODEBOOK).replace(' ','')

  def filter_signal(self, signal):
    filtered_signal = filters.bandpass(signal, self.sample_rate,
                                       MORSE_FREQUENCY-self.options['bandwidth'],
                                       MORSE_FREQUENCY+self.options['bandwidth'])
    return filtered_signal

  def sample_signal(self, signal):
    samples = []

    for x in range(0, len(signal), self.segment_size):
      samples.append(np.std(signal[x:x+self.segment_size]))

    threshold = np.mean(samples)
    for x in range(len(samples)):
      if samples[x] < threshold:
        samples[x] = 0

    return samples

  def group_samples(self, samples):
    groups = []

    length = 0
    is_tone = False
    for sample in samples:

      if (is_tone and sample) or (not is_tone and not sample):
        length += 1
      if length and ((is_tone and not sample) or (not is_tone and sample)):
        if length >= self.options['min_sample_length']:
          groups.append((is_tone, length))
        length = 0
      is_tone = bool(sample)

    return groups

  def predict(self, groups):
    c = self.remainder[:]
    message = []
    for is_tone, length in groups:
      if is_tone:
        if length < self.tonetype:
          c += '.'
        else:
          c += '-'
        if len(c) == 6:
          if c in utils.CODEBOOK:
            message.append(c)
            c = ''
          else:
            _c = c[:]
            c = ''
            while _c:
              c += _c[-1]
              _c = _c[:-1]
              if _c in utils.CODEBOOK:
                message.append(_c)
                break
            if len(c) == 6:
              message.append('*')
              c = ''
      elif length >= self.wordbreak and (message or c):
        message.append(c)
        message.append('!')
        c = ''
      elif length >= self.charbreak:
        if c:
          message.append(c)
          c = ''
    self.remainder = c
    return message

