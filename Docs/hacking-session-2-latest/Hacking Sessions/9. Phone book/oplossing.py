import json, secrets, urllib.request

BASE = "http://cns-test.idlab.uantwerpen.be:50011"
l2b = lambda m: m.to_bytes((m.bit_length() + 7) // 8, "big")
inv = lambda a, m: pow(a, -1, m)

# 1. Haal de publieke parameters p en g op
params = json.loads(urllib.request.urlopen(f"{BASE}/params").read())
p, g = int(params["p"]), int(params["g"])

# 2. Genereer je eigen ElGamal-sleutelpaar (privésleutel x, publieke sleutel y)
x = secrets.randbelow(p - 2) + 2
y = pow(g, x, p)

# 3. Registreer je publieke sleutel onder een eigen naam in de directory
name = f"mallory_{secrets.token_hex(4)}"
req = urllib.request.Request(
    f"{BASE}/directory",
    data=json.dumps({"name": name, "y": y}).encode(),
    headers={"Content-Type": "application/json"},
    method="POST",
)
print("POST /directory:", urllib.request.urlopen(req).read().decode())

# 4. Laat Alice haar geheim naar jouw naam versleutelen
res = json.loads(urllib.request.urlopen(f"{BASE}/send?to={name}").read())
print("GET /send:", res)

# Haal c1 en c2 uit het antwoord (ondersteunt zowel {"c1":..,"c2":..} als {"cipher":[c1,c2]})
if "c1" in res and "c2" in res:
    c1, c2 = int(res["c1"]), int(res["c2"])
elif "cipher" in res:
    c1, c2 = map(int, res["cipher"])
else:
    raise KeyError(f"Pas even de JSON-keys aan op basis van de output hierboven: {res}")

# 5. Ontsleutel met jouw eigen privésleutel x: m = c2 * (c1^x)^-1 mod p
s = pow(c1, x, p)
m = (c2 * inv(s, p)) % p
print("Secret:", l2b(m).decode())