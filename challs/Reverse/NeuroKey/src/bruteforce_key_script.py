def caesar_shift(s, key):
    return ''.join([chr(ord(c) + key) for c in s])

with open("flag.txt", "rb") as f:
    for key in range(101):
        cybernight = "CYBERNIGHT2025"
        shifted_cybernight = caesar_shift(cybernight, key)

        decrypted = []
        i = 0
        while (ch := f.read(1)):
            decrypted.append(chr(ch[0] ^ ord(shifted_cybernight[i % len(shifted_cybernight)])))
            i += 1
        
        decrypted_str = ''.join(decrypted)

        if decrypted_str.startswith("CYBN{"):
            print(f"Found the flag : {decrypted_str}")
            print(f"With shifted CYBERNIGHT2025 (key={key}) in bytes: {shifted_cybernight.encode()}")
            break
        
        f.seek(0)