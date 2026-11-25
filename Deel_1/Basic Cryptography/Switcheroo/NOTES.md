# Switcheroo — gegeven vervangalfabet

Script: [custom.py](custom.py). Start in deze map met `python custom.py`.

## Vraag en herkenbaar patroon

De opdracht geeft een normaal alfabet, een versleuteld alfabet en ciphertext.
Dat wijst op **monoalfabetische substitutie**: een letter wordt steeds door
dezelfde andere letter vervangen. De twee alfabetten vormen samen de sleutel.

## Wat doet de code en wat pas ik aan?

Vul de ciphertext, `plain` en `cipher` in bij `decipher_custom(...)`.
Houd de volgorde van beide alfabetten exact zoals gegeven. Dezelfde positie
in de twee alfabetten hoort bij elkaar. Tekens buiten het cipher-alfabet
worden door het script behouden.

## Waarom werkt het?

Bij versleutelen ga je van de gewone letter naar de letter op dezelfde positie
in het cipher-alfabet. Ontsleutelen doet het omgekeerde: zoek de ontvangen
letter in `cipher`, en pak `plain[index]`.

## Klein voorbeeld

Met `plain = "ABC"` en `cipher = "QWE"` geldt:

```text
ABC → QWE     versleutelen
EWQ → CBA     ontsleutelen
```

## Bij soortgelijke vragen

- Een nieuw vervangalfabet betekent een nieuwe tabel; een vaste Caesar-shift
  hoeft daar niet bij te passen.
- Is de tabel onbekend, maar zijn woordgrenzen zichtbaar? Dan kunnen
  letterpatronen en woordkandidaten helpen; zie Count the letters.
- Werkt dezelfde vervanging niet op alle posities, onderzoek dan een
  wisselend alfabet of sleutelwoord, bijvoorbeeld Vigenère.

## Als het niet werkt

Controleer de richting van de tabel, hoofdletters en of beide alfabetten even
lang zijn. Voor een omkeerbare lettervervanging mag iedere letter maar één keer
voorkomen. Verkeerd overgenomen of dubbele letters maken de inverse onjuist.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Switcheroo-2).
