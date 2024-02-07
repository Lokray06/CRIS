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
    for i in range(len(file.read())):
    
        #Reading the first byte of the set
        file.seek(offset)
        byte1 = int.from_bytes(file.read(1), "big")
        offset += 1

        #Reading the second byte of the set
        file.seek(offset)
        byte2 = int.from_bytes(file.read(2), "big")
        offset += 1
    
        #Reading the third byte of the set 
        file.seek(offset)
        byte3 = int.from_bytes(file.read(3), "big")
        offset += 1
        
        #Setting the pixel
        pixel = (byte1, byte2, byte3)
        pixelCoords = (random.randint(0,imgX), random.randint(0,imgY))
        img.putpixel(pixelCoords, pixel)
    
        #Writing the pixel in the lookuptable
        dataCoordinates.append(pixelCoords)
        print(pixel)
print(dataCoordinates)