# CNS-oefeningen en notities

Begin met het herkenbare patroon en lees daarna de notitie van die challenge.
Daarin staan de vraag, de werking van je code, aanpassingen voor soortgelijke
opgaven, een klein voorbeeld en controles als het niet werkt.

De indeling volgt de [challengepagina](https://cns-test.idlab.uantwerpen.be/challenges).
De notities maken onderscheid tussen uitgewerkte code, losse fragmenten en
helpers. Vooral `mars.py` is nog geen volledige oplossing van het relayprotocol.

| Categorie | Challenge | Patroon herkennen | Code en notities |
| --- | --- | --- | --- |
| Basic Cryptography | Test challenge | Caesar: vaste letterverschuiving | [NOTES.md](Basic%20Cryptography/Test%20challenge/NOTES.md), [caesar.py](Basic%20Cryptography/Test%20challenge/caesar.py) |
| Basic Cryptography | Switcheroo | Gegeven vervangalfabet | [NOTES.md](Basic%20Cryptography/Switcheroo/NOTES.md), [custom.py](Basic%20Cryptography/Switcheroo/custom.py) |
| Basic Cryptography | The French Cipher | Vigenère: herhalend sleutelwoord | [NOTES.md](Basic%20Cryptography/The%20French%20Cipher/NOTES.md), [vigenere.py](Basic%20Cryptography/The%20French%20Cipher/vigenere.py) |
| Basic Cryptography | Count the letters | Substitutie: woordpatronen en woordenlijst | [NOTES.md](Basic%20Cryptography/Count%20the%20letters/NOTES.md), [Frequentie.py](Basic%20Cryptography/Count%20the%20letters/Frequentie.py) |
| Basic Cryptography | Dutch Exclusivity | XOR met herhalende sleutel; mogelijke extra hexlaag | [NOTES.md](Basic%20Cryptography/Dutch%20Exclusivity/NOTES.md), [exclusivity.py](Basic%20Cryptography/Dutch%20Exclusivity/exclusivity.py) |
| Basic Cryptography | My First Enigma Machine | Rotortabellen en veranderende toestand | [NOTES.md](Basic%20Cryptography/My%20First%20Enigma%20Machine/NOTES.md), [enigma_machine.py](Basic%20Cryptography/My%20First%20Enigma%20Machine/enigma_machine.py) |
| Stream Ciphers | Replanting | Bekende plaintext plus voorspelbare LCG/seed | [NOTES.md](Stream%20Ciphers/Replanting/NOTES.md), [cipher.py](Stream%20Ciphers/Replanting/cipher.py) |
| Stream Ciphers | Secure Bank | Ciphertext wijzigen zonder authenticatiecontrole | [NOTES.md](Stream%20Ciphers/Secure%20Bank/NOTES.md), [salsa20.py](Stream%20Ciphers/Secure%20Bank/salsa20.py), [secure_bank.py](Stream%20Ciphers/Secure%20Bank/secure_bank.py) |
| Block Ciphers | Key standardisation | Voorspelbaar sleutelformaat; weinig kandidaten | [NOTES.md](Block%20Ciphers/Key%20standardisation/NOTES.md), [key_standardisation.py](Block%20Ciphers/Key%20standardisation/key_standardisation.py) |
| Block Ciphers | Noncense | Hergebruik van CTR-keystream | [NOTES.md](Block%20Ciphers/Noncense/NOTES.md), [challenge.py](Block%20Ciphers/Noncense/challenge.py) |
| Block Ciphers | AES 2 demo version | Dubbele encryptie met kleine sleutels; meet-in-the-middle | [NOTES.md](Block%20Ciphers/AES%202%20demo%20version/NOTES.md), [AES2.py](Block%20Ciphers/AES%202%20demo%20version/AES2.py) |
| Hashing | Secure Bank 2 | Botsing in ingekorte fingerprint | [NOTES.md](Hashing/Secure%20Bank%202/NOTES.md), [secure_bank_2.py](Hashing/Secure%20Bank%202/secure_bank_2.py) |
| Hashing | Better Hash | Omkeerbare bewerkingen terugdraaien | [NOTES.md](Hashing/Better%20Hash/NOTES.md), [better_hashing.py](Hashing/Better%20Hash/better_hashing.py) |
| Hashing | Space Race 1 | Protocol onderzoeken; bestaande code is SHA-helper | [NOTES.md](Hashing/Space%20Race%201/NOTES.md), [mars.py](Hashing/Space%20Race%201/mars.py) |
| Hashing | Security Cam | Offline kandidaten vergelijken met digest uit capture | [NOTES.md](Hashing/Security%20Cam/NOTES.md), [security_camera.py](Hashing/Security%20Cam/security_camera.py) |
| HMAC | Signed, Sealed, Misinterpreted | Dubbele JSON-velden; verschil in interpretatie | [NOTES.md](HMAC/Signed%2C%20Sealed%2C%20Misinterpreted/NOTES.md) |
| HMAC | Token of Trust | JWT-claims en onjuist geaccepteerd alg: none | [NOTES.md](HMAC/Token%20of%20Trust/NOTES.md), [jwt.py](HMAC/Token%20of%20Trust/jwt.py) |

## Uitvoeren

Start vanuit de map van de challenge, zodat invoerbestanden gevonden worden.
Bijvoorbeeld vanuit de map met deze README:

```bash
cd "Hashing/Space Race 1"
python mars.py
```

Werkt `python` niet, probeer dan `python3`. Gebruik bij ontbrekende modules
hetzelfde Python-programma waarmee je het script draait. De bestaande scripts
gebruiken deze externe pakketten:

```bash
python -m pip install pycryptodome wordfreq werkzeug
```

De overige gebruikte modules, zoals `hashlib` en `json`, zitten in Python.
Security Cam vereist de lokale `rockyou.txt` naast het script. AES 2 vereist
`enc.bmp` uit de opdracht; het bestandspad in `AES2.py` moet naar jouw lokale
bestand wijzen. Zie de betreffende notities voor deze voorwaarden.

Bij nieuwe opgaven: controleer eerst of de aannames van de techniek kloppen.
Een bekend patroon is een startpunt, geen garantie dat dezelfde invoer of
payload opnieuw werkt.
