
def decipher_vigenere(text, key):
    result = ""
    key_index = 0

    for char in text:
        if char.isalpha():
            offset = ord('A') if char.isupper() else ord('a')

            shift = ord(key[key_index % len(key)].lower()) - ord('a')

            decrypted_char = chr(
                (ord(char) - offset - shift) % 26 + offset
            )

            result += decrypted_char
            key_index += 1
        else:
            result += char

    return result


print(decipher_vigenere("eeg{kjgiflceha-sje-oxvksz-lzaa-ikqni}", "croissant"))