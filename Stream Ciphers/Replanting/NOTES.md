# Replanting — voorspelbare keystream

Script: [cipher.py](cipher.py). Start met `python cipher.py`.

## Vraag en herkenbaar patroon

De vraag geeft een bekend statusbericht en een geheim bericht, versleuteld
met dezelfde streamcipherconfiguratie. De meegeleverde generator is een
**LCG met een seed**. Bekende plaintext kan zo helpen om de seed te testen.

## Wat doet de code en wat pas ik aan?

Vervang `known`, `ct` en `secret` door de bytes uit de nieuwe opgave.
Controleer ook `A`, `C`, `M`, de beginpositie en de manier waarop een
state een uitvoerbyte wordt. Hier is dat `(state >> 16) & 0xff`, nadat de
state met `next_state` is bijgewerkt.

Het script probeert seeds in `range(2**24)`. Dit is de gekozen zoekruimte
van de huidige code, geen algemene grens: `M = 2**31` laat meer states toe.
Een seed buiten de onderzochte reeks wordt niet gevonden.

## Waarom werkt het?

Voor XOR-versleuteling geldt `C = P XOR K`, dus `K = C XOR P`.
De eerste bekende byte levert een goedkope filter voor seeds. De code
controleert daarna het hele bekende bericht, want een match op één byte
alleen is veel te weinig. Met een juiste seed kan de generator ook latere
keystreambytes maken voor het langere geheime bericht.

## Klein voorbeeld

Ken je `P = 0x41` en `C = 0x51`, dan is de keystreambyte `0x10`.
Dat geeft één byte informatie. Het voorspelt pas volgende bytes als je
de gebruikte generator en de juiste state/seed hebt vastgesteld.

## Bij soortgelijke vragen

- Hergebruikte keystream plus bekende tekst: begin met XOR op dezelfde posities.
- Is de geheime tekst langer dan de bekende tekst? Alleen XOR levert slechts
  het overlappende deel; voor de rest heb je extra kennis nodig, hier de seed.
- Pas de zoekruimte aan op een onderbouwde beperking van de seed.
- Een veilige willekeurige generator met een grote geheime state is niet
  automatisch op dezelfde manier doorzoekbaar als deze kleine LCG-zoekruimte.

## Als het niet werkt

Controleer exacte bekende tekst, newlines, hex versus tekst en de streampositie.
Geen seed gevonden kan ook een te kleine zoekruimte betekenen.
Controleer vóór gebruik van de gevonden seed altijd meerdere bekende bytes.
De code is offline: hij leest de aangeleverde waarden en verbindt niet met een server.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Replanting-7) en [cipher.py](cipher.py).
