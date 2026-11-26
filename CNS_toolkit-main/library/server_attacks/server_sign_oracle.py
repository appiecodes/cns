"""SERVER: RSA signing oracle (e.g. signing_server).

The server signs any message EXCEPT the one you need (say, an admin token).
RSA signatures are multiplicative: sig(a)*sig(b) = sig(a*b) mod n.
So write target = a*b (mod n) with a,b != target, get both signed, multiply.

Edit CONFIG and the sign() request line.  python3 server_sign_oracle.py
"""

# ===================== EDIT CHECKLIST (do these, nothing else) =============
#  1. BASE : the server's real address:port (replace 500XX)
#  2. N, E : modulus and public exponent (from the challenge)
#  3. TARGET : the integer message you need signed (e.g. an admin token as int)
#  4. the `url =` line in sign() : the server's real sign endpoint path
#  5. the field in sign()'s return : the key in the server's JSON reply
#  The forgery math (sig(a)*sig(b)) does NOT change.
# ===========================================================================

import json, urllib.request
from cns_toolkit import inv

# ---- CONFIG --------------------------------------------------------------
BASE   = "http://cns-test.idlab.uantwerpen.be:500XX"
N = None            # modulus
E = None            # public exponent
TARGET = None       # the integer message you need a signature for
A = 2               # any factor != 1; B is derived so A*B == TARGET mod n
# --------------------------------------------------------------------------

def sign(message_int):
    """ADAPT: ask the server to sign `message_int`, return the integer signature."""
    url = f"{BASE}/sign?m={message_int}"               # <-- change endpoint
    body = urllib.request.urlopen(url, timeout=15).read().decode()
    print("sign ->", body[:200])
    try:    return int(json.loads(body)["signature"])  # <-- change field name
    except: return int(body.strip())

B = TARGET * inv(A, N) % N
forged = sign(A) * sign(B) % N
print("forged signature:", forged)
print("verifies:", pow(forged, E, N) == TARGET % N)
