from Crypto.Util.number import long_to_bytes
from sympy.ntheory.modular import crt
from sympy import integer_nthroot

n1 = 1003022023051
e1 = 3
c1 = 970165728721

n2 = 1007040085027
e2 = 3
c2 = 214394990991

n3 = 1016091238147
e3 = 3
c3 = 730282205408

crt = crt([n1, n2, n3], [c1, c2, c3])

print(crt)

M = integer_nthroot(crt[0], 3)[0]
print(M)
print(long_to_bytes(M))