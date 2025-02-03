from PIL import Image
import random
import hashlib

def encode_file(input_file, output_image):
    # Read file data
    with open(input_file, "rb") as f:
        data = f.read()
    data_length = len(data)
    
    # Create deterministic seed from filename
    seed = int(hashlib.sha256(output_image.encode()).hexdigest(), 16) % 10**8
    random.seed(seed)
    
    # Open/create image
    try:
        img = Image.open(output_image).convert("RGBA")
    except FileNotFoundError:
        img = Image.new("RGBA", (1000, 1000))  # Default size if creating new
    
    # Store data length in first pixel (4 bytes using RGBA)
    length_bytes = data_length.to_bytes(4, 'big')
    img.putpixel((0, 0), tuple(length_bytes))
    
    # Data structures
    pixel_usage = {}
    indexed_dict = {}
    
    # Process each byte
    for i, byte in enumerate(data):
        byte_val = byte
        if byte_val in indexed_dict:
            continue  # Skip duplicates
            
        # Find available pixel/channel
        while True:
            x = random.randint(1, img.width-1)  # Skip first pixel
            y = random.randint(0, img.height-1)
            used = pixel_usage.get((x, y), [])
            available = [c for c in range(4) if c not in used]
            
            if available:
                channel = available[0]
                break
                
            # Resize if no space
            img = img.resize((img.width*2, img.height*2))
            
        # Update pixel
        pixel = list(img.getpixel((x, y)))
        pixel[channel] = byte_val
        img.putpixel((x, y), tuple(pixel))
        
        # Track usage
        pixel_usage.setdefault((x, y), []).append(channel)
        indexed_dict[byte_val] = (x, y, channel)
    
    img.save(output_image)