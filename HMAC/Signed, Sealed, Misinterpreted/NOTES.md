# Signed, Sealed, Misinterpreted

Categorie: **HMAC**. Labserver: `http://cns-test.idlab.uantwerpen.be:50007`.

## 1. Wanneer gebruik ik deze aanpak?

Deze challenge geeft een geldig ondertekend JSON-verzoek voor de rol `user`.
Je wilt toegang tot de admin-vault krijgen met de meegegeven handtekening.
In jouw uitvoering leverde het onderstaande verzoek HTTP 200 met een flag op.

## 2. De werkende stappen

Haal eerst het bericht en de bijbehorende handtekening op:

```bash
curl -i 'http://cns-test.idlab.uantwerpen.be:50007/challenge'
```

Het bericht uit jouw uitvoering was `{"action":"view","role":"user"}`.
Kopieer de waarde van `signature` uit het antwoord en vervang daarmee
`PLAK_HIER_DE_SIGNATURE` in dit verzoek:

```bash
curl -i -X POST \
  'http://cns-test.idlab.uantwerpen.be:50007/vault' \
  -H 'Content-Type: application/json' \
  -H 'X-Signature: PLAK_HIER_DE_SIGNATURE' \
  -d '{"action":"view","role":"admin","role":"user"}'
```

Let op de volgorde: **eerst `admin`, daarna `user`**.
Je gebruikt de bestaande handtekening en houdt `action` gelijk aan `view`.

## 3. Waarom kan dit werken?

Het verzoek bevat twee velden met dezelfde naam, `role`. Software kan zulke
dubbele velden verschillend behandelen. De JSON-standaard raadt unieke
veldnamen aan en beschrijft dat het gedrag bij dubbele namen kan verschillen.
Zie [RFC 8259, objecten](https://www.rfc-editor.org/rfc/rfc8259#section-4).

Je resultaat past bij deze verklaring: de handtekeningcontrole gebruikt
`role=user`, terwijl de toegangscontrole `role=admin` gebruikt. Zo blijft de
handtekening bruikbaar voor een verzoek dat anders wordt geïnterpreteerd.
Dit is een verklaring op basis van je resultaat; de exacte servercode is
niet zichtbaar. De fout zit vermoedelijk in de verwerking van het bericht.

## 4. Klein lokaal voorbeeld

Python gebruikt bij `json.loads` standaard de **laatste** waarde van een
dubbele veldnaam. Zie de [Python-documentatie](https://docs.python.org/3/library/json.html#repeated-names-within-an-object).

```python
import json

body = '{"action":"view","role":"admin","role":"user"}'
print(json.loads(body)["role"])
```

Verwachte uitvoer: `user`. Dit laat zien hoe één parser dit bericht leest;
het bewijst niet welke parser de labserver voor iedere controle gebruikt.

## 5. Het werkt niet — wat controleer ik?

| Probleem | Eerst controleren |
| --- | --- |
| De handtekening wordt geweigerd | Gebruik de `signature` uit het antwoord van `/challenge` van dezelfde labserver. Controleer de headernaam `X-Signature` en de waarde van `action`. |
| Geen admin-toegang | Zijn beide `role`-velden nog aanwezig, met `admin` vóór `user`? |
| Het werkt met curl, maar niet vanuit Python | Bewaar de body als ruwe JSON-string. Een gewone dictionary houdt maar één waarde per sleutel over; bij `requests` gebruik je daarom `data=body` met de JSON-contentheader. |
| De server meldt ongeldige JSON | Gebruik de gewone aanhalingstekens uit het codeblok en stuur `Content-Type: application/json` mee. |
| Geen verbinding | Controleer de poort `50007` en je toegang tot het labnetwerk. |

De les: handtekeningcontrole en autorisatie moeten dezelfde eenduidige
interpretatie van het bericht gebruiken. Dubbele veldnamen weigeren voorkomt
deze ambiguïteit.
