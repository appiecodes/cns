# Cryptografie — snelle examenreferentie

Offline | RSA · ElGamal · DSA · RSA-signatures

Open dit bestand in PyCharm of een teksteditor. Zoek met Ctrl+F op de naam van de aanval. De formules staan ook in gewone tekst, dus een Markdown- of LaTeX-renderer is niet nodig. De uitgebreide uitleg en voorbeelden staan in `Cryptografie_examenbundel.pdf`.

## 0. Welke aanval?

| Gegeven / herkenning | Wat zoeken? | Ga naar |
|---|---|---|
| RSA: n, e; kleine n | p, q, d | RSA-1 |
| RSA: p en q liggen dicht bij elkaar | p, q | RSA-1 Fermat |
| RSA: e = 3, ciphertext exacte derdemacht | M | RSA-2 |
| RSA: zelfde M en e, verschillende n | M | RSA-3 Håstad |
| RSA: zelfde n en M, verschillende e | M | RSA-4 common modulus |
| RSA: verschillende n, gedeelde priem | d | RSA-5 common prime |
| RSA: snelle decryptie, kleine d | d | RSA-6 Wiener |
| RSA: p, q, d bekend; snelle decryptie | M | RSA-7 CRT |
| RSA: signature of raw oracle | S / M | RSA-8 |
| ElGamal: Ma, Ca, Cb; zelfde c1 | Mb | EG-2 nonce reuse |
| ElGamal: Ma, Ca, Cb; verschillende c1 | Mb | EG-3 related nonce |
| ElGamal: p,g,y; kleine x of kleine groepsorde | x | EG-4 discrete log |
| ElGamal: p,g,y,c1,c2; kleine k | k, M | EG-4 discrete log |
| ElGamal: decryptie-oracle / small subgroup | M / info over x | EG-5 |
| DSA: k bekend | x | DSA-2 |
| DSA: r1 == r2 | k, x | DSA-3 |
| DSA: klein k of bekend verschil k2-k1 | x | DSA-4 |
| ElGamal-signature: zelfde r | k,x | EG-SIG |

## 1. Python en wiskunde

```python
from math import gcd, isqrt
from sympy import gcdex, factorint, integer_nthroot, discrete_log, n_order
from sympy.ntheory.modular import crt
from Crypto.Util.number import bytes_to_long, long_to_bytes
```

| Wiskunde | Python |
|---|---|
| a^e mod n | `pow(a,e,n)` |
| inverse a^(-1) mod n | `pow(a,-1,n)` (gcd(a,n) moet 1 zijn) |
| a^(-k) mod n | `pow(a,-k,n)` |
| Bézout: a*u+b*v=gcd(a,b) | `u,v,g = map(int,gcdex(a,b))` |
| exacte e-de machtswortel | `m,exact = integer_nthroot(C,e)` |
| gehele vierkantswortel | `r = isqrt(D)`; exact als `r*r == D` |
| factoren | `factorint(n)` geeft `{prime: exponent}` |
| log: g^x = y mod p | `x = int(discrete_log(p,y,g))` |
| orde van g modulo p | `R = int(n_order(g,p))` |
| CRT: X mod ns[i] = rs[i] | `X,N = crt(ns,rs)` |
| bytes naar integer | `bytes_to_long(b'ABC')` |
| integer naar bytes | `long_to_bytes(int(M))` |

Gebruik `pow` met drie argumenten; geen floats voor RSA. SymPy en PyCryptodome moeten lokaal geïnstalleerd zijn. Alternatieven voor bytes: `int.from_bytes(b,'big')` en `m.to_bytes(max(1,(m.bit_length()+7)//8),'big')`.

### CRT zonder library

N = product van de onderling coprieme moduli. Ni = N // ni. yi = inverse van Ni modulo ni. X = som(ri * Ni * yi) mod N.

```python
from math import prod
def crt_coprime(ns, rs):
    N = prod(ns)
    return sum(r*(N//n)*pow(N//n,-1,n) for n,r in zip(ns,rs))%N, N
```

## 2. RSA

Publiek: n,e. Privaat: d,p,q. n = p*q, phi = (p-1)*(q-1) voor verschillende priemen.

