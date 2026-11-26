"""CNS toolkit – topics 5-7 (RSA, ElGamal, signatures, Diffie-Hellman).
Pure Python 3.8+, no external packages. Import with:  from cns_toolkit import *
"""
from math import gcd, isqrt
import random

# ---------- number theory ----------
def egcd(a, b):
    """returns (g, x, y) with a*x + b*y = g = gcd(a, b)"""
    if b == 0:
        return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a // b) * y

def inv(a, m):
    """modular inverse a^-1 mod m"""
    return pow(a, -1, m)

def crt(remainders, moduli):
    """solve x = r_i (mod m_i) for pairwise coprime m_i; returns (x, M)"""
    M = 1
    for m in moduli:
        M *= m
    x = 0
    for r, m in zip(remainders, moduli):
        Mi = M // m
        x += r * Mi * inv(Mi, m)
    return x % M, M

def iroot(x, k):
    """integer k-th root: returns (root, exact?)"""
    lo, hi = 0, 1 << ((x.bit_length() + k - 1) // k + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** k <= x:
            lo = mid
        else:
            hi = mid - 1
    return lo, lo ** k == x

def is_prime(n, rounds=40):
    """Miller-Rabin"""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for _ in range(rounds):
        a = random.randrange(2, n - 1)
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def phi(n):
    """Euler totient via factorization"""
    result = n
    for p in set(factor(n)):
        result -= result // p
    return result

def pollard_rho(n):
    if n % 2 == 0:
        return 2
    while True:
        x = y = random.randrange(2, n)
        c = random.randrange(1, n)
        d = 1
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = gcd(abs(x - y), n)
        if d != n:
            return d

def fermat_factor(n, max_steps=10**6):
    """fast when p and q are close together"""
    a = isqrt(n)
    if a * a < n:
        a += 1
    for _ in range(max_steps):
        b2 = a * a - n
        b = isqrt(b2)
        if b * b == b2:
            return a - b, a + b
        a += 1
    return None

def factor(n):
    """list of prime factors (with repetition)"""
    if n == 1:
        return []
    if is_prime(n):
        return [n]
    for p in range(2, 10000):
        if n % p == 0:
            return [p] + factor(n // p)
    f = fermat_factor(n, 10**5)
    d = f[0] if f and f[0] > 1 else pollard_rho(n)
    return sorted(factor(d) + factor(n // d))

def is_primitive_root(a, p):
    """p prime"""
    return all(pow(a, (p - 1) // f, p) != 1 for f in set(factor(p - 1)))

def primitive_roots(p):
    return [a for a in range(2, p) if is_primitive_root(a, p)]

def dlog(base, target, p):
    """discrete log: x with base^x = target (mod p); baby-step giant-step"""
    m = isqrt(p - 1) + 1
    table = {}
    e = 1
    for j in range(m):
        table.setdefault(e, j)
        e = e * base % p
    factor_ = pow(base, -m, p)
    g = target % p
    for i in range(m):
        if g in table:
            return i * m + table[g]
        g = g * factor_ % p
    return None

# ---------- bytes <-> int ----------
def i2b(x):
    return x.to_bytes((x.bit_length() + 7) // 8, "big")

def b2i(b):
    return int.from_bytes(b, "big")

def show(m):
    """print a decrypted int as text if possible"""
    try:
        return i2b(m).decode()
    except Exception:
        return m

# ---------- RSA ----------
def rsa_keys(p, q, e=65537):
    n, ph = p * q, (p - 1) * (q - 1)
    return n, e, inv(e, ph)          # n, e, d

def rsa_enc(m, e, n):
    return pow(m, e, n)

def rsa_dec(c, d, n):
    return pow(c, d, n)

def rsa_dec_crt(c, d, p, q):
    vp, vq = pow(c, d % (p - 1), p), pow(c, d % (q - 1), q)
    xp, xq = q * inv(q, p), p * inv(p, q)
    return (vp * xp + vq * xq) % (p * q)

def rsa_crack(n, e, c):
    """factor n -> d -> m"""
    p, q = factor(n)[0], n // factor(n)[0]
    d = inv(e, (p - 1) * (q - 1))
    return pow(c, d, n)

def rsa_from_phi(n, e, ph, c):
    return pow(c, inv(e, ph), n)

def rsa_small_m(c, e):
    """m^e < n, so c was never reduced"""
    return iroot(c, e)

def hastad(cs, ns, e=3):
    """same m sent to e receivers with exponent e, no padding"""
    x, _ = crt(cs, ns)
    return iroot(x, e)

def common_modulus(c1, c2, e1, e2, n):
    """same m, same n, two coprime exponents"""
    g, a, b = egcd(e1, e2)
    assert g == 1
    return pow(c1, a, n) * pow(c2, b, n) % n

def shared_prime(n1, n2):
    """two moduli sharing a prime"""
    p = gcd(n1, n2)
    return (p, n1 // p, n2 // p) if 1 < p < n1 else None

def cca_blind(c, e, n, r=2):
    """step 1: send X to the oracle"""
    return c * pow(r, e, n) % n

def cca_unblind(y, n, r=2):
    """step 2: oracle returned y = r*m mod n"""
    return y * inv(r, n) % n

def wiener(e, n):
    """small d attack; returns d or None"""
    def cf(a, b):
        while b:
            q = a // b
            yield q
            a, b = b, a - q * b
    h0, h1, k0, k1 = 0, 1, 1, 0
    for a in cf(e, n):
        h0, h1 = h1, a * h1 + h0
        k0, k1 = k1, a * k1 + k0
        k, d = h1, k1
        if k == 0 or (e * d - 1) % k:
            continue
        ph = (e * d - 1) // k
        s = n - ph + 1
        disc = s * s - 4 * n
        if disc >= 0 and isqrt(disc) ** 2 == disc:
            return d
    return None

def rsa_sign(h, d, n):
    return pow(h, d, n)

def rsa_verify(h, s, e, n):
    return pow(s, e, n) == h % n

# ---------- ElGamal ----------
def elgamal_keys(q, alpha, xa):
    return pow(alpha, xa, q)          # ya

def elgamal_enc(m, q, alpha, ya, k):
    K = pow(ya, k, q)
    return pow(alpha, k, q), K * m % q   # (c1, c2)

def elgamal_dec(c1, c2, q, xa):
    K = pow(c1, xa, q)
    return c2 * inv(K, q) % q

def elgamal_k_reuse(c2_known, m_known, c2_target, q):
    """same k (same c1) used twice, one plaintext known"""
    K = c2_known * inv(m_known, q) % q
    return c2_target * inv(K, q) % q

def elgamal_crack(c1, c2, q, alpha, ya):
    """small q: brute-force private key"""
    xa = dlog(alpha, ya, q)
    return elgamal_dec(c1, c2, q, xa)

# ---------- Diffie-Hellman ----------
def dh_public(alpha, x, q):
    return pow(alpha, x, q)

def dh_shared(other_public, my_private, q):
    return pow(other_public, my_private, q)

def dh_crack(q, alpha, ya, yb):
    """small q: recover shared key from public values"""
    xb = dlog(alpha, yb, q)
    return pow(ya, xb, q)

# ---------- DSA ----------
def dsa_sign(h, p, q, g, x, k):
    r = pow(g, k, p) % q
    s = inv(k, q) * (h + x * r) % q
    return r, s

def dsa_verify(h, r, s, p, q, g, y):
    if not (0 < r < q and 0 < s < q):
        return False
    w = inv(s, q)
    u1, u2 = h * w % q, r * w % q
    return (pow(g, u1, p) * pow(y, u2, p) % p) % q == r

def dsa_k_reuse(h1, s1, h2, s2, r, q):
    """two signatures with the same r (same k) -> (k, x)"""
    k = (h1 - h2) * inv(s1 - s2, q) % q
    x = (s1 * k - h1) * inv(r, q) % q
    return k, x

# ---------- input / output helpers (hex, base64, JSON, servers) ----------
import json, base64, urllib.request

def load_json(path):
    """read a challenge .json file into a dict"""
    with open(path) as f:
        return json.load(f)

def to_int(v):
    """accept int, decimal string or hex string ('0x..' or bare hex)"""
    if isinstance(v, int):
        return v
    v = str(v).strip()
    if v.lower().startswith("0x"):
        return int(v, 16)
    try:
        return int(v)
    except ValueError:
        return int(v, 16)

def unhex(s):
    return bytes.fromhex(s.strip())

def b64d(s):
    """base64 or base64url, missing '=' padding is fine"""
    s = s.strip().replace("-", "+").replace("_", "/")
    return base64.b64decode(s + "=" * (-len(s) % 4))

def b64e(b, url=False):
    out = base64.urlsafe_b64encode(b) if url else base64.b64encode(b)
    return out.decode().rstrip("=") if url else out.decode()

def xor(a, b):
    """xor two byte strings (repeats b if shorter)"""
    return bytes(x ^ b[i % len(b)] for i, x in enumerate(a))

def http_get(url, headers=None):
    """GET -> (status, text). Use json.loads(text) if it's JSON."""
    req = urllib.request.Request(url, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()

def http_post_json(url, data, headers=None):
    """POST a dict as JSON -> (status, text)"""
    h = {"Content-Type": "application/json"}
    h.update(headers or {})
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers=h, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()
