from hashlib import sha256

def get_selmer_point(n, P):
    x, y = P.xy()
    X, Y = (36*n - y)/6/x, (36*n + y)/6/x
    denom = gcd(X.denominator(), Y.denominator())
    return (X*denom, Y*denom, denom)

E = EllipticCurve([0, -432*(538**2)])
G = E.gen(0)
for i in range(1, 100):
  x,y,z = get_selmer_point(538, G*i)
  if x**3 + y**3 == 538*z**3:
    if x > 0 and y > 0 and z > 0:
      print(x,y,z)
      h = sha256(str(z).encode()).hexdigest()
      print(f"CYBN{{{h}}}")
      exit(1)