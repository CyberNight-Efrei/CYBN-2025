# Build

1. Compiler payload.c

```bash
gcc -O2 -Wall -Wextra -Wshadow -Wformat=2 -Wconversion \
          -fstack-protector-strong -D_FORTIFY_SOURCE=2 \
          -fPIC -fPIE -pie \
          -s \
          -o payload payload.c
```

2. Génerer une version hex du binaire `payload`

```bash
xxd -i payload > payload.hex
```

3. Génerer le fichier `main.go`

```bash
python transform.py payload.hex
```

4. Compiler le loader

```
go build -ldflags="-s -w" -trimpath -o ditto main.go
```
