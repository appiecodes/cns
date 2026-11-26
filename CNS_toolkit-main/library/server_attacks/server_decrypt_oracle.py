"""SERVER: RSA chosen-ciphertext / "let's decrypt" oracle.

The server decrypts any ciphertext you send EXCEPT the target one.
RSA is multiplicative, so blind the target, get it decrypted, then unblind:
  send  X = C * r^e mod n   ->  oracle returns  r*M mod n   ->  M = that * r^-1 mod n.

Edit CONFIG and the oracle() request line.  python3 server_decrypt_oracle.py
"""

# ===================== EDIT CHECKLIST (do these, nothing else) =============
#  1. BASE : the server's real address:port (replace 500XX)
#  2. N, E, C : modulus, public exponent, target ciphertext (from the challenge)
#  3. the `url =` line in oracle() : the server's real decrypt endpoint path
#  4. the field in oracle()'s return : the key in the server's JSON reply
#     (run once, read the "oracle ->" printout, then set the right name)
#  The attack math (blind / unblind) does NOT change.
# ===========================================================================

import json, urllib.request
from cns_toolkit import inv, show

# ---- CONFIG --------------------------------------------------------------
BASE = "http://cns-test.idlab.uantwerpen.be:500XX"
N = None      # the modulus  (from the challenge file/description)
E = None      # public exponent
C = None      # the target ciphertext you must decrypt
R = 2         # blinding factor (any small int coprime to n)
# --------------------------------------------------------------------------

def oracle(ciphertext):
    """ADAPT: send `ciphertext` to the decrypt endpoint, return the integer it gives back."""
    url = f"{BASE}/decrypt?c={ciphertext}"            # <-- change to the real endpoint
    body = urllib.request.urlopen(url, timeout=15).read().decode()
    print("oracle ->", body[:200])
    try:    return int(json.loads(body)["plaintext"]) # <-- change field name
    except: return int(body.strip())

blinded = C * pow(R, E, N) % N
answer  = oracle(blinded)
M = answer * inv(R, N) % N
print("FLAG:", show(M))
