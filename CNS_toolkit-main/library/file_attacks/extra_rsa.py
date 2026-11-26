"""Extra RSA attacks not in the four weeklies. Import or copy the function you need.
   from extra_rsa import *
"""
from cns_toolkit import inv, b2i, show, i2b, is_prime
from math import gcd, isqrt

# ---- batch GCD: many moduli, some share a prime ----
def batch_shared_primes(ns):
    """return {index: prime} for every modulus that shares a factor with another"""
    found = {}
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            g = gcd(ns[i], ns[j])
            if 1 < g < ns[i]:
                found[i] = g
                found[j] = g
    return found

# ---- modulus is a prime power n = p^k ----
def _iroot(x, k):
    if x < 2: return x
    lo, hi = 1, 1 << ((x.bit_length() + k - 1) // k + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** k <= x: lo = mid
        else: hi = mid - 1
    return lo

def prime_power(n):
    for k in range(2, 17):
        r = _iroot(n, k)
        for cand in (r - 1, r, r + 1):
            if cand > 1 and cand ** k == n and is_prime(cand):
                return cand, k   # phi = p^(k-1)*(p-1)
    return None

# ---- e shares a factor with phi: e-th root has gcd(e,phi) solutions ----
def roots_when_e_not_coprime(c, e, p, q):
    """returns candidate messages when gcd(e,(p-1)(q-1)) > 1 (small gcd only)"""
    phi = (p - 1) * (q - 1)
    g = gcd(e, phi)
    # reduce: find d for e/g
    d = inv(e // g, phi)
    base = pow(c, d, p * q)        # this is m^g
    # take g-th roots of base mod n by CRT of roots mod p and mod q
    import itertools
    def roots_mod(a, g, pr):
        return [x for x in range(pr) if pow(x, g, pr) == a % pr] if pr < 100000 else []
    out = []
    rp, rq = roots_mod(base, g, p), roots_mod(base, g, q)
    for xp, xq in itertools.product(rp, rq):
        x = (xp * q * inv(q, p) + xq * p * inv(p, q)) % (p * q)
        out.append(x)
    return out

# ---- Franklin-Reiter: two related messages, m2 = a*m1 + b, same n, same small e ----
def _poly_mulmod(A, B, n):
    R = [0] * (len(A) + len(B) - 1)
    for i, a in enumerate(A):
        for j, b in enumerate(B):
            R[i + j] = (R[i + j] + a * b) % n
    return R

def _poly_mod(A, B, n):
    A = A[:]
    while len(A) >= len(B) and any(A):
        if A[-1] == 0:
            A.pop(); continue
        lead = A[-1] * inv(B[-1], n) % n
        shift = len(A) - len(B)
        for i in range(len(B)):
            A[i + shift] = (A[i + shift] - lead * B[i]) % n
        while A and A[-1] == 0:
            A.pop()
    return A

def _poly_gcd(A, B, n):
    while any(B):
        A, B = B, _poly_mod(A, B, n)
    # make monic
    if A and A[-1] != 1:
        ai = inv(A[-1], n)
        A = [x * ai % n for x in A]
    return A

def franklin_reiter(n, e, c1, c2, a=1, b=1):
    """m2 = a*m1 + b. returns m1 or None. Works for small e."""
    # g1(x) = x^e - c1 ;  g2(x) = (a x + b)^e - c2
    g1 = [0] * (e + 1); g1[e] = 1; g1[0] = (-c1) % n
    poly = [b % n, a % n]          # a x + b
    acc = [1]
    for _ in range(e):
        acc = _poly_mulmod(acc, poly, n)
    acc[0] = (acc[0] - c2) % n
    g = _poly_gcd(g1, acc, n)
    if len(g) == 2:                # (x - m): g = [ -m, 1 ]
        return (-g[0]) % n
    return None

if __name__ == "__main__":
    import random
    def prime(bb):
        while True:
            p = random.getrandbits(bb) | 1 | (1 << (bb - 1))
            if is_prime(p): return p
    # test batch gcd
    p = prime(256); q = prime(256); r = prime(256)
    ns = [p*q, p*r, prime(256)*prime(256)]
    print("batch gcd:", {k: (v == p) for k, v in batch_shared_primes(ns).items()})
    # test prime power
    pp = prime(256); print("prime power:", prime_power(pp**3) == (pp, 3))
    # test franklin-reiter
    p = prime(512); q = prime(512); n = p*q; e = 3
    m1 = b2i(b"cns{franklin_reiter_related_msg}")
    a, b = 1, 1234567
    m2 = (a*m1 + b) % n
    c1, c2 = pow(m1, e, n), pow(m2, e, n)
    got = franklin_reiter(n, e, c1, c2, a, b)
    print("franklin-reiter:", show(got) if got else "FAILED")
