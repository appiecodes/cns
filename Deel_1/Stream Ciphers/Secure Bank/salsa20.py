import json
import secrets
from Crypto.Cipher import Salsa20


def encrypt_transaction(transaction):
    """Encrypt a transaction using Salsa20."""
    nonce = secrets.token_bytes(8)

    cipher = Salsa20.new(key=KEY, nonce=nonce)

    plaintext = json.dumps(
        transaction,
        separators=(",", ":")
    ).encode()
    print(plaintext)

    ciphertext = cipher.encrypt(plaintext)

    # Transmit nonce alongside ciphertext
    return nonce + ciphertext


object = plaintext = json.dumps(
    {"from": "alice", "to": "bob", "amount": "999999"},
        separators=(",", ":")
    ).encode()




encrypted = "6ffdede06f7aaad55ec4319ae96e7126a97575a9301a5d3aeca89e1102bf9ba3abd077f76065411bbab28e498dd1c2a21fbe1e3a72"
known_plaintext = b'{"from":"alice","to":"bob","amount":"000010"}'
print(len(known_plaintext))
encrypted_transaction = bytes.fromhex(encrypted)[8:]  # Remove the nonce from the beginning of the ciphertext
print(len(encrypted_transaction))

solved = bytearray()

for c, k in zip(encrypted_transaction, known_plaintext):
    solved.append(c ^ k)

keystream = bytes(solved)

forged = bytearray()

for f, k in zip(keystream, object):
    forged.append(f ^ k)

forged = encrypted_transaction = bytes.fromhex(encrypted)[:8] + bytes(forged)  # Prepend the nonce to the forged ciphertext

print(forged.hex())
