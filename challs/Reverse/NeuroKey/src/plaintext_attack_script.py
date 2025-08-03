with open("flag.txt", "rb") as file:
    flag_bytes = file.read()

rotation_char = chr(flag_bytes[0] ^ ord("C"))
rotation_offset = ord(rotation_char) - ord("C")

encryption_key = "CYBERNIGHT2025"

shifted_key_values = [ord(char) + rotation_offset for char in encryption_key]
print(shifted_key_values)

result = bytearray()
for i in range(len(flag_bytes)):
    key_value = shifted_key_values[i % len(shifted_key_values)]
    result.append(flag_bytes[i] ^ key_value)

print(result)