# H(m) = int(sha256(m)) mod q
from _sha2 import sha256
import json

with open("dsa1_challenge.json") as f:
    challenge = json.load(f)
    p = challenge["p"]
    q = challenge["q"]
    g = challenge["g"]
    y = challenge["y"]
    signatures = challenge["signatures"]
    encrypted_flag = challenge["encrypted_flag"]




def H(m: bytes, q: int) -> int:
    return int(sha256(m).hexdigest(), 16) % q

def keystream(x: int, length: int) -> bytes:
    result = b''
    i = 0
    while len(result) < length:
        result += sha256(f'{x}:{i}'.encode()).digest()
        i += 1
    return result[:length]




s1 = signatures[0]["s"]
s2 = signatures[1]["s"]
r1 = signatures[0]["r"]
r2 = signatures[1]["r"]
h1 = H(signatures[0]["message"].encode(), q)
h2 = H(signatures[1]["message"].encode(), q)

k = ((h1 - h2) * pow(s1 - s2, -1, q)) % q
x = ((k * s1 - h1) * pow(r1, -1, q)) % q

assert pow(g, x, p) == y, "Failed to recover the private key"

flag = bytes.fromhex(encrypted_flag)
print(encrypted_flag)
key = keystream(x, len(flag))
decrypted_flag = bytes(a ^ b for a, b in zip(flag, key))

print(decrypted_flag.decode())