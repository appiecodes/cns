"""CTFd: Asymmetric Nonsense  (ElGamal, reused nonce).

Run:  python3 elgamal_solve.py challenge.json
Needs cns_toolkit.py in the same folder.

The idea (reused nonce):
  Both ciphertexts share the SAME first number c1  ->  same one-time key K.
  We know one plaintext, so:  K = c2_known * inverse(m_known) mod p
  Then the flag:              m_flag = c2_flag * inverse(K) mod p
"""
import sys, json
from cns_toolkit import inv, b2i, show

data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "challenge.json"))

# 1. READ THE INPUT  (change these keys if the next challenge names them differently)
p = data["p"]
known_text = data["known_plaintext"]            # the message given in the clear
c_known = data["cipher_known"]                   # [c1, c2] for the known message
c_flag = data["cipher_flag"]                     # [c1, c2] for the flag

print("same nonce?", c_known[0] == c_flag[0])    # must be True for this attack

# 2. THE ATTACK
m_known = b2i(known_text.encode())               # text -> number
K = c_known[1] * inv(m_known, p) % p             # recover the one-time key
m_flag = c_flag[1] * inv(K, p) % p               # unmask the flag

# 3. THE FLAG
print("Flag:", show(m_flag))
