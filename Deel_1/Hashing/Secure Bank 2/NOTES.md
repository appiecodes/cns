# Secure Bank 2 — botsing in een korte fingerprint

Script: [secure_bank_2.py](secure_bank_2.py). Start met `python secure_bank_2.py`.

## Vraag en herkenbaar patroon

De bank bewaart een ingekorte fingerprint en verwacht twee verschillende,
geldige JSON-records. Het patroon is een **collision**: verschillende invoer
met dezelfde bewaarde hashwaarde. De code neemt 8 hextekens van SHA-256: 32 bits.

## Code gebruiken en aanpassen

Het script varieert `reference` en onthoudt per fingerprint de eerdere
referentie. Het zoekt met `base`; de variabele `object` bovenaan is ongebruikt.
Houd de overige velden tijdens het zoeken vast, inclusief de timestamp.

De server verlangt precies deze velden en regels:

- `reference`: string van 1–128 tekens;
- `from_account` en `to_account`: verschillend en allebei beginnend met `SIM-`;
- `amount`: het getal `10`; `currency`: de string `EUR`;
- `timestamp`: een geldige ISO 8601-tijdstempel.

Gebruik dezelfde canonieke JSON als de server: gesorteerde sleutels,
compacte separators en `ensure_ascii=True`.

## Waarom werkt het?

8 hextekens geven `2**32` mogelijke waarden. Door het verjaardagseffect
wordt zoeken naar een willekeurige botsing van orde `2**16` kandidaten
interessant. Dit is een kansinschatting, geen gegarandeerd aantal pogingen.
Zie [NIST over ingekorte hashes, §5.1](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-107r1.pdf).

## Klein voorbeeld

Probeer in een tijdelijke kopie `[:2]` in plaats van `[:8]`. Met maar 8 bits
zie je het principe sneller. Zet voor de echte challenge `[:8]` terug.
Controleer een gevonden paar opnieuw: verschillende records, geldige velden
en dezelfde eerste 8 hashtekens van de canonieke bytes.

## Bij soortgelijke vragen

Reken eerst de werkelijk gecontroleerde bits uit. **Een willekeurig paar
laten botsen** is iets anders dan **een vast opgegeven doelhash treffen**;
die tweede taak heeft niet hetzelfde verjaardagsvoordeel.
Pas ook de toegestane veranderlijke velden en JSON-canonicalisatie aan.

## Als het niet werkt

De code print Python-bytes, zoals `b'{...}'`, en een lege tussenregel.
De server wil twee gewone JSON-regels: **zonder `b'...'` en zonder lege regel**.
Print bijvoorbeeld `canonicalize(base).decode("utf-8")` in plaats van bytes.
Verander een gevonden record daarna niet meer; ook een nieuwe timestamp
verandert de fingerprint.

Verbind met `nc cns-test.idlab.uantwerpen.be 50003` en stuur ieder record op
een eigen regel. De huidige code zoekt lokaal en verstuurt niets.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Secure%20Bank%202-13).
