# Security Cam — kandidaten tegen een digest testen

Script: [security_camera.py](security_camera.py). Start met `python security_camera.py`.
De capture en de lokale `rockyou.txt` komen uit de challengebijlagen;
deze grote woordenlijst staat niet in Git.

## Vraag en herkenbaar patroon

De opdracht geeft onderschept cameraverkeer en vraagt het wachtwoord te
vinden. Het patroon is **offline kandidaten controleren**: een digest
wordt opgebouwd uit bekende protocolvelden en een onbekend wachtwoord.

## Code gebruiken en aanpassen

Open `security-cam.pcapng` in Wireshark. Bij de afwijkende poort kan
Analyze → Decode As → RTSP nodig zijn. Zie [Wireshark Decode As](https://www.wireshark.org/docs/wsug_html_chunked/ChCustProtocolDissectionSection.html).

Neem uit één samenhorende uitwisseling over: gebruikersnaam, realm, nonce,
methode, URI en response-digest. Hier is de methode `DESCRIBE`, geen `GET`.
Zet `rockyou.txt` naast het script.

**Let op:** de `if` vergelijkt met een letterlijk opgeschreven digest.
Alleen `response` bovenaan aanpassen is niet genoeg; die variabele wordt
in de lus overschreven. Pas de doelwaarde in de vergelijking aan.

## Waarom werkt het?

Voor de gebruikte MD5-variant zonder `qop` geldt:

```text
HA1 = MD5(username + ":" + realm + ":" + kandidaat)
HA2 = MD5(method + ":" + uri)
response = MD5(HA1 + ":" + nonce + ":" + HA2)
```

HA1 en HA2 worden als hextekst ingevoegd. Iedere kandidaat levert een
controleerbare response op; je draait dus niet rechtstreeks MD5 terug.
Zie [de legacy digestformule in RFC 2617](https://www.rfc-editor.org/rfc/rfc2617.html#section-3.2.2.1).

## Klein voorbeeld

```python
import hashlib

def md5(tekst):
    return hashlib.md5(tekst.encode()).hexdigest()

ha1 = md5("user:demo:guess")
ha2 = md5("DESCRIBE:rtsp://example/video")
response = md5(f"{ha1}:nonce:{ha2}")
print(len(response))
```

Verwacht: `32`. Een echte match vereist gelijkheid van de volledige waarde.

## Bij soortgelijke vragen

Controleer het algoritme en de velden `qop`, `cnonce` en `nc`.
Bij `qop=auth`, `MD5-sess` of SHA-256 volstaat deze exacte formule niet.
Gebruik gegevens uit dezelfde uitwisseling; een nieuwe verbinding kan een
nieuwe nonce geven. Test alleen kandidaten die in de gebruikte lijst staan.

## Als het niet werkt

Controleer exact gespelde methode en URI, de doelresponse en de woordenlijst.
De huidige code laadt de hele lijst in het geheugen; bij geheugenproblemen
kun je regel voor regel lezen. Bij andere wachtwoorden kan `.strip()`
betekenisvolle spaties weghalen; alleen regeleindes verwijderen bewaart ze.
Gebruik een gevonden kandidaat daarna volgens de labinstructies om de
camerastream te bekijken. Een digestmatch toont op zichzelf geen videobeeld.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Security%20Cam-16).
