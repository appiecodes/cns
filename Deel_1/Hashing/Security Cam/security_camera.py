import hashlib
import pathlib


def get_list(path):
    path = pathlib.Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Path {path} does not exist.")
    if not path.is_file():
        raise NotADirectoryError(f"Path {path} is not a file.")

    list = []
    with open(path, "r", encoding="utf-8", errors="ignore") as file:
        for line in file:
            list.append(line.strip())
    return list



WORDLIST_PATH = pathlib.Path(__file__).resolve().with_name("rockyou.txt")
list = get_list(WORDLIST_PATH)


usernaem = "user"
realm = "PythonRTSP"
nonce = "4874a055c3f4390506d99e6c51a9e3e360cbef8a62abd7079e11faddcb70a38c"
methode = "DESCRIBE"
uri = "rtsp://cns-test.idlab.uantwerpen.be:50002/video"
response="083ae471a613399abb781f9e3"

HA2 = hashlib.md5(f"{methode}:{uri}".encode()).hexdigest()

for item in list:
    HA1 = hashlib.md5(f"{usernaem}:{realm}:{item}".encode()).hexdigest()
    response = hashlib.md5(f"{HA1}:{nonce}:{HA2}".encode()).hexdigest()
    if response == "b3539154c5b784bba2c47a1a6c7c4ab0":
        print(f"Password found: {item}")
        break

# After running the code, the password found is:
password = "camera123456789"
