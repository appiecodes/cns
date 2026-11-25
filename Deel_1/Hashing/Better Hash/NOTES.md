# Better Hash — omkeerbare bewerkingen terugdraaien

Script: [better_hashing.py](better_hashing.py). Start met `python better_hashing.py`.

## Vraag en herkenbaar patroon

Je krijgt de volledige eigen hashfunctie en een uitkomst. De functie
bestaat uit XOR, bitrotaties en het verplaatsen van bytes. Onderzoek
**of de bewerkingen omkeerbaar zijn en of er informatie verloren gaat**.
De naam “hash” alleen zegt niet dat de functie een veilige hashfunctie is.

## Code gebruiken en aanpassen

Vervang `HASH` door de gegeven hexwaarde. De bovenste functies beschrijven
de voorwaartse constructie; `reverse_better_hash` draait haar terug.
Rondeaantal, rotatieformule en maskers moeten bij de nieuwe constructie passen.

## Waarom werkt het?

XOR met hetzelfde masker maakt zichzelf ongedaan. Links roteren is
omkeerbaar met rechts roteren; ook cyclisch verplaatsen van bytes is omkeerbaar.
Per ronde draait de code daarom eerst de byteverplaatsing terug, daarna de
XOR tussen buurbytes van rechts naar links, daarna de bitrotatie en het masker.
De rondes lopen daarbij van 7 terug naar 0.

Rechts naar links is nodig om bij de buur-XOR nog de juiste tussenwaarden
beschikbaar te houden. Zowel de stappen als de rondes moeten worden omgekeerd.

## Klein voorbeeld

```python
x, masker = 65, 23
print((x ^ masker) ^ masker)
```

Verwacht: `65`. Met de gegeven functies geldt ook:
`rol(129, 1) == 3` en `reverse_rol(3, 1) == 129`.

## Bij soortgelijke vragen

Schrijf de stappen uit en zoek van elke stap de inverse. Test de hele route
met een eigen bericht: `reverse_better_hash(better_hash("test"))` hoort
`"test"` te geven. Dat controleert meer dan alleen een leesbare uitkomst.

Gooit een nieuwe constructie bytes weg of kort zij de uitkomst in, dan is
deze directe inverse mogelijk niet beschikbaar. Dit is geen algemene
manier om SHA-256 terug te rekenen.

## Als het niet werkt

Controleer `& 0xff`, rotatieafstanden, rondevolgorde en de volgorde van de
inverse stappen. Bij een decodeerfout kunnen de herstelde bytes ook geen
UTF-8 voorstellen; bekijk dan eerst hun hexweergave.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Better%20Hash-14) en [de code](better_hashing.py).
