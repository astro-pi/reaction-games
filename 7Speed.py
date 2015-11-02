import pygame, random, datetime, time, math
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
#This version of the of joystick checks the time regularaly which is less efficient
#But that allows for a higher degree of accuracy which was needed as the speed of
#The ball is relatively high
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
                
            
        
        if timeout != -1:
            endTime = datetime.datetime.now()
            totalTime = endTime - startTime
            
            if totalTime.microseconds >= timeout:
                return "NONE"
        
    return jPressed




def create_new():
    global endLocation, location, height

    length = random.randint(6,9)
    height = length

    base = []
    for row in range(height):
        base.append([])
        for col in range(maxWidth):
            base[row].append("w")


    #Creates new track
    for row in range(-1,height):
        for l in range(-1,2):
            base[height-2-row][location+l] = "e"


    if location + length >= maxWidth-4:
        direction = "LEFT"

    elif location - length <= 0+4:
        direction = "RIGHT"

    else:
        point = random.randint(1,3)
        if point == 1:
            direction = "RIGHT"

        elif point == 2:
            direction = "LEFT"

        else:
            direction = "UP"

    for row in range(height-2):
        for i in range(length+1):
            if direction == "RIGHT":
                base[row][location-1+i] = "e"

            elif direction == "LEFT":
                base[row][location+1-i] = "e"

    if direction == "RIGHT":
        location += length-2
        
    elif direction == "LEFT":
        location -= length-2

    elif direction == "UP":
        height = 6


    return base

        


def main():
    global board, location, locationY, moves, timeDelay, locationOfCharacter


    if moves % 10 == 0:
        timeDelay -= round((timeDelay/100)*7, 2)

    create_board()
    dead = print_board()

    timeRemaining = timeDelay

    if not dead:
        while timeRemaining >= 0:

            startTime = datetime.datetime.now()

            direction = joystick(timeRemaining)

            if direction == "RIGHT":
                if board[locationY][locationOfCharacter+1] != "w":
                    locationOfCharacter += 1
                    print_board()

            elif direction == "LEFT":
                
                if board[locationY][locationOfCharacter-1] != "w":
                    locationOfCharacter -= 1
                    print_board()

            
            endTime = datetime.datetime.now()
            finalTime = endTime - startTime
            
            timeRemaining -= finalTime.microseconds/1000000

        board.pop(0)
        create_board()
        print_board()
        moves += 1

    else:
        return True


def create_board():
    global board, height
    
    while len(board)<10:
        toAdd = create_new()
        
        for row in range(height):
            board.append(toAdd[height-1-row])

    


def print_board():
    global locationOfCharacter, board, locationY      



    for row in range(8):
        printingCol = 0
        for col in range(locationOfCharacter-3, locationOfCharacter+5):

            if [7-row,col] == [locationY,locationOfCharacter]:
                if board[7-row][col] == "w":
                    return True

                else:
                    board[7-row][col] = "o"

                                        
            if board[7-row][col] == "w":
                colour = [100,0,0]

            elif board[7-row][col] == "e":
                colour = [0,0,0]

            elif board[7-row][col] == "o":
                colour = [0,100,0]

            ap.set_pixel(printingCol, row, colour)

            printingCol += 1





maxWidth = 41

location = math.ceil(maxWidth/2)

locationOfCharacter = math.ceil(maxWidth/2)
locationY = 1

moves = 0
timeDelay = 0.3

endLocation = location

board = []

height = 8


dead = False

startTime = datetime.datetime.now()

while not dead:
    dead = main()

endTime = datetime.datetime.now()
finalTime = endTime - startTime

fileObject = open("7Speed/data.txt", "a")
fileObject.write("\n"+str(startTime)+","+str(finalTime))
fileObject.close()











