# CNS Hacking Session — START HERE

Everything for topics 5–7 (RSA, ElGamal, signatures, key distribution).
Two docs to read, one template to copy, a library to pull from.

## How to use it (the whole workflow)

1. **Per challenge: duplicate the `_TEMPLATE_challenge/` folder** and rename it
   (e.g. `01_group_chat`). It already contains `cns_toolkit.py` + `autosolve.py`.
2. **Drop the challenge's files into that copy.**
3. **Run the first move:**
   ```
   cd <your copy>
   python3 autosolve.py *
   ```
4. Flag? Submit it. Nothing? Open **`SCENARIOS.md`** and work down it. It may tell
   you to grab a specific script from `library/` — copy that script into your
   challenge folder (next to `cns_toolkit.py`) and run it.

**The one rule:** whatever script you run, `cns_toolkit.py` must sit in the same
folder. The template already has it; for a library script, copy it in too.

## Navigation map

```
START_HERE.md              <- you are here
SCENARIOS.md               <- what to do / what to run, step by step (keep open)

_TEMPLATE_challenge/        <- DUPLICATE this per challenge
    cns_toolkit.py             the library (needed by everything)
    autosolve.py               your main tool — always run first

library/                   <- pull extra scripts from here when SCENARIOS says so
    cns_toolkit.py             master copy
    autosolve.py               master copy
    file_attacks/
        group_chat.py          RSA Håstad broadcast (worked example)
        elgamal_solve.py       ElGamal reused nonce (same c1)
        fresh_solve.py         ElGamal stepped nonce
        dsa_solve.py           DSA reused nonce (same r) — rewrite part 2B
        extra_rsa.py           import for Franklin-Reiter, batch-GCD, prime-power
    server_attacks/        (each has an EDIT CHECKLIST at the top)
        server_directory.py        key directory: register / overwrite a key
        server_decrypt_oracle.py   server decrypts all but the target
        server_sign_oracle.py      server signs all but your message
        server_parity_oracle.py    server leaks one bit per query
        server_dh_mitm.py          unauthenticated Diffie-Hellman
        server_socket.py           raw `nc host port` server (not http)
        phonebook_solve.py         the worked Phone Book example
```

## What's automatic vs. what you edit

- `autosolve.py`: run as-is, never edit. (Rename odd fields in the *data* file only.)
- `file_attacks/*`: maybe change the key names at the top; `dsa_solve.py` needs its
  part 2B rewritten to match how the flag was encrypted (the file guides you).
- `server_attacks/*`: fill the EDIT CHECKLIST at the top (URL, numbers, endpoint,
  field names). The attack math never changes.


## Libraries — nothing to install
Every script uses only Python's **standard library**, which Ubuntu's `python3` already
has. You do **not** `pip install` anything. AES (one DSA sub-case) uses the included
`aes_pure.py`, also pure standard library. So: zero installs, works offline.

## First 5 minutes on the lab PC (do this before challenges open)

1. Open a terminal. Run `python3 --version`. If `python3` isn't found, try `python`.
   Use whichever works in every command below.
2. `cd` into a copied template folder and run `python3 autosolve.py` with no args —
   it should print its help text. That proves Python + the toolkit work here.
3. Check you can actually reach your files (USB/OneDrive) and the challenge server
   (you're on the lab network, so it should be fine).

## If a script errors, read the LAST line — it tells you what's wrong

| Error ends with... | Meaning | Fix |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'cns_toolkit'` | the library isn't in this folder | copy `cns_toolkit.py` into the folder |
| `KeyError: 'n'` (or any name) | the file uses a different field name | rename that field in the data file, or edit the key in the script |
| `No module named 'Crypto'` | a script tried pycryptodome | not needed — use `aes_pure.py` (included) instead |
| `ConnectionRefused` / timeout | can't reach the server | check the port, and that you're on the lab/VPN network |
| `ValueError: invalid literal for int()` | a hand-written script got a hex/base64 value (autosolve handles these itself) | wrap it: `int(x,16)` for hex, or use the toolkit's `b64d` |
| prints a flag but CTFd rejects it | copy/typo | copy-paste the WHOLE `cns{...}`, no spaces |

If autosolve seems to hang, it's factoring — give it up to a minute before stopping it.


## Also keep (export to PDF — no internet in the session)
- Study guide (theory), Cheat sheet (formulas + full catalog), Run-sheet (the procedure).

## Mindset
You never break the math. Every challenge has one planted mistake — spot it, grab
the matching tool, plug in the numbers. Recognition + small edits, under a clock.
