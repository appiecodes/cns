# Secure Bank — een versleutelde transactie wijzigen

Gebruik [salsa20.py](salsa20.py): `python salsa20.py`.
[secure_bank.py](secure_bank.py) is een los fragment, geen volledige client.

## Vraag en herkenbaar patroon

De bank gebruikt Salsa20 voor JSON-transacties en stuurt `nonce + ciphertext`.
De vraag is of je een transactie kunt aanpassen. Het patroon is **malleability**:
zonder gecontroleerde authenticatie kan een gewijzigde ciphertext een gericht
gewijzigde plaintext opleveren.

Lees de labinstructies via `nc cns-test.idlab.uantwerpen.be 50001`.
Neem de vereiste transactie en het doelbedrag uit die instructies over.

## Wat doet de code en wat pas ik aan?

Vervang `encrypted`, `known_plaintext` en de gewenste transactie (`object`).
De eerste 8 bytes zijn in deze opgave de nonce. Die worden apart gehouden
en later ongewijzigd vóór de aangepaste ciphertext gezet.

De JSON-bytes moeten exact kloppen, inclusief veldvolgorde, spaties, quotes
en het verschil tussen een getal en een string. De code gebruikt compacte
JSON. Houd de gewijzigde plaintext even lang als de bekende plaintext.
De waarde `999999` is een ingevuld voorbeeld, geen universeel doelbedrag.

## Waarom werkt het?

```text
C = P XOR K
K = C XOR P
C_nieuw = C XOR P XOR P_nieuw
```

De server ontsleutelt `C_nieuw` met dezelfde keystream en krijgt `P_nieuw`.
Dit verandert één bestaande transactie; er hoeft niet eerst hergebruik van
een nonce tussen twee aparte versleutelingen aangetoond te worden.
Een geldig gecontroleerde MAC of authenticatietag zou deze wijziging detecteren.
Zie [Salsa20 en authenticatie](https://www.pycryptodome.org/src/cipher/salsa20).

## Klein voorbeeld

```python
oud = ord('1')
nieuw = ord('9')
cipherbyte = oud ^ 0x42
aangepast = cipherbyte ^ oud ^ nieuw
print(chr(aangepast ^ 0x42))
```

Verwacht: `9`. Voor JSON moet ook de rest van het bericht geldig blijven.

## Bij soortgelijke vragen

Pas bekende bytes op hun eigen posities aan en behoud de overige bytes.
Een langere nieuwe tekst past niet vanzelf in een bekende keystream.
Dezelfde XOR-eigenschap geldt voor andere streamconstructies, waaronder CTR;
de precieze nonce-opmaak en authenticatie verschillen per protocol.

## Als het niet werkt

- `zip` stopt bij de kortste invoer: controleer alle lengtes, anders verdwijnt
  een deel van de JSON. Getallen met vaste breedte helpen verschuivingen te voorkomen.
- Laat de 8 noncebytes buiten de XOR-berekening, maar stuur ze wel weer mee.
- De helper `encrypt_transaction` gebruikt de onbekende serverwaarde `KEY`;
  die functie hoef je voor deze wijziging niet aan te roepen.
- Het script print hex en verstuurt niets. Gebruik het formaat dat het lab vraagt.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Secure%20Bank-8).
