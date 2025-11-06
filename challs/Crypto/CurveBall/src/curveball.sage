from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from random import randint
import hashlib

FLAG = b'CYBN{REDACTED}'


def generate_pub_key():
    private = randint(1, E.order() - 1)
    public = G * private
    return(public, private)


def shared_secret(public_key, private_key):
    S = public_key * private_key
    return S.xy()[0]


def encrypt_flag(flag):
    b_x = 0x8081e3da61ff6271ddf41da42a9d1d5cedc834db863d71885c8fdb41bbe13f90ca3222f3feed314d4e1497768b1945c9267f405d5f2c837f58def95a4cc8e3a2
    b_y = 0x8502988d0a17f2fd0d16ec2b21931fa5349a942fea6bb2c123c233a18f61223815a942e352a5bca74ed12bb155baa17d485464f29fdd945cbcbefd117c3ab30a
    B = E(b_x, b_y)
    A, nA = generate_pub_key()
    print(f'Public Key: {A}')
    secret = shared_secret(B, nA)
    sha1 = hashlib.sha1()
    sha1.update(str(secret).encode('ascii'))
    key = sha1.digest()[:16]
    iv = os.urandom(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    ciphertext = cipher.encrypt(pad(FLAG, 16))
    data = {}
    data['iv'] = iv.hex()
    data['encrypted_flag'] = ciphertext.hex()
    return data


p  = 0xa9dc8d42494a205d29b690b6087e29edc3ee3a124a9a32f4d86c02b88d50a43efc4b396ea6aac16abb00d828259d3a72024cd5fc433d65c72b71069ded4a4c27
a  = 0x9671afb42502fa77570b2eba83b725f77766d49121b5c08f243688926cd79ebbfb1ebf03ade06d6c698909c28e1558ee326d5e24637e727b5a32023219e98304
b  = 0x06c494ab12f90109a30944fffe08a68f0f83fd3b656e2fa41e539a838bd8a39e37c40df97ef7fd8bce2503ae733c1b358b53801128dc5317316cfe4cb294230a

E = EllipticCurve(GF(p), [a, b])

assert is_prime(E.order())

G = E.gens()[0]
print(f'Generator: {G}')

encrypted_flag = encrypt_flag(FLAG)
print(encrypted_flag)