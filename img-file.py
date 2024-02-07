from PIL import Image

resultImagePath = "image1.png"
outputFilePath = "reconverted_file"

dataCoordinates = [(12, 190), (361, 73), (485, 429), (131, 50), (506, 497)]

img = Image.open(resultImagePath)
imgX = img.width
imgY = img.height

reconverted_data = bytearray()

for coord in dataCoordinates:
    x, y = coord
    pixel = img.getpixel((x, y))
    reconverted_data.extend([pixel[0], pixel[1], pixel[2]])

with open(outputFilePath, "wb") as output_file:
    output_file.write(reconverted_data)