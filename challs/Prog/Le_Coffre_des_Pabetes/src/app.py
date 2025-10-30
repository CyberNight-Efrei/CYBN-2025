import socket
import os

# --------------------- Variables de configuration --------------------- #
HOST = '0.0.0.0' # A changer par mes chers admins
PORT = 31337 # kifkif
FLAG = os.get('FLAG', 'CYBN{les problèmes... contact un admin}')
ALLOWED_CHARS = set(".,<>-+[]")


# ---------------------- Fonction d'exécution Brainfuck ----------------- #
def run_bf(code, input_value=""):

    # Initialisation de la machine Brainfuck
    cells = [0] * 30000
    ptr = 0
    output = ""
    input_ptr = 0
    input_str = str(input_value) + "\n"

    # Pré-calcul des correspondances [ et ]
    loop_map = {}
    stack = []
    for i, c in enumerate(code):
        if c == "[":
            stack.append(i)
        elif c == "]":
            start = stack.pop()
            loop_map[start] = i
            loop_map[i] = start


    # Exécution du code Brainfuck
    i = y = 0
    while i < len(code) and y < 100000: # Limite d'instructions pour éviter les boucles infinies
        c = code[i]
        if c == ">":
            ptr += 1
        elif c == "<":
            ptr -= 1
        elif c == "+":
            cells[ptr] = (cells[ptr] + 1) % 256
        elif c == "-":
            cells[ptr] = (cells[ptr] - 1) % 256
        elif c == ".":
            output += chr(cells[ptr])
        elif c == ",":
            if input_ptr < len(input_str):
                cells[ptr] = ord(input_str[input_ptr])
                input_ptr += 1
            else:
                cells[ptr] = 0
        elif c == "[":
            if cells[ptr] == 0:
                i = loop_map[i]
        elif c == "]":
            if cells[ptr] != 0:
                i = loop_map[i]
        i += 1
        y += 1
    return output



# ---------------------- Serveur TCP --------------------- #
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen()
    print(f"Serveur Brainfuck avec input en écoute sur {HOST}:{PORT}")

    while True:
        conn, addr = s.accept()
        with conn:
            print(f"Connexion de {addr}")

            # 1. Recevoir le code Brainfuck
            code = conn.recv(8192).decode('utf-8').strip()
            print(f"Code reçu (longueur {len(code)}):  [ {code} ]")

            if not all(c in ALLOWED_CHARS for c in code):
                conn.sendall("Code Brainfuck invalide, un des caractères n'est pas existant\n".encode('utf-8'))
                continue
            
            # 2. Tester le code avec toutes les entrées possibles (1-9)
            test_list = [run_bf(code, str(i+1)) == str((i+1)**2) for i in range(9)]
            is_valid = all(test_list)


            # 3. Envoyer le résultat au client
            if is_valid:
                conn.sendall(f"GG WP Sale Neuille ! \n{FLAG}\n".encode('utf-8'))
                print(f"Code valide, flag envoyé: {FLAG}\n")
            else:
                conn.sendall("Code incorrect pour au moins une entrée.\n".encode('utf-8'))
                print("Code invalide pour au moins une entrée.\ntest_list: " + str(test_list) + "\n")