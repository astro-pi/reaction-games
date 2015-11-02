import pygame, random, datetime
import time as ti
from pygame.locals import *
from astro_pi import AstroPi

ap = AstroPi()

pygame.init()
pygame.display.set_mode((640, 480))

def handle_event(event):
    if event.key == pygame.K_DOWN:
        return "DOWN"
        
    elif event.key == pygame.K_UP:
        return "UP"
        
    elif event.key == pygame.K_LEFT:
        return "LEFT"
        
    elif event.key == pygame.K_RIGHT:
        return "RIGHT"
        
    elif event.key == pygame.K_RETURN:
        return "RETURN"
    
#Gets a joystick input with optional timeout        
def joystick(timeout=-1):
    running = True    
    startTime = datetime.datetime.now()
    while running:        
        for event in pygame.event.get():
            if event.type == KEYUP:            
                jPressed = handle_event(event)
                running = False
                
            
        
        if timeout != -1:
            endTime = datetime.datetime.now()
            totalTime = endTime - startTime
            
            if totalTime.seconds >= timeout:
                return "NONE"
        
    return jPressed

def countdown():
    colour = [100,0,0]

    ap.clear()
    ap.show_message("3 2 1",0.125, colour)
    randomWait = random.randint(0,5)

    if joystick(randomWait) != "NONE":
        return True

    else:
        return False



#GAMES
def reaction():
    global direction

    b = [0,0,0]
    p = [0,100,100]
    

    UP = [b,b,b,p,p,b,b,b,
          b,b,p,p,p,p,b,b,
          b,p,p,p,p,p,p,b,
          b,b,b,p,p,b,b,b,
          b,b,b,p,p,b,b,b,
          b,b,b,p,p,b,b,b,
          b,b,b,p,p,b,b,b,
          b,b,b,p,p,b,b,b]

    DOWN=[b,b,b,p,p,b,b,b,
          b,b,b,p,p,b,b,b,
          b,b,b,p,p,b,b,b,
          b,b,b,p,p,b,b,b,
          b,b,b,p,p,b,b,b,
          b,p,p,p,p,p,p,b,
          b,b,p,p,p,p,b,b,
          b,b,b,p,p,b,b,b]

    LEFT=[b,b,b,b,b,b,b,b,
          b,b,p,b,b,b,b,b,
          b,p,p,b,b,b,b,b,
          p,p,p,p,p,p,p,p,
          p,p,p,p,p,p,p,p,
          b,p,p,b,b,b,b,b,
          b,b,p,b,b,b,b,b,
          b,b,b,b,b,b,b,b]

    RIGHT=[b,b,b,b,b,b,b,b,
           b,b,b,b,b,p,b,b,
           b,b,b,b,b,p,p,b,
           p,p,p,p,p,p,p,p,
           p,p,p,p,p,p,p,p,
           b,b,b,b,b,p,p,b,
           b,b,b,b,b,p,b,b,
           b,b,b,b,b,b,b,b]

    direction = random.randint(0,3)
    startTime = datetime.datetime.now()
    notPressed = True
    
    if direction == 0:
        ap.set_pixels(UP)

    elif direction == 1:
        ap.set_pixels(DOWN)

    elif direction == 2:
        ap.set_pixels(LEFT)

    else:
        ap.set_pixels(RIGHT)


    while notPressed:
        pressed = joystick()
        if direction == 0:
            if pressed == "UP":
                direction = "UP"
                notPressed = False
                
        elif direction == 1:
            if pressed == "DOWN":
                direction = "DOWN"
                notPressed = False

        elif direction == 2:
            if pressed == "LEFT":
                direction = "LEFT"
                notPressed = False

        elif direction == 3:
            if pressed == "RIGHT":
                direction = "RIGHT"
                notPressed = False

    
    endTime = datetime.datetime.now()
    totalTime = endTime - startTime

    timeTaken = (totalTime.seconds * 1000000) + totalTime.microseconds

    print(timeTaken/1000,"miliseconds")
    return timeTaken/1000

for i in range(3):
    playing = True
    while playing:
        cheat = countdown()
        if not cheat:
            time = reaction()
            ap.show_message(str(time), text_colour=[100,0,0])
            playing = False

        else:
            ap.show_message("Too Quick")
            playing = True

    fileObject = open("1Reaction/data.txt","a")
    toWrite = "\n"+str(datetime.datetime.now())+","+str(time)+","+direction
    fileObject.write(toWrite)
    fileObject.close()


pygame.quit()
