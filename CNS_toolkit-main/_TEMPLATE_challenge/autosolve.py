#!/usr/bin/env python3
"""autosolve.py - last-resort "try everything" solver for file-based
RSA / ElGamal / DSA challenges.  Needs cns_toolkit.py in the same folder.

Usage:   python3 autosolve.py challenge.json [more files ...]
It reads every number it can find (JSON, "name = value" text, hex or decimal),
guesses what each one is from its name, tries every attack it knows and
prints anything that decodes to readable text (flags look like cns{...}).
Live-server challenges are NOT covered.
"""
import sys, json, re, time, itertools, hashlib
from math import gcd
from cns_toolkit import (inv, egcd, crt, iroot, factor, fermat_factor, pollard_rho,
                         is_prime, wiener, dlog, i2b)

# ---------------------------------------------------------------- parsing
NUM = re.compile(r"^(0x[0-9a-fA-F]+|[0-9]+|[0-9a-fA-F]{16,})$")

def to_num(v):
    if isinstance(v, bool):
        return None
    if isinstance(v, int):
        return v
    if isinstance(v, str) and NUM.match(v.strip()):
        s = v.strip()
        if s.lower().startswith("0x"):
            return int(s, 16)
        if s.isdigit():
            return int(s)
        return int(s, 16)
    return None

def flatten(obj, path=()):
    """yield (path_tuple, value) for every leaf"""
    if isinstance(obj, dict):
        for k, v in obj.items():
            yield from flatten(v, path + (str(k),))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten(v, path + (str(i),))
    else:
        yield path, obj

def read_file(fn):
    raw = open(fn, "rb").read()
    try:
        text = raw.decode()
    except UnicodeDecodeError:
        return []
    leaves = []
    try:
        leaves = list(flatten(json.loads(text)))
    except Exception:
        block = 0
        for line in text.splitlines():
            if re.match(r"^\s*-{2,}.*-{2,}\s*$", line) or not line.strip():
                block += 1
                continue
            m = re.match(r"^\s*([A-Za-z_][\w\s\-]*?)\s*[=:]\s*(\S+)\s*$", line)
            if m:
                leaves.append(((str(block), m.group(1).strip()), m.group(2).strip().strip('",')))
    out = []
    lists = {}
    for path, v in leaves:
        if len(path) >= 2 and path[-1].isdigit() and to_num(v) is not None:
            lists.setdefault(path[:-1], []).append(to_num(v))
        if path and re.sub(r"[^a-z]", "", path[-1].lower()) in ("blocksize", "blocklen", "blockbytes") and to_num(v):
            BLOCK_SIZE[0] = to_num(v)
    for p, vals in lists.items():
        BLOCKS.append((p[-1], vals))
    for path, v in leaves:
        n = to_num(v)
        if n is not None:
            out.append((fn, path, n))
        elif isinstance(v, str):
            out.append((fn, path, v))      # keep strings (known plaintexts, messages)
    return out

def name_of(path):
    if not path:
        return ""
    last = path[-1]
    if last.isdigit() and len(path) >= 2:      # element of a list: use the list's name
        last = path[-2]
    return re.sub(r"[^a-z0-9]", "", last.lower())

BLOCKS = []   # (name, [ints]) lists of ciphertext blocks, in order
BLOCK_SIZE = [None]

def decrypt_blocks(label, d, n):
    """message split over several RSA blocks: decrypt each and glue them together"""
    for nm, blocks in BLOCKS:
        if len(blocks) < 2 or any(c >= n for c in blocks):
            continue
        bs = BLOCK_SIZE[0]
        parts = [pow(c, d, n) for c in blocks]
        if bs:
            data = b"".join(m.to_bytes(bs, "big") for m in parts)
        else:
            data = b"".join(i2b(m) for m in parts)
        txt = data.rstrip(b"\x00")
        if b"cns{" in txt or sum(32 <= c < 127 for c in txt) / max(len(txt), 1) > 0.9:
            out = txt.decode(errors="replace")
            if (label, out) not in hits:
                hits.append((label + " (blocks glued)", out))
                print(f"\n*** [{label}, {len(blocks)} blocks glued] -> {out}\n")

def group_of(path):
    return path[:-1]

