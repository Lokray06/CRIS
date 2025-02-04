from PIL import Image
import random
import rsa
import argparse

def load_private_key(private_key_path):
    """
    Load the private key from a .pem file.
    """
    with open(private_key_path, "rb") as f:
        private_key = rsa.PrivateKey.load_pkcs1(f.read())
    return private_key

def decode_file(image_path, output_file_path, private_key_path):
    """
    Reads the encoded image at 'image_path', recovers the file bytes,
    and writes them to 'output_file_path'.
    """
    # Open the encoded image and convert to RGBA.
    img = Image.open(image_path).convert("RGBA")
    width, height = img.width, img.height

    # Read header from pixel (0,0) to determine file length.
    header = img.getpixel((0, 0))
    file_length = (header[0] << 24) + (header[1] << 16) + (header[2] << 8) + header[3]
    print(f"File length: {file_length} bytes")

    # Load private key
    private_key = load_private_key(private_key_path)
    key_size_bits = private_key.n.bit_length()
    key_size_bytes = key_size_bits // 8

    # Read encrypted seed from fixed pixels (row 0, starting from y=1)
    encrypted_seed = []
    seed_pixels_needed = (key_size_bytes + 3) // 4  # Same calculation as encoder
    for i in range(seed_pixels_needed):
        x, y = 0, i + 1
        pixel = img.getpixel((x, y))
        for channel in range(4):
            encrypted_seed.append(pixel[channel])
    encrypted_seed_bytes = bytes(encrypted_seed[:key_size_bytes])  # Trim padding
    print(f"Extracted Encrypted Seed Size: {len(encrypted_seed_bytes)} bytes")

    # Decrypt the seed
    try:
        decrypted_seed_bytes = rsa.decrypt(encrypted_seed_bytes, private_key)
        decrypted_seed = int.from_bytes(decrypted_seed_bytes, 'big')
        #print("Seed decrypted successfully:", decrypted_seed)
        print("Seed decrypted successfully")
    except rsa.pkcs1.DecryptionError:
        print("Failed to decrypt seed. Ensure the private key matches the public key used for encoding.")
        return

    # Rebuild available slots excluding header and seed pixels
    available_slots = []
    for y in range(height):
        for x in range(width):
            if (x == 0 and y == 0) or (x == 0 and 1 <= y <= seed_pixels_needed):
                continue  # Skip header and seed pixels
            for channel in range(4):
                available_slots.append((x, y, channel))

    # Shuffle the available slots using the decrypted seed
    random.seed(decrypted_seed)
    random.shuffle(available_slots)

    # Recover file data from the shuffled slots.
    file_data = bytearray()
    for i in range(file_length):
        x, y, channel = available_slots[i]
        pixel = img.getpixel((x, y))
        file_data.append(pixel[channel])

    # Write the recovered data to the output file.
    with open(output_file_path, "wb") as f:
        f.write(file_data)
    print(f"Decoded file saved to {output_file_path}")


def main():
    parser = argparse.ArgumentParser(description="Decode a file from an encoded image using RSA.")
    parser.add_argument("--image", required=True, help="Path to the image with the encoded data.")
    parser.add_argument("--file", required=True, help="Path to the output file into which to write the decoded data.")
    parser.add_argument("--key", required=True, help="Path to the private key (.pem file).")
    
    args = parser.parse_args()
    
    decode_file(args.image, args.file, args.key)

if(__name__) == "__main__":
    main()