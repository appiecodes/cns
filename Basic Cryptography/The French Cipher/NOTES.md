# The French Cipher — Vigenère

Script: [vigenere.py](vigenere.py). Start met `python vigenere.py`.

## Vraag en herkenbaar patroon

De opdracht geeft een bericht en een aanwijzing voor een Frans ontbijtproduct:
het sleutelwoord in de code is `croissant`. Een **herhalend sleutelwoord dat
verschillende letterverschuivingen bepaalt** past bij Vigenère.

## Wat doet de code en wat pas ik aan?

Vervang ciphertext en sleutel in `decipher_vigenere(...)`. Gebruik een sleutel
met letters A–Z. In deze uitvoering schuift de sleutel alleen door bij letters;
een streepje of accolade verbruikt geen sleutelletter.

## Waarom werkt het?

Elke sleutelletter wordt een verschuiving: A=0, B=1, enzovoort.
Ontsleutelen berekent `(cipherletter - sleutelletter) % 26`. Na de laatste
sleutelletter begint de sleutel opnieuw via `key_index % len(key)`.

## Klein voorbeeld

```text
Tekst:       ABC
Sleutel:     BBB
Ciphertext:  BCD
```

Iedere B in de sleutel betekent +1. Het script trekt bij ontsleutelen die 1 af.

## Bij soortgelijke vragen

- Gebruik een sleutelwoord uit de nieuwe hint; `croissant` is geen algemene sleutel.
- Een sleutel van één letter geeft één vaste verschuiving, zoals Caesar.
- Geen sleutel bekend? Onderzoek herhaling en mogelijke sleutelwoorden of
  sleutellengtes. Dit script doet zelf geen onderzoek naar een onbekende sleutel.
- Controleer of de nieuwe variant de sleutel ook bij spaties en leestekens
  laat doorschuiven. Zo ja, moet de indexering worden aangepast.

## Als het niet werkt

Controleer spelling van de sleutel, de beginpositie en de behandeling van
leestekens. Een lege sleutel geeft een fout. Cijfers, accenten of een ander
alfabet vragen een andere omzetting dan deze A–Z-versie.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#The%20French%20Cipher-3).
