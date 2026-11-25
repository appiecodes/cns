# My First Enigma Machine — bewegende substituties

Script: [enigma_machine.py](enigma_machine.py).
Start met `python enigma_machine.py`.

## Vraag en herkenbaar patroon

De vraag beschrijft drie rotoren, hun alfabetten en startpositie `0,0,0`.
Rotor 1 draait vóór iedere letter, rotor 2 na een volledige omwenteling van
rotor 1 en rotor 3 na een volledige omwenteling van rotor 2. Dit is het
vereenvoudigde model uit de opgave; implementeer precies die regels.

## Wat doet de code en wat pas ik aan?

Vervang ciphertext, rotoralfabetten en eventuele startposities.
Een rotoralfabet moet alle 26 letters precies één keer bevatten.
De code laat alleen A–Z de rotoren verplaatsen; leestekens blijven staan.
Begin voor elk nieuw bericht opnieuw bij de afgesproken rotorstand.

## Waarom werkt het?

Een rotor is een vervangtabel die door de rotatie telkens verandert.
`mapping.index(char)` zoekt de inverse vervanging voor één rotor.
Met dezelfde beginstand en exact dezelfde rotatiestappen kun je de
lettervervangingen terugdraaien. De gegeven code levert voor dit bericht
een begrijpelijke volledige tekst op.

## Klein voorbeeld en belangrijke volgorde

Voor `mapping = "BCA"` versleutelt een tabel `A → B`; de inverse zoekt
`B` op positie 0 en vindt weer `A`.

Bij meerdere stappen draai je normaal **ook de volgorde om**.
Als een nieuwe variant versleutelt via rotor `1 → 2 → 3`, is de inverse:

```python
decoded_char = rotor3.decode(char)
decoded_char = rotor2.decode(decoded_char)
decoded_char = rotor1.decode(decoded_char)
```

Het huidige bestand gebruikt `1 → 2 → 3` bij het decoderen. Voor de gegeven
tekst geven beide volgordes hetzelfde resultaat; dat is geen garantie voor
andere rotoren of berichten. Gebruik voor een nieuwe variant de inverse van
de werkelijk gebruikte encryptievolgorde.

## Bij soortgelijke vragen

Controleer vier dingen: rotoralfabetten, startstanden, vóór/na de letter
draaien en wanneer de volgende rotor meedraait. Test met een eigen kort
bericht dat versleutelen en terugdraaien exact het origineel oplevert.

## Als het niet werkt

Een fout vanaf de eerste letter wijst vaak op een verkeerde startstand of
stapvolgorde. Een fout vanaf letter 26/27 kan bij het doorschakelen zitten.
Controleer of leestekens meetellen en reset gebruikte rotorobjecten; hun
toestand verandert tijdens het verwerken.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#My%20First%20Enigma%20Machine-4).
