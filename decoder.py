from PIL import Image
import random
import hashlib

def decode_file(input_image, output_file):
    img = Image.open(input_image).convert("RGBA")
    
    # Get data length from first pixel
    length_pixel = img.getpixel((0, 0))
    data_length = int.from_bytes(bytes(length_pixel), 'big')
    
    # Create deterministic seed from filename
    seed = int(hashlib.sha256(input_image.encode()).hexdigest(), 16) % 10**8
    random.seed(seed)
    
    # Generate coordinates
    pixel_usage = {}
    indexed_dict = {}
    data = bytearray()
    
    while len(data) < data_length:
        # Find next byte location
        while True:
            x = random.randint(1, img.width-1)
            y = random.randint(0, img.height-1)
            used = pixel_usage.get((x, y), [])
            available = [c for c in range(4) if c not in used]
            
            if available:
                channel = available[0]
                break
                
        # Read byte
        pixel = img.getpixel((x, y))
        byte_val = pixel[channel]
        
        # Store and track
        data.append(byte_val)
        pixel_usage.setdefault((x, y), []).append(channel)
        indexed_dict[byte_val] = (x, y, channel)
    
    # Write output
    with open(output_file, "wb") as f:
        f.write(data[:data_length])  # Trim to exact length