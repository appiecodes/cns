
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ciphertext = "HKV{BSBU-B-SJYZNNB-DNFW-IXH-YTA-RPL-RTXOLWFQ}"

class rotor:
    def __init__(self, mapping):
        self.mapping = mapping
        self.position = 0

    def decode(self, char):
        index = self.mapping.index(char)
        return alphabet[index]

    def rotate(self):
        self.position = (self.position + 1) % 26
        self.mapping = self.mapping[1:] + self.mapping[0]

    def begin(self):
        return self.position == 0


rotor1 = rotor("MACHINEBDFGJKLOPQRSTUVWXYZ")
rotor2 = rotor("ORBITACDEFGHJKLMNPQSUVWXYZ")
rotor3 = rotor("CIPHERABDFGJKLMNOQSTUVWXYZ")

result = ""

for char in ciphertext:
    if char in alphabet:
        rotor1.rotate()

        if rotor1.begin():
            rotor2.rotate()

            if rotor2.begin():
                rotor3.rotate()

        decoded_char = rotor3.decode(char)
        decoded_char = rotor2.decode(decoded_char)
        decoded_char = rotor1.decode(decoded_char)

        result += decoded_char
    else:
        result += char

print(result)
