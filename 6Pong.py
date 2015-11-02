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


#I made this to tell me if the ball would be able to move and
#If not able to, what it hit
def in_boundary(col, row):
    global batMiddle, ballLocation


    #Check if at top of board
    if row < 0:
        return "BOARD", "TOP"
    
    #Check if at the bottom of the board
    elif row > 7:
        return "BOARD", "BOTTOM"

    #Check if it hit the side of the board
    elif col > 7:
        return "BOARD", "SIDE"
    

    #This check to see if it hit the bat
    if col == 0:
        #If it hit the bat on a direct hit then return board as same angle
        #change applies
        if ballLocation[1] == batMiddle:
            return "BOARD", "SIDE"

        #This checks to see if it would have hit the bat from the top or bottom
        #I added this becasue it allows for more game variety
        elif row == batMiddle:

            #Check if it cam from above the bat
            if row > ballLocation[1]:
                return "BAT", "TOP"

            #If it didn't hit the top it hit the bottom
            else:
                return "BAT", "BOTTOM"

    #If it doesn't hit anything allow it to move
    return "FALSE", "FALSE"

def teleport_pixels(colour):
    for i in range(2):
        ap.set_pixel(teleportLocations[i][0], teleportLocations[i][1], colour)

#Create a teleporter so you don't catch on too quick that there is an easy way to win
#Also makes the game kinda hard becasue you have to think about if
#The ball would go through a teleporter
def create_teleport():
    global ballLocation, teleportLocations


    #Initialises the variables that will check of the location of the teleporter
    #Has been created
    startPlaced = False
    endPlaced = False
    bothPlaced = False


    #This will create the locations of the teleporters
    while not bothPlaced:
        #Chooses a random location but cannot be created in the bat area
        randomCol = random.randint(1,7)
        randomRow = random.randint(0,7)

        #As there are two paths the ball can follow throughout the game as it is on
        #An 8 by 8 grid and cannot do angles as a result it creates one teleport
        #On one path and another on the other path. This allows for you to always
        #Be in line for a teleport

        if (randomRow + randomCol) % 2 == 0:
            teleportLocations[0] = [randomCol, randomRow]
            startPlaced = True
            
        else:
            teleportLocations[1] = [randomCol, randomRow]
            endPlaced = True

        #If both have alocation to be then break from the loop
        if startPlaced and endPlaced:
            bothPlaced = True
        

    #Show the user where the teleports are by making a purple pixel
    teleport_pixels([155,0,155])


#I used this to check and change the location of the users bat
def update_bat(direction):
    global batMiddle

    #If the user wanted to go up it will check to see it it is already at the bottom
    if direction == "UP":
        if batMiddle-1 >= 0:

            #If it is not at the bottom then change where the bat is
            ap.set_pixel(0,batMiddle,[0,0,0])
            batMiddle -= 1

    elif direction == "DOWN":
        if batMiddle+1<8:
            #visa versa
            ap.set_pixel(0,batMiddle,[0,0,0])
            batMiddle+=1

    #Did this out of the if statements for efficiency
    ap.set_pixel(0,batMiddle,[100,100,100])

    

def change_angle(angle, board, side):

    #Reason for different sides is because
    #different formula required for some to mirror angle
    if board == "BOARD":        
        if side == "SIDE":
            
            angle = (360-(angle-180)) % 360

            #This stops an easy win where the ball bounces back and forth
            if angle == 0:
                direction = random.randint(0,1)
                if direction == 0:
                    angle = 45

                elif direction == 1:
                    angle = 315

        elif side == "TOP":
            
            #This stops an easy win and occurs when the bat has not been
            #Directily hit
            if angle == 90:
                direction = random.randint(0,1)
                if direction == 0:
                    angle = 225

                elif direction == 1:
                    angle = 315

            else:
                angle = (360 - angle) % 360

        elif side == "BOTTOM":
            #This stops an easy win occurs when not hit bat directly
            if angle == 270:
                direction = random.randint(0,1)
                if direction == 0:
                    angle = 45

                elif direction == 1:
                    angle = 135

            else:
                angle = (360 - angle) % 360

            

    elif board == "BAT":

        #If the ball hit the bat on the top change the angle so it goes straight
        #Up
        if side == "TOP":
            angle = 90

        else:
            #Or down
            angle = 270

    return angle
        
def check_move_ball():
    
    global ballLocation, angle

    #Starts an infinite loop and uses a break to return the value
    #I used a loop here because if the ball hit's a corner it will need to
    #Re-check the angle it can go or it will mess up
    
    while True:

        #The reason I had to use so much code here is becasue to make a formula
        #To figure out the move would have used just as much space and was therefore
        #Pointless. You can't use other angles i.e. 30 degrees as it is on an 8 by 8
        #And after doing the math multiples of 45 seemed to be the only reasonable
        #Option.
        
        if angle == 0:
            board, side = in_boundary(ballLocation[0]-1, ballLocation[1])

        elif angle == 45:
            board, side = in_boundary(ballLocation[0]-1, ballLocation[1]-1)

        elif angle == 90:
            board, side = in_boundary(ballLocation[0], ballLocation[1]-1)

        elif angle == 135:
            board, side = in_boundary(ballLocation[0]+1, ballLocation[1]-1)

        elif angle == 180:
            board, side = in_boundary(ballLocation[0]+1, ballLocation[1])

        elif angle == 225:
            board, side = in_boundary(ballLocation[0]+1, ballLocation[1]+1)

        elif angle == 270:
            board, side = in_boundary(ballLocation[0], ballLocation[1]+1)

        elif angle == 315:
            board, side = in_boundary(ballLocation[0]-1, ballLocation[1]+1)

        #If it is safe then return the angle or else change it
        if board != "FALSE":
            angle = change_angle(angle, board, side)

        else:
            return angle

