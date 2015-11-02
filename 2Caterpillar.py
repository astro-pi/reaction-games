import pygame,random,datetime, time
from pygame.locals import *
from astro_pi import AstroPi

#Length; Survival


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


def change_direction(previous):
    #See if the directin is changed within specified time
    direction = joystick(0.3)

    #If a joystick is moved within the given time return the way it was moved
    if direction != "NONE" and  direction != "RETURN":
        return direction

    else:
        #If no joystick is moved then return the direction from before
        return previous



def create_apple():
    global appleCo

    #Initialise the check variable
    inSnake = True
    
    while inSnake:

        #Create the apple in a random location
        appleCol = random.randint(0,7)
        appleRow = random.randint(0,7)

        #Check if the apple would be created in snake
        for location in snakeBodyCoords:
            if appleRow == location[0] and appleCol == location[1]:
                #If the apple would be created in the snake then keep the loop
                #Going and break from the for loop to restart the process in
                #A new location
                inSnake = True
                break

            else:
                inSnake = False

    #Apple location should be in a valid place and can therefore be globally
    #Set to allow it to be used elsewhere
    appleCo = [appleRow,appleCol]

def check_death():
    #Checks to see if it's out of bounds
    row = snakeBodyCoords[0][0]
    col = snakeBodyCoords[0][1]

    #If the snakes head is out of bounds then return True for dead.
    #Reason it doesnt check all parts of body due to 
    if row > 7 or row < 0:
        return True

    if col > 7 or col < 0:
        return True

    #Start of a counter for the loop
    place = 0
    
    #Check to see if it has hit one of the other parts of body
    for places in snakeBodyCoords:

        #Checks to see if the head is in another part of the body
        if snakeBodyCoords[0] == places:

            #If it's not the first count (as the head is the first location) return that it's dead
            if place != 0:
                return True

        #Adds one to the counter so there is no mistaking it for the head itself
        place += 1

    return False
    
    
def move_body():
    global previous, snakeBodyLength,snakeColor,snakeBodyCoords, appleCo, applesEaten

    #Sets the direction of the snake to a new direction
    previous = change_direction(previous)
    

    #Change positions of snakes body
    for bodyPos in range(len(snakeBodyCoords),0,-1):

        #If the body position is the head then perform something else
        if bodyPos == 1:

            #This alows for the snake to change direction or it would always follow
            #Itself
            if previous == "UP":
                snakeBodyCoords[0][1] -= 1

            elif previous == "DOWN":
                snakeBodyCoords[0][1] += 1

            elif previous == "RIGHT":
                snakeBodyCoords[0][0] += 1

            elif previous == "LEFT":
                snakeBodyCoords[0][0] -= 1      
        
        else:
            #Changes the position of the snake to the one in front of it
            snakeBodyCoords[bodyPos-1] = list(snakeBodyCoords[bodyPos-2])



    #NEEDS OPTIMISING
    if check_death():
        dead = True
    else:
        dead = False
    
    #Print out the changes
    ap.clear()
    ap.set_pixel(appleCo[0],appleCo[1],[155,0,0])

    appleEaten = False

    #If you aren't dead CAN BE OPTIIMISED FUTHER
    if not dead:

        #Update all pixels INEFFICIENT, ALOT NEEDS TO CHANGE TO OPTIMISE
        for places in snakeBodyCoords:
            ap.set_pixel(places[0],places[1],snakeColour)
            if places == appleCo:
                appleCo = []
                applesEaten += 1
                appleEaten = True

        #The max length of the snake is 64 so if the length is that you must have won
        if len(snakeBodyCoords) >= 63:
            return "WON"

        #If the apple has been eaten then do that
        if appleEaten:
            eat_apple()


    #If you are dead
    else:
        return "DEAD"



def eat_apple():
    global snakeBodyLength, endOfBody

    #Gets the place you ate the apple
    endOfBody = list(appleCo)

    #Create a new apple straight away
    create_apple()
    
    for i in range(2):
        #Adds the snake body on in the palce it ate the apple
        snakeBodyLength += 1
        snakeBodyCoords.append(endOfBody)
        move_body()
        




#Set up snake
snakeColour = [0,100,0]
snakeBodyLength = 1
snakeBodyCoords = [[0,0]]
applesEaten = 0

#State of death flashing initialised
state = True

#Create a colour for reference, unecessary
black = [0,0,0]

#Starts the snake going right
previous = "RIGHT"

#Set the first snakes colour and locaiton
ap.set_pixel(0,0,snakeColour)

#Create an apple to start
create_apple()

#Tell the loop the snake is alive
alive = True



startTime = datetime.datetime.now()
while alive:
    #Move body and store return of it in check variable
    check = move_body()

    #Tells program if you are dead or alive
    if check == "DEAD" or check == "WON":
        alive = False

endTime = datetime.datetime.now()
survivalTime = endTime - startTime

#If you are dead then do this
if check == "DEAD":

    #Remove the apple visually
    ap.set_pixel(appleCo[0], appleCo[1], black)

    #Create a flashing animation to symbolise death
    for i in range(8):

        #Turn each pixel on then off 8 times with a 0.4 second wait
        for places in snakeBodyCoords:
            #Try this
            try:

                #If the state is to turn things on
                if state:
                    #All the locations will be green
                    ap.set_pixel(places[0],places[1],snakeColour)

                #If the state is to turn things off
                if not state:
                    #Set all the pixels to black
                    ap.set_pixel(places[0],places[1],black)

            #If a pixel is out of range then instead of crashing just print "error"
            except ValueError:
                pass
            
        #Inverts the state
        if state:
            state = False

        else:
            state = True

        #Sleeps to allow for the visual flashing
        time.sleep(0.4)

#If you win show the won message in red
if check == "WON":
    ap.show_message("You won!", red)

fileObject = open("2Caterpillar/data.txt", "a")
fileObject.write("\n"+str(datetime.datetime.now())+","+str(snakeBodyLength)+","+str(survivalTime))
fileObject.close()