```
d = e^(-1) mod phi
C = M^e mod n
M = C^d mod n
ed - 1 = k*phi
```

### RSA-1 | Factorisatie

```python
f = factorint(n)
assert len(f)==2 and all(v==1 for v in f.values())
p,q = map(int,f)
phi = (p-1)*(q-1)
d = pow(e,-1,phi)
M = pow(C,d,n)
```

Fermat: n = a² - b² = (a-b)(a+b). Vooral als p en q dicht bij elkaar liggen.

```python
def fermat(n, limit=100000):
    a = isqrt(n-1)+1
    for _ in range(limit):
        b2 = a*a-n
        b = isqrt(b2)
        if b*b==b2 and a-b>1:
            return a-b,a+b
        a+=1
    return None
```

Pollard rho voor factorisatie; Pollard p-1 voor gladde p-1. `factorint` is niet praktisch voor normale grote RSA-sleutels.

### RSA-2 | Low public exponent

Als M^e < n dan C = M^e; neem de exacte wortel. Als er weinig modulo-reducties zijn, test C+j*n met kleine j.

```python
for j in range(1000):
    M, exact = integer_nthroot(C+j*n,e)
    if exact and M<n:
        print(long_to_bytes(int(M)))
        break
```

### RSA-3 | Håstad broadcast (CRT)

Zelfde M, zelfde kleine e, minstens e onderling coprieme moduli, geen willekeurige padding. CRT reconstrueert M^e omdat M^e kleiner is dan het product van e moduli.

```python
X,N = crt([n1,n2,n3],[C1,C2,C3])
M,exact = integer_nthroot(X,3)
assert exact
print(long_to_bytes(int(M)))
```

Zijn ciphertexts identiek? Probeer eerst de directe wortel. Controleer anders gcd van moduli.

### RSA-4 | Common modulus

Zelfde n, zelfde M, verschillende e1,e2 met gcd=1. Bézout a*e1+b*e2=1. Dus C1^a*C2^b = M mod n.

```python
a,b,g = map(int,gcdex(e1,e2))
assert g==1
M = pow(C1,a,n)*pow(C2,b,n)%n
```

Bij negatieve exponent is inverse nodig. Bij gcd(e1,e2)>1 krijg je een macht van M modulo n, niet meteen M.

### RSA-5 | Common prime

```python
p = gcd(n1,n2)
assert 1<p<min(n1,n2)
q1 = n1//p
phi = (p-1)*(q1-1)
d1 = pow(e1,-1,phi)
M1 = pow(C1,d1,n1)
```

### RSA-6 | Wiener

Kleine d, vergelijkbare priemen; voldoende klassieke grens d < n^(1/4)/3. e/n benadert k/d. Test de convergents met phi=(e*d-1)/k, S=n-phi+1, D=S²-4n. p,q=(S±sqrt(D))/2.

```python
def wiener(e,n):
    a,b=e,n
    n0,n1,d0,d1=0,1,1,0
    while b:
        t,a,b=a//b,b,a%b
        k,d=t*n1+n0,t*d1+d0
        n0,n1,d0,d1=n1,k,d1,d
        if k==0 or (e*d-1)%k:
            continue
        phi=(e*d-1)//k
        S=n-phi+1
        D=S*S-4*n
        if D<0:
            continue
        r=isqrt(D)
        if r*r!=D or (S+r)%2:
            continue
        p,q=(S+r)//2,(S-r)//2
        if p>1 and q>1 and p*q==n:
            return d
    return None
```

### RSA-7 | CRT-decryptie (geen aanval)

```python
Vp=pow(C,d%(p-1),p)
Vq=pow(C,d%(q-1),q)
M,N=crt([p,q],[Vp,Vq])
# Of zonder library:
M=(Vp*q*pow(q,-1,p)+Vq*p*pow(p,-1,q))%(p*q)
```

### RSA-8 | Handtekening / raw RSA

Textbook: `S=pow(h,d,n)`; verify `pow(S,e,n)==h`. Moderne signatures gebruiken padding/encoding zoals PSS; hash alleen is niet voldoende.

