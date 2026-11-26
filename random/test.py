from sympy import gcd

n = 3233
e = 17

m = 123
s_faulty = 2799

v = pow(s_faulty, e, n)
print("v: ", v)

q = gcd(s_faulty**e - m, n)

print("q: ", q)
p = n // q
print("p: ", p)
print("n: ", p * q)
