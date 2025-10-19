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