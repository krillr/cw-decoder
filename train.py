import decoder, itertools, sys, Levenshtein

bandwidths = [('bandwidth',x) for x in range(5,51)]
segment_seconds = [('segment_seconds', x/1000.0) for x in range(1,50, 10)]
chunk_seconds = [('chunk_seconds', x/2.0) for x in range(1, 5)]
min_sample_length = [('min_sample_length', x) for x in range(1,5)]

possible_options = list(itertools.product(bandwidths, segment_seconds, chunk_seconds, min_sample_length))
print len(possible_options)
results = []
for optionset in possible_options:
  options = dict(optionset)
  _decoder = decoder.Decoder(sys.argv[1], options)
  import time
  t = time.time()
  _decoder.process()
  results.append((time.time()-t, Levenshtein.distance(_decoder.message_as_string(), '63BTNYH7OJ7XKBNYOV49'), options))
  print results[-1][:2]
f=open("training", 'w')
import json
json.dump(results, f)
f.close()
