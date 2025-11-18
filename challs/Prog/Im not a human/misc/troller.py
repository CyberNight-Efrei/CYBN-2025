import requests

challenge_url = input("Challenge url: ")
submit_url = challenge_url.replace('/challenge', '/submit')

s = requests.Session()
s.get(challenge_url)

for i in range(10):
	res = s.post(submit_url, data={"slots":""})
	print(res.text)