# Data Encryption and Decryption into image

## Overview

This Python program provides a simple and effective method for encrypting and decrypting files using images. The process involves embedding the contents of a file into an image, creating a visually identical but modified image. The reverse operation extracts the original file from the modified image, restoring it to its initial state.

## How It Works

### File into Image Conversion

The encryption process begins by opening the target file in binary mode and reading it in sets of three bytes. Each set represents the RGB color values of a pixel in an image. The script then randomly selects a pixel in the image and alters its color based on the byte values. The coordinates of the modified pixels are stored in an array.

```python
# Example of converting a set of three bytes into an RGB color
pixel = (byte1, byte2, byte3, 0)  # Setting alpha channel to 0 for full transparency
pixelCoords = (random.randint(0, imgX - 1), random.randint(0, imgY - 1))
img.putpixel(pixelCoords, pixel)
dataCoordinates.append(pixelCoords)
open("dataCoordinates", "w").write(str(dataCoordinates))
