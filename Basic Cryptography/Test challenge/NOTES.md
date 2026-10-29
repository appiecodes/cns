# Test challenge — Caesar

Script: [caesar.py](caesar.py). Start in deze map met `python caesar.py`.

## Vraag en herkenbaar patroon

De vraag noemt Caesar en geeft een versleuteld bericht. Denk aan een **vaste
verschuiving van het alfabet**. Elke letter krijgt dezelfde verschuiving;
woordlengtes en leestekens blijven herkenbaar.

## Wat doet de code en wat pas ik aan?

Vervang de tekst bij `decipher_caesar(...)`. De code probeert verschuivingen
1 tot en met 25 en print iedere kandidaat. Zoek een begrijpelijke tekst en
controleer de volledige inhoud, niet alleen een bekende flag-prefix.

## Waarom werkt het?

Letters worden nummers van 0 tot 25. Voor ontsleutelen trekt de code de
verschuiving af. `% 26` laat het alfabet rondlopen: vóór A kom je bij Z.
Hoofdletters en kleine letters worden apart behandeld; leestekens blijven staan.

## Klein voorbeeld

`HELLO` met verschuiving 3 wordt `KHOOR`. Bij ontsleutelen geeft kandidaat
3 dus `HELLO`. Ook `Z + 3` loopt rond naar `C`.

## Bij soortgelijke vragen

- Krijg je een andere ciphertext, vervang alleen de invoer en bekijk alle kandidaten.
- Geen sleutel gegeven is hier geen groot probleem: er zijn slechts 26 mogelijke
  verschuivingen, inclusief de identiteit. Het script slaat verschuiving 0 over.
- Werkt één vaste verschuiving nergens? Bekijk of er een vervangalfabet of
  een sleutelwoord is gegeven; zie Switcheroo en The French Cipher.

## Als het niet werkt

Controleer de kopie van de ciphertext, de richting van de verschuiving en het
alfabet. Deze code is bedoeld voor gewone A–Z/a–z-letters; een ander alfabet
vereist een aangepaste nummering. Spaties en accolades zijn geen bewijs van
welk cijfer gebruikt is, maar geven wel handige structuur.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Test%20challenge-1).