- Multiplicativiteit: S1*S2 mod n is een raw signature op h1*h2 mod n. Niet noodzakelijk een vindbaar echt bericht met die hash.
- Raw decryptie-oracle (lokaal lab): C' = C*r^e mod n. Als oracle M' levert, M = M'*r^(-1) mod n; r moet inverteerbaar zijn. Raw signing-oracle analoog met h en S.
- Faulty CRT-signature (Bellcore): `gcd(pow(Sf,e,n)-h,n)` of `gcd(S-Sf,n)` bij dezelfde representatie. Alleen bij geschikte fout; controleer factor strikt tussen 1 en n.

## 3. ElGamal

### EG-1 | Basis

```
y = g^x mod p      # x private key
c1 = g^k mod p     # k verse nonce
s = y^k mod p = c1^x mod p
c2 = M*s mod p
M = c2*s^(-1) mod p
```

```python
# x bekend:
s = pow(c1,x,p)
M = c2*pow(s,-1,p)%p
# k bekend:
s = pow(y,k,p)
M = c2*pow(s,-1,p)%p
```

### EG-2 | Known plaintext + nonce reuse

Gegeven: p,g,y,Ma,Ca=(a1,a2),Cb=(b1,b2). Ma moet niet nul zijn. Als a1==b1 onder dezelfde publieke sleutel, zijn de maskers gelijk.

```python
sA = a2*pow(Ma,-1,p)%p
Mb = b2*pow(sA,-1,p)%p
# Direct:
Mb = b2*Ma*pow(a2,-1,p)%p
```

Zonder Ma: b2/a2 = Mb/Ma modulo p (geen unieke plaintext).

### EG-3 | Related nonce (a1 != b1)

kB=kA+t. ratio=b1*a1^(-1)=g^t mod p. Zoek t, daarna sB=sA*y^t mod p.

```python
ratio = b1*pow(a1,-1,p)%p
sA = a2*pow(Ma,-1,p)%p
# Eerst kleine positieve/negatieve verschillen proberen:
for t in range(-10000,10001):
    if pow(g,t,p)==ratio:
        sB=sA*pow(y,t,p)%p
        Mb=b2*pow(sB,-1,p)%p
        print(long_to_bytes(Mb))
        break
```

Als ratio==g, t=1 werkt. Voor zwakke groepsorde kan `t=discrete_log(p,ratio,g)` werken. Een gewone log is niet betrouwbaar na modulo-reductie. Bij bekende affine relatie kB=u*kA+v: b1=a1^u*g^v mod p; sB=sA^u*y^v mod p. Zonder zwakte of relatie geen algemene plaintext recovery.

### EG-4 | Discrete log (ook DH / DSA publieke sleutel)

Doel H=y (x zoeken), H=c1 (k zoeken), of H=ratio (t zoeken). Vind z met g^z=H mod p.

```python
# Klein zoekbereik:
for z in range(100000):
    if pow(g,z,p)==H:
        print(z)
        break
# Zwakke groepsorde:
z = int(discrete_log(p,H,g))
assert pow(g,z,p)==H
```

BSGS: O(sqrt(R)) tijd en geheugen. Pollard rho DLP: verwacht O(sqrt(R)) tijd, constant geheugen. R = orde(g), niet altijd p-1.

Pohlig–Hellman: als orde R bestaat uit kleine priemmachten, los discrete logs in subgroepen op en combineer met CRT.

```python
R=int(n_order(g,p))
rs=[int(l**a) for l,a in factorint(R).items()]
zs=[discrete_log(p,pow(H,R//r,p),pow(g,R//r,p)) for r in rs]
z=int(crt(rs,zs)[0])
assert pow(g,z,p)==H
```

### EG-5 | Malleability / CCA / small subgroup

- Malleability: wijzig (c1,c2) naar (c1,a*c2 mod p); plaintext wordt a*M mod p.
- Als lokaal decryptie-oracle die aangepaste plaintext Mp geeft: `M=Mp*pow(a,-1,p)%p`.
- Small subgroup: als ongeldige c1 met kleine orde r geaccepteerd wordt, heeft c1^x maar r mogelijke waarden. Alleen met bruikbare feedback kan info over x mod r lekken. CRT kan verschillende resten combineren.

## 4. DSA

### DSA-1 | Signing en verification

Publiek: p,q,g,y. Privaat: x. g heeft orde q. h = hashrepresentatie. k = geheime nonce.

