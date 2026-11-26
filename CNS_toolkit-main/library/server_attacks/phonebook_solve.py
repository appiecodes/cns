"""CTFd: Phone Book  (ElGamal key directory, man-in-the-middle).

Run:  python3 phonebook_solve.py
Needs cns_toolkit.py in the same folder. Must be on a network that can reach
the server (campus / VPN).

The trick: the directory lets ANYONE register a key, and Alice will encrypt
her secret to whatever key is listed under the name you ask for. So we
register OUR OWN key, ask Alice to send to us, and decrypt with our private key.
"""
import json, random
from cns_toolkit import http_get, http_post_json, inv, show

BASE = "http://cns-test.idlab.uantwerpen.be:50011"
NAME = "ayman_" + str(random.randint(1000, 9999))   # a name unlikely to be taken

# 1. get the public parameters
st, body = http_get(BASE + "/params")
print("[/params]", st, body)
params = json.loads(body)
p = int(params["p"])
g = int(params["g"])

# 2. make our own keypair (we know the private key x)
x = random.randrange(2, p - 1)
y = pow(g, x, p)

# 3. register our public key under our name
st, body = http_post_json(BASE + "/directory", {"name": NAME, "y": y})
print("[register]", st, body)

# 4. make Alice encrypt her secret to OUR key
st, body = http_get(BASE + "/send?to=" + NAME)
print("[/send]", st, body)
resp = json.loads(body)

# the ciphertext is an ElGamal pair; the server may name the fields differently.
# look at the printed [/send] line above and set c1, c2 accordingly.
def grab(d, *names):
    for n in names:
        if n in d:
            return int(d[n])
    return None

c1 = grab(resp, "c1", "a", "gamma")
c2 = grab(resp, "c2", "b", "delta")
if c1 is None and "ciphertext" in resp:          # maybe it's a list [c1, c2]
    c1, c2 = int(resp["ciphertext"][0]), int(resp["ciphertext"][1])

# 5. decrypt with our private key x
K = pow(c1, x, p)
m = c2 * inv(K, p) % p
print("Flag:", show(m))
