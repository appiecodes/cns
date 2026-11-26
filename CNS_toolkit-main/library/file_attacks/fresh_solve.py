"""CTFd: Fresh Every Time  (ElGamal, nonce is a counter: k, k+1, k+2 ...).

Run:  python3 fresh_solve.py challenge.json
Needs cns_toolkit.py in the same folder.

Same as elgamal_solve.py, with ONE change:
  nonce k+delta  ->  c1 gets multiplied by g^delta
                 ->  the one-time key K gets multiplied by y^delta
So: find delta by comparing the two c1's, then adjust K.
"""
import sys, json
from cns_toolkit import inv, b2i, show

data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "challenge.json"))

# 1. READ THE INPUT
p, g, y = data["p"], data["g"], data["y"]
known_text = data["known_plaintext"]
c_known = data["cipher_known"]       # [c1, c2]
c_flag = data["cipher_flag"]         # [c1, c2]

# 2. THE ATTACK
m_known = b2i(known_text.encode())
K = c_known[1] * inv(m_known, p) % p                 # key of the known message

# find how far the flag's nonce is from the known nonce (try +1, +2, ... and -1, -2, ...)
delta = None
for d in range(1, 100000):
    if c_known[0] * pow(g, d, p) % p == c_flag[0]:
        delta = d
        break
    if c_known[0] * pow(g, -d, p) % p == c_flag[0]:
        delta = -d
        break
print("nonce difference:", delta)                    # here: 1

K_flag = K * pow(y, delta, p) % p                    # THE one extra line
m_flag = c_flag[1] * inv(K_flag, p) % p

# 3. THE FLAG
print("Flag:", show(m_flag))
