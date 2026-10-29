import pathlib
import hashlib
import datetime

c1 = "fb0da430977c40d3399cbe0a032a55df9939c6ec19ea259536398193753228e9"

c2 = "d1d3ebe4de479c3eff908cdb008fb09cd8d04046a5717dce1ecef4209cba7b58"

c3 = "c3ec154541c1305d787d08e372b56e727dbadd44fb7e47c672b592eb5d4e6f78"



hash = hashlib.sha256(bytes.fromhex("ebde11dcf3accb43be1d4ec999fd5097c59cac379a34f0ebad7651035f7987c9")).hexdigest()

print(hash)