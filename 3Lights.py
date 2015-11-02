#19/05/15
import pygame, random, datetime, time
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
                
        endTime = datetime.datetime.now()
        totalTime = endTime - startTime
        
        if timeout != -1:
            if totalTime.seconds >= timeout:
                return "NONE"
        
    return jPressed

#Print the board onto the pi
def print_board(pointer): 
        
    lightOn = [155,155,31]
    lightOff = [0,0,0]
    blueLight = [155,0,155]
    pointerColour = [155,155,155]
    
    for row in range(boundaryStart,boundaryEnd):
        for col in range(boundaryStart, boundaryEnd):
            pos = fullBoard[row][col]
            pointerPos = pointer[row][col]
            
            if pos == 1:
                ap.set_pixel(row, col, lightOn)

            elif pos == 0:
                ap.set_pixel(row, col, lightOff)

            elif row == 3 and col == boundaryStart:
                ap.set_pixel(row, col, blueLight)

            if pointerPos == 1:
                ap.set_pixel(row, col, pointerColour)


def check_move(position):
    global pointerMiddle
    
    if position >= boundaryStart and position < boundaryEnd:
            return True

    elif position >= boundaryStart-1 and pointerMiddle[1] == 4:
        return True

    return False

def check_win():
    
    for i in range(boundaryStart, boundaryEnd):
        for l in range(boundaryStart, boundaryEnd):
            if fullBoard[i][l] == 1:
                return False

    return True
            

def change_board(location):
    
    if check_move(location[0]-1):
        state = fullBoard[location[0]-1][location[1]]
        fullBoard[location[0]-1][location[1]] = 1 - state

    if check_move(location[0]+1):
        state = fullBoard[location[0]+1][location[1]]
        fullBoard[location[0]+1][location[1]] = 1 - state

    if check_move(location[1]-1):
        state = fullBoard[location[0]][location[1]-1]
        fullBoard[location[0]][location[1]-1] = 1 - state

    if check_move(location[1]+1):
        state = fullBoard[location[0]][location[1]+1]
        fullBoard[location[0]][location[1]+1] = 1 - state

    state = fullBoard[location[0]][location[1]]
    fullBoard[location[0]][location[1]] = 1 - state
        
   


def move_pointer(state):
    global moves, pointerMiddle
    
    #Move the pointer
    direction = joystick(0.67)

    if direction == "UP":
        if check_move(pointerMiddle[1]-1):
            pointerMiddle[1] -= 1              
                    
    elif direction == "DOWN":
        if check_move(pointerMiddle[1]+1):
            pointerMiddle[1] += 1
            
    elif direction == "RIGHT":
        if check_move(pointerMiddle[0]+1):
            pointerMiddle[0] += 1
            
    elif direction == "LEFT":
        if check_move(pointerMiddle[0]-1):
            pointerMiddle[0] -= 1
            
    elif direction == "RETURN":
        moves += 1
        if pointerMiddle[0] < boundaryStart:
            pygame.quit()
            quit()

        change_board(pointerMiddle)



    #Updates the pointer list
    pointer = [[0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0],
               [0,0,0,0,0,0,0,0]]
    
    pointer[pointerMiddle[0]][pointerMiddle[1]] = 1 * state
    
    if check_move(pointerMiddle[0]-1):
        pointer[pointerMiddle[0]-1][pointerMiddle[1]] = 1 * state

    if check_move(pointerMiddle[0]+1):
        pointer[pointerMiddle[0]+1][pointerMiddle[1]] = 1 * state

    if check_move(pointerMiddle[1]-1):
        pointer[pointerMiddle[0]][pointerMiddle[1]-1] = 1 * state

    if check_move(pointerMiddle[1]+1):
        pointer[pointerMiddle[0]][pointerMiddle[1]+1] = 1 * state

    
    print_board(pointer)

    if state == 1:
        return 0

    else:
        return 1
        

global pointerMiddle, fullBoard, boundaryStart, boundaryEnd, moves
moves = 0

pointerMiddle = [3,3]
boundaryStart = 1
boundaryEnd = 6
fullBoard = []

def make_new():
    #Allows you to cheat if you are on a computer and works out minimum number of moves
    coordinates = []
    ordered = []

    
    #Create the board
    for i in range(8):

        #Make 8 rows so it's easier to calculate positions that need changing
        fullBoard.append([])

        
        for l in range(8):
            #Make them all off so when puzzle created, solution is availiable
            fullBoard[i].append(0)

    #Make the puzzle
    for i in range(32):

        #The boundary means it only creates the puzzle inside the level bounds
        randRow = random.randint(boundaryStart,boundaryEnd-1)
        randCol = random.randint(boundaryStart,boundaryEnd-1)
        randomLoc = [randRow, randCol]
        coordinates.append(randomLoc)

        #Simulate a user pressing the buttons as then the puzzle is definitely
        #Solvable
        change_board(randomLoc)



    #Initialises the flashing pointer
    state = 0

    #Clear the board
    ap.clear()

    red = [155,0,0]
    blue = [0,0,155]

    #Makes the boar the red colour
    #Only need to change the pixels once instead of every click as the only part of
    #The board that changes is the boundary. This is more efficient and easier
    for row in range(8):
        for col in range(8):            
            if row == 0 and col == 4:
                ap.set_pixel(row, col, blue)

            else:
                ap.set_pixel(row, col, red)
                       


    playing = True
    ordered = sorted(coordinates)

    number = []
    count = 0
    previous = [-1,-1]

    #Find irrelevant moves
    for i in ordered:
        
        if i != previous:
            previous = i
            number.append(count)
            count = 1

        else:
            count += 1

    number.append(count)
    number.pop(0)

    removeFrom = 0
    
    for number in number:
        if number % 2 == 0:
            for i in range(number):
                ordered.pop(removeFrom)

        else:
            for i in range(number -1):
                ordered.pop(removeFrom)
                
            removeFrom += 1

    print(ordered)
    minMoves = len(ordered)
    
    
    
    while playing:

        #move_pointer(x) returns the state the pointer needs to be changed to
        state = move_pointer(state)
        if check_win():
            playing = False


    #If the user beats the round show that message
    ap.show_message("You won!")

    return minMoves


#Initialises all the statistics that I will be using
level = 0
startTimeV = datetime.datetime.now()
totalMoves = 0
time = []
moveLevel = []
minMoves = []
level = 1

fileObject = open("3Lights/data.txt","a")
fileObject.write(str(datetime.datetime.now()))

#This will make the 3 rounds and increment the boundary accordingly
#The boundary is a global variable and can therefore be seen in all
#Function. It also updates all statistics

startTime = datetime.datetime.now()
minMoves = make_new()
endTime = datetime.datetime.now()
time.append(endTime-startTime)

#Time taken, level, made in moves, moves made
fileObject.write("\n        "+str(endTime-startTime)+","+str(minMoves)+","+str(moves))
fileObject.close()

