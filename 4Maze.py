#20/05/15
import pygame, random, datetime, math
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

#Gets a joystick input with optional timeout        
def joystick(timeout=-1):
    running = True    
    startTime = datetime.datetime.now()
    enterDown = False
    
    while running:        
        for event in pygame.event.get():
            if event.type == KEYUP:            
                jPressed = handle_event(event)
                if event.key == K_RETURN:
                    enterDown = False
                
                if enterDown != True:
                    running = False

            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    enterDown = True
                
            
        
        if timeout != -1:
            endTime = datetime.datetime.now()
            totalTime = endTime - startTime
            
            if totalTime.seconds >= timeout and enterDown == False:
                return "NONE"

            elif totalTime.seconds >= 3 and enterDown == True:
                pygame.quit()
                quit()
        
    return jPressed




def check_win():
    global characterLocation, winLocation

    if characterLocation == winLocation:
        ap.show_message("You won!")
        return True

    else:
        return False


def create_maze():
    global height, width, maze, winLocation

    winLocation = [random.randint(round(width/2),width+1),random.randint(1,height-2)]
    pointToCreate = []

    #Makes the maze without any sort of path
    for i in range(width):
        maze.append([])

    for col in range(2,width+3):
        for row in range(height):

            if  row == 0 or row == height-1 or col == width+2:
                maze[col].append("w")

            elif col%2 ==0 and row%2 == 0:
                maze[col].append("w")
                pointToCreate.append([col, row])

            else:
                maze[col].append("e")

    for locationToCreate in pointToCreate:
        direction = random.randint(1,4)

        if direction == 1:
            maze[locationToCreate[0]+1][locationToCreate[1]] = "w"

        elif direction == 2:
            maze[locationToCreate[0]-1][locationToCreate[1]] = "w"

        elif direction == 3:
            maze[locationToCreate[0]][locationToCreate[1]+1] = "w"

        elif direction == 4:
            maze[locationToCreate[0]][locationToCreate[1]-1] = "w"

    #Add the end point

    
    maze[winLocation[0]][winLocation[1]] = "o"
                     






def show_board(toShow):

    global characterLocation, characterShow, width, winLocation
    
    winCol = winLocation[0]
    yourCol = characterLocation[0]

    percentage = yourCol/winCol * 100

    if percentage > 100:
        percentageAway = 200 - percentage

    else:
        percentageAway = percentage

    numberNeedLighting = round(percentageAway / 12.5)

    ap.clear()

    for col in range(8):
        for row in range(7):
            if toShow[col][row] == "w":
                colour = [100,0,0]

            elif toShow[col][row] == "c":
                colour = 100,100,100

            elif toShow[col][row] == "o":
                colour = [0,100,0]

            else:
                colour = [0,0,0]

            ap.set_pixel(col, row, colour)

    for col in range(8):
        if col < numberNeedLighting:
            ap.set_pixel(col, 7, [100,100,51])


def does_hit(direction, area):

    if direction == "RIGHT":
        try:
            
            if maze[area[0]+1][area[1]] == "w":
                
                return True

        except IndexError:
            return True

    elif direction == "LEFT":
        try:
            if maze[area[0]-1][area[1]] == "w":
                return True

        except IndexError:
            return True

    elif direction == "UP":
        try:
            if maze[area[0]][area[1]-1] == "w":
                return True

        except IndexError:
            return True

    elif direction == "DOWN":
        try:
            if maze[area[0]][area[1]+1] == "w":
                return True

        except IndexError:
            return True

    else:
        return False

    return False



def move_board():
    global height, width, maze, characterLocation, characterShow

    direction = joystick(1)
    
    hitWall = does_hit(direction, characterLocation)

    characterShowMoved = False

    if not hitWall:       
        
        if direction == "UP":
            if characterLocation[1] != 0:
                characterLocation[1] -= 1
                if height-characterLocation[1] < 3 or characterLocation[1] < 3 or characterShow[1] < 3 or characterShow[1] > 3:
                    characterShow[1] -= 1
            
        elif direction == "DOWN":
            if characterLocation[1] != height:
                characterLocation[1] += 1
                if height-characterLocation[1] < 3 or characterLocation[1] < 3 or characterShow[1] < 3 or characterShow[1] > 3:
                    characterShow[1] += 1

        elif direction == "RIGHT":
            if characterLocation[0] != width:
                characterLocation[0] += 1
                if width - characterLocation[0] < 4 or characterLocation[0] < 3 or characterShow[0] < 3 or characterShow[0] > 3:                  
                    characterShow[0] += 1
                    

        elif direction == "LEFT":
            if characterLocation[0] != 0:
                characterLocation[0] -= 1
                if characterLocation[0] < 3 or width - characterLocation[0] < 4 or characterShow[0] < 3 or characterShow[0] > 3:                  
                    characterShow[0] -= 1

    toShow = []
    positionInList = -1


    colLow = characterLocation[0] - characterShow[0]
    colHigh = characterLocation[0] - characterShow[0] + 8

    rowLow = characterLocation[1] - characterShow[1]
    rowHigh = characterLocation[1] - characterShow[1] + 7
    
    for col in range(colLow, colHigh):
        toShow.append([])
        positionInList += 1
        for row in range(rowLow,rowHigh):
            toShow[positionInList].append(maze[col][row])

    toShow[characterShow[0]][characterShow[1]] = "c"

    show_board(toShow)

#Top is 0
#Bottom is height
maze = [[]]





height = 50
width = 100



for i in range(height):
    maze[0].append("w")

for i in range(1,3):
    maze.append([])
    for l in range(height):
        maze[i].append("e")



create_maze()

height = len(maze[0])-1
width = len(maze)-1

characterShow = [2,3]
characterLocation = [2,round(height/2)]

startTime = datetime.datetime.now()
while not check_win():
    move_board()
endTime = datetime.datetime.now()

fileObject = open("4Maze/data.txt", "a")
fileObject.write("\n"+str(startTime)+","+str(endTime-startTime))
fileObject.close()


        
