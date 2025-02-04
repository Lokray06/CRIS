# CRIS (Cryptographic RSA Image Steganography)

A Python-based steganography tool that hides files within images using RSA encryption for secure data embedding. This repository provides bidirectional functionality for encoding files into images and decoding them back.

---

## Overview

CRIS allows you to:

- **Encode** a file into an image (e.g., PNG, JPG) by scattering its bytes across the image's pixels.
- **Decode** an encrypted file from an image using a private RSA key.

The encoding process includes:

1. Storing the file length in the image header (pixel (0,0)).
2. Encrypting a seed for shuffling the data placement within the image.
3. Distributing the file bytes across the image using a shuffled order.

The decoding process retrieves the file by reversing these steps.

---

## Table of Contents

- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

---

## How It Works

### Key Components

1. **RSA Encryption**: The tool uses RSA encryption to secure the seed used for shuffling the data placement within the image.
2. **Shuffling**: The seed determines the order in which the file bytes are embedded into the image's pixels.
3. **File Length Header**: The first pixel (0,0) stores the file length as a 4-byte header.
4. **Encrypted Seed**: The seed is encrypted using the public key and stored in a fixed set of pixels (row 0, starting from y=1).

### Encoding Process

1. Convert the image to RGBA format.
2. Read the file to be encoded.
3. Generate a seed, encrypt it using RSA, and store it in the image.
4. Shuffle the available pixels using the seed.
5. Embed the file bytes into the shuffled pixel locations.

### Decoding Process

1. Read the file length from the header pixel (0,0).
2. Decrypt the seed using the private key.
3. Reconstruct the shuffled pixel order using the decrypted seed.
4. Extract the file bytes from the image.

---

## Getting Started

### Prerequisites

- Python 3.x
- `Pillow` library (for image handling)
- ` rsa` library (for RSA encryption)
- A pair of RSA keys (public and private)

To install the required libraries:

```bash
pip install Pillow rsa
```

### Usage

#### Encoding

```bash
python encode.py --file <your_file_path> --image <your_image_path> --key <public_key_path>
```

#### Decoding

```bash
python decode.py --image <encoded_image_path> --output <output_file_path> --key <private_key_path>
```

---

## Examples

### Example 1: Encoding a Text File

1. Create a text file.
   ```bash
   echo "Hello, CRIS!" > secret.txt
   ```

2. Encode the text file into an image.
   ```bash
   python encode.py --file secret.txt --image input.png --key public.pem
   ```

   Example Output:
   ```
   Encoded 13 bytes into encoded_input.png
   Seed Size: 64 bytes
   ```

3. The resulting image `encoded_input.png` now contains your file!

### Example 2: Decoding the Encoded File

1. Decode the image to retrieve the hidden file.
   ```bash
   python decode.py --image encoded_input.png --output output.txt --key private.pem
   ```

   Example Output:
   ```
   File length: 13 bytes
   Seed decrypted successfully
   Decoded file saved to output.txt
   ```

2. Verify the decoded file.
   ```bash
   cat output.txt
   ```
   Output:
   ```
   Hello, CRIS!
   ```

---

## Contributing
Contributions are welcome! If you find any issues or want to suggest improvements, feel free to [open an issue](https://github.com/Lokray06/CRIS/issues) or submit a pull request.

---

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## References

- RSA Encryption: https://en.wikipedia.org/wiki/RSA_(cryptosystem)
- Steganography: https://en.wikipedia.org/wiki/Steganography

---

## Security Note
This implementation is for demonstration purposes and may not be suitable for production use. Using steganography and RSA encryption may not provide complete anonymity or security against advanced attacks.

---

## Author
- [Your Name] ([contact@jpgp.es])
