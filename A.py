# i strongly recommend you *the user* to run this in pypy, if you are using pypy, execute this command:
#pypy -m pip install bfi

import sys
import os
import re
try:
    import bfi
except:
    print("You do not have Brainf*ck interpreter installed, would you like to install it?")
    x = input("(y/n): ")
    if x == "y":
        os.system("python -m pip install bfi")
    else:
        print("Goodbye!")
        exit(1)
    try:
        import bfi
    except:
        print("Still, could not import, please run the program again.")
        exit(1)

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
        tape = get_list(re.sub(r'\(.*?\)', '', code), 4)
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
    

if len(sys.argv) >= 1:
    if sys.argv[1] == "compf" and len(sys.argv) >= 2:
        with open(".AAA", "w+") as f:
            code = AAA(open(sys.argv[2], "r").read(), "bf")
            code = get_list(code, 30)
            f.write('\n'.join(code))
    elif sys.argv[1] == "compA" and len(sys.argv) >= 2:
        code = AAA(open(sys.argv[1], "r").read(), "AAA")
        with open(".AAA", "w+") as f:
            f.write(code)
    else:
        code = AAA(open(sys.argv[1], "r").read(), "AAA")
        bfi.interpret(code)