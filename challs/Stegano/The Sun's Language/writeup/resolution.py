from PIL import Image
image_ref = Image.open("1.png")
image_modified = Image.open("2.png")
finale = ""

width, height = image_ref.size
for w in range(width):
    for h in range(height):
        if image_modified.getpixel((w,h))[0] < image_ref.getpixel((w,h))[0]:
            finale += '0'
            continue

        if image_modified.getpixel((w,h))[0] > image_ref.getpixel((w,h))[0]: finale += "1"
print(finale)