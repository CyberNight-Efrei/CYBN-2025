#!/usr/bin/env python3
import socketserver, time, hashlib
from Crypto.Util.number import long_to_bytes

FLAG = b'CYBN{1M_F4$t_4F_BOIII!!!}'

def gen_key():
    current_time = int(time.time())
    key = long_to_bytes(current_time)
    return hashlib.sha256(key).digest()

def encrypt(b):
    key = gen_key()
    ciphertext = b''
    for i in range(len(b)):
        ciphertext += bytes([b[i] ^ key[i % len(key)]])
    return ciphertext.hex()

PROMPT = "BE FAST AF BOI!\nHere is the encrypted flag:\n"

class ChallengeHandler(socketserver.StreamRequestHandler):
    def handle(self):
        self.wfile.write(PROMPT.encode())
        self.wfile.write(encrypt(FLAG).encode())
        self.wfile.write(b"\n")
        self.finish()

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    allow_reuse_address = True

with ThreadedTCPServer(("0.0.0.0",2222),ChallengeHandler) as s:
    try:s.serve_forever()
    except KeyboardInterrupt:pass