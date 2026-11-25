# Space Race 1 — SHA-256

## 1. Vraag en herkenbaar patroon

De website vraagt een Mars-relay te onderzoeken en geeft alleen
`cns-test.idlab.uantwerpen.be:50006`. Begin met
`nc cns-test.idlab.uantwerpen.be 50006` en lees de banner en instructies.
Noteer welke waarden je krijgt en wat je moet terugsturen.

**Dit script is een SHA-256-rekenhulp, geen volledige relay-oplossing.**
De vraagtekst beschrijft de precieze hashrelatie niet. Gebruik de helper
om een hypothese uit de serveruitvoer te controleren.

[mars.py](mars.py) berekent nu één hash van de ingevulde hexdata. De variabelen `c1`,
`c2` en `c3` worden nog niet gebruikt. Welke waarde je moet hashen en waarmee
je de uitkomst moet vergelijken, haal je uit de opdracht.

## 2. Wat moet ik aanpassen?

1. Zoek uit of de invoer **hexdata** of **gewone tekst** is.
2. Vervang de lange waarde binnen `bytes.fromhex("...")` in `mars.py` door
   de hexdata uit je opdracht. Bij gewone tekst gebruik je bijvoorbeeld
   `"abc".encode("utf-8")` als invoer voor `hashlib.sha256(...)`.
3. Start vanuit de hoofdmap van de repo:

```bash
python "Hashing/Space Race 1/mars.py"
```

Werkt het commando `python` niet, probeer dan `python3`.
Voor deze oefening zijn geen extra Python-pakketten nodig.

## 3. Waarom werkt dit?

De stappen zijn: **hex omzetten naar bytes → SHA-256 berekenen → de hash als
hextekst tonen**. Dezelfde bytes leveren steeds dezelfde hash op.
`hexdigest()` toont de volledige SHA-256-hash als 64 hextekens.
Zie de [Python-uitleg over hashlib](https://docs.python.org/3/library/hashlib.html).

Hex is een manier om bytes op te schrijven. `bytes.fromhex("616263")` geeft
`b"abc"`, terwijl `"616263".encode()` de zes cijfers als tekst omzet naar
`b"616263"`. Dat zijn verschillende invoerwaarden.
Zie [bytes.fromhex](https://docs.python.org/3/library/stdtypes.html#bytes.fromhex).

## 4. Klein voorbeeld dat je kunt controleren

```python
import hashlib

data = bytes.fromhex("616263")  # De bytes van de tekst abc.
doelhash = "ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"

berekend = hashlib.sha256(data).hexdigest()
print(data)
print(berekend == doelhash.lower())
```

Verwachte uitvoer:

```text
b'abc'
True
```

`True` betekent dat de berekende hash overeenkomt met de doelhash.
Bij een eigen opdracht vervang je de invoer en de doelhash door de gegeven waarden.

Vervang de regel met `data` door `data = "abc".encode("utf-8")`.
Je hoort precies dezelfde uitvoer te krijgen: de bytes zijn gelijk.

## 5. Het werkt niet — wat nu?

| Wat zie ik? | Wat controleer ik eerst? |
| --- | --- |
| `ValueError` bij `fromhex` | Heb je echte hexdata? Per byte zijn twee hextekens nodig. Neem een eventuele `0x`-prefix niet mee. |
| `TypeError` bij `sha256` | Geef bytes mee: `bytes.fromhex(...)` voor hexdata of `.encode("utf-8")` voor tekst. |
| Mijn hash verschilt van de verwachte hash | Controleer hex versus tekst, hoofdletters in de oorspronkelijke tekst, spaties en een eventuele newline. Die kunnen de invoerbytes veranderen. |
| Ik vergelijk een onleesbare byteswaarde met een hexstring | Gebruik `.hexdigest()` voor een vergelijking met een hash in hextekst. `.digest()` geeft ruwe bytes. |
| Er wordt een hash geprint, maar ik kom niet verder | Lees welk verband de opdracht vraagt. Het huidige script vergelijkt niets met `c1`, `c2` of `c3`. |

Om de invoer te bekijken, zet je in het kleine voorbeeld vóór het hashen:

```python
print(repr(data), len(data), data.hex())
```

Voor `abc` verwacht je `b'abc' 3 616263`. Klopt dit niet, verbeter dan eerst
de invoer voordat je een andere aanpak probeert.

Heb je **alleen een volledige hash**, zonder mogelijke invoer of verdere
aanwijzingen? Er is geen algemene praktische manier om daar de oorspronkelijke
invoer uit terug te halen. Zoek in de opdracht naar hints die mogelijke invoer
beperken, zoals een korte pincode of een opgegeven lijst met kandidaten.
Zie [NIST over de eenweg-eigenschap van hashes](https://csrc.nist.gov/glossary/term/hash_function).

## 6. Bij soortgelijke vragen

Werk van protocolobservatie naar een hypothese en daarna een kleine lokale
controle. Is de invoer ruwe data, hextekst, een combinatie met een nonce of
het resultaat van een vorige stap? Dat verschil bepaalt wat je moet hashen.

Bij een echte hashketen is de volgende hash van `bytes.fromhex(vorige_hash)`
iets anders dan de hash van `vorige_hash.encode()`. Leid de juiste keuze
af uit de constructie. De aanwezigheid van `c1`, `c2` en `c3` alleen bewijst
geen hashketen; die variabelen worden in dit script niet gebruikt.
Houd sessiewaarden bij dezelfde verbinding en neem geen oude nonce over
als de server een nieuwe uitgeeft.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Space%20Race%201-15).
