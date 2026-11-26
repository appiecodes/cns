"""CTFd: DSA with two signatures sharing a nonce (e.g. Double Entry).

Run:  python3 dsa_solve.py <challenge.json>
Needs cns_toolkit.py in the same folder.

Part A (always the same): two signatures with the SAME r share the nonce k, so:
    k = (H1 - H2) / (s1 - s2)   mod q
    x = (s1*k - H1) / r         mod q      <- the private key
Part B (CHANGES every challenge): use x to get the flag. See the big comment below.
"""
import sys, json, hashlib
from cns_toolkit import inv

data = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "challenge.json"))

# 1. READ THE INPUT  (rename keys here if the file uses different ones)
p, q, g, y = data["p"], data["q"], data["g"], data["y"]
sig1, sig2 = data["signatures"][0], data["signatures"][1]
r = sig1["r"]
s1, s2 = sig1["s"], sig2["s"]
print("same r (= same nonce)?", sig1["r"] == sig2["r"])

# The file usually states the hash, e.g. "H(m) = int(sha256(m)) mod q".
# Match this to it (change sha256 / the mod q if the file says otherwise):
def H(message):
    return int(hashlib.sha256(message.encode()).hexdigest(), 16) % q

H1, H2 = H(sig1["message"]), H(sig2["message"])

# 2A. RECOVER THE PRIVATE KEY  (this part never changes)
k = (H1 - H2) * inv(s1 - s2, q) % q
x = (s1 * k - H1) * inv(r, q) % q
print("private key x =", x)
print("check g^x == y:", pow(g, x, p) == y)        # MUST print True before you trust x

# ===========================================================================
# 2B. GET THE FLAG FROM x.
#
# WHERE TO LOOK: the challenge tells you how the flag was locked. Check, in order:
#   - a JSON field named "flag_encryption", "encryption", "note", or "hint"
#   - the assignment.txt / challenge description text
#   - any field holding the ciphertext: "encrypted_flag", "ct", "flag", "cipher"
#
# Then match what it says to ONE of the patterns below. Uncomment that one,
# comment the others. `x` is your key; `ct` is the ciphertext bytes.
# ===========================================================================

ct = bytes.fromhex(data.get("encrypted_flag") or data.get("ct") or data.get("flag"))

# --- Pattern A: XOR with a keystream = sha256(f"{x}:0") || sha256(f"{x}:1")... ---
#     (this is the Double Entry scheme)
keystream = b""
i = 0
while len(keystream) < len(ct):
    keystream += hashlib.sha256(f"{x}:{i}".encode()).digest()
    i += 1
flag = bytes(a ^ b for a, b in zip(ct, keystream))

# --- Pattern B: XOR with a single hash of x (ct is one block, <= 32 bytes) ---
# key = hashlib.sha256(str(x).encode()).digest()
# flag = bytes(a ^ b for a, b in zip(ct, key))

# --- Pattern C: AES, key = sha256(x). No install needed - uses aes_pure.py. ---
# from aes_pure import aes_ecb_dec, aes_cbc_dec, aes_ctr_dec   (copy aes_pure.py into the folder)
# key = hashlib.sha256(str(x).encode()).digest()          # or sha256(i2b(x))
# flag = aes_ecb_dec(key, ct)                             # ECB
# # CBC: iv = bytes.fromhex(data["iv"]); flag = aes_cbc_dec(key, iv, ct)
# # CTR: nonce = bytes.fromhex(data["nonce"]); flag = aes_ctr_dec(key, nonce, ct)

# --- Pattern D: the flag IS x as bytes (no separate ciphertext) ---
# flag = x.to_bytes((x.bit_length()+7)//8, "big")

# 3. THE FLAG
try:
    print("Flag:", flag.decode())
except Exception:
    print("Flag (raw bytes, wrong pattern? try another):", flag)
