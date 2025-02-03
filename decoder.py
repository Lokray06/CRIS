from PIL import Image
import random
import rsa

def load_private_key(private_key_path):
    with open(private_key_path, "rb") as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
    return private_key

def decode_file(image_path, output_file_path, private_key_path):
    img = Image.open(image_path).convert("RGBA")
    width, height = img.size

    header = img.getpixel((0, 0))
    file_length = (header[0] << 24) + (header[1] << 16) + (header[2] << 8) + header[3]
    print(f"File length: {file_length} bytes")

    private_key = load_private_key(private_key_path)
    key_size_bytes = private_key.n.bit_length() // 8

    available_slots = []
    for y in range(height):
        for x in range(width):
            if x == 0 and y == 0:
                continue
            for channel in range(4):
                available_slots.append((x, y, channel))

    encrypted_seed_pos = file_length
    encrypted_seed = []
    for i in range(encrypted_seed_pos, encrypted_seed_pos + key_size_bytes):
        x, y, channel = available_slots[i]
        encrypted_seed.append(img.getpixel((x, y))[channel])

    encrypted_seed_bytes = bytes(encrypted_seed)
    decrypted_seed = rsa.decrypt(encrypted_seed_bytes, private_key)

    random.seed(int.from_bytes(decrypted_seed, 'big'))
    random.shuffle(available_slots)

    file_data = bytearray()
    for i in range(file_length):
        x, y, channel = available_slots[i]
        pixel = img.getpixel((x, y))
        file_data.append(pixel[channel])

    with open(output_file_path, "wb") as f:
        f.write(file_data)
    print(f"Decoded file saved to {output_file_path}")

if __name__ == "__main__":
    image_path = input("Enter the encoded image path: ")
    output_file_path = input("Enter the output file path: ")
    private_key_path = input("Enter the private key path: ")
    decode_file(image_path, output_file_path, private_key_path)