# ---------------------------------------------------------------- reporting
hits = []
def report(attack, m):
    if m is None or m <= 0:
        return False
    try:
        b = i2b(m)
    except Exception:
        return False
    printable = sum(32 <= c < 127 for c in b) / max(len(b), 1)
    if b"cns{" in b or printable > 0.9:
        txt = b.decode(errors="replace")
        if (attack, txt) not in hits:
            hits.append((attack, txt))
            print(f"\n*** [{attack}] -> {txt}\n")
        return b"cns{" in b
    return False

def info(msg):
    print("   ", msg)

def timed(seconds):
    end = time.time() + seconds
    return lambda: time.time() > end

# ---------------------------------------------------------------- collect
def collect(items):
    by = {}
    for fn, path, v in items:
        by.setdefault(name_of(path), []).append((group_of(path), v))
    def nums(*names):
        out = []
        for nm in names:
            out += [v for g, v in by.get(nm, []) if isinstance(v, int)]
        return out
    return by, nums

# ---------------------------------------------------------------- RSA
def rsa_attacks(items):
    by, nums = collect(items)
    Ns = list(dict.fromkeys(nums("n", "modulus", "nn", "n1", "n2", "n3", "n4", "n5")))
    Es = list(dict.fromkeys(nums("e", "exponent", "publicexponent", "e1", "e2", "e3")))
    Cs = list(dict.fromkeys(nums("c", "ct", "ciphertext", "cipher", "enc", "encrypted", "flag",
                                 "c1", "c2", "c3", "c4", "c5", "ciphertext1", "ciphertext2")))
    Ds = nums("d", "privateexponent")
    Ps = nums("p", "prime1"); Qs = nums("q", "prime2"); PHIs = nums("phi", "phin", "totient")
    if not Ns or not Cs:
        return
    if not Es:
        Es = [65537, 3]
    print(f"[RSA] {len(Ns)} n, {len(Es)} e, {len(Cs)} c  (e values: {[e if e < 10**6 else 'big' for e in Es]})")

    # pair n/e/c that sit in the same JSON object or text block
    triples = []
    groups = {}
    for nm, lst in by.items():
        for g, v in lst:
            if isinstance(v, int):
                groups.setdefault(g, {})[nm] = v
    for g, d in groups.items():
        n = d.get("n") or d.get("modulus"); e = d.get("e") or d.get("exponent")
        c = next((d[k] for k in ("c", "ct", "ciphertext", "cipher", "enc") if k in d), None)
        if n:
            triples.append((n, e, c))

    # 1. given private info
    for n in Ns:
        for c in Cs:
            for d in Ds:
                report("given d", pow(c, d, n))
            for e in Es:
                for ph in PHIs:
                    try: report("given phi", pow(c, inv(e, ph), n))
                    except Exception: pass
                for p in Ps + Qs:
                    if p > 1 and n % p == 0:
                        q = n // p
                        try: report("given p/q", pow(c, inv(e, (p - 1) * (q - 1)), n))
                        except Exception: pass

    # 2. small message: c = m^e without wraparound
    for c in Cs:
        for e in Es:
            if e < 100:
                r, exact = iroot(c, e)
                if exact:
                    report(f"plain {e}-th root", r)

    # 3. Hastad: same small e, several n
    for e in Es:
        if e < 20 and len(Ns) >= 2:
            k = min(len(Ns), len(Cs))
            for nsel in itertools.islice(itertools.permutations(range(k)), 50):
                try:
                    x, _ = crt([Cs[i] for i in range(k)], [Ns[j] for j in nsel])
                    r, exact = iroot(x, e)
                    if exact and report(f"Hastad e={e}", r):
                        break
                except Exception:
                    pass

    # 4. common modulus: one n, two e, two c
    for n in Ns:
        for (e1, e2) in itertools.combinations(Es, 2):
            for (c1, c2) in itertools.permutations(Cs, 2):
                g, a, b = egcd(e1, e2)
                if g == 1:
                    try: report("common modulus", pow(c1, a, n) * pow(c2, b, n) % n)
                    except Exception: pass

    # 5. shared prime between moduli
    for n1, n2 in itertools.combinations(Ns, 2):
        p = gcd(n1, n2)
        if 1 < p < n1:
            info(f"shared prime found between two n's")
            for n in (n1, n2):
                q = n // p
                for e in Es:
                    for c in Cs:
                        try: report("shared prime", pow(c, inv(e, (p - 1) * (q - 1)), n))
                        except Exception: pass

    # 6. Wiener (huge e)
    for n in Ns:
        for e in Es:
            if e > 2 ** 32:
                d = wiener(e, n)
                if d:
                    info(f"Wiener found d = {d}")
                    for c in Cs:
                        report("Wiener small d", pow(c, d, n))
                    decrypt_blocks("Wiener small d", d, n)

    # 7. factoring (Fermat for close primes, then trial/rho with a time limit)
    for n in Ns:
        f = fermat_factor(n, 2 * 10 ** 5)
        p = f[0] if f and f[0] > 1 else None
        if not p:
            for t in range(2, 200000):
                if n % t == 0:
                    p = t; break
        if not p and n.bit_length() <= 160:
            p = pollard_rho(n)
        if not p:
            p = pollard_rho_timed(n, 20)
        if p:
            q = n // p
            info(f"factored n ({n.bit_length()} bits)")
            for e in Es:
                try:
                    dd = inv(e, (p - 1) * (q - 1))
                except Exception:
                    continue
                for c in Cs:
                    if c < n:
                        report("factored n", pow(c, dd, n))
                decrypt_blocks("factored n", dd, n)
        else:
            info(f"could not factor n ({n.bit_length()} bits) quickly")

