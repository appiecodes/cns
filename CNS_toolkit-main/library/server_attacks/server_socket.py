"""SERVER: raw TCP socket (the `nc host port` kind, like session 1's database one).

Many crypto servers are NOT http - you connect with a socket, the server prints
prompts/menus, you send lines back. Uses only the standard library (works on any
lab PC; no pip install). If pwntools is installed it's nicer, but this is enough.

Flow: read until a prompt, send your line, repeat. Parse numbers out of what it prints.
"""
import socket, re

# ===================== EDIT CHECKLIST (do these, nothing else) =============
#  1. HOST, PORT : from the challenge (e.g. cns-test.idlab.uantwerpen.be 50010)
#  2. the conversation at the bottom : match the server's prompts and what to send
#  The recv/send helpers below do NOT change.
# ===========================================================================
HOST = "cns-test.idlab.uantwerpen.be"
PORT = 50000

sock = socket.create_connection((HOST, PORT), timeout=15)

def recv_until(marker=b"\n", limit=65536):
    """read bytes until `marker` appears (or connection pauses). Returns decoded str."""
    data = b""
    while marker not in data and len(data) < limit:
        try:
            chunk = sock.recv(4096)
        except socket.timeout:
            break
        if not chunk:
            break
        data += chunk
    print(data.decode(errors="replace"), end="")   # show what the server said
    return data.decode(errors="replace")

def send(line):
    """send one line (adds newline)."""
    sock.sendall((str(line) + "\n").encode())

def grab_int(text):
    """pull the first big integer out of the server's text."""
    m = re.search(r"\d{3,}", text)
    return int(m.group()) if m else None

# ---- THE CONVERSATION (ADAPT this to the server's actual prompts) ----------
# Example skeleton:
#   banner = recv_until(b"?")           # read the menu / first prompt
#   send("1")                           # choose an option
#   reply = recv_until(b"\n")           # read its answer
#   n = grab_int(reply)                 # pull a number it gave you
#   send(my_value)                      # send something back
#   flag_line = recv_until(b"}")        # read until the flag's closing brace
#   print("FLAG:", flag_line)
# ----------------------------------------------------------------------------
banner = recv_until(b"\n")
print("\n[connected - now edit the conversation block to match this server]")
