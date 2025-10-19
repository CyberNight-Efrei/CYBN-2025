#!/usr/bin/env python3
import json, socketserver, binascii

FLAG = "CYBN{H4sH_1t_H4sH_1t_&_Fl4G_1t_L1k3_1tS_h0t}"

BLOCK_SIZE = 32
W = [0xa4b5c2d3,0x7e39f8a1,0x1bd47c9e,0x93f20b64,0xce55a81d,0x28d4e9b2,0x5f80c6a7,0xe13da057]
X = [0x41fc78b2,0x9a5e3f64,0x2f14cb91,0xf6b8d32e,0x0c9a7f5d,0x87b16ea0,0x5e024f38,0xdb97a1cc]
Y = [0x6b9d03fa,0x35f4ae70,0xc4b8d592,0x18e62f3d,0xa02d7b49,0x7d5c98e1,0xf91b4a27,0x529c0de6]
Z = [0xed1843b9,0x4c7b92d1,0x93f2a507,0xb68c3e4a,0x17a5c0fd,0x2ef849b3,0x80d71365,0xfa526e9c]
W_bytes = b"".join([x.to_bytes(4,"big") for x in W])
X_bytes = b"".join([x.to_bytes(4,"big") for x in X])
Y_bytes = b"".join([x.to_bytes(4,"big") for x in Y])
Z_bytes = b"".join([x.to_bytes(4,"big") for x in Z])

def pad(data):
    padding_len = (BLOCK_SIZE - len(data)) % BLOCK_SIZE
    return data + bytes([padding_len]*padding_len)
def blocks(data):
    return [data[i:(i+BLOCK_SIZE)] for i in range(0,len(data),BLOCK_SIZE)]
def xor(a,b):
    return bytes([x^y for x,y in zip(a,b)])
def rotate_left(data,x):
    x = x % BLOCK_SIZE
    return data[x:] + data[:x]
def rotate_right(data,x):
    x = x % BLOCK_SIZE
    return data[-x:] + data[:-x]
def scramble_block(block):
    local_W = bytearray(W_bytes)
    local_X = bytearray(X_bytes)
    for i in range(40):
        for j in range(len(local_W)):
            local_W[j] ^= (i * 13 + j) & 0xFF
            local_X[j] ^= (i * 29 + j * 7) & 0xFF
        block = xor(bytes(local_W), block)
        block = rotate_left(block, (6 + block[0]) % BLOCK_SIZE)
        block = xor(bytes(local_X), block)
        block = rotate_right(block, (17 + block[-1]) % BLOCK_SIZE)
    return block
def hashitlikeitshot(msg):
    initial_state = xor(Y_bytes, Z_bytes)
    msg_padded = pad(msg)
    msg_blocks = blocks(msg_padded)
    for i, b in enumerate(msg_blocks):
        mix_in = scramble_block(xor(b, initial_state))
        rot_val = (i * 7 + sum(b) + mix_in[0]) % BLOCK_SIZE
        mix_in = rotate_left(mix_in, rot_val)
        for r in range(i + 1):
            mix_in = rotate_right(mix_in, (r * 11 + mix_in[r % len(mix_in)]) % BLOCK_SIZE)
            mix_in = xor(mix_in, rotate_left(X_bytes, (r * 3) % BLOCK_SIZE))
            mix_in = rotate_left(mix_in, (r * 6 + mix_in[-1]) % BLOCK_SIZE)
        initial_state = xor(initial_state, mix_in)
        initial_state = rotate_left(initial_state, (mix_in[0] + i) % BLOCK_SIZE)
    return initial_state.hex()

PROMPT = (
    "If you find a collision, you'll be rewarded with a flag.\n\n"
    "Send two hex encoded messages m1, m2 in JSON format, like this:\n"
    '{"m1": "68656c6c6f", "m2": "776f726c64"}\n\n'
    "> "
)
MAX_LINE_LENGTH = 10000
MAX_MSG_BYTES = 4096

class ChallengeHandler(socketserver.StreamRequestHandler):
    def handle(self):
        try:
            self.request.settimeout(60)
            self.wfile.write(PROMPT.encode())
            line = self.rfile.readline(MAX_LINE_LENGTH)
            if not line: return
            try: s = line.decode().strip()
            except: return self._send_json({"error":"invalid-encoding"})
            try: obj = json.loads(s)
            except: return self._send_json({"error":"invalid-json"})
            if not isinstance(obj,dict) or "m1" not in obj or "m2" not in obj:
                return self._send_json({"error":"expected-keys-m1-and-m2"})
            m1_hex,m2_hex=obj["m1"],obj["m2"]
            if not isinstance(m1_hex,str) or not isinstance(m2_hex,str):
                return self._send_json({"error":"m1-and-m2-must-be-hex-strings"})
            try:
                m1=binascii.unhexlify(m1_hex); m2=binascii.unhexlify(m2_hex)
            except: return self._send_json({"error":"invalid-hex"})
            if len(m1)>MAX_MSG_BYTES or len(m2)>MAX_MSG_BYTES:
                return self._send_json({"error":"message-too-large"})
            h1=hashitlikeitshot(m1); h2=hashitlikeitshot(m2)
            if h1==h2 and m1!=m2:
                return self._send_json({"flag":FLAG})
            else:
                return self._send_json({"error":"not-a-collision"})
        except:
            try:self._send_json({"error":"internal"})
            except:pass
    def _send_json(self,obj):
        s=json.dumps(obj,separators=(",",":"))+"\n"
        self.wfile.write(s.encode())

class ThreadedTCPServer(socketserver.ThreadingMixIn,socketserver.TCPServer):
    allow_reuse_address=True

with ThreadedTCPServer(("0.0.0.0",2222),ChallengeHandler) as s:
    try:s.serve_forever()
    except KeyboardInterrupt:pass