# Noncense — hergebruikte AES-CTR-keystream

Script: [challenge.py](challenge.py), met de drie invoerbestanden in deze map.
Start met `python challenge.py`. Vereist `pycryptodome`.

## Vraag en herkenbaar patroon

De opdracht hint naar onzorgvuldig noncegebruik en geeft een bekende tekst
met ciphertext en een tweede ciphertext. De code gebruikt AES-CTR.
Het relevante patroon is **dezelfde sleutel, nonce, counterstart en streampositie**.

## Wat doet de code en wat pas ik aan?

Vervang `message`, `cipher` en `cipher_flag` door de nieuwe gegevens.
Neem de bekende tekst byte voor byte over. De losse bestanden kunnen helpen
om kopieerfouten in de hardcoded waarden te ontdekken.

## Waarom werkt het?

CTR maakt een keystream en XOR-t die met de plaintext:

```text
K = C_bekend XOR P_bekend
P_geheim = C_geheim XOR K
```

Dit werkt voor de posities waar dezelfde keystream is gebruikt. AES zelf
wordt niet teruggedraaid of van zijn sleutel ontdaan; de bekende bytes
verraden hier de gebruikte keystreambytes.
Zie [CTR-mode](https://www.pycryptodome.org/src/cipher/classic#ctr-mode).

## Klein voorbeeld

```python
k = 0x51 ^ ord('A')
geheim_cipher = ord('B') ^ k
print(chr(geheim_cipher ^ k))
```

Verwacht: `B`. Zonder bekende plaintext weet je uit twee ciphertexts alleen
hun XOR, niet automatisch beide oorspronkelijke teksten.

## Bij soortgelijke vragen

- Controleer nonce, sleutel én counterpositie; alleen dezelfde nonce is niet genoeg.
- Bij een andere startpositie moet je de juiste overlappende bytes uitlijnen.
- Je herstelt maximaal het deel waarvoor keystreambytes bekend zijn.
  Voor het volledige tweede bericht moet de bekende keystream lang genoeg zijn.
- Een gecontroleerde authenticatietag kan wijzigingen afwijzen, maar maakt
  al gelekte plaintext door keystreamhergebruik niet ongedaan.

## Als het niet werkt

Bekijk `len(message.encode())`, `len(cipher)` en `len(cipher_flag)`.
`zip` kapt stil af bij de kortste invoer. Controleer newlines, encoding en
of de ciphertextbestanden alleen hex bevatten. CTR heeft geen blockpadding
nodig; willekeurig padding toevoegen verschuift je gegevens.

Bron: [challengevraag](https://cns-test.idlab.uantwerpen.be/challenges#Noncense-10).
