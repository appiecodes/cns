# Count the letters — substitutie met woordpatronen

Script: [Frequentie.py](Frequentie.py), met [wordlist.txt](wordlist.txt).
Start vanuit deze map: `python Frequentie.py`. Het pakket `wordfreq` is nodig.

## Vraag en herkenbaar patroon

Je krijgt een Engels versleuteld bericht, zichtbare woordgrenzen en een
woordenlijst. Herhaalde letters en woorden wijzen op een **vaste substitutie**.
De code zoekt vooral met woordpatronen en terugzoeken; ondanks de bestandsnaam
is het geen eenvoudige telling die alleen de meest voorkomende letter vervangt.

## Wat doet de code en wat pas ik aan?

Vervang `ciphertext`. Controleer de woordenlijst, de taal (`"en"`) en de
bekende prefixmapping. `q → c`, `n → n`, `b → s` is een aanname voor deze
challenge en mag niet blind worden overgenomen voor een ander bericht.

## Waarom werkt het?

Een vaste één-op-één-vervanging behoudt het patroon van herhaalde letters.
De code groepeert woorden op lengte en patroon. `test_mapping` weigert
tegenstrijdige vervangingen. Backtracking probeert kandidaten en keert terug
als een later woord onmogelijk wordt. Het kiest eerst het woord met de
minste geldige kandidaten om minder combinaties te hoeven onderzoeken.

## Klein voorbeeld

`paper` en `title` hebben allebei patroon `(0, 1, 0, 2, 3)`:
de eerste en derde letter zijn gelijk. Dat maakt ze patroon-kandidaten;
de vervangingen moeten daarnaast bij alle andere woorden passen.

## Bij soortgelijke vragen

- Behoud woordgrenzen en herhalingen als informatie; één korte ciphertext
  zonder structuur geeft veel meer mogelijke oplossingen.
- Pas taal en woordenlijst aan. Een correct antwoord kan ontbreken in de lijst.
- Een onbekende prefix betekent dat je de vaste prefixmapping moet verwijderen
  of opnieuw onderbouwen.
- Als één cipherletter op verschillende plekken verschillende gewone letters
  moet voorstellen, past dit vaste-substitutiemodel mogelijk niet.

## Als het niet werkt

`FileNotFoundError`: start in de map waar `wordlist.txt` staat.
`ModuleNotFoundError`: installeer `wordfreq` in je gebruikte Python-omgeving.
`No solution found`: controleer prefixmapping en taal; verlaag eventueel de
frequentiedrempel `2.5`, want die kan zeldzame maar juiste woorden uitsluiten.
Een eerste gevonden oplossing blijft een kandidaat: lees de hele zin na.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Count%20the%20letters-5).