def pollard_rho_timed(n, seconds):
    import random
    stop = timed(seconds)
    while not stop():
        x = y = random.randrange(2, n); c = random.randrange(1, n); d = 1; i = 0
        while d == 1 and not stop():
            x = (x * x + c) % n; y = (y * y + c) % n; y = (y * y + c) % n
            i += 1
            if i % 100 == 0:
                d = gcd(abs(x - y), n)
        if 1 < d < n:
            return d
    return None

# ---------------------------------------------------------------- ElGamal / DH
def elgamal_attacks(items):
    by, nums = collect(items)
    P = nums("p", "q", "prime", "modulus")
    G = nums("g", "alpha", "generator", "a")
    Y = nums("y", "ya", "h", "publickey", "pub", "pk", "yb", "y_a")
    if not P or not G:
        return
    # ciphertext pairs (c1, c2) grouped by object
    groups = {}
    for nm, lst in by.items():
        for g, v in lst:
            groups.setdefault(g, {})[nm] = v
    pairs = []
    for g, d in groups.items():
        a = next((d[k] for k in ("c1", "a", "gamma", "alpha_k") if isinstance(d.get(k), int)), None)
        b = next((d[k] for k in ("c2", "b", "delta") if isinstance(d.get(k), int)), None)
        if a is not None and b is not None and g != ():
            m = next((d[k] for k in ("m", "plaintext", "message", "msg", "known", "pt") if k in d), None)
            pairs.append((g, a, b, m))
    if not pairs:
        return
    print(f"[ElGamal] p ({P[0].bit_length()} bits), {len(pairs)} ciphertext pairs, "
          f"{sum(1 for x in pairs if x[3] is not None)} with known plaintext")
    for p in P:
        for g in G:
            if g >= p:
                continue
            known = []
            for grp, c1, c2, m in pairs:
                if m is not None:
                    mi = m if isinstance(m, int) else int.from_bytes(str(m).encode(), "big")
                    known.append((c1, c2, mi % p))
            targets = [(c1, c2) for grp, c1, c2, m in pairs if m is None]
            if not targets:
                targets = [(c1, c2) for grp, c1, c2, m in pairs]
            for (kc1, kc2, km) in known:
                try:
                    K = kc2 * inv(km, p) % p
                except Exception:
                    continue
                for (c1, c2) in targets:
                    # nonce reuse
                    if c1 == kc1:
                        report("ElGamal nonce reuse", c2 * inv(K, p) % p)
                    # related nonces k2 = k1 + delta  (needs y)
                    for y in Y:
                        gd, yd = 1, 1
                        ginv, yinv = inv(g, p), inv(y, p)
                        for delta in range(1, 5001):
                            gd = gd * g % p; yd = yd * y % p
                            if kc1 * gd % p == c1:
                                report(f"ElGamal k2=k1+{delta}", c2 * inv(K * yd % p, p) % p)
                            if kc1 * pow(ginv, delta, p) % p == c1:
                                report(f"ElGamal k2=k1-{delta}", c2 * inv(K * pow(yinv, delta, p) % p, p) % p)
                    # k2 = a * k1
                    for a in range(2, 2001):
                        if pow(kc1, a, p) == c1:
                            report(f"ElGamal k2={a}*k1", c2 * inv(pow(K, a, p), p) % p)
            # small p: brute force the private key
            if p.bit_length() <= 48:
                for y in Y:
                    x = dlog(g, y, p)
                    if x is not None:
                        info(f"discrete log found: x = {x}")
                        for (c1, c2) in targets:
                            report("ElGamal small p", c2 * inv(pow(c1, x, p), p) % p)

