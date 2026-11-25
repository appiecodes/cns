from sympy import factorint


n = 34664911185892166593
e = 65537

factors = factorint(n)
print(factors)


print(pow(e,-1, (3539306293-1) * (9794267101-1)))
