#!/usr/bin/env python3
from pwn import remote; import json

HOST,PORT="127.0.0.1",2222

m1= b"A"*31
m2 = m1+b"\x01"

line=(json.dumps({"m1":m1.hex(),"m2":m2.hex()},separators=(",",":"))+"\n").encode()

with remote(HOST, PORT, timeout=5) as r:
    p= r.recv(timeout=1)
    print(p.decode(errors="replace"), end="") if p else None
    r.send(line)
    resp = r.recvline(timeout=5)
    print(resp.decode(errors="replace").rstrip("\n")) if resp else None