# ---------------------------------------------------------------- DSA
def dsa_attacks(items):
    by, nums = collect(items)
    Q = nums("q")
    groups = {}
    for nm, lst in by.items():
        for g, v in lst:
            groups.setdefault(g, {})[nm] = v
    sigs = []
    for g, d in groups.items():
        if isinstance(d.get("r"), int) and isinstance(d.get("s"), int):
            h = next((d[k] for k in ("h", "hash", "hm", "z", "digest") if isinstance(d.get(k), int)), None)
            msg = next((d[k] for k in ("m", "msg", "message", "order", "data") if k in d), None)
            sigs.append((d["r"], d["s"], h, msg))
    if len(sigs) < 2 or not Q:
        return
    q = Q[0]
    print(f"[DSA] {len(sigs)} signatures, q ({q.bit_length()} bits)")
    for (r1, s1, h1, m1), (r2, s2, h2, m2) in itertools.combinations(sigs, 2):
        if r1 != r2:
            continue
        info("two signatures share r -> nonce reuse")
        cands = []
        if h1 is not None and h2 is not None:
            cands.append(("given hash", h1, h2))
        for hn in ("sha1", "sha256", "sha512", "sha224", "sha384", "md5"):
            if m1 is not None and m2 is not None:
                b1 = m1 if isinstance(m1, bytes) else (str(m1).encode() if not isinstance(m1, int) else i2b(m1))
                b2 = m2 if isinstance(m2, bytes) else (str(m2).encode() if not isinstance(m2, int) else i2b(m2))
                H1 = int.from_bytes(hashlib.new(hn, b1).digest(), "big")
                H2 = int.from_bytes(hashlib.new(hn, b2).digest(), "big")
                cands.append((hn, H1, H2))
                L = q.bit_length()            # FIPS: keep leftmost bits of the hash
                cands.append((hn + " truncated", H1 >> max(0, H1.bit_length() - L), H2 >> max(0, H2.bit_length() - L)))
        for label, H1, H2 in cands:
            try:
                k = (H1 - H2) * inv((s1 - s2) % q, q) % q
                x = (s1 * k - H1) * inv(r1, q) % q
            except Exception:
                continue
            ys = nums("y")
            ok = ""
            ps, gs = nums("p"), nums("g")
            if ys and ps and gs:
                if pow(gs[0], x, ps[0]) != ys[0]:
                    continue
                ok = "  (verified: g^x = y)"
            print(f"\n*** [DSA nonce reuse, {label}] private key x = {x}{ok}\n    k = {k}\n")
            report("DSA x as text", x)

# ---------------------------------------------------------------- main
from math import isqrt, gcd