def move_ball():
    global ballLocation, teleportLocations
    
    check_move_ball()

    #Remove old ball location
    ap.set_pixel(ballLocation[0], ballLocation[1], [0,0,0])

    #Change the ball location
    #Same logic for movement applies here as it did earlier

    
    if angle == 0:
        ballLocation[0] -= 1
        

    elif angle == 45:
        ballLocation[0] -= 1
        ballLocation[1] -= 1
        

    elif angle == 90:
        ballLocation[1] -= 1
        

    elif angle == 135:
        ballLocation[0] += 1
        ballLocation[1] -= 1
        

    elif angle == 180:
        ballLocation[0] += 1
        

    elif angle == 225:
        ballLocation[0] += 1
        ballLocation[1] += 1
        

    elif angle == 270:
        ballLocation[1] += 1
        

    elif angle == 315:
        ballLocation[0] -= 1
        ballLocation[1] += 1


    #This checks to see if the ball is on a portal and if it needs to teleport
    #I made it so you could land on either and still teleport as if you hit the top
    #Or bottom of the bat then it is possible to change paths and you will therefore
    #Not make the teleport
    if ballLocation == teleportLocations[0]:
        ballLocation = teleportLocations[1]
        teleported = True

    elif ballLocation == teleportLocations[1]:
        ballLocation = teleportLocations[0]
        teleported = True

    else:
        
        teleported = False

    #If the ball did teleport then it needs to reset the teleportation
    if teleported:
        #Remove the portal pixels and clean them
        teleport_pixels([0,0,0])
        
        #reset the portal locations so it doesnt teleport from the same place
        #Again
        teleportLocations = [[],[]]

        
    #Show where the ball is on screen
    ap.set_pixel(ballLocation[0], ballLocation[1], [100,0,0])

def not_dead():
    global ballLocation

    #If the ball is in the bats column then it is unable to be hit and you are
    #therefore dead. As I used "not_dead" as the name of the function it will
    #Return true if you are alive
    if ballLocation[0] < 1:
        return False

    else:
        return True


def next_move(move, ballMoveTime):

    #Every 10 moves increase the speed by 20% of the speed it's at
    #I used a percentage increase to stop impossible playing speeds and to allow
    #For a fairer increase. Although as it only rounds to 2 decimal places the speed
    #Does have a cap of about a move every 0.01 seconds which means it will take
    #Just 0.8 seconds to moe across the board which is a fair speed.
    if move % 10 == 0:
        ballMoveDeduction = round((ballMoveTime/100)*5, 2)
        ballMoveTime -= ballMoveDeduction

    #Every 17 moves, unless there is already a teleport, create a teleport.
    #Should mention not 17 moves from the last creation just moves in general.
    #All moves are moves of the ball
    if move % 17 == 0:
        if teleportLocations == [[],[]]:
            create_teleport()

    #The amount of time remaining for the ball to move is initially the ballMoveTime
    ballTimeLeft = ballMoveTime

    #This checks to see if the ball needs to move. This means that when you move
    #The bat it doesn't automatically move the ball aswell
    while ballTimeLeft >= 0:

        #I use datetime to get the time as it is accurate(microseconds) and easy
        #To use
        startTime = datetime.datetime.now()

        #Use the timeout I built into the joystick to act as a futher countdowm
        #This uses ballTimeLeft to change so that you can't wait on the joystick
        #And allow cheating
        direction = joystick(ballTimeLeft)

        #Only updates the bat if it moves up or down as there is no left and right
        #And meant less code was required
        if direction == "UP" or direction == "DOWN":
            update_bat(direction)

        #Gets the time you pressed the joystick
        endTime = datetime.datetime.now()

        #Finds the differnce between the start and deducts it from ballTimeLeft
        #If the time left is less than 0 break from the loop
        finalTime = endTime - startTime
        
        ballTimeLeft -= finalTime.microseconds/1000000
        

    if teleportLocations != [[],[]]:
        #Resets the tp pixels just incase something went wrong (as it did in a test)
        #And the colour goes
        teleport_pixels([155,0,155])

    #When it has broken from the loop it moves the ball
    move_ball()

    #Adds a move
    move += 1

    #Return these variables because I didn't get my head around globalling at the
    #Start, but it no difference to performance
    return move, ballMoveTime

#Clears the board incase there was something on it before
ap.clear()

#Sort and show bat straight away            
batMiddle = 3
ap.set_pixel(0,batMiddle, [100,100,100])

#Choose starting location of ball
randomRow = random.randint(2,4)
ballLocation = [3,randomRow]

#Sets the time interval the ball moves
ballMoveTime = 0.4

#Initialises the teleports
teleportLocations = [[],[]]

#Starts the angle going towards the side without bat as it's the nice thing
#to do
angle = 180

#Sets the amount of moves the ball has made
move = 1

#This gets the time you started the game
startTime = datetime.datetime.now()

#While you are still alive(the ball hasn't gone past you) it plays it
while not_dead():
    move, ballMoveTime = next_move(move, ballMoveTime)

#When you die it gets the time of death and works out how long you lasted
endTime = datetime.datetime.now()

finalTime = endTime - startTime
fileObject = open("6Pong/data.txt","a")
fileObject.write("\n"+str(startTime)+","+str(finalTime))
fileObject.close()
