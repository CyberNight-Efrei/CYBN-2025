import requests, pickle, concurrent.futures

BASE_URL = input("URL of your challenge : ")
API_POS = "/api/pos-info?x={x}&y={y}"

s = requests.Session()
SIZE = 150
count = 0
count_max = SIZE**2
part = count_max//10

pixels = [[None]*SIZE for _ in range(SIZE)]
users = set()

def fetch(x, y):
    r = s.get(BASE_URL + API_POS.format(x=x, y=y))
    if r.status_code != 200:
        exit(1)
    data = r.json()
    u = f"{data['pixel']['user']['username']}:{data['pixel']['user']['id']}"
    return x, y, u

print("Fetching pixels...")
with concurrent.futures.ThreadPoolExecutor(max_workers=100) as ex:
    for x, y, u in ex.map(lambda xy: fetch(*xy), [(x, y) for y in range(SIZE) for x in range(SIZE)]):
        pixels[y][x] = u
        users.add(u)
        count += 1
        if count % part == 0:
            print(f"\tFetched {count}/{count_max} pixels {(count/count_max)*100}%")

print("Exporting data for future use...")
with open('pixels.pickle', 'wb') as h: pickle.dump(pixels, h, pickle.HIGHEST_PROTOCOL)
with open('users.pickle', 'wb') as h: pickle.dump(list(users), h, pickle.HIGHEST_PROTOCOL)

print("Printing grids...")
for user in users:
    print("USER:", user)
    for y in pixels:
        for x in y:
            if user == x:
                print("#", end="")
            else:
                print(" ", end="")
        print()
    print(f"\n\n{'='*SIZE}\n\n")
