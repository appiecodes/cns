from math import gcd, isqrt
l2b = lambda m: m.to_bytes((m.bit_length()+7)//8, "big")   # int -> bytes (long_to_bytes)
b2l = lambda b: int.from_bytes(b, "big")                    # bytes -> int (bytes_to_long)
inv = lambda a, m: pow(a, -1, m)                            # modulaire inverse (Python 3.8+)

def iroot(x, k):                  # integer k-de wortel, floor; check: iroot(x,k)**k == x
    lo, hi = 0, 2**(x.bit_length()//k + 1)
    while lo < hi:
        mid = (lo+hi)//2
        if mid**k < x: lo = mid+1
        else: hi = mid
    return lo if lo**k == x else lo-1

def egcd(a, b):                   # (g, x, y) met a*x + b*y = g
    if b == 0: return a, 1, 0
    g, x, y = egcd(b, a % b)
    return g, y, x - (a//b)*y

def crt(cs, ns):                  # x = ci mod ni, ni onderling copriem
    N = 1
    for n in ns: N *= n
    return sum(c*(N//n)*inv(N//n, n) for c, n in zip(cs, ns)) % N


c=1148176102467930159856714719821330971449602527964126426770344293712866719611027934580388248910690062744474773139786182084511607713966499366265508001141309234043702051769340910511513570512371901969864293
e=3
n=83070775017400312771924958652523550174876970032198824894485803990647401326585645419168010276752754281220521091737241531623587366614877536741795974783883608947001667394720201384646684654209380451903193093145030177252481951786407944077748350388257188686591610624482542959686201501255221078521538009830962618753
m = iroot(c, e); assert pow(m, e) == c; print(l2b(m))
# m^e net groter dan n? probeer c + k*n
for k in range(100000):
    m = iroot(c + k*n, e)
    if pow(m, e) == c + k*n: print(l2b(m)); break