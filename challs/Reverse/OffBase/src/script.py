import base64

CUSTOM_B64 = "ZYXABCDEFGHIJKLMNOPQRSTUVWzyxabcdefghijklmnopqrstuvw0123456789-_"

STANDARD_B64 = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

TRANS_TABLE = str.maketrans(CUSTOM_B64, STANDARD_B64)

def custom_b64_decode(s: str) -> bytes:
    std_b64 = s.translate(TRANS_TABLE)
    return base64.b64decode(std_b64)

if __name__ == "__main__":
    chunks = [
        "N1iX", "Qkqr", "JCOc", "RwYc",
        "PAOv", "OC90", "JC9D", "JT5B",
        "U0e1", "PE0="
    ]
    encoded = "".join(chunks)

    decoded = custom_b64_decode(encoded)
    print("Flag:", decoded.decode())