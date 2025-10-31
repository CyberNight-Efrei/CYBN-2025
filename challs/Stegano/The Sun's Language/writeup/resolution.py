from PIL import Image
image_ref = Image.open("../dist/1.png")
image_modified = Image.open("../dist/2.png")
finale = ""

# https://stackoverflow.com/questions/32675679/convert-binary-string-to-bytearray-in-python-3
def bitstring_to_bytes(s):
    v = int(s, 2)
    b = bytearray()
    while v:
        b.append(v & 0xff)
        v >>= 8
    return bytes(b[::-1])

width, height = image_ref.size
for w in range(width):
    for h in range(height):
        if image_modified.getpixel((w,h))[0] < image_ref.getpixel((w,h))[0]:
            finale += '0'
            continue

        if image_modified.getpixel((w,h))[0] > image_ref.getpixel((w,h))[0]: finale += "1"
print(finale)
print(bitstring_to_bytes(finale).decode(('utf-8')))