def _iroot(x, k):
    if x < 2: return x
    lo, hi = 1, 1 << ((x.bit_length() + k - 1) // k + 1)
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if mid ** k <= x: lo = mid
        else: hi = mid - 1
    return lo

def _prime_power(n):
    for k in range(2, 17):
        r = _iroot(n, k)
        for cand in (r - 1, r, r + 1):
            if cand > 1 and cand ** k == n and is_prime(cand):
                return cand, k
    return None


def _factor_many(n, seconds):
    """fully factor n into primes, time-limited; returns None if it can't finish."""
    import time as _t
    deadline = _t.time() + seconds
    work, primes = [n], []
    while work:
        if _t.time() > deadline:
            return None
        m = work.pop()
        if m == 1:
            continue
        if is_prime(m):
            primes.append(m); continue
        f = None
        for sp in range(2, 100000):
            if m % sp == 0:
                f = sp; break
        if f is None:
            f = pollard_rho_timed(m, max(1, int(deadline - _t.time())))
        if not f or f == m:
            return None
        work.append(f); work.append(m // f)
    return primes

def _try_phi(label, n, phi, Es, Cs):
    for e in Es:
        if gcd(e, phi) != 1:
            continue
        d = inv(e, phi)
        for c in Cs:
            if c < n:
                report(label, pow(c, d, n))
        decrypt_blocks(label, d, n)

def structural_and_leakage(items):
    """RSA cases the main routine misses: given key parameters (instant),
    n prime, n = p^k, and many small primes (slow, last resort)."""
    by, nums = collect(items)
    Ns = list(dict.fromkeys(nums("n", "modulus", "nn")))
    Es = list(dict.fromkeys(nums("e", "exponent", "publicexponent"))) or [65537, 3]
    Cs = list(dict.fromkeys(nums("c", "ct", "ciphertext", "cipher", "enc", "encrypted", "flag")))
    if not Ns or not Cs:
        return

    # 1. KEY LEAKAGE (instant, definitive) --------------------------------
    PHI = nums("phi", "phin", "totient", "phi_n")
    LAM = nums("lambda", "lambdan", "carmichael")
    PQsum = nums("psum", "p_plus_q", "pplusq", "ppq")
    PQdif = nums("pdiff", "p_minus_q", "pminusq", "pmq")
    for n in Ns:
        for phi in PHI:
            _try_phi("known phi", n, phi, Es, Cs)
        for lam in LAM:
            _try_phi("known lambda", n, lam, Es, Cs)
        for s in PQsum:                      # phi = n - (p+q) + 1
            _try_phi("known p+q", n, n - s + 1, Es, Cs)
        for dmin in PQdif:                   # solve p,q from n and p-q
            disc = dmin * dmin + 4 * n
            r = isqrt(disc)
            if r * r == disc:
                p = (r + dmin) // 2
                if p > 1 and n % p == 0:
                    _try_phi("known p-q", n, (p - 1) * (n // p - 1), Es, Cs)

    # 2. FAST STRUCTURE: n prime, or n = p^k ------------------------------
    for n in Ns:
        if is_prime(n):
            info("n is prime -> phi = n-1")
            _try_phi("n prime", n, n - 1, Es, Cs)
            continue
        pp = _prime_power(n)
        if pp:
            p, k = pp
            info(f"n = p^{k} (prime power)")
            _try_phi("prime power", n, p ** (k - 1) * (p - 1), Es, Cs)

    # 3. SLOW: many small primes (only if nothing solved it yet) ----------
    if hits:
        return
    for n in Ns:
        if is_prime(n) or _prime_power(n):
            continue
        facs = _factor_many(n, 60)
        if facs and len(facs) >= 3 and all(is_prime(f) for f in facs):
            from collections import Counter
            phi = 1
            for pr, m in Counter(facs).items():
                phi *= (pr - 1) * pr ** (m - 1)
            info(f"n splits into {len(facs)} small primes")
            _try_phi("many small primes", n, phi, Es, Cs)

def main():
    files = sys.argv[1:]
    if not files:
        print(__doc__); return
    items = []
    for fn in files:
        try:
            got = read_file(fn)
            items += got
            print(f"read {fn}: {sum(isinstance(v, int) for _, _, v in got)} numbers")
        except Exception as ex:
            print(f"could not read {fn}: {ex}")
    print("names seen:", sorted({name_of(p) for _, p, _ in items})[:40])
    for attack in (rsa_attacks, structural_and_leakage, elgamal_attacks, dsa_attacks):
        try:
            attack(items)
        except Exception as ex:
            print(f"   ({attack.__name__} crashed: {ex})")
    print("\n==== RESULT ====")
    if hits:
        for a, t in hits:
            print(f"[{a}] {t}")
    else:
        print("Nothing found. Look at the 'names seen' line: rename fields in a copy of the file"
              " (n, e, c / p, g, y, c1, c2 / r, s, q) and run again.")

if __name__ == "__main__":
    main()
