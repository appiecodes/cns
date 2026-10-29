"""
Encryption module.

This module implements a custom stream cipher.
"""

from pathlib import Path

# LCG parameters
A = 1103515245
C = 12345
M = 2**31


def next_state(state):
    """Generate the next PRNG state."""
    return (A * state + C) % M


def generate_keystream(seed, length):
    """Generate a pseudorandom keystream."""
    state = seed
    keystream = bytearray()

    for _ in range(length):
        state = next_state(state)
        keystream.append((state >> 16) & 0xff)

    return bytes(keystream)


def encrypt(plaintext, seed):
    """Encrypt plaintext using XOR."""
    keystream = generate_keystream(seed, len(plaintext))
    return bytes(
        p ^ k for p, k in zip(plaintext, keystream)
    )


def decrypt(ciphertext, seed):
    """Decrypt ciphertext using XOR."""
    return encrypt(ciphertext, seed)


"""
Oplossing:
"""


known = b"STATUS: SERVER ONLINE"
ct = bytes.fromhex("22135cc0b9daa9e717f98a998e6ee5e92655e1a88f")
secret = bytes.fromhex("12296eef9eece6b42dd2bf90aa63b6d21a7cc98b95c78b4b01d833d628a941b82fb65176b4ed3c3f64")

k0 = known[0] ^ ct[0]        # het eerste keystream-getal (0x71)

for seed in range(2**24):
    if (next_state(seed) >> 16) & 0xff != k0:
        continue             # eerste getal klopt niet: meteen de volgende seed
    if decrypt(ct, seed) == known:
        print(decrypt(secret, seed))
        break