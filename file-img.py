from PIL import Image
import random

filePath = "file"
imagePath = "image.png"
img = Image.open(imagePath)
imgX = img.width
imgY = img.height
offset = 0
dataCoordinates = []

with open(filePath, "rb") as file:
    for i in range(0, len(file.read()), 3):
        # Reading the first byte of the set
        file.seek(offset)
        byte1 = int.from_bytes(file.read(1), "big")
        offset += 1

        # Reading the second byte of the set
        file.seek(offset)
        byte2 = int.from_bytes(file.read(1), "big")
        offset += 2  # Fix: Increment by 2 instead of 1

        # Reading the third byte of the set
        file.seek(offset)
        byte3 = int.from_bytes(file.read(1), "big")
        offset += 3  # Fix: Increment by 3 instead of 1

        # Setting the pixel
        pixel = (byte1, byte2, byte3)
        pixelCoords = (random.randint(0, imgX - 1), random.randint(0, imgY - 1))  # Fix: Adjusted coordinates range
        img.putpixel(pixelCoords, pixel)

        # Writing the pixel in the lookuptable
        dataCoordinates.append(pixelCoords)
        print(pixel)

print(dataCoordinates)
img.save("image1.png")