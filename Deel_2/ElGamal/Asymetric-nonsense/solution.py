import json
from Crypto.Util.number import bytes_to_long, long_to_bytes

with open("challenge.json") as f:
    challenge = json.load(f)
    known_plaintext = challenge["known_plaintext"]
    p = challenge["p"]
    g = challenge["g"]
    y = challenge["y"]
    cipher_known = challenge["cipher_known"]
    cipher_flag = challenge["cipher_flag"]

m = bytes_to_long(known_plaintext.encode())

flag = m * cipher_flag[1] * pow(cipher_known[1], -1, p) % p

print(long_to_bytes(flag).decode())