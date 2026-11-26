import json, re, base64, hashlib
from math import gcd, isqrt, prod

l2b = lambda m: m.to_bytes((m.bit_length()+7)//8, "big") if m > 0 else b"\x00"   # int -> bytes (long_to_bytes)
b2l = lambda b: int.from_bytes(b, "big")                                        # bytes -> int (bytes_to_long)
inv = lambda a, m: pow(a, -1, m)                                                # modulaire inverse (Python 3.8+)

def hex2b(h: str) -> bytes:
    """Hex string (met of zonder '0x', ook bij oneven lengte) -> bytes"""
    h = h.removeprefix("0x").strip()
    if len(h) % 2: h = "0" + h
    return bytes.fromhex(h)

def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR twee byte-strings"""
    return bytes(x ^ y for x, y in zip(a, b))

def iroot(x, k):                  # integer k-de wortel, floor; check: iroot(x,k)**k == x
    if x < 2: return x
    lo, hi = 0, 2**(x.bit_length()//k + 1)
    while lo < hi:
        mid = (lo+hi)//2
        if mid**k < x: lo = mid+1
        else: hi = mid
    return lo if lo**k == x else lo-1

def egcd(a, b):                   # (g, x, y) met a*x + b*y = g
    if b == 0: return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a//b)*y

def crt(cs, ns):                  # x = ci mod ni, ni onderling copriem
    N = 1
    for n in ns: N *= n
    return sum(c*(N//n)*inv(N//n, n) for c, n in zip(cs, ns)) % N

#################################################################

# Stap 1: Vul de variabelen uit de JSON in:
d = json.load(open("fresh-every-time-ElGamal_challenge.json"))
p, g, y = d["p"], d["g"], d["y"]
known_pt = d["known_plaintext"]           # bv. "Nonces are never reused here"
c1_known, c2_known = d["cipher_known"]    # koppel [c1, c2] van bekende tekst
c1_flag,  c2_flag  = d["cipher_flag"]     # koppel [c1, c2] van de flag

m_known = b2l(known_pt.encode())            # zet bekende tekst eerst om naar een getal (int)!
s_known = (c2_known * inv(m_known, p)) % p  # geheime masker y^k1 van bekende tekst

# Geval A: Teller / verschuiving k2 = k1 + t (zoekt -5000 <= t <= 5000)
r = (c1_flag * inv(c1_known, p)) % p
for t in range(-5000, 5001):
    if pow(g, t, p) == r:
        print("Gevonden: k2 = k1 +", t)
        s_flag = (s_known * pow(y, t, p)) % p
        m_flag = (c2_flag * inv(s_flag, p)) % p
        print(l2b(m_flag).decode())
        break

# Geval B: Veelvuldig k2 = a * k1 (bv. k2 = 2 * k1)
for a in range(2, 5001):
    if pow(c1_known, a, p) == c1_flag:
        print("Gevonden: k2 = a * k1 met a =", a)
        s_flag = pow(s_known, a, p)
        m_flag = (c2_flag * inv(s_flag, p)) % p
        print(l2b(m_flag).decode())
        break