"""Pure-Python AES (no pycryptodome needed). Decrypt only: ECB, CBC, CTR.
Use when a flag is AES-encrypted with a key derived from a recovered secret and
the lab PC has no pycryptodome / no internet.

    from aes_pure import aes_ecb_dec, aes_cbc_dec, aes_ctr_dec
    flag = aes_ecb_dec(key, ct)                 # key is 16/24/32 bytes
    flag = aes_cbc_dec(key, iv, ct)
    flag = aes_ctr_dec(key, nonce_or_counter, ct)
"""
SBOX = [0] * 256
p = q = 1
while True:
    p = p ^ ((p << 1) & 0xFF) ^ (0x1B if p & 0x80 else 0)
    q ^= q << 1; q ^= q << 2; q ^= q << 4; q &= 0xFF
    if q & 0x80: q ^= 0x09
    x = (q ^ ((q << 1) | (q >> 7)) ^ ((q << 2) | (q >> 6)) ^ ((q << 3) | (q >> 5)) ^ ((q << 4) | (q >> 4))) & 0xFF
    SBOX[p] = (x ^ 0x63) & 0xFF
    if p == 1: break
SBOX[0] = 0x63
INV = [0] * 256
for i, v in enumerate(SBOX): INV[v] = i

def _xt(a): return ((a << 1) ^ 0x1B) & 0xFF if a & 0x80 else (a << 1)
def _mul(a, b):
    r = 0
    while b:
        if b & 1: r ^= a
        a = _xt(a); b >>= 1
    return r

def _expand(key):
    nk = len(key) // 4; nr = nk + 6
    w = [list(key[4*i:4*i+4]) for i in range(nk)]
    rc = 1
    for i in range(nk, 4*(nr+1)):
        t = list(w[i-1])
        if i % nk == 0:
            t = t[1:]+t[:1]; t = [SBOX[b] for b in t]; t[0] ^= rc; rc = _xt(rc)
        elif nk > 6 and i % nk == 4:
            t = [SBOX[b] for b in t]
        w.append([a ^ b for a, b in zip(w[i-nk], t)])
    return [sum(w[4*r:4*r+4], []) for r in range(nr+1)]

def _dec_block(rk, b):
    s = [x ^ k for x, k in zip(b, rk[-1])]
    for r in range(len(rk)-2, -1, -1):
        s = [s[(i - 4*(i % 4)) % 16] for i in range(16)]      # inv shiftrows
        s = [INV[x] for x in s]                                # inv subbytes
        s = [x ^ k for x, k in zip(s, rk[r])]                  # addroundkey
        if r != 0:
            n = []
            for c in range(4):
                a = s[4*c:4*c+4]
                n += [_mul(a[0],14)^_mul(a[1],11)^_mul(a[2],13)^_mul(a[3],9),
                      _mul(a[0],9)^_mul(a[1],14)^_mul(a[2],11)^_mul(a[3],13),
                      _mul(a[0],13)^_mul(a[1],9)^_mul(a[2],14)^_mul(a[3],11),
                      _mul(a[0],11)^_mul(a[1],13)^_mul(a[2],9)^_mul(a[3],14)]
            s = n
    return bytes(s)

def _enc_block(rk, b):
    s = [x ^ k for x, k in zip(b, rk[0])]
    for r in range(1, len(rk)):
        s = [SBOX[x] for x in s]
        s = [s[(i + 4*(i % 4)) % 16] for i in range(16)]
        if r != len(rk)-1:
            n = []
            for c in range(4):
                a = s[4*c:4*c+4]
                n += [_mul(a[0],2)^_mul(a[1],3)^a[2]^a[3],
                      a[0]^_mul(a[1],2)^_mul(a[2],3)^a[3],
                      a[0]^a[1]^_mul(a[2],2)^_mul(a[3],3),
                      _mul(a[0],3)^a[1]^a[2]^_mul(a[3],2)]
            s = n
        s = [x ^ k for x, k in zip(s, rk[r])]
    return bytes(s)

def aes_ecb_dec(key, ct):
    rk = _expand(key)
    return b"".join(_dec_block(rk, ct[i:i+16]) for i in range(0, len(ct)-len(ct)%16, 16))

def aes_cbc_dec(key, iv, ct):
    rk = _expand(key); out = b""; prev = iv
    for i in range(0, len(ct)-len(ct)%16, 16):
        blk = ct[i:i+16]
        out += bytes(a ^ b for a, b in zip(_dec_block(rk, blk), prev)); prev = blk
    return out

def aes_ctr_dec(key, counter, ct):
    rk = _expand(key); out = b""; ctr = int.from_bytes(counter, "big")
    for i in range(0, len(ct), 16):
        ks = _enc_block(rk, ctr.to_bytes(16, "big"))
        out += bytes(a ^ b for a, b in zip(ct[i:i+16], ks)); ctr += 1
    return out
