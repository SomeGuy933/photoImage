import cv2
import numpy as np
from PIL import Image, ImageSequence,ImageDraw
import random
from tqdm import tqdm
import time
import multiprocessing

def pic(h, w, color):
    image = np.ones((h, w, 3), dtype=np.uint8)
    image[:, :] = (color[0], color[1], color[2])
    return image
def avgColor(path, size):
    # Read the image
    image = cv2.imread(path)

    # Convert the image to RGB color space
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Get the image dimensions
    height, width, _ = image.shape

    # Initialize empty lists to store the average colors and coordinates
    avg = []
    cords = []

    #bottom to top
    for y in range(height - 1, -1, -size):
        #left to right
        for x in range(0, width, size):

            redTotal = 0
            greenTotal = 0
            blueTotal = 0

  
            for j in range(y, max(y - size, -1), -1):
                for i in range(x, min(x + size, width)):

                    red, green, blue = image[j, i]

                   
                    redTotal += red
                    greenTotal += green
                    blueTotal += blue

           
            pixels = min(size, width - x) * min(size, y + 1)
            redAvg = redTotal // pixels
            greenAvg = greenTotal // pixels
            blueAvg = blueTotal // pixels


            avg.append((redAvg, greenAvg, blueAvg))
            cords.append((x, y))

    return avg, cords

    
def doIt(path,thiCCness = 1,gif = True, randomize = False, fps = 5, save = 'animation', show = False, threshold1 = int(0.3 * 255), threshold2 = int(0.7 * 255), drawColor = False,rez = 25):
    # Read the image
    
    color = (0,0,0)
    
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, threshold1, threshold2)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Create a blank white image
    height, width, _ = image.shape
    white = pic(height, width, (255, 255, 255))

    
    picToShow = Image.fromarray(white)
    if drawColor:

        avg, cords = avgColor(path, rez)
        draw = ImageDraw.Draw(picToShow)       
        counter = 0
        
        for square, (c, coordinates) in enumerate(zip(avg, cords)):
            #print(f"Square {square + 1} - Average Color: {color}, Coordinates: {coordinates}")
            draw.ellipse((coordinates[0]-rez, coordinates[1]-rez,coordinates[0]+rez, coordinates[1]+rez),fill=c)
   
        white = np.array(picToShow)
        

    cv2.drawContours(white, contours, -1, color, thiCCness)
    picToShow = Image.fromarray(white)
    print(save)
    picToShow.save(save)
    white = pic(height, width, (255, 255, 255))
          
    frames = []

    counter = 0
    
    amountOfContours = len(contours)



