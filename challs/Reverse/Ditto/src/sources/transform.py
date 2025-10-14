import re
import sys
import uuid

# =============================================================================
# =============================================================================

def bytes_to_uuids(byte_list: list[int]) -> list[uuid.UUID]:
    uuid_list = []

    for i in range(0, len(byte_list), 16):
        chunk = byte_list[i:i+16]

        if len(chunk) < 16:
            padding_needed = 16 - len(chunk)
            chunk.extend([0] * padding_needed)
            print(f"Note: The last chunk was padded with {padding_needed} zero(s).")

        xored_chunk = [b ^ 0x69 for b in chunk]

        byte_chunk = bytes(xored_chunk)
        new_uuid = uuid.UUID(bytes=byte_chunk)
        uuid_list.append(new_uuid)

    return uuid_list

# =============================================================================
# =============================================================================

def parse_file(file: str) -> list[int]:
    with open(file) as f:
        content = f.read()

    match = re.search(r"\{\s*([\s\S]+?)\s*}", content)

    if not match:
        return []

    hex_values_str = match.group(1)

    byte_list = [
        int(h.strip(), 16)
        for h in hex_values_str.split(",") if h.strip()
    ]

    return byte_list

# =============================================================================
# =============================================================================

def save(uuids: list[uuid.UUID]) -> None:
    with open("template.go") as source, open("main.go", "w") as target:
        template = source.read()
        template = template.replace(
            "// uuids",
            ",".join(f'"{i}"' for i in uuids) + ","
        )

        target.write(template)

# =============================================================================
# =============================================================================

def main() -> None:
    if len(sys.argv) < 2:
        print(f"Usage: python {sys.argv[0]} <path_to_file>")

    input_filename = sys.argv[1]

    bytes_from_file = parse_file(input_filename)

    if bytes_from_file:
        save(bytes_to_uuids(bytes_from_file))

# =============================================================================
# =============================================================================

if __name__ == "__main__":
    main()

