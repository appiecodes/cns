from sympy import integer_nthroot
from Crypto.Util.number import long_to_bytes, bytes_to_long
import json
import math

with open("challenge.json", "r") as f:
    challenge = json.load(f)

n = challenge["n"]
e1 = challenge["e1"]
e2 = challenge["e2"]
c1 = challenge["c1"]
c2 = challenge["c2"]

print(math.gcd(e1,e2))
a = pow(e1, -1, e2)
b = (1 - a * e1)// e2
print(a , b)

# common modulus attack
M = (pow(c1, a, n) * pow(c2, b, n)) % n
print(M)
print(long_to_bytes(M))