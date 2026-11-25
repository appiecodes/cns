# Key standardisation — een kleine sleutelruimte

Script: [key_standardisation.py](key_standardisation.py).
Start met `python key_standardisation.py`. Vereist `pycryptodome`.

## Vraag en herkenbaar patroon

De opdracht noemt DES en geeft de namespace `IOTDEV`. Denk aan een sleutel
met een **voorspelbaar vast deel en weinig onbekende tekens**.
Een bekende sleutelindeling kan de zoekruimte veel kleiner maken dan de
nominale grootte van de gebruikte versleuteling.

## Wat doet de code en wat pas ik aan?

Vervang `ct`, de namespace en het kandidaatbereik als de opgave verandert.
De code test `IOTDEV00` tot en met `IOTDEV99`, gebruikt DES-ECB en zoekt een
uitkomst die met `cns{` begint. Twee decimale cijfers zijn hier de aanname
van het script; de vraag noemt niet letterlijk dat iedere suffix uit cijfers bestaat.

## Waarom werkt het?

DES neemt een sleutel van 8 bytes aan. `IOTDEV` gebruikt er al 6; met de
aangenomen twee cijfers zijn er slechts 100 kandidaten. Iedere kandidaat
kan lokaal worden geprobeerd. De leesbare verwachte structuur helpt de
juiste kandidaat te herkennen. Zie [DES-documentatie](https://www.pycryptodome.org/src/cipher/des).

## Klein voorbeeld

```python
key = f"IOTDEV{7:02d}".encode()
print(key, len(key))
```

Verwacht: `b'IOTDEV07' 8`. De voorloopnul is onderdeel van de sleutel.

## Bij soortgelijke vragen

- Vraag hoeveel tekens werkelijk onbekend zijn en welke waarden ze mogen hebben.
- Bij twee letters in plaats van twee cijfers heb je een andere kandidatenlijst.
- Controleer algoritme, mode en eventuele IV apart. De huidige code probeert ECB;
  een CBC-opgave vraagt ook de juiste IV en bijbehorende decryptie.
- Een passende prefix is een aanwijzing. Controleer het hele bericht of een
  tweede gegeven voordat je een kandidaat definitief accepteert.

## Als het niet werkt

Controleer sleutelbytes, voorloopnullen, hoofdletters en de juiste mode.
Bij DES-ECB moet de ciphertextlengte een veelvoud van 8 bytes zijn.
Een verkeerde sleutelindeling kun je niet oplossen door alleen langer over
dezelfde 100 kandidaten te blijven zoeken.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Key%20standardisation-9).
