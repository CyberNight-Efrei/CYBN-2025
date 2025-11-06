from Crypto.Cipher import AES
from Crypto.Util.number import inverse
from Crypto.Util.Padding import pad, unpad
from collections import namedtuple
from random import randint
import hashlib

def SmartAttack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp

    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)


def shared_secret(public_key, private_key):
    S = public_key * private_key
    return S.xy()[0]

p  = 0xa9dc8d42494a205d29b690b6087e29edc3ee3a124a9a32f4d86c02b88d50a43efc4b396ea6aac16abb00d828259d3a72024cd5fc433d65c72b71069ded4a4c27
a  = 0x9671afb42502fa77570b2eba83b725f77766d49121b5c08f243688926cd79ebbfb1ebf03ade06d6c698909c28e1558ee326d5e24637e727b5a32023219e98304
b  = 0x06c494ab12f90109a30944fffe08a68f0f83fd3b656e2fa41e539a838bd8a39e37c40df97ef7fd8bce2503ae733c1b358b53801128dc5317316cfe4cb294230a

E = EllipticCurve(GF(p), [a, b])

G = E.gens()[0]
public=E(4523191617887051228273614422200763120688285363135430223776805390484925019007216406348149283489577578979767012145931394272506793432087683174193011998118516 , 1944445003077626104144428684375886679111855595787693717922062822818725938981991709668607139094416051815058532325346420434300094252384678639949600559385394)


private_key=SmartAttack(G,public,p)

b_x = 0x8081e3da61ff6271ddf41da42a9d1d5cedc834db863d71885c8fdb41bbe13f90ca3222f3feed314d4e1497768b1945c9267f405d5f2c837f58def95a4cc8e3a2
b_y = 0x8502988d0a17f2fd0d16ec2b21931fa5349a942fea6bb2c123c233a18f61223815a942e352a5bca74ed12bb155baa17d485464f29fdd945cbcbefd117c3ab30a
B = E(b_x, b_y)

secret = shared_secret(B, private_key)

sha1 = hashlib.sha1()
sha1.update(str(secret).encode('ascii'))
key = sha1.digest()[:16]

iv= bytes.fromhex('4495f397c5e6da92fd11927008b326e8')
encrypted_flag=bytes.fromhex('1272beee7794f2b00f4c181916536c36a1b54e53eb4c37936f5aa6d0d21524b5b5cadfff1c09f449c4268fa6c2562c35')

cipher = AES.new(key, AES.MODE_CBC, iv)
m=cipher.decrypt(pad(encrypted_flag, 16))

print(m)