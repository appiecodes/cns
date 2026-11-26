"""CTFd: The group chat (RSA, same message to several people).

Run in Terminal from the folder that holds this file:
    python3 group_chat.py
Needs ciphertexts.txt, public_keys.txt and cns_toolkit.py in the same folder.
"""
import re
from cns_toolkit import crt, iroot, show

# 1. READ THE INPUT -------------------------------------------------------
# Grab every "name = number" line from both files.
def read_numbers(filename):
    text = open(filename).read()
    return re.findall(r"(\w+)\s*=\s*(\d+)", text)

cts = [int(v) for k, v in read_numbers("ciphertexts.txt")]
keys = read_numbers("public_keys.txt")
ns = [int(v) for k, v in keys if k == "n"]
es = [int(v) for k, v in keys if k == "e"]

print("ciphertexts:", len(cts), " moduli:", len(ns), " exponents:", es)

# 2. THE ATTACK -----------------------------------------------------------
e = es[0]                      # everyone uses the same small e (check the print above!)

# Case A: m^e was smaller than n, so the ciphertext is just m^e -> take the e-th root.
root, exact = iroot(cts[0], e)
if exact:
    print("Case A (m^e < n):", show(root))

# Case B: Hastad. Combine e ciphertexts with CRT into m^e mod (n1*n2*...),
# which equals m^e exactly, then take the e-th root.
x, _ = crt(cts[:e], ns[:e])
root, exact = iroot(x, e)
print("Case B (Hastad) exact root?", exact)
print("Flag:", show(root))
