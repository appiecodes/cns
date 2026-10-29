from Crypto.Cipher import DES

ct = bytes.fromhex("74eb40cf03b84d0bc4cd2c6e0fe97fb4e70546d3e09c530d35b344e530351bac")

for i in range(100):
    key = f"IOTDEV{i:02d}".encode()
    cipher = DES.new(key, DES.MODE_ECB)
    pt = cipher.decrypt(ct)
    if pt.startswith(b"cns{"):
        print(pt)
        break