# CNS-oefeningen

De categorieën en challengenamen volgen de
[challengepagina](https://cns-test.idlab.uantwerpen.be/challenges).
Elke challenge heeft een eigen map met de bijbehorende code en invoerbestanden.

| Categorie | Challenge op de website | Bestanden |
| --- | --- | --- |
| Basic Cryptography | Test challenge | [caesar.py](Basic%20Cryptography/Test%20challenge/caesar.py) |
| Basic Cryptography | Switcheroo | [custom.py](Basic%20Cryptography/Switcheroo/custom.py) |
| Basic Cryptography | The French Cipher | [vigenere.py](Basic%20Cryptography/The%20French%20Cipher/vigenere.py) |
| Basic Cryptography | Count the letters | [Frequentie.py](Basic%20Cryptography/Count%20the%20letters/Frequentie.py), [wordlist.txt](Basic%20Cryptography/Count%20the%20letters/wordlist.txt) |
| Basic Cryptography | Dutch Exclusivity | [exclusivity.py](Basic%20Cryptography/Dutch%20Exclusivity/exclusivity.py) |
| Basic Cryptography | My First Enigma Machine | [enigma_machine.py](Basic%20Cryptography/My%20First%20Enigma%20Machine/enigma_machine.py) |
| Stream Ciphers | Replanting | [cipher.py](Stream%20Ciphers/Replanting/cipher.py) |
| Stream Ciphers | Secure Bank | [secure_bank.py](Stream%20Ciphers/Secure%20Bank/secure_bank.py), [salsa20.py](Stream%20Ciphers/Secure%20Bank/salsa20.py) |
| Block Ciphers | Key standardisation | [key_standardisation.py](Block%20Ciphers/Key%20standardisation/key_standardisation.py) |
| Block Ciphers | Noncense | [challenge.py](Block%20Ciphers/Noncense/challenge.py) en [invoerbestanden](Block%20Ciphers/Noncense/) |
| Block Ciphers | AES 2 demo version | [AES2.py](Block%20Ciphers/AES%202%20demo%20version/AES2.py) |
| Hashing | Secure Bank 2 | [secure_bank_2.py](Hashing/Secure%20Bank%202/secure_bank_2.py) |
| Hashing | Better Hash | [better_hashing.py](Hashing/Better%20Hash/better_hashing.py) |
| Hashing | Space Race 1 | [mars.py](Hashing/Space%20Race%201/mars.py) |
| Hashing | Security Cam | [security_camera.py](Hashing/Security%20Cam/security_camera.py), [notities](Hashing/Security%20Cam/security_camera.txt) |
| HMAC | Signed, Sealed, Misinterpreted | [curl-aanpak en uitleg](HMAC/Signed%2C%20Sealed%2C%20Misinterpreted/NOTES.md) |
| HMAC | Token of Trust | [jwt.py](HMAC/Token%20of%20Trust/jwt.py) |

Start een script vanuit de map van die challenge. Bijvoorbeeld vanuit de map
met deze README:

```bash
cd "Hashing/Space Race 1"
python mars.py
```

Security Cam gebruikt de lokale `rockyou.txt` naast het script; die woordlijst
staat niet in Git. Voor AES 2 demo version is `enc(1).bmp` nodig; pas het pad
naar die afbeelding in `AES2.py` aan.

Bij Space Race 1 staan ook de [eerste SHA-notities](Hashing/Space%20Race%201/NOTES.md).
