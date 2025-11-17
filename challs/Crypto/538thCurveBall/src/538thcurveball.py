from itertools import count
from hashlib import sha256

for x in count(start=1):
    for y in range(1,x+1):
        for z in range(1,x+1):
            if x**3+y**3==538*z**3:
                h=sha256(str(z).encode()).hexdigest()
                print(f'CYBN{{{h}}}')
                exit(1)