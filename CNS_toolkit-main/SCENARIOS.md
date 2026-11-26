# SCENARIOS — what to do, step by step

> **Setup:** duplicate `_TEMPLATE_challenge/`, rename it, drop the challenge files in.
> It already has `cns_toolkit.py` + `autosolve.py`. When a step names another script
> (e.g. `dsa_solve.py`, `server_directory.py`), copy it from `library/...` into this
> same folder, then run. `cns_toolkit.py` must always be in the folder you run from.


## HOW TO RUN EACH SCRIPT (exact commands)

All run from inside your challenge folder, with `cns_toolkit.py` beside them.

| Script | Command | Takes a file? |
| --- | --- | --- |
| autosolve.py | `python3 autosolve.py *`  (or name the file) | yes — the challenge file(s) |
| elgamal_solve.py | `python3 elgamal_solve.py challenge.json` | yes |
| fresh_solve.py | `python3 fresh_solve.py challenge.json` | yes |
| dsa_solve.py | `python3 dsa_solve.py challenge.json` | yes (then edit part 2B) |
| group_chat.py | `python3 group_chat.py` | no — expects `ciphertexts.txt` + `public_keys.txt` |
| extra_rsa.py | `python3 -c "from extra_rsa import *; print(show(franklin_reiter(n,e,c1,c2,a,b)))"` | no — you pass the numbers |
| server_*.py (all) | edit the CONFIG block first, then `python3 server_directory.py` (etc.) | no — it talks to the server |
| server_socket.py | edit HOST/PORT, then `python3 server_socket.py` | no |

The file-based ones work like autosolve: you give them the challenge file.
The server ones take no file — you fill their CONFIG block, then just run them.

---

Work top to bottom. For every challenge, **run `autosolve.py` first.**

```
python3 autosolve.py <challenge files>
```

Flag printed → submit the whole `cns{...}`, copy-pasted. Done.
Nothing printed → find your situation below.

---

## STEP 1 — identify the type by the FIELDS (not the story; the story lies)

| Fields in the file | Type |
| --- | --- |
| `n`, `e`, `c` | RSA |
| `p`, `g`, `y` + ciphertext pairs `(c1, c2)` | ElGamal |
| `p`, `g`, `y`, one shared value | Diffie-Hellman |
| `(r, s)` pairs + `q` | DSA |
| a URL / host / port | SERVER → jump to the SERVER section |

## STEP 2 — if autosolve found nothing on a FILE

1. **Odd field names?** Rename them in a copy to the vocabulary autosolve knows:
   `n e c p g y c1 c2 r s q`. Re-run. Check the printed count line (e.g. `2 e, 2 c`)
   matches what the attack needs.
2. **Check the numbers:**
   - two ElGamal pairs share `c1`? → reused nonce → `elgamal_solve.py`
   - different c1 + a known plaintext? → `fresh_solve.py`
   - two signatures share `r`? → `dsa_solve.py`
3. **Still nothing?** Re-read the hint/pun. Is a value mislabeled (a "ciphertext"
   that's really p, φ, or d)? Rename and re-run.
4. **Two identical values?** They carry no extra info — treat it as a single
   ciphertext and look for the single-ciphertext weakness.

## SPECIFIC FILE CASES

| Situation | Command |
| --- | --- |
| RSA, two messages related by `m2 = a*m1 + b` (same n, e) | `python3 -c "from extra_rsa import *; print(show(franklin_reiter(n,e,c1,c2,a,b)))"` |
| everything else automatic (Håstad, common modulus, Wiener, factoring, n prime, n=p^k, many primes, known φ/p+q/p−q) | `autosolve.py` already covers it |

---

## SERVER CHALLENGES

**HTTP or socket?** If the challenge gives a URL or `http://...`, it's HTTP -> use the
templates below (they use urllib, the curl/requests equivalent, no install needed).
If it says `nc host port` or just `host port`, it's a RAW SOCKET -> use
`server_socket.py` instead (same idea: read prompt, send line, repeat).

**Always first:** hit every endpoint once and READ what it returns. Then pick the
template, set its CONFIG block (URL, port, field names) to match, and run.
Needs campus network or VPN.

| The server... | Run | Edit |
| --- | --- | --- |
| is a key directory (register/lookup keys) | `server_directory.py` | BASE, TARGET, MYNAME. Can't register a new name? Set MYNAME = the target and **overwrite** it. |
| decrypts anything except the target ciphertext | `server_decrypt_oracle.py` | BASE, N, E, C, and the `oracle()` request line |
| signs anything except your target message | `server_sign_oracle.py` | BASE, N, E, TARGET, and the `sign()` request line |
| tells you one bit per query (odd/even, high/low half) | `rsa_parity_oracle.py` | fill N, E, C; wire `send_and_get_bit()` to the server |
| does an unauthenticated Diffie-Hellman exchange | `server_dh_mitm.py` | P, G, and relay g^d to both sides |
| is a raw `nc host port` server (prompts, not http) | `server_socket.py` | HOST, PORT, and the conversation block |

**The server trick in one line:** the server trusts whatever you send. You're not
breaking crypto — you're getting the server to do the secret operation for you
(decrypt your blinded text, sign a piece of a forbidden message, encrypt to a key
you planted).

---

## WHEN STUCK

- ~25 min max per challenge, then move on. A second flag beats a perfect first.
- Keep the folder, your edited script, and notes.
- After the session, email BOTH wouter.lemoine@uantwerpen.be AND
  Douglas.Agbeve@uantwerpen.be with your approach — partial progress can earn half a point.
