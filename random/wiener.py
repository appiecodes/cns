from math import isqrt

import sympy
from Crypto.Util.number import long_to_bytes
from sympy import gcdex

n = 1000987777931946668890669

e = 292259205235020636821273

c = 898856304126468087762192



def wiener(e, n):
    a,b = e,n
    n0,n1 = 0,1 # vorige tellers
    d0,d1 = 1,0 # vorige noemers
    while b:
        t,a,b = a//b,b,a%b
        k,d = t*n1+n0,t*d1+d0
        n0,n1,d0,d1 = n1,k,d1,d
        if k == 0 or (e*d-1)%k:
            continue
        phi = (e*d-1)//k
        S = n-phi+1
        D = S*S-4*n
        if D < 0:
            continue
        root = isqrt(D)
        if root*root != D or (S+root)%2:
            continue
        p,q = (S+root)//2,(S-root)//2
        print(p,q)
        if p>1 and q>1 and p*q==n:
            return d
    return None

d = wiener(e, n)
if d != None:
    m = pow(c, d, n)
    print(long_to_bytes(m))
