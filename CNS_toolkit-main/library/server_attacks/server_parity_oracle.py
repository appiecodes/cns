"""TEMPLATE: RSA LSB / parity decryption oracle (a server attack).

Use when: a server decrypts ciphertexts you send and tells you ONE bit about the
result - whether the plaintext is even/odd, or bigger/smaller than n/2.
That single bit, asked ~log2(n) times, binary-searches the whole message.

You MUST adapt send_and_get_bit() to the actual server. Everything else is generic.
"""

# ===================== EDIT CHECKLIST (do these, nothing else) =============
#  1. N, E, C and BASE : from the challenge
#  2. send_and_get_bit(ciphertext) : make it send `ciphertext` to the server
#     and return 1 if the server says ODD / upper-half, else 0.
#     (run once, read the reply, decide which word means 1)
#  The binary-search math does NOT change.
# ===========================================================================

from fractions import Fraction
from cns_toolkit import http_get, inv   # or write your own request

N = None   # fill in from the challenge
E = None
C = None
BASE = "http://cns-test.idlab.uantwerpen.be:500XX"

def send_and_get_bit(ciphertext):
    """ADAPT THIS. Send `ciphertext` to the oracle, return 1 if the decrypted
    plaintext is ODD (or >= n/2, depending on the oracle), else 0.
    Example skeleton:
        st, body = http_get(f"{BASE}/oracle?c={ciphertext}")
        return 1 if "odd" in body else 0
    """
    raise NotImplementedError("wire this to the server's response")

def attack():
    lo, hi = Fraction(0), Fraction(N)
    mult = pow(2, E, N)
    c = C
    for _ in range(N.bit_length()):
        c = c * mult % N                 # double the plaintext each round
        if send_and_get_bit(c):          # odd  -> plaintext wrapped past n -> upper half
            lo = (lo + hi) / 2
        else:
            hi = (lo + hi) / 2
    m = int(hi)
    return m.to_bytes((m.bit_length() + 7) // 8, "big")

if __name__ == "__main__":
    print(attack())
