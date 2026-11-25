"""
Plain : ABCDEFGHIJKLMNOPQRSTUVWXYZ
Cipher: QWERTYUIOPASDFGHJKLZXCVBNM
Ciphertext: EFL{STZZTK-LGXH}
"""

def decipher_custom(text, plain, cipher):
    result = ""

    for char in text:
        if char in cipher:
            index = cipher.index(char)
            result += plain[index]
        else:
            result += char

    return result


print(decipher_custom("EFL{STZZTK-LGXH}", "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "QWERTYUIOPASDFGHJKLZXCVBNM"))

