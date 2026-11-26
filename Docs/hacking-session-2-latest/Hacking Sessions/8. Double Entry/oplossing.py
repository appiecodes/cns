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

# Stap 1: Vul de variabelen uit de JSON in:
d = json.load(open("double-entry-dsa1_challenge.json"))
p, q, g, y = d["p"], d["q"], d["g"], d["y"]
m1, r1, s1 = d["signatures"][0]["message"], d["signatures"][0]["r"], d["signatures"][0]["s"]
m2, r2, s2 = d["signatures"][1]["message"], d["signatures"][1]["r"], d["signatures"][1]["s"]
ct = hex2b(d["encrypted_flag"])

assert r1 == r2, "r1 en r2 zijn niet gelijk: k is niet hergebruikt"
H = lambda m: int(hashlib.sha256(m.encode()).hexdigest(), 16) % q

k = (H(m1) - H(m2)) * inv(s1 - s2, q) % q
x = (s1 * k - H(m1)) * inv(r1, q) % q
assert pow(g, x, p) == y, "Controle pow(g, x, p) == y faalde (check hashfunctie!)"
print("Privésleutel x =", x)

# Stap 2: Sleutel afgeleid uit x (zoals Double Entry): XOR met sha256(f"{x}:{i}") blokken
ks = b"".join(hashlib.sha256(f"{x}:{i}".encode()).digest() for i in range(10))
print(xor_bytes(ct, ks).decode())