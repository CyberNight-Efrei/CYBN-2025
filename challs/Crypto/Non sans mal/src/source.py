from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os


key = os.urandom(16)
nonce = os.urandom(8)

def encryptCTR(data, key, nonce):
    cipher = AES.new(key, AES.MODE_CTR, nonce=nonce)
    return cipher.encrypt(data)

def main():
    with open("block-cipher-modes.png", 'rb') as f:
        fileToEnc = f.read()

    encryptedFile = encryptCTR(fileToEnc, key, nonce)
    with open(f"block-cipher-modes.png.enc", 'wb') as f:
        f.write(encryptedFile)
    print(f"Encrypted block-cipher-modes.png")

    print("Now encrypting the flag using the same key")
    flag = os.getenv('SECRET_FLAG', 'CYBN{test_flag}').encode()
    encryptedFlag = encryptCTR(flag, key, nonce)
    with open("flag.enc", 'wb') as f:
        f.write(encryptedFlag)
    print("Encrypted SECRET_FLAG as flag.enc")

if __name__ == "__main__":
    main()