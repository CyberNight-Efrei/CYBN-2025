import socket, time, hashlib
from Crypto.Util.number import long_to_bytes

HOST, PORT = "localhost", 2222

def recv_line(s):
    b = b""
    while not b.endswith(b"\n"):
        c = s.recv(1)
        if not c: raise EOFError
        b += c
    return b

with socket.create_connection((HOST, PORT)) as s:
    print(recv_line(s).decode(), end="")
    print(recv_line(s).decode(), end="")
    ct_hex = recv_line(s).decode().strip()
    print(ct_hex)

ct = bytes.fromhex(ct_hex)
ts = int(time.time())
k = hashlib.sha256(long_to_bytes(ts)).digest()
pt = bytes(c ^ k[i % len(k)] for i, c in enumerate(ct))
print(pt.decode())