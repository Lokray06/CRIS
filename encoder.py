from PIL import Image
import random
import rsa

def load_public_key(public_key_path):
    with open(public_key_path, "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    return public_key

def get_seed():
    return random.getrandbits(256)

def encode_file(file_path, image_path, public_key_path):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    with open(file_path, "rb") as f:
        file_data = f.read()
    file_length = len(file_data)

    public_key = load_public_key(public_key_path)
    key_size_bytes = public_key.n.bit_length() // 8

    seed = get_seed()
    encrypted_seed = rsa.encrypt(seed.to_bytes(key_size_bytes, 'big'), public_key)
    encrypted_seed_length = len(encrypted_seed)

    header = (
        (file_length >> 24) & 0xFF,
        (file_length >> 16) & 0xFF,
        (file_length >> 8) & 0xFF,
        file_length & 0xFF
    )
    img.putpixel((0, 0), header)

    available_slots = []
    for y in range(height):
        for x in range(width):
            if x == 0 and y == 0:
                continue
            for channel in range(4):
                available_slots.append((x, y, channel))

    if file_length + encrypted_seed_length > len(available_slots):
        raise ValueError("The file is too large to encode in this image.")

    random.seed(seed)
    random.shuffle(available_slots)

    combined_data = file_data + encrypted_seed
    for i, byte in enumerate(combined_data):
        x, y, channel = available_slots[i]
        pixel = list(img.getpixel((x, y)))
        pixel[channel] = byte
        img.putpixel((x, y), tuple(pixel))

    img.save(image_path)
    print(f"Encoded {file_length} bytes into {image_path}")

if __name__ == "__main__":
    file_path = input("Enter the file path to encode: ")
    image_path = input("Enter the image path to encode into: ")
    public_key_path = input("Enter the public key path: ")
    encode_file(file_path, image_path, public_key_path)
