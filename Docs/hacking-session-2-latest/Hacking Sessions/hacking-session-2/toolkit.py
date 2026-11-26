import hashlib
import json
from math import gcd, isqrt

# ==========================================
# 1. CONVERSIES & BASIS WISKUNDE
# ==========================================

def l2b(m: int) -> bytes:
    """Integer -> Bytes (vervangt Crypto.Util.number.long_to_bytes)"""
    return m.to_bytes((m.bit_length() + 7) // 8, "big")

def b2l(b: bytes) -> int:
    """Bytes -> Integer (vervangt Crypto.Util.number.bytes_to_long)"""
    return int.from_bytes(b, "big")

def hex2b(h: str) -> bytes:
    """Hex string (ook met '0x' of oneven lengte) -> Bytes"""
    h = h.removeprefix("0x").strip()
    if len(h) % 2:
        h = "0" + h
    return bytes.fromhex(h)

def xor_bytes(a: bytes, b: bytes) -> bytes:
    """XOR twee byte-strings van gelijke (of afgeknipte) lengte"""
    return bytes(x ^ y for x, y in zip(a, b))

def iroot(x: int, k: int) -> tuple[int, bool]:
    """Exacte integer k-de machtswortel: geeft (wortel, is_exact)"""
    if x < 2:
        return x, True
    lo, hi = 1, 1 << (x.bit_length() // k + 2)
    while lo < hi:
        mid = (lo + hi) // 2
        if mid**k < x:
            lo = mid + 1
        else:
            hi = mid
    return lo, (lo**k == x)

def egcd(a: int, b: int) -> tuple[int, int, int]:
    """Uitgebreid Euclidisch algoritme: geeft (g, x, y) met a*x + b*y = g"""
    if a == 0:
        return b, 0, 1
    g, y, x = egcd(b % a, a)
    return g, x - (b // a) * y, y

def crt(remainders: list[int], moduli: list[int]) -> int:
    """Chinese Reststelling: lost x ≡ r_i (mod m_i) op"""
    N = 1
    for m in moduli:
        N *= m
    total = 0
    for r, m in zip(remainders, moduli):
        Mi = N // m
        total += r * Mi * pow(Mi, -1, m)
    return total % N

# ==========================================
# 2. RSA AANVALLEN
# ==========================================

def rsa_small_e(c: int, e: int) -> bytes:
    m, exact = iroot(c, e)
    assert exact, "m^e was groter dan n (geen exacte wortel)"
    return l2b(m)

def rsa_hastad(ciphertexts: list[int], moduli: list[int], e: int) -> bytes:
    x = crt(ciphertexts, moduli)
    m, exact = iroot(x, e)
    assert exact, "CRT-resultaat is geen exacte e-de macht"
    return l2b(m)

def rsa_common_modulus(c1: int, c2: int, e1: int, e2: int, n: int) -> bytes:
    g, a, b = egcd(e1, e2)
    assert g == 1, "e1 en e2 zijn niet copriem"
    part1 = pow(c1, a, n) if a >= 0 else pow(pow(c1, -1, n), -a, n)
    part2 = pow(c2, b, n) if b >= 0 else pow(pow(c2, -1, n), -b, n)
    m = (part1 * part2) % n
    return l2b(m)

def rsa_wiener(e: int, n: int, c: int) -> tuple[int, bytes]:
    # Kettingbreuk van e/n
    cf = []
    a, b = e, n
    while b:
        cf.append(a // b)
        a, b = b, a % b
    # Convergenten testen
    h0, h1, k0, k1 = 0, 1, 1, 0
    for q in cf:
        h0, h1 = h1, q * h1 + h0
        k0, k1 = k1, q * k1 + k0
        k, d = h1, k1
        if k == 0 or (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        s = n - phi + 1  # p + q
        disc = s * s - 4 * n
        if disc >= 0 and isqrt(disc) ** 2 == disc:
            m = pow(c, d, n)
            return d, l2b(m)
    raise ValueError("Geen geldige Wiener-sleutel gevonden")

def pollard_rho(n: int) -> int:
    if n % 2 == 0:
        return 2
    for c in range(1, 20):
        x, y, d = 2, 2, 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d
    raise ValueError("Pollard rho vond geen factor")

def fermat_factor(n: int, max_steps: int = 100000) -> tuple[int, int]:
    """Voor als p en q dicht bij elkaar liggen"""
    a = isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(max_steps):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1
    raise ValueError("p en q liggen niet dicht genoeg bij elkaar")

# ==========================================
# 3. ELGAMAL & DSA AANVALLEN
# ==========================================

def elgamal_known_plaintext_attack(p: int, g: int, y: int, known_pt: bytes,
                                   c_known: list[int], c_flag: list[int]) -> bytes:
    c1_k, c2_k = c_known
    c1_f, c2_f = c_flag
    m_k = b2l(known_pt)
    s_k = (c2_k * pow(m_k, -1, p)) % p  # s_k = y^k1 mod p

    # Geval A: Zelfde nonce (k2 = k1)
    if c1_k == c1_f:
        m_f = (c2_f * pow(s_k, -1, p)) % p
        return l2b(m_f)

    # Geval B: Lineaire verschuiving k2 = k1 + delta (bv. teller k+1)
    for delta in range(-5000, 5001):
        if (c1_k * pow(g, delta, p)) % p == c1_f:
            s_f = (s_k * pow(y, delta, p)) % p
            m_f = (c2_f * pow(s_f, -1, p)) % p
            return l2b(m_f)

    # Geval C: Veelvuldig k2 = a * k1 (bv. k2 = 2 * k1)
    for a in range(2, 5001):
        if pow(c1_k, a, p) == c1_f:
            s_f = pow(s_k, a, p)
            m_f = (c2_f * pow(s_f, -1, p)) % p
            return l2b(m_f)

    raise ValueError("Geen simpel verband gevonden tussen de nonces")

def dsa_nonce_reuse(p: int, q: int, g: int, y: int,
                    m1: bytes, r1: int, s1: int,
                    m2: bytes, r2: int, s2: int) -> int:
    assert r1 == r2, "r1 en r2 zijn niet gelijk: k is niet hergebruikt"
    h1 = b2l(hashlib.sha256(m1).digest()) % q
    h2 = b2l(hashlib.sha256(m2).digest()) % q

    k = ((h1 - h2) * pow(s1 - s2, -1, q)) % q
    x = ((s1 * k - h1) * pow(r1, -1, q)) % q
    assert pow(g, x, p) == y, "Controle g^x mod p == y faalde!"
    return x

# ==========================================
# 4. TEST OP JOUW JSON BESTANDEN
# ==========================================
if __name__ == "__main__":
    # Test ElGamal 1
    with open("assymetric-nonsense-challenge.json") as f:
        d = json.load(f)
    print("ElGamal 1:", elgamal_known_plaintext_attack(
        d["p"], d["g"], d["y"], d["known_plaintext"].encode(), d["cipher_known"], d["cipher_flag"]
    ))

    # Test ElGamal 2
    with open("fresh-every-time-ElGamal_challenge.json") as f:
        d = json.load(f)
    print("ElGamal 2:", elgamal_known_plaintext_attack(
        d["p"], d["g"], d["y"], d["known_plaintext"].encode(), d["cipher_known"], d["cipher_flag"]
    ))

    # Test DSA
    with open("double-entry-dsa1_challenge.json") as f:
        d = json.load(f)
    sig1, sig2 = d["signatures"]
    x = dsa_nonce_reuse(
        d["p"], d["q"], d["g"], d["y"],
        sig1["message"].encode(), sig1["r"], sig1["s"],
        sig2["message"].encode(), sig2["r"], sig2["s"]
    )
    ct = hex2b(d["encrypted_flag"])
    keystream = b""
    i = 0
    while len(keystream) < len(ct):
        keystream += hashlib.sha256(f"{x}:{i}".encode()).digest()
        i += 1
    print("DSA:", xor_bytes(ct, keystream))