```python
y=pow(g,x,p)
r=pow(g,k,p)%q
s=pow(k,-1,q)*(h+x*r)%q
# r,s mogen niet nul zijn
w=pow(s,-1,q)
u1,u2=h*w%q,r*w%q
v=(pow(g,u1,p)*pow(y,u2,p)%p)%q
valid=0<r<q and 0<s<q and v==r
```

Waarom? s*k = h+x*r mod q. Dus u1+x*u2 = w*(h+x*r) = k mod q. Omdat g orde q heeft, wordt g^(u1+x*u2) mod p gelijk aan g^k mod p. Nog eens mod q geeft r.

### DSA-2 | Bekende nonce

Start: s*k = h+x*r mod q.

```python
x=(s*k-h)*pow(r,-1,q)%q
assert pow(g,x,p)==y
```

### DSA-3 | Nonce reuse

Zelfde private key, gelijke r is aanwijzing voor zelfde k. Trek s1*k=h1+x*r en s2*k=h2+x*r af.

```python
assert r1==r2
k=(h1-h2)*pow(s1-s2,-1,q)%q
x=(s1*k-h1)*pow(r1,-1,q)%q
assert pow(g,x,p)==y and pow(g,k,p)%q==r1
```

Bij s1==s2 mod q bestaat geen inverse. Verifieer altijd de key.

### DSA-4 | Kleine of gerelateerde nonce

```python
# Klein k:
for k in range(1,min(q,100000)):
    if pow(g,k,p)%q==r:
        x=(s*k-h)*pow(r,-1,q)%q
        if pow(g,x,p)==y:
            print(k,x)
            break
```

Bij bekend k2=k1+t:

```python
x=(s1*h2-s2*h1-s1*s2*t)*pow(s2*r1-s1*r2,-1,q)%q
k1=(h1+x*r1)*pow(s1,-1,q)%q
assert pow(g,x,p)==y
```

Noemer moet inverteerbaar zijn. Kleine onbekende t kan als hypothese worden getest. Gedeeltelijk bekende/bias in veel nonces: lattice-aanvallen (niet uitgewerkt). Kleine x: discrete log op y. Bij DSA is `discrete_log(p,r,g)` niet algemeen correct door extra mod q.

## 5. EG-SIG | ElGamal-handtekening (niet encryptie)

L=p-1. Kies k met gcd(k,L)=1.

```
r = g^k mod p
s = k^(-1)*(h-x*r) mod L    # MIN, DSA heeft PLUS
verify: g^h = y^r*r^s mod p
```

Bij bekende k: r*x = h-s*k mod L. Bij hergebruik: (s1-s2)*k = h1-h2 mod L. L is samengesteld; inverse kan ontbreken. Los dan lineaire congruentie op:

```python
def lincong(a,b,m):
    d=gcd(a,m)
    if b%d: return
    mod=m//d
    u=(b//d)*pow(a//d,-1,mod)%mod if mod>1 else 0
    for i in range(d):
        yield u+i*mod
L=p-1
for k in lincong(s1-s2,h1-h2,L):
    if gcd(k,L)!=1 or pow(g,k,p)!=r: continue
    for x in lincong(r,h1-s1*k,L):
        if pow(g,x,p)==y: print(k,x)
```

## 6. Controle voor je antwoord

- RSA: p*q==n; (e*d)%phi==1 of modulo lambda(n); pow(M,e,n)==C.
- ElGamal/DSA: pow(g,x,p)==y. Voor ElGamal: pow(g,k,p)==c1.
- DSA: signing-algebra modulo q, groepsmachten modulo p. ElGamal-signing: modulo p-1.
- Lees `integer_nthroot` als (wortel, exact), niet alleen de wortel.
- Een mislukte attack betekent niet dat het systeem veilig is. Een kleine of voorspelbare exponent is een specifieke aanname, geen garantie.

Scope: de besproken asymmetrische algoritmen en verwante technieken. Niet de volledige CNS-cursus (bijv. AES, DES, HMAC, JWT en overige topics). Alle snippets zijn lokale rekenvoorbeelden of templates voor oefenparameters; vervang de variabelen door de gegeven waarden. Er zijn geen online bronnen nodig tijdens het gebruik.
