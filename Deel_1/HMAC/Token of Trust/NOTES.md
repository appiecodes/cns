# Token of Trust — onjuist gecontroleerde JWT

Script: [jwt.py](jwt.py). Start met `python jwt.py`.
De huidige import `werkzeug` moet beschikbaar zijn om het bestand ongewijzigd
te draaien, hoewel die niet voor de JWT-bewerking gebruikt wordt.

## Vraag en herkenbaar patroon

De vraag geeft een guest-account en vraagt toegang tot `/admin` zonder de
geheime sleutel te kennen. Het token heeft drie delen:
`header.payload.signature`. Onderzoek **de claims en algoritmevalidatie**.
De labapp draait op poort `50009`; neem na inloggen een actueel token over.

## Code gebruiken en aanpassen

Vervang `token` en bekijk de gedecodeerde header en payload.
Het script bouwt daarna een token met `alg: none`, een aangepaste rol en
een lege signature. De laatste punt blijft onderdeel van het token.

**Let op:** het oorspronkelijke voorbeeld heeft claim `user`, maar de
opgebouwde voorbeeldpayload gebruikt `username`. Behoud bij een nieuwe
poging de echte payloadvelden en wijzig alleen de benodigde claim.
Ook verplichte claims en verloopdatums kunnen tot afwijzing leiden.

## Waarom kan het werken?

Base64url is een representatie die de inhoud leesbaar maakt na decoderen.
`alg: none` betekent een token zonder cryptografische handtekening.
De aanpak slaagt alleen als de server zo'n token ten onrechte voor deze
authenticatie accepteert. Correct afgedwongen algoritmen en signatures
voorkomen dat een willekeurige claimwijziging toegang oplevert.
Zie [RFC 7519, unsecured JWTs](https://www.rfc-editor.org/rfc/rfc7519.html#section-6).

## Klein voorbeeld

```python
import base64
import json

part = "eyJyb2xlIjoidXNlciJ9"
padding = "=" * (-len(part) % 4)
print(json.loads(base64.urlsafe_b64decode(part + padding)))
```

Verwacht: `{'role': 'user'}`. Dit decodeert alleen; het verifieert niets.
De bestaande `decode`-functie voegt de eventueel benodigde padding niet
toe en kan daardoor bij andere tokens falen.

## Bij soortgelijke vragen

Behoud de juiste claimnamen en gebruik de cookie of Authorization-header
waarin het legitieme verzoek het token verstuurt. Alleen een token printen
vraagt nog geen adminpagina op. Een nieuwe payload maakt de oude signature
normaal ongeldig; elke JWT is dus niet automatisch op deze manier aanpasbaar.

## Als het niet werkt

Controleer padding, JSON, de lege derde sectie, verloopdatum en claimvelden.
Weigert de server `none`, dan is deze specifieke zwakte niet aangetoond.
Een ontbrekende lokale Python-module is een uitvoeringsprobleem en zegt
niets over de beveiliging van de server.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Token%20of%20Trust-19).
