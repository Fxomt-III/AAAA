import sys

def execute(filename):
  f = open(filename, "r")
  evaluate(f.read())
  f.close()


class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


getch = _Getch()

def evaluate(code):
  code     = cleanup(list(code))
  bracemap = buildbracemap(code)

  cells, codeptr, cellptr = [0], 0, 0

  while codeptr < len(code):
    command = code[codeptr]

    if command == ">":
      cellptr += 1
      if cellptr == len(cells): cells.append(0)

    if command == "<":
      cellptr = 0 if cellptr <= 0 else cellptr - 1

    if command == "+":
      cells[cellptr] = cells[cellptr] + 1 if cells[cellptr] < 255 else 0

    if command == "-":
      cells[cellptr] = cells[cellptr] - 1 if cells[cellptr] > 0 else 255

    if command == "[" and cells[cellptr] == 0: codeptr = bracemap[codeptr]
    if command == "]" and cells[cellptr] != 0: codeptr = bracemap[codeptr]
    if command == ".": sys.stdout.write(chr(cells[cellptr]))
    if command == ",": cells[cellptr] = ord(getch())
      
    codeptr += 1


def cleanup(code):
  return ''.join(filter(lambda x: x in ['.', ',', '[', ']', '<', '>', '+', '-'], code))


def buildbracemap(code):
  temp_bracestack, bracemap = [], {}

  for position, command in enumerate(code):
    if command == "[": temp_bracestack.append(position)
    if command == "]":
      start = temp_bracestack.pop()
      bracemap[start] = position
      bracemap[position] = start
  return bracemap

import sys
import os
# bfpp = open("bfpp.py", "r").read()

# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
tapes = {
    "AaAa": "-",
    "AAAA": "+",
    "aAaA": ">",
    "AAaa": "<",
    "aaAA": "[", 
    "aaaA": "]",
    "aaaa": ",",
    "aAaa": "."
}
compiled = ""

def get_list(code, ind):
    return [code.replace("\n", "")[i:i+ind] for i in range(0, len(code), ind)]

def AAA(code, mode):
    global compiled
    if mode == "AAA":
        # Translate AAAAAAAAAAA to bf++
        tape = get_list(code, 4)
        for item in tape:
            for i, token in tapes.items():
                if item == i:
                    compiled += token
                # else:
                #     pass

    elif mode == "bf":
        # Translate bf++ to AAAAAAAAAAAAAAAAAAAAA
        tape = get_list(code, 1)
        for item in tape:
            for i, token in tapes.items():
                if item == token:
                    compiled += i
    return compiled
    

if len(sys.argv) > 1:
    if sys.argv[1] == "comp" and len(sys.argv) >= 2:
        with open(sys.argv[2].split(".")[0]+".AAA", "w+") as f:
            code = AAA(open(sys.argv[2], "r").read(), "bf")
            code = get_list(code, 30)
            f.write('\n'.join(code))
    else:
        code = AAA(open(sys.argv[1], "r").read(), "AAA")
        evaluate(code)
