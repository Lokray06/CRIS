from PIL import Image

resultImagePath = "image1.png"
outputFilePath = "reconverted_file"

# Read coordinates from the file and parse the string representation of the list
with open("dataCoordinates", "r") as f:
    dataCoordinates = eval(f.read())

img = Image.open(resultImagePath)
imgX, imgY = img.size

reconverted_data = bytearray()

for x, y in dataCoordinates:
    pixel = img.getpixel((x, y))
    reconverted_data.extend([pixel[0], pixel[1], pixel[2]])

with open(outputFilePath, "wb") as output_file:
    output_file.write(reconverted_data)
