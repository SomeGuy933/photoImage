import cv2
import numpy as np
from PIL import Image, ImageSequence,ImageDraw
import random
from tqdm import tqdm
import time
import multiprocessing
multiprocessing.set_start_method('spawn', True)

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

def offSet(rows,frames,rez, off = 0,):
    
    amount = 0
    should = 0
    
    inc = rows/frames + off

    for i in range(frames):
        if amount > 1:
            should += 1
            amount = 0
        amount += inc
    
    if should < (rows+1):
        return offSet(rows,frames, rez, off+0.0005)
    else:
        return(off)
    
    
    
def doIt(path, color = (0,0,0),thiCCness = 1,gif = True, randomize = False, fps = 5, save = 'animation', show = False, threshold1 = int(0.3 * 255), threshold2 = int(0.7 * 255), drawColor = False,rez = 25):
    # Read the image
    
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
    
    
    
    if show:
        picToShow.show()
    picToShow.save(f"Final/{save}.jpeg")
    white = pic(height, width, (255, 255, 255))
          
    frames = []

    counter = 0
    
    amountOfContours = len(contours)
    print(f"Contours: {amountOfContours}")
    if gif:
        white = pic(height, width, (255, 255, 255))
        start = 0

        
        if randomize:
         # Convert contours from tuples to lists
            contours = [contour.tolist() for contour in contours]
            # Randomize the order of contours
            random.shuffle(contours)
            # Convert contours back from lists to tuples
            contours = [np.array(contour) for contour in contours]
        if drawColor:
            avg, cords = avgColor(path, rez)
            amountOfContours = len(contours)
            amountOfRows = (height) // rez
            
            print(f"Amount of rows: {amountOfRows}")
            
            
            
        
            colorUpdate = amountOfRows / amountOfContours + offSet(amountOfRows,amountOfContours, rez)
            colorCounter = .9
            print(f"offset: {offSet(amountOfRows,amountOfContours,rez)}")
            
            
            with tqdm(total=len(contours), desc="Processing contours and color") as pbar:
                for contour in contours:
               
                    if colorCounter >= (1):
                        # Draw the current contour on the white image
                        picToShow = Image.fromarray(white.copy())
                        draw = ImageDraw.Draw(picToShow)

                        # Calculate the row index to add colors to
                        start_idx = start
                        end_idx = start_idx + 1

                        # Add colors to the current row
                        for row in range(start_idx, end_idx):
                            row_start = row * (width // rez)
                            row_end = row_start + (width // rez)

                            # Add colors to the squares in the current row
                            for square, (c, coordinates) in enumerate(zip(avg[row_start:row_end], cords[row_start:row_end]), start=row_start):
                                draw.ellipse((coordinates[0] - rez, coordinates[1] - rez, coordinates[0] + rez, coordinates[1] + rez), fill=c)

                            white = np.array(picToShow)
                            
                        
                        colorCounter = 0
                        start += 1
                    colorCounter += colorUpdate
                    cv2.drawContours(white, [contour], -1, color, thiCCness)

                    # Create a copy of the image and store it in the frames list
                    
                    if counter % fps == 0:
                        frames.append(Image.fromarray(white.copy()))
                    counter += 1
                    pbar.update()

        else:
            with tqdm(total=len(contours), desc="Processing contours") as pbar:
                for contour in contours:

                    # Draw the current contour on the white image
                    cv2.drawContours(white, [contour], -1, (0, 0, 0), thiCCness)

                    # Create a copy of the image and store it in the frames list
                    if counter % fps == 0:
                        frames.append(Image.fromarray(white.copy()))
                    counter += 1
                    pbar.update()

        cv2.drawContours(white, contours, -1, color, thiCCness)
        print(f"Actual: {start}")
        for i in range(40):
            frames.insert(0, Image.fromarray(white.copy()))
        print(len(frames))
        print("Saving")
        
        frames[0].save(f"Gifs/{save}.gif", format='GIF', save_all=True, append_images=frames[1:], duration=20, loop=0)
        frames.clear()
       
        cv2.destroyAllWindows()
    print("Done")



#doIt('Images/grad.jpeg',gif = False, drawColor = True,rez = 5, fps = 5, show = False,save= "grad",threshold1 = int(0.3 * 255), threshold2 = int(0.7 * 255),thiCCness=1)
#doIt('Images/bird.jpeg',gif = False, drawColor = True,rez = 5, fps = 5, show = False,save= "bird",threshold1 = int(0.6 * 255), threshold2 = int(0.3 * 255),thiCCness=2)
doIt('Images/lamp.jpeg',gif = True, drawColor = True,rez = 1, fps = 5, show = False,save= "final",threshold1 = int(0.5 * 255), threshold2 = int(0.5 * 255),thiCCness=1)


#doIt('Images/car.jpeg',gif= False,drawColor = True,show = True,save= "car",threshold1 = int(0.5 * 255), threshold2 = int(0.7 * 255),thiCCness=3)


#doIt('Images/hotel.jpeg',gif= True,drawColor = True,show = True,fps = 7,save= "hotel",threshold1 = int(0.3 * 255), threshold2 = int(0.5 * 255),thiCCness=2)
#70%