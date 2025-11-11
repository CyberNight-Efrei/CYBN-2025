from PIL import Image

slots = [None]*46

img = Image.open("debug_slots_dots.png")

width,height = img.size
print(img.size)
colors = (255, 130)
for y in range(height):
	for x in range(width):
		pixel = img.getpixel((x, y))
		if pixel[0] == colors[0] and pixel[1] == colors[1]:
			print(pixel[2])
			slots[pixel[2]] = (x,y)
print(slots)