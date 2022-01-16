# convert normal string to AAA

import sys

def string(s):
    compiled = ''
    for item in s:
        compiled += 'AAAA'*ord(item)+'aAaa'+'AaAa'*ord(item)+"\n"
    return compiled

if len(sys.argv) > 0:
    print(string(sys.argv[1]))