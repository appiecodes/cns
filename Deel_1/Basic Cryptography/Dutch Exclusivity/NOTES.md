# Dutch Exclusivity — XOR met herhalende sleutel

Script: [exclusivity.py](exclusivity.py). Start met `python exclusivity.py`.

## Vraag en herkenbaar patroon

De opdracht geeft ciphertext en een sleutel in hex. De code behandelt dit als
**XOR met een herhalende sleutel**. De naam van de opdracht is een extra hint
naar exclusive-or; controleer de constructie bij een andere vraag altijd apart.

## Wat doet de code en wat pas ik aan?

Vervang de hexwaarden van `ciphertext` en `key`. `bytes.fromhex(...)` maakt
er bytes van. `key[i % len(key)]` herhaalt de sleutel wanneer de tekst langer
is dan de sleutel. De laatste stap leest in deze challenge nog een laag hextekst.

## Waarom werkt het?

XOR met dezelfde waarde maakt zichzelf ongedaan:
`(P XOR K) XOR K = P`. Daarom zijn versleutelen en ontsleutelen hier dezelfde
bewerking. De sleutel hoeft niet even lang te zijn als het bericht, zolang je
precies dezelfde herhaling en beginpositie gebruikt.

## Klein voorbeeld

```python
cipher = 0x41 ^ 0x10
plain = cipher ^ 0x10
print(hex(cipher), chr(plain))
```

Verwacht: `0x51 A`.

## Bij soortgelijke vragen

- XOR werkt op bytes. Een hexweergave eerst omzetten is iets anders dan de
  zichtbare hexletters zelf XOR-en.
- Controleer na iedere laag het resultaat. Is het leesbare tekst, dan kan je
  klaar zijn. Is het geldige hextekst, dan kan nog `bytes.fromhex(...)` volgen.
- Bij een verschoven sleutel moet ook de indexering meeschuiven.
- Geen sleutel gegeven? De huidige code lost dat niet vanzelf op; zoek naar
  bekende plaintext of een beperkte verzameling sleutels.

## Als het niet werkt

Controleer hexformaat, sleutellengte en positie. Een lege sleutel werkt niet.
`UnicodeDecodeError` betekent niet automatisch dat XOR fout is: de uitkomst
kan binair zijn. Bekijk eerst `.hex()`. Voer de laatste hexdecode alleen uit
als de tussenuitkomst werkelijk hextekst is.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Dutch%20Exclusivity-6).
