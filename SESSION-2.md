# Hacking session 2

Naslag voor **RSA, ElGamal, digitale handtekeningen en key distribution**. De voorbeelden staan volledig op deze pagina. Ze gebruiken kleine oefengetallen en Python zonder extra pakketten.

## Snel zoeken

| Als de vraag draait om… | Ga naar |
| --- | --- |
| RSA-sleutel, encryptie, decryptie of padding | [RSA](#rsa) |
| Een ciphertext met twee delen en een tijdelijke exponent | [ElGamal](#elgamal) |
| De geldigheid van een handtekening of de rol van de nonce | [Digitale handtekeningen](#digitale-handtekeningen) |
| Een publieke sleutel ophalen, koppelen aan een naam of vervangen | [Key distribution](#key-distribution) |
| Een nieuwe vraag onder tijdsdruk | [Startcontrole](#startcontrole) |
| Een snelle controle van alle rekenvoorbeelden | [Python-zelftest](#python-zelftest) |

## Startcontrole

1. Schrijf op wat gevraagd wordt. Gaat het om vertrouwelijkheid, een geldige handtekening of de identiteit achter een sleutel?
2. Geef elke invoer een rol. Markeer publieke parameters, geheime waarden, bericht, handtekening of ciphertext. Check of getallen decimaal of hex zijn.
3. Noteer de modulus vóór je rekent. Bij DSA gaat het groepswerk modulo `p` en het rekenen met exponenten en handtekeningwaarden modulo `q`.
4. Kies één controle die bij de vraag hoort. Ontsleutel een eigen voorbeeld terug, verifieer een echte en een gewijzigde handtekening, of leg uit welk bewijs een sleutel aan een persoon koppelt.

Gebruik `pow(a, b, m)` voor machten modulo `m`. Voor `pow(a, -1, m)` moet `gcd(a, m) == 1` gelden.

## RSA

**Publiek** `(n, e)`. **Privaat** `d` en de factoren `p, q`. Bij twee verschillende priemen geldt `n = p*q` en `phi = (p-1)*(q-1)`. Kies een `e` die inverteerbaar is modulo `phi` en bepaal `d` uit `e*d ≡ 1 (mod phi)`.

| Bewerking | Formule |
| --- | --- |
| Encryptie van een oefenbericht | `C = pow(M, e, n)` |
| Decryptie met je eigen privésleutel | `M = pow(C, d, n)` |
| Controle van invoer | `0 <= M < n`, `gcd(e, phi) == 1` |

**Voorbeeld.** Bij `p=11`, `q=13` en `e=7` krijg je `n=143`, `phi=120` en `d=103`. Voor `M=9` is `C=48`. Met `d=103` komt er weer `9` uit.

**Probeer zelf.** Gebruik dezelfde sleutel voor $M=4$. Bereken de cijfertekst en controleer dat decryptie weer $4$ oplevert.

<details>
<summary>Controleantwoord RSA</summary>

De cijfertekst is $82$. Dat getal tot de macht $103$ modulo $143$ geeft weer $4$.

</details>

In een vraag over een echt systeem hoort het gebruikte RSA-schema bij de beoordeling. OAEP wordt gebruikt voor RSA-encryptie, PSS voor RSA-handtekeningen. De formule met een kale modulaire macht hierboven dient voor de wiskunde-oefening.

## ElGamal

**Publiek** `(p, g, y)` met `y = g^x mod p`. **Privaat** `x`. De verzender kiest per encryptie een verse geheime exponent `k`.

| Stap | Formule |
| --- | --- |
| Encryptie | `c1 = g^k mod p`, `s = y^k mod p`, `c2 = M*s mod p` |
| Decryptie met je eigen privésleutel | `s = c1^x mod p`, `M = c2*inverse(s, p) mod p` |

**Voorbeeld.** Kies `p=23`, `g=5`, `x=6`, `k=7` en `M=10`. Dan is `y=8`, `c1=17`, `s=12` en `c2=5`. De inverse van `12` modulo `23` is `2`. De ontvanger krijgt dus `5*2 mod 23 = 10` terug.

**Controle.** De verzender en ontvanger moeten dezelfde `s` uitrekenen. Een verschillende `c1` zegt op zichzelf niets over een voorspelbare relatie tussen de geheime exponenten. Bij een ontwerpvraag kijk je naar de groepsparameters, de generatie van `k` en de integriteitsbescherming van het bericht.

**Probeer zelf.** Gebruik dezelfde parameters en publieke sleutel met $k=9$ en $M=12$. Bereken beide delen van de ciphertext en controleer de decryptie.

<details>
<summary>Controleantwoord ElGamal</summary>

Je krijgt $(c_1,c_2)=(11,16)$. Beide kanten berekenen dezelfde groepswaarde $9$. De inverse modulo $23$ is $18$, dus $16\cdot18\bmod 23=12$.

</details>

## Digitale handtekeningen

Een verifier gebruikt het bericht, de handtekening en de publieke sleutel van de ondertekenaar. Ook de herkomst van die publieke sleutel telt.

### DSA

**Publiek** `(p, q, g, y)`, waar `g` orde `q` heeft en `y = g^x mod p`. **Privaat** `x`. `h` is de gehele hashrepresentatie volgens het schema en `k` is de geheime waarde voor de ondertekening.

| Stap | Formule |
| --- | --- |
| Ondertekenen | `r = (g^k mod p) mod q`, `s = inverse(k, q)*(h + x*r) mod q` |
| Eerst bij verificatie | Controleer `0 < r < q` en `0 < s < q` vóór de inverse |
| Verifiëren | `w = inverse(s, q)`, `u1 = h*w mod q`, `u2 = r*w mod q` |
| Vergelijken | `v = ((g^u1 * y^u2) mod p) mod q`, geldig als `v == r` |

**Voorbeeld.** Met `p=47`, `q=23`, `g=4`, `x=5`, `k=7` en `h=9` is `y=37` en de handtekening `(5,18)`. De verificatie geeft `w=9`, `u1=12`, `u2=22` en `v=5`.

**Probeer zelf.** Neem voor dezelfde handtekening $h=10$ en controleer of die nog geldig is.

<details>
<summary>Controleantwoord DSA</summary>

Je krijgt $u_1=21$, $u_2=22$ en $v=19$. De verificatie faalt omdat $19$ verschilt van $r=5$.

</details>

Controleer de waardegebieden en voorkom hergebruik van een nonce voor verschillende berichten. Houd bij het lezen van de opgave de nonce `k` en de langetermijnsleutel `x` uit elkaar. Bij RSA-handtekeningen controleert de verifier volgens het afgesproken encodingschema, bijvoorbeeld RSA-PSS.

## Key distribution

**De vraag die je moet kunnen beantwoorden:** welk bewijs koppelt deze publieke sleutel aan deze persoon?

| Situatie | Wat je controleert |
| --- | --- |
| Sleutel uit een directory | Wie mag registreren of wijzigen? Hoe is de koppeling tussen identiteit en sleutel bevestigd? |
| Certificaat | Controleer de vertrouwensketen, identiteit, geldigheid en toepasselijke intrekkingsstatus. |
| Fingerprint | Vergelijk via een vooraf vertrouwd, onafhankelijk kanaal. Een fingerprint uit dezelfde onbevestigde directory levert zelf geen onafhankelijk bewijs. |
| Sleutelrotatie | Verifieer opnieuw wie de nieuwe sleutel beheert. Leg vast welke sleutel is vervangen en respecteer geldigheid en intrekking. |
| Diffie–Hellman | Beide kanten berekenen een gedeelde waarde. Authenticatie van de uitgewisselde waarden is een aparte controle. |

**Rekenvoorbeeld Diffie–Hellman.** Voor `p=29` en `g=2` gebruikt Alice `a=5` en Bob `b=9`. Hun publieke waarden zijn `A=3` en `B=19`. Zij berekenen allebei `21`, respectievelijk met `B^a mod p` en `A^b mod p`.

**Zelfstandige directory-oefening.** Alice heeft eerder via een vertrouwd kanaal Bobs fingerprint voor sleutel K1 gekregen. De directory toont vandaag K2 onder Bobs naam. Wat controleert Alice vóór ze K2 gebruikt? Wat verandert er als Bob de wissel onafhankelijk heeft bevestigd?

<details>
<summary>Controleantwoord</summary>

De naam in de directory alleen geeft Alice geen bewijs dat K2 van Bob is. Ze controleert de nieuwe fingerprint via een vertrouwd kanaal of valideert een certificaat dat de juiste identiteit aan K2 bindt. Als Bob K2 onafhankelijk bevestigt, kan Alice haar bekende koppeling bijwerken en rekening houden met de geldigheid of intrekking van K1.

</details>

## Python-zelftest

De verwachte uitkomst is vier regels met `OK`. Gebruik de testwaarden hieronder als je eerst het rekenpad wilt controleren.

```python
from math import gcd

# RSA
p, q, e, message = 11, 13, 7, 9
n = p * q
phi = (p - 1) * (q - 1)
assert gcd(e, phi) == 1
d = pow(e, -1, phi)
ciphertext = pow(message, e, n)
assert (d, ciphertext, pow(ciphertext, d, n)) == (103, 48, 9)
print("RSA OK")

# ElGamal
p, g, private_key, nonce, message = 23, 5, 6, 7, 10
public_key = pow(g, private_key, p)
c1 = pow(g, nonce, p)
sender_secret = pow(public_key, nonce, p)
c2 = message * sender_secret % p
receiver_secret = pow(c1, private_key, p)
assert (public_key, c1, c2) == (8, 17, 5)
assert sender_secret == receiver_secret
assert c2 * pow(receiver_secret, -1, p) % p == message
print("ElGamal OK")

# DSA
p, q, g, private_key, nonce, h = 47, 23, 4, 5, 7, 9
public_key = pow(g, private_key, p)
r = pow(g, nonce, p) % q
s = pow(nonce, -1, q) * (h + private_key * r) % q

def verify_dsa(hash_value, r, s, p, q, g, public_key):
    if not (0 < r < q and 0 < s < q):
        return False
    inverse_s = pow(s, -1, q)
    u1 = hash_value * inverse_s % q
    u2 = r * inverse_s % q
    v = (pow(g, u1, p) * pow(public_key, u2, p) % p) % q
    return v == r

assert (public_key, r, s) == (37, 5, 18)
assert verify_dsa(h, r, s, p, q, g, public_key)
assert not verify_dsa(h + 1, r, s, p, q, g, public_key)
assert not verify_dsa(h, r, 0, p, q, g, public_key)
print("DSA OK")

# Diffie–Hellman
p, g, alice_private, bob_private = 29, 2, 5, 9
alice_public = pow(g, alice_private, p)
bob_public = pow(g, bob_private, p)
assert (alice_public, bob_public) == (3, 19)
assert pow(bob_public, alice_private, p) == pow(alice_public, bob_private, p) == 21
print("Diffie–Hellman OK")
```
