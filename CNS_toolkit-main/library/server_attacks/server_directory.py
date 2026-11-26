"""SERVER: ElGamal key-directory attack (Phone Book + the overwrite twist).

The directory never checks who you are. Two cases:
  (a) you can register a NEW name  -> register your key, have the victim send to it.
  (b) you can only OVERWRITE names  -> overwrite the TARGET's key with yours.
Either way the victim encrypts to a key whose PRIVATE part you know.

Edit the CONFIG block and the three request lines to match the challenge text.
Run on campus / VPN.  python3 server_directory.py
"""

# ===================== EDIT CHECKLIST (do these, nothing else) =============
#  1. BASE : the server's real address:port (replace 500XX)
#  2. TARGET : the name the victim encrypts to (from the challenge, e.g. "bob")
#  3. MYNAME : a NEW name to register,  OR set it = TARGET to OVERWRITE (the twist)
#  4. the `req("/directory", {...})` fields and the `req("/send?to=...")` path:
#     match the endpoints/field names the challenge lists
#  5. the c1/c2 lines : match the field names in the "/send ->" printout
#  The decryption math does NOT change.
# ===========================================================================

import json, random, urllib.request
from cns_toolkit import inv, show

# ---- CONFIG: read these from the challenge description --------------------
BASE   = "http://cns-test.idlab.uantwerpen.be:500XX"
TARGET = "bob"                 # the name the victim encrypts to
MYNAME = "bob"                 # register under this name: your own for (a), the TARGET for the overwrite twist (b)
# --------------------------------------------------------------------------

def req(path, data=None):
    """GET if data is None, else POST json. Returns parsed json (prints raw)."""
    url = BASE + path
    if data is None:
        r = urllib.request.urlopen(url, timeout=15)
    else:
        r = urllib.request.urlopen(urllib.request.Request(
            url, data=json.dumps(data).encode(),
            headers={"Content-Type": "application/json"}, method="POST"), timeout=15)
    body = r.read().decode()
    print(path, "->", body[:200])
    try:    return json.loads(body)
    except: return body

# 1. public parameters
params = req("/params")
p = int(params["p"]); g = int(params["g"])

# 2. our own keypair
x = random.randrange(2, p - 1)
y = pow(g, x, p)

# 3. register (new name) or overwrite (the target's slot)
req("/directory", {"name": MYNAME, "y": y})      # ADAPT field names if needed

# 4. make the victim encrypt the secret to the name we control
resp = req("/send?to=" + TARGET)                 # ADAPT the endpoint/param name

# pull the ciphertext pair (ADAPT the field names from the printed response)
c1 = int(resp.get("c1") or resp.get("a") or resp["ciphertext"][0])
c2 = int(resp.get("c2") or resp.get("b") or resp["ciphertext"][1])

# 5. decrypt with our private key
K = pow(c1, x, p)
print("FLAG:", show(c2 * inv(K, p) % p))
