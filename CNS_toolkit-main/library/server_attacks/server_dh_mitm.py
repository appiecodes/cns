"""SERVER: Diffie-Hellman man-in-the-middle (relay template).

Unauthenticated DH: you sit between Alice and Bob. Replace each public value
you forward with g^d (your own), so you share one key with each and can
read/alter everything.  K_with_alice = A^d,  K_with_bob = B^d.

This one is a RELAY, so the exact flow depends on the server. Fill in how you
receive A and B and how you forward values; the key math is fixed below.
"""

# ===================== EDIT CHECKLIST (do these, nothing else) =============
#  1. P, G : the public parameters (from the challenge)
#  2. the relay : receive Alice's A and Bob's B, but forward D (=g^d) to BOTH.
#     Then key_with(A) is your shared key with Alice, key_with(B) with Bob.
#  The key math does NOT change.
# ===========================================================================

import random
from cns_toolkit import inv

# ---- CONFIG: p, g from the challenge -------------------------------------
P = None
G = None
# --------------------------------------------------------------------------
d = random.randrange(2, (P or 10) - 1)        # your middle-man exponent
D = pow(G, d, P) if P else None               # the value you send to BOTH sides

def key_with(their_public):
    """shared key between you and whoever sent `their_public` (A or B)."""
    return pow(their_public, d, P)

# Typical use:
#   A = <receive Alice's public>   ; forward D to Bob instead of A
#   B = <receive Bob's public>     ; forward D to Alice instead of B
#   k_alice = key_with(A) ; k_bob = key_with(B)
#   decrypt Alice's message with k_alice, re-encrypt with k_bob (and vice versa)
print("DH MITM template ready: fill P, G and the relay, then use key_with().")
