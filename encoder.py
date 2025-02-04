import os
from PIL import Image
import random
import rsa

def load_public_key(public_key_path):
    """
    Load the public key from a .pem file.
    """
    with open(public_key_path, "rb") as f:
        public_key = rsa.PublicKey.load_pkcs1(f.read())
    return public_key

def encode_file(file_path, image_path, public_key_path):
    """
    Encodes the contents of 'file_path' into the image at 'image_path'.
    The file length is stored in the header pixel (0,0), and the encrypted seed
    is stored in fixed pixels (0,1) to (0,64). The file bytes are scattered
    (in a deterministic shuffled order) in the remaining pixels.
    """
    # Open the cover image and convert it to RGBA.
    img = Image.open(image_path).convert("RGBA")
    width, height = img.width, img.height

    # Read file data.
    with open(file_path, "rb") as f:
        file_data = f.read()
    file_length = len(file_data)

    # Load public key
    public_key = load_public_key(public_key_path)
    key_size_bits = public_key.n.bit_length()
    key_size_bytes = key_size_bits // 8
    max_seed_size = key_size_bytes - 11  # Adjust for RSA padding

    # Generate a seed based on the maximum allowable size
    seed = random.getrandbits(max_seed_size * 8)
    #print(f"Seed: {seed}")

    # Convert seed to bytes appropriately
    seed_bytes = seed.to_bytes(max_seed_size, byteorder='big')

    try:
        # Encrypt the seed using RSA with PKCS#1 v1.5 padding
        encrypted_seed = rsa.encrypt(seed_bytes, public_key)
        print(f"Encrypted Seed Size: {len(encrypted_seed)} bytes")
    except OverflowError:
        print("Seed size exceeds maximum allowed by RSA key.")
        return

    # Reserve a header: use the pixel at (0,0) to store the file length (4 bytes, big-endian).
    header = (
        (file_length >> 24) & 0xFF,
        (file_length >> 16) & 0xFF,
        (file_length >> 8) & 0xFF,
        file_length & 0xFF,
    )
    img.putpixel((0, 0), header)

    # Reserve fixed pixels for encrypted seed (e.g., next 64 pixels in row 0)
    encrypted_seed_length = len(encrypted_seed)
    seed_pixels_needed = (encrypted_seed_length + 3) // 4  # 4 channels per pixel
    for i in range(seed_pixels_needed):
        x, y = 0, i + 1  # Use row 0, starting from column 0, row 1 onwards
        if x >= img.width or y >= img.height:
            raise ValueError("Image too small to store encrypted seed.")
        pixel = []
        for channel in range(4):
            index = i * 4 + channel
            if index < encrypted_seed_length:
                pixel.append(encrypted_seed[index])
            else:
                pixel.append(0)  # Padding if needed
        img.putpixel((x, y), tuple(pixel))

    # Build a list of available pixel-channel slots, skipping the header and seed pixels.
    available_slots = []
    for y in range(height):
        for x in range(width):
            if (x == 0 and y == 0) or (x == 0 and 1 <= y <= seed_pixels_needed):
                continue  # Skip header and seed pixels
            for channel in range(4):
                available_slots.append((x, y, channel))

    if file_length > len(available_slots):
        raise ValueError("The file is too large to encode in this image.")

    # Shuffle the available slots using the seed
    random.seed(seed)
    random.shuffle(available_slots)

    # Encode the file data into the image slots
    for i, byte in enumerate(file_data):
        x, y, channel = available_slots[i]
        pixel = list(img.getpixel((x, y)))
        pixel[channel] = byte  # Replace the specific channel with our file byte.
        img.putpixel((x, y), tuple(pixel))

    # Save the encoded image
    image_dir, image_filename = os.path.split(image_path)
    image_path_encoded = os.path.join(image_dir, "encoded_" + image_filename)
    img.save(image_path_encoded)
    print(f"Encoded {file_length} bytes into {image_path_encoded}\nSeed Size: {max_seed_size} bytes")