import cv2
import numpy as np
from PIL import Image, ImageDraw,ImageFont

def pic(h, w, color):
   image = Image.new("RGB", (h, w),color)
   return image

def avg(path, size):
    # Read the image
    image = cv2.imread(path)

    # Convert the image to RGB color space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get the image dimensions
    height, width, _ = image.shape

    # Initialize empty lists to store the average colors and coordinates
    avg = []
    cords = []

    # Loop through the image rows from bottom to top
    for y in range(height - 1, -1, -size):
        # Loop through the image columns from left to right
        for x in range(0, width, size):
            # Initialize variables to calculate the sum of RGB values
            redTotal = 0
            greenTotal = 0
            blueTotal = 0

            # Loop through the pixels in the current square
            for j in range(y, max(y - size, -1), -1):
                for i in range(x, min(x + size, width)):
                    # Get the RGB values of the current pixel
                    red, green, blue = image[j, i]

                    # Accumulate the RGB values
                    redTotal += red
                    greenTotal += green
                    blueTotal += blue

            # Calculate the average RGB values for the current square
            pixels = min(size, width - x) * min(size, y + 1)
            redAvg = redTotal // pixels
            greenAvg = greenTotal // pixels
            blueAvg = blueTotal // pixels

            # Add the average color and coordinates to the lists
            avg.append((redAvg, greenAvg, blueAvg))
            cords.append((x, y))

    return avg, cords

# Example usage
path = 'Images/house.jpeg'
size = 50  # Size of the square (change it to your desired value)
avg, cords = avg(path, size)

image = cv2.imread(path)
height, width, _ = image.shape

white = pic(height, width, (255, 255, 255))

draw = ImageDraw.Draw(white)
 
for square, (color, coordinates) in enumerate(zip(avg, cords)):
    #print(f"Square {square + 1} - Average Color: {color}, Coordinates: {coordinates}")
    draw.ellipse((coordinates[0]-size, coordinates[1]-size,coordinates[0]+size, coordinates[1]+size),fill=color)
white.show()