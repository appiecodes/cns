import json

jobject = {"from":"user1","to":"user2","amount": "xxxxxx"}

json_string = json.dumps(jobject)

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