from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup
import base64
import re

challenge_url = input("Challenge url: ")
submit_url = challenge_url.replace('/challenge', '/submit')

flag_regex = r"CYBN\{[!-~]+\}"

slots = [None]*46
real_color = (139,139,139,255)

img = Image.open("debug_slots_dots.png")

width,height = img.size
print(img.size)
colors = (255, 130)
for y in range(height):
	for x in range(width):
		pixel = img.getpixel((x, y))
		if pixel[0] == colors[0] and pixel[1] == colors[1]:
			slots[pixel[2]] = (x,y)

flagged = False

s = requests.Session()

while not flagged:
	res = s.get(challenge_url)
	if res.status_code != 200:
		print('An error has occured:', res.text)
		exit(1)
	if flag := re.search(flag_regex, res.text):
		print("\n\n########################################")
		print(f"Here is your flag : {flag.group()}")
		print("########################################")
		flagged = True
		break
	soup = BeautifulSoup(res.text, 'html.parser')
	level = soup.find_all('h1')[0].text.strip()
	print("\n-------------------")
	print(level)
	img = soup.find_all('img')[0]['src']

	im = Image.open(BytesIO(base64.b64decode(img.replace('data:image/png;base64,', ''))))
	valid_slots = []
	for i in range(len(slots)):
		pixel = im.getpixel(slots[i])
		if pixel != real_color:
			print(f'found pane, slot {i} : {pixel}')
			valid_slots.append(str(i))
	submit_text = ', '.join(valid_slots)
	print("Submit:", submit_text)

	res = s.post(submit_url, data={'slots': submit_text}, allow_redirects=True)
	if res.status_code != 200:
		print('An error has occured:', res.text)
		exit(1)