#!/usr/bin/env python3
import hashlib
import pyzipper
import os


def fibonacci(n):
    if n <= 1: return n
    a, b = 0, 1
    for _ in range(n - 1): a, b = b, a + b
    return b


def generate_password(layer):
    fib_number = fibonacci(layer)
    return hashlib.sha256(str(fib_number).encode()).hexdigest()[:16]


def solve_matryoshka(input_file="matryoshka.zip"):
    current_zip, layer = input_file, 0
    
    print(f"Solving Matryoshka challenge...")
    print("=" * 60)
    
    while layer < 1000:
        password = generate_password(layer)
        
        try:
            with pyzipper.AESZipFile(current_zip, 'r') as zf:
                zf.setpassword(password.encode())
                
                inner_file = zf.namelist()[0]
                extracted_data = zf.read(inner_file)
                
                if inner_file.endswith('.txt'):
                    with open(inner_file, 'wb') as f:
                        f.write(extracted_data)
                    print(f"Layer {layer} extracted (FINAL)")
                    print("=" * 60)
                    print(f"\nFlag saved to: {inner_file}")
                    print(f"Content:\n{extracted_data.decode()}")
                    break
                
                temp_file = f"temp_layer_{layer + 1}.zip"
                with open(temp_file, 'wb') as f: f.write(extracted_data)
                current_zip = temp_file
                
                if (layer + 1) % 50 == 0: print(f"Progress: {layer + 1} layers...")
                
                layer += 1
        
        except Exception as e:
            print(f"Error at layer {layer}: {e}")
            break
    
    import glob
    for temp_file in glob.glob("temp_layer_*.zip"):
        try: os.remove(temp_file)
        except: pass
    
    print("=" * 60)
    print(f"Solved! ({layer + 1} layers)\n")


if __name__ == "__main__":
    solve_matryoshka()