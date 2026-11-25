import json
from sympy.ntheory import discrete_log
from Crypto.Util.number import bytes_to_long, long_to_bytes
from math import log
with open("ElGamal_challenge.json") as f:
    challenge = json.load(f)
    known_plaintext = challenge["known_plaintext"]
    p = challenge["p"]
    g = challenge["g"]
    y = challenge["y"]
    cipher_known = challenge["cipher_known"]
    cipher_flag = challenge["cipher_flag"]


C1a = cipher_known[0]
C1b = cipher_flag[0]
C2a = cipher_known[1]
C2b = cipher_flag[1]

r = (C1b * pow(C1a, -1, p)) % p

t = log(r, g)
print(t)
Ma = bytes_to_long(known_plaintext.encode())
print(known_plaintext)

Mb = (C2b  * Ma * pow(C2a, -1, p)* pow(y, -1, p)) % p

print(long_to_bytes(Mb).decode())
