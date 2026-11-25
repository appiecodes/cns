from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad, pad
from pathlib import Path

def encrypt(key, data):
    return AES.new(key, AES.MODE_ECB).encrypt(data)

def decrypt(key, data):
    return AES.new(key, AES.MODE_ECB).decrypt(data)

def make_key(number):
    return number.to_bytes(3, "big") + b"\x00" * 13


# Read the encrypted image.
image = Path(r"C:\Users\abdir\Downloads\enc(1).bmp").read_bytes()

# Our guessed original block and its encrypted version.
original_guess = bytes.fromhex("0000ff0000ff0000ff000000000000ff")
encrypted_block = image[54:70]

# The encrypted promo code from the challenge.
promo = bytes.fromhex(
    "df7c7dfbd5e1ba2af108d658132d5f20"
    "d34de27da16375ceabd7a79cbfe738244"
    "027a4a0b26ec498a2c223a545b9567c20"
    "bf423bb38514e6cd6f043ab9e23a84f"
    "fa6745294c224068e1cffd9e8c9e294"
)

# Try every first key. Save each possible middle value.
table = {}

for k1 in range(2**20):
    middle = encrypt(make_key(k1), original_guess)
    table[middle] = k1
    # Table has key -> middle value mapping.


# Try every second key. Look for a matching middle value.
for k2 in range(2**20):
    middle = decrypt(make_key(k2), encrypted_block)
    k1 = table.get(middle)

    if k1 is None:
        continue

    # Match found: undo both encryption layers on the promo.
    halfway = decrypt(make_key(k2), promo)
    flag = decrypt(make_key(k1), halfway)

    print(flag.decode("utf-8"))
    break