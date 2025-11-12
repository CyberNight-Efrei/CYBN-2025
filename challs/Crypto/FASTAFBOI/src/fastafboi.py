#!/usr/bin/env python3
import time, hashlib
from Crypto.Util.number import long_to_bytes

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