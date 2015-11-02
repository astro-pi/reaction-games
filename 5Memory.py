#30/05/15

import pygame, random, datetime, time
from pygame.locals import *
from astro_pi import AstroPi

ap = AstroPi()

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
                
            
        
        if timeout != -1:
            endTime = datetime.datetime.now()
            totalTime = endTime - startTime
            
            if totalTime.microseconds >= timeout:
                return "NONE"
        
    return jPressed

def see_moves(order, delay):
    global blueColour, redColour, greenColour, yellowColour

    show_board()
    time.sleep(0.5)

    for colour in order:
        if colour == "BLUE":
            blueColour = [0,0,255]
            show_board()
            time.sleep(delay)
            blueColour = [0,0,100]
            
        elif colour == "RED":
            redColour = [255,0,0]
            show_board()
            time.sleep(delay)
            redColour = [100,0,0]

        elif colour == "GREEN":
            greenColour = [0,255,0]
            show_board()
            time.sleep(delay)
            greenColour = [0,100,0]

        elif colour == "YELLOW":
            yellowColour = [255,255,0]
            show_board()
            time.sleep(delay)
            yellowColour = [100,100,0]

        show_board()
        time.sleep(0.2)

    ap.clear()
    time.sleep(0.5)


    
def make_moves(moves):
    global blueColour, redColour, greenColour, yellowColour

    delay = 0.5
    
    movesDone = []

    for i in range(moves):
        #Create a number to choose the colour
        colour = random.randint(0,3)

        if colour == 0:
            movesDone.append("BLUE")

        elif colour == 1:
            movesDone.append("RED")

        elif colour == 2:
            movesDone.append("GREEN")

        elif colour == 3:
            movesDone.append("YELLOW")

    return movesDone
            

def play_moves(level):
    global userLocation, X, lives

    state = True
    orderItShouldBe = make_moves(level)
    
    
    returnPressed = False
    
    while lives > 0:

        userInput = []

        delay = 0.5
        see_moves(orderItShouldBe, delay)
        
        for i in range(level):
            while not returnPressed:
                
                direction = joystick(0.4)
                
                if direction == "UP":
                    if userLocation[1] != 0:
                        userLocation[1] -= 1

                elif direction == "DOWN":
                    if userLocation[1] != 1:
                        userLocation[1] += 1

                elif direction == "RIGHT":
                    if userLocation[0] != 1:
                        userLocation[0] += 1

                elif direction == "LEFT":
                    if userLocation[0] != 0:
                        userLocation[0] -= 1

                elif direction == "RETURN":
                    if userLocation == [0,0]:
                        userInput.append("BLUE")

                    elif userLocation == [1,0]:
                        userInput.append("RED")

                    elif userLocation == [0,1]:
                        userInput.append("GREEN")

                    elif userLocation == [1,1]:
                        userInput.append("YELLOW")

                    returnPressed = True

                pointer = []
                
                if state: 
                    
                    userCol = userLocation[0] * 4
                    userRow = userLocation[1] * 4
                    
                    for col in range(4):
                        colToAdd = col + userCol
                        
                        for row in range(4):
                            rowToAdd = row + userRow
                            pointer.append([colToAdd, rowToAdd])

                    state = False

                         

                else:
                    state = True



                show_board(pointer)
            returnPressed = False

        if userInput == orderItShouldBe:
            return True

        else:
            ap.set_pixels(X)
            time.sleep(2)
            lives -= 1

    return False
    

def show_board(pointer = []):
    global blue, red, green, yellow
    global blueColour, redColour, greenColour, yellowColour


    pointerColour = [100,100,100]
    
    if pointer == []:
        pointerNeeded = False

    else:
        pointerNeeded = True

    for colours in range(4):
        if colours == 0:
            colour = blue
            penColour = blueColour

        elif colours == 1:
            colour = red
            penColour = redColour

        elif colours == 2:
            colour = green
            penColour = greenColour

        elif colours == 3:
            colour = yellow
            penColour = yellowColour
            
        
        for point in colour:
            ap.set_pixel(point[0], point[1], penColour)

    if pointerNeeded:
        for places in pointer:
            ap.set_pixel(places[0], places[1], pointerColour)
        

#These are the colours locations
blue = [[0,0],[0,1],[0,2],[0,3],
        [1,0],[1,1],[1,2],[1,3],
        [2,0],[2,1],[2,2],[2,3],
        [3,0],[3,1],[3,2],[3,3]]



red = [[4,0],[4,1],[4,2],[4,3],
       [5,0],[5,1],[5,2],[5,3],
       [6,0],[6,1],[6,2],[6,3],
       [7,0],[7,1],[7,2],[7,3]]



green = [[0,4],[0,5],[0,6],[0,7],
         [1,4],[1,5],[1,6],[1,7],
         [2,4],[2,5],[2,6],[2,7],
         [3,4],[3,5],[3,6],[3,7]]



yellow = [[4,4],[4,5],[4,6],[4,7],
          [5,4],[5,5],[5,6],[5,7],
          [6,4],[6,5],[6,6],[6,7],
          [7,4],[7,5],[7,6],[7,7]]


e = [0,0,0]
r = [100,0,0]
g = [0,100,0]

X = [r,e,e,e,e,e,e,r,
     r,r,e,e,e,e,r,r,
     e,r,r,e,e,r,r,e,
     e,e,r,r,r,r,e,e,
     e,e,e,r,r,e,e,e,
     e,e,r,r,r,r,e,e,
     e,r,r,e,e,r,r,e,
     r,r,e,e,e,e,r,r]

W = [e,e,e,e,e,e,e,e,
     e,e,e,e,e,e,e,g,
     e,e,e,e,e,e,g,g,
     e,e,e,e,e,g,g,e,
     g,e,e,e,g,g,e,e,
     g,g,e,g,g,e,e,e,
     e,g,g,g,e,e,e,e,
     e,e,g,e,e,e,e,e]



lives = 3


#These are the actual colours
blueColour = [0,0,100]
redColour = [100,0,0]
greenColour = [0,100,0]
yellowColour = [100,100,0]

ap.clear()
show_board()
userLocation = [0,0]
level = 2

while play_moves(level):
    level+=1
    ap.set_pixels(W)
    time.sleep(2)

print("You completed",level-1,"Levels!")
fileObject = open("5Memory/data.txt", "a")
fileObject.write("\n"+str(datetime.datetime.now())+","+str(level))
fileObject.close()
