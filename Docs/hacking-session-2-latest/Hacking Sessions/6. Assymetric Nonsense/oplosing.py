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

#p=9225490125574615879730976858978883339687070873947320688584654974419813809012895853303730427204473740303819641837307102411215367044323099559109895480428321
#g=2
#y=4952666711519976220942676756728614898283642420154401733481772104551597055639626227780996026603693891074158283017966063324105993922726181729946347869560583
#m1="This message is public"
#c1=1662786473391137158035370524098469088383722658610494512543995018747569826751458929525257082567025886979608414460845926634129266968165224106812530591889879
#c2=5781794697050394524727333015887004837679769139427197921276822613868543508092919220576155743441119281198273427779950179477877814420321998389891765913745598
#flag1=1662786473391137158035370524098469088383722658610494512543995018747569826751458929525257082567025886979608414460845926634129266968165224106812530591889879
#flag2=1826632435538462363641561028250444205170081577123372077737105705251042960292425294282802410949124336793435578928068281265015662881671634602480595515710611

# Stap 1: Vul de variabelen uit de JSON in (of laad de JSON direct):
d = json.load(open("assymetric-nonsense-challenge.json"))
p = d["p"]
known_pt = d["known_plaintext"]           # bv. "This message is public"
c1_known, c2_known = d["cipher_known"]    # koppel [c1, c2] van bekende tekst
c1_flag,  c2_flag  = d["cipher_flag"]     # koppel [c1, c2] van de flag

assert c1_known == c1_flag                  # controleer of k echt hergebruikt is!
m_known = b2l(known_pt.encode())            # zet bekende tekst eerst om naar een getal (int)!

m_flag = (c2_flag * m_known * inv(c2_known, p)) % p
print(l2b(m_flag).decode())

# Zonder bekende m_known: m1/m2 = c2_known/c2_flag mod p, gok tekst/crib en vergelijk