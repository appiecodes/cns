n=122669927411406727028788626411679443825688776964989352296475427773238194525648382371552761821855169263312605721407880877201759835810127064710476447051953689721330492645804679815792399036086826175563763597773587160877571184108516088814876030806480091013658263418131474441195440823023139298901952911255011539271
e=93570199767358024291201010969804528185370907625457279260926085845016814204197871528076645182086290233543797522608794365343079838239595866737414231665735577696295318454369964329852287041541654159409978529168799334787687422979841162861038975098731934708646455041406657882224493351947655156228657436753078459681
c=63190008952747037070429205997813552737461029227687467209185847535467974587640762563475064539913916079017028949672905146132754696181065925175268042787315140973476806461302280659042070005545642451857859868819928731084766790121697292805285631884013218055705384394531201778850069464339792949444208423036622974887


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
def cf(a, b):
    q = []
    while b: q.append(a//b); a, b = b, a % b
    return q
def convs(q):
    h0, h1, k0, k1 = 0, 1, 1, 0
    for a in q:
        h0, h1 = h1, a*h1+h0; k0, k1 = k1, a*k1+k0
        yield h1, k1
for k, d in convs(cf(e, n)):
    if k == 0 or (e*d-1) % k: continue
    phi = (e*d-1)//k; s = n-phi+1; disc = s*s-4*n
    if disc >= 0 and isqrt(disc)**2 == disc:
        print("d =", d); print(l2b(pow(c, d, n))); break