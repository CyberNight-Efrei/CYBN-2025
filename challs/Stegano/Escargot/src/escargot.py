from PIL import Image, ImageDraw
import argparse
import os.path

def convert_bytes_to_bits(text):
    return ''.join(format(i, '08b') for i in text)


def convert_str_to_bits(text):
    return ''.join(format(ord(i), '08b') for i in text)


def convert_bits_to_str(bits):
    return ''.join(chr(int(''.join(x), 2)) for x in zip(*[iter(bits)] * 8))


def change_int_value_bit(bits, value, position=0):
    if value not in '01':
        raise ValueError('Value needs to be 0 or 1.')
    if not 0 <= position <= 7:
        raise ValueError('Position needs to be between 0 and 7 included.')

    s = list(get_bits_from_int(bits))
    position = 7 - position
    s[position] = value
    return int(''.join(s), 2)


def get_bits_from_int(value):
    return f'{value:08b}'


def bitstring_to_bytes(s):
    s = s.ljust(len(s) + (8-(len(s)%8)), '0') # Pad to 8
    return int(s, 2).to_bytes(len(s) // 8, byteorder='big')


def max_spiral_pixels(width, height):
    total = 0
    depth = 0

    while True:
        w = width - 4 * depth
        h = height - 4 * depth
        if w <= 1 or h <= 1:
            break
        perimeter = 2 * (w + h - 2)
        total += perimeter
        depth += 1
    return total


def draw_spiral(image_path, data):
    img = Image.open(image_path).convert("RGB")

    # Directions : droite, bas, gauche, haut
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # Initialisation
    x, y = 0, 0
    width, height = img.size
    dir_index = 0
    data_size = len(data)

    # Verification de la taille
    assert data_size <= max_spiral_pixels(width, height), f"Cannot embed {data_size} bits, max is {max_spiral_pixels(width, height)} for this image."

    # Limites internes de la spirale
    x_length = width - 1
    y_length = height - 1

    i = 0

    while i < data_size:

        dx, dy = directions[dir_index % 4]
        # On détermine la longueur du segment courant
        if dx != 0:  # horizontal
            length = x_length
        else:        # vertical
            length = y_length

        for _ in range(length):
            if i >= data_size:
                break
            pixel = list(img.getpixel((x, y)))
            pixel[0] = change_int_value_bit(pixel[0], data[i]) # Red only
            img.putpixel((x, y), tuple(pixel))
            x += dx
            y += dy
            i += 1

        # Rétrécir la zone pour la prochaine couche (1 pixel pour trait, 1 pour espace)
        if dir_index >= 1:
            match dir_index % 2:
                case 0:
                    x_length -= 2
                case 1:
                    y_length -= 2

        dir_index += 1
    return img


def read_spiral(image_path):
    img = Image.open(image_path).convert("RGB")

    # Directions : droite, bas, gauche, haut
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    # Initialisation
    x, y = 0, 0
    width, height = img.size
    dir_index = 0
    done = False

    data = ""
    sanitize_count = 12
    max_size = max_spiral_pixels(width, height)

    # Limites internes de la spirale
    x_length = width - 1
    y_length = height - 1
    length = 0

    i = 0

    while i < max_size and length > -1 and not done:

        dx, dy = directions[dir_index % 4]
        # On détermine la longueur du segment courant
        if dx != 0:  # horizontal
            length = x_length
        else:        # vertical
            length = y_length

        for _ in range(length):
            if i >= max_size or (i > 8 * (sanitize_count + 1) and
                    (data[len(data) - 8 * sanitize_count:] == '0' * 8 * sanitize_count or
                     data[len(data) - 8 * sanitize_count:] == '1' * 8 * sanitize_count)):
                data = data[:len(data) - 8 * sanitize_count]
                done = True
                break
            pixel = list(img.getpixel((x, y)))
            data += get_bits_from_int(pixel[0])[-1]
            x += dx
            y += dy
            i += 1

        # Rétrécir la zone pour la prochaine couche (1 pixel pour trait, 1 pour espace)
        if dir_index >= 1:
            match dir_index % 2:
                case 0:
                    x_length -= 2
                case 1:
                    y_length -= 2

        dir_index += 1
        
    return data


DEFAULT_OUTPUT = "embedded.png"

parser = argparse.ArgumentParser(
    prog='LSB Spiral embedder and extractor',
    description='Extracts and embed text into images, using spirals')

parser.add_argument('image',
                    type=str,
                    help='Image to embed/extract data')
parser.add_argument('-t', '--text',
                    type=str,
                    default=None,
                    required=False,
                    help='Text to be embed')
parser.add_argument('-f', '--file',
                    type=str,
                    default=None,
                    required=False,
                    help='File to be embed (.txt in plain text, other in binary)')
parser.add_argument('-o', '--output',
                    type=str,
                    default=DEFAULT_OUTPUT,
                    required=False,
                    help="File to output extracted data (.txt in plain text, other in binary)")
parser.add_argument('-v', '--verbose',
                    action="store_true",
                    required=False,
                    help="increase verbosity")

args = parser.parse_args()

if not os.path.isfile(args.image):
    parser.error(f'Image {args.image} does not exists.')

if args.file and not os.path.isfile(args.file):
    parser.error(f'File {args.image} does not exists.')

# Embedding mode
if args.text or args.file:

    # Get data from file or text
    data = ''
    if args.file:
        mode = 'r' if args.file.endswith('.txt') else 'rb'
        f = open(args.file, mode)
        data = f.read()
        f.close()
        print('[+] Embedding file :', args.file)
    elif args.text:
        data = args.text
        print('[+] Embedding data :', data)
    if args.verbose:
        print('[+] data :', data)

    # convert data to binary format
    if args.verbose:
        print('[+] data type :', type(data))
    if type(data) == str:
        to_embed = convert_str_to_bits(data)
    else:
        try:
            to_embed = convert_bytes_to_bits(data)
        except:
            raise TypeError(f'Cannot convert data type {type(data)}')

    if args.verbose:
        print('[+] data to embed :', to_embed)

    embedded = draw_spiral(args.image, to_embed)
    embedded.save(args.output)
    print(f"[+] Data embedded successfully to  : {args.output}")


# Extract mode
else:
    print('[+] Extracting data')

    data = read_spiral(args.image)

    if args.verbose:
        print('[+] data found :', data)

    if not data:
        print('[-] No data was found.')
    elif args.output != DEFAULT_OUTPUT:
        with open(args.output, 'wb') as f:
            print(' \n', data)
            print(bitstring_to_bytes(data))
            f.write(bitstring_to_bytes(data))
        print(f'[+] Successfully extracted {len(data)} bytes to {args.output}')
    else:
        print(f'[+] Extracted data : {convert_bits_to_str(data)}')