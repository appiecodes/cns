from Crypto.Util.number import long_to_bytes
from sympy import gcdex

n = 100000000013333335457121932657285475527

e1 = 17
e2 = 65537

c1 = 9866836740419942369663564470859750669
c2 = 10454601987294025436868196381153224694

a, b, g = map(int, gcdex(e1,e2))

print(f"a: {a}, b: {b}, g: {g}")

m = (pow(c1, a, n) * pow(c2, b, n)) % n
print(f"m: {m}")
print(long_to_bytes(m))