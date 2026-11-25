import json
import hashlib
import datetime


object = {"reference": "128", "from_account": "SIM-alice", "to_account": "SIM-bob", "amount": 10, "currency": "EUR", "timestamp": "2026-10-26T11:15:18.386684+00:00"}

def canonicalize(payment):
    return json.dumps(
        payment,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode("utf-8")


seen = {}
base = {"from_account":"SIM-alice","to_account":"SIM-bob","amount":10,
        "currency":"EUR"}
base["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()

for i in range(2**32):
    base["reference"] = str(i)
    m = hashlib.sha256(canonicalize(base)).hexdigest()[:8]
    if m in seen:
        print(canonicalize(base))
        print('\n')
        base["reference"] = str(seen[m])
        print(canonicalize(base))

        break
    seen[m] = i