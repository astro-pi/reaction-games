#05/06/15
import pygame, random, datetime, math, os, time
from pygame.locals import *
from astro_pi import AstroPi
ap = AstroPi()


ap.clear()

pygame.init()
pygame.display.set_mode((640, 480))


#Handle the joystick input
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
    if timeout != -1:
        timeout = timeout * 1000000
    
    startTime = datetime.datetime.now()
    while running:        
        for event in pygame.event.get():
            if event.type == KEYUP:            
                jPressed = handle_event(event)
                running = False

            if event.type == QUIT:
                pygame.quit()
                quit()
                
            
        
        if timeout != -1:
            endTime = datetime.datetime.now()
            totalTime = endTime - startTime
            
            if totalTime.microseconds >= timeout:
                return "NONE"
        
    return jPressed

def load_animations():
    global pixels, animationNames, gameNames
    
    directory = os.getcwd()
    
    animationNames = sorted(os.listdir(directory))
    gameNames = []

    for file in os.listdir(directory):
        print(file)
        for char in range(len(file)):
            if file[char] == ".":
                animationNames.remove(file)


        if file[len(file)-3:len(file)] == ".py":
            if file[0:4] != "Main":
                gameNames.append(file)

    gameNames = sorted(gameNames)
    pixels = []

    for i in range(len(animationNames)):

        toStore = []
        pixels.append([])

        frames = sorted(os.listdir(animationNames[i]))


        for frame in range(len(frames)-1):
            #Arrange into rows and colums
            frameNow = ap.load_image(animationNames[i]+"/"+str(frame+1)+".png", False)

            if animationNames[i] != "8Shutdown":
                frameNow[i*8] = [255,255,255]
                for loc in range(8):
                    frameNow[(loc*8)+1] = [255,0,0]

            pixels[i].append(frameNow)


def show_animation(name, always=True):
    global pixels, animationNames
    game = animationNames.index(name)

    if always:
        while True:
            for i in range(len(pixels[game])):
                ap.set_pixels(pixels[game][i])
                direction = joystick(0.3)

                if direction != "RIGHT" and direction != "LEFT" and direction != "NONE":
                    print(direction)
                    return direction

    else:
        for i in range(len(pixels[game])):
            ap.set_pixels(pixels[game][i])
            direction = joystick(0.3)

ap.clear()
load_animations()
selected = False
menu = 0
notQuit = True

while notQuit:
    while not selected:
        
        direction = show_animation(animationNames[menu])
        
        if direction == "UP" and menu != 0:
            menu -= 1

        elif direction == "DOWN" and menu != 7:
            menu += 1

        elif direction == "RETURN":
            selected = True

    if menu == 7:
        notQuit = False
        break

    pygame.quit()
    os.system("python3 "+gameNames[menu])
    pygame.init()
    pygame.display.set_mode((640, 480))
    selected = False

show_animation(animationNames[menu], False)
pygame.quit()
os.system("shutdown -s -t 1")
