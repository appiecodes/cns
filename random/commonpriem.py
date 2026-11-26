from sympy import factorint, discrete_log
import math
n1 = 1000036000099
e1 = 65537
c1 = 598195729194

n2 = 1000040000111
e2 = 65537
c2 = 393182114155


print(factorint(n1))
print(factorint(n2))


from math import gcd
p = gcd(n1,n2)
if 1 < p < min(n1,n2):
    q1, q2 = n1//p, n2//p
    d1 = pow(e1,-1,(p-1)*(q1-1))
    d2 = pow(e2,-1,(p-1)*(q2-1))
    M1, M2 = pow(c1,d1,n1), pow(c2,d2,n2)

    print(f"p: {p}, q1: {q1}, q2: {q2}")
    print(f"M1: {M1}, M2: {M2}")