# AES 2 demo version — meet-in-the-middle

Script: [AES2.py](AES2.py). Vereist `pycryptodome` en de afbeelding `enc.bmp`
uit de opdracht. Het script bevat momenteel een Windows-pad naar `enc(1).bmp`;
dat bestand staat niet in de repo en het pad moet naar jouw lokale bestand wijzen.

## Vraag en herkenbaar patroon

De opdracht gebruikt twee achtereenvolgende AES-versleutelingen met ieder
slechts 20 onbekende sleutelbits. De sleutelopmaak staat erbij: 3 bytes voor
het getal, gevolgd door 13 nulbytes. Denk aan **meet-in-the-middle** als je
een passend plaintext/ciphertext-blok onder diezelfde sleutels kent.

## Wat doet de code en wat pas ik aan?

Vul het bestandspad, `original_guess`, het bijbehorende ciphertext-blok en
`promo` in. `make_key` moet exact de opgegeven sleutelopmaak volgen.
Het script neemt ECB aan en gebruikt 16-byteblokken.

De huidige gok komt uit een verwacht patroon van afbeeldingspixels.
`image[54:70]` is slechts correct als dat de juiste 16 ciphertextbytes bij
deze plaintextgok zijn. De pixeldata van een BMP begint niet altijd bij 54;
de offset staat normaal in bytes 10–13 van de BMP-header.

## Waarom werkt het?

Bij `C = E_K2(E_K1(P))` moet in het midden gelden:

```text
E_K1(P) = D_K2(C)
```

De code bewaart links alle middenwaarden voor kandidaat K1 en zoekt daarna
rechts met kandidaat K2 een match. Ongeveer twee keer `2**20` berekeningen
en een grote tabel vervangen hier het proberen van `2**40` sleutelparen.
Een match controleer je met meer data of een overtuigend correct eindbericht.
AES heeft blokken van 16 bytes; zie [AES-documentatie](https://www.pycryptodome.org/src/cipher/aes).

## Klein voorbeeld

Stel dat iedere sleutel maar 8 kandidaten heeft. Alle paren proberen geeft
64 combinaties. De middentabel heeft 8 invoeren en je probeert 8 kandidaten
van de andere kant. Dat is het idee van twee zoeklussen met een tabel.
De werkelijke opgave heeft veel grotere, maar nog beperkte reeksen.

## Bij soortgelijke vragen

- Controleer eerst of het echt twee opeenvolgende encrypties zijn, met de
  betreffende sleutels opnieuw gebruikt voor je bekende blok en doelbericht.
- Zoek een exact bekend blok: bestandsstructuur, vast bericht of bekende pixels.
- Pas sleutelbereik, bytevolgorde, nulbytes en mode aan op de nieuwe constructie.
- Een bestandstype alleen geeft niet automatisch het volledige juiste blok.
  Verkeerde plaintextgokken leveren geen bruikbare middenmatch op.

## Als het niet werkt

- `FileNotFoundError`: zet de opdrachtbijlage lokaal en verbeter het pad.
- Geen match: controleer plaintextgok, blokoffset en sleutelopmaak voordat je
  dezelfde dure berekening opnieuw uitvoert.
- Veel geheugen: de tabel heeft circa een miljoen invoeren, met Python-overhead.
- Onleesbare uitvoer: controleer beide sleutels en de tweede decryptiestap.
  Verwijder padding alleen volgens de daadwerkelijk gebruikte paddingmethode.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#AES%202%20demo%20version-12).
