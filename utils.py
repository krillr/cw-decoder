import re, string

RESULT_RE = re.compile('^[A-Z0-9]+$')
ALLOWED = string.uppercase + string.digits
CODEBOOK = {
  '.-'  :'A', '-...':'B', '-.-.':'C', '-..' :'D', '.' :'E',
  '..-.':'F', '--.' :'G', '....':'H', '..'  :'I', '.---':'J',
  '-.-':'K', '.-..' : 'L', '--' :'M', '-.' :'N', '---':'O',
  '.--.' : 'P', '--.-' : 'Q', '.-.':'R', '...':'S', '-'  :'T',
  '..-':'U', '...-' : 'V', '.--':'W', '-..-' : 'X', '-.--' : 'Y',
  '--..' : 'Z', '.----' : '1', '..---' : '2', '...--' : '3',
  '....-' : '4', '.....' : '5', '-....' : '6', '--...' : '7',
  '---..' : '8','----.' : '9','-----' : '0',
  '-...-' : '=', '.-.-':'~', '.-...' :'*', '.-.-.' : '*', '...-.-' : '*',
  '-.--.' : '*', '..-.-' : '*', '....--' : '*', '...-.' : '*',
  '.-..-.' : '\\', '.----.' : '\'', '...-..-' : '$', '-.--.' : '(', '-.--.-' : ')',
  '--..--' : ',', '-....-' : '-', '.-.-.-' : '.', '-..-.' : '/', '---...' : ':',
  '-.-.-.' : ';', '..--..' : '?', '..--.-' : '_', '.--.-.' : '@', '-.-.--' : '!', '!': ' ', '*': '*'
}

def cmp(x,y):
  if len(x) == 20 and len(y) != 20: return -1
  if len(y) == 20 and len(x) != 20: return 1
  if RESULT_RE.match(x) and not RESULT_RE.match(y): return -1
  if RESULT_RE.match(y) and not RESULT_RE.match(x): return 1

  x_bad = len([z for z in x if z not in ALLOWED])
  y_bad = len([z for z in y if z not in ALLOWED])

  if y_bad > x_bad: return -1
  if x_bad > y_bad: return 1

  x_len_delta = abs(20-len(x))
  y_len_delta = abs(20-len(y))

  if y_len_delta > x_len_delta: return -1
  if x_len_delta > y_len_delta: return 1

  return 0
