def decipher_caesar(text):
    results = []

    for shift in range(1, 26):
        result = ""
        for char in text:
            if char.isupper():
                result += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            elif char.islower():
                result += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                result += char
        results.append((shift, result))

    return results


list = decipher_caesar("fqv{iluvw-fkdoohqjh}")


for shift, result in list:
    print(f"Shift {shift}: {result}")




