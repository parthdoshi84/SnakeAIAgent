import pygame
import time
import random
import numpy as np
import math
import time
import pickle

pygame.init()

display_width = 500
display_height = 500

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0,0,255)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()


alpha = 0.3
gamma = 0.9

def rect(thingx, thingy, thingw, thingh, color):
    pygame.draw.rect(gameDisplay, color, [thingx, thingy, thingw, thingh])


# Up = 0
# Down = 1
# Left = 2
# Right = 3

def init():
    Q = []
    for i in range(625):
        Q.append(np.zeros(4))
        np.save("QAlternate.npy", Q)


def check(tempAction, prevAction):
    if ((tempAction == 0 and prevAction == 1) or (tempAction == 1 and prevAction == 0)):
        return False

    if ((tempAction == 2 and prevAction == 3) or (tempAction == 3 and prevAction == 2)):
        return False

    return True

def detectCollision(headX, headY, snakeX,snakeY):
    for i in range(0, len(snakeX)-1):
        if headX == snakeX[i] and headY == snakeY[i]:
            return True
    return False



def QLearning(Q, snakeX, snakeY, ballX, ballY,prevAction):
    collision = False
    state = []

    i = 0
    while i < len(snakeX):
        snakeIndex = (snakeY[i]/100)*5 + (snakeX[i]/100)
        state.append(snakeIndex)
        i+=1

    for j in range(i,25):
        state.append(-1)

    ballIndex = (ballY/100)*5 + (ballX/100)
    state.append(ballIndex)
    state = tuple(state)

    print state
    if state not in Q.keys():
        Q[state] = np.zeros(4)

    maxValue = -100000
    maxIndexes = []



    for tempAction in range(4):
        tempX = 0
        tempY = 0

        if check(prevAction, tempAction) == True:
            if tempAction == 0:
                tempY = snakeY[0] - 100
            if tempAction == 1:
                tempY = snakeY[0] + 100
            if tempAction == 2:
                tempX = snakeX[0] - 100
            if tempAction == 3:
                tempX = snakeX[0] + 100


            if tempX<500 and tempY <500 and tempX>=0 and tempY>=0:

                if Q[state][tempAction] > maxValue:
                    maxIndexes = []
                    maxValue = Q[state][tempAction]
                    maxIndexes.append(tempAction)
                elif Q[state][tempAction] == maxValue:
                    maxIndexes.append(tempAction)

    lim = len(maxIndexes)
    #print maxIndexes
    actionIndex = np.random.randint(lim)
    action = maxIndexes[actionIndex]


    tailX = snakeX[len(snakeX) - 1]
    tailY = snakeY[len(snakeY) - 1]

    i = len(snakeX) - 1
    while i>0:
        snakeX[i] = snakeX[i-1]
        snakeY[i] = snakeY[i-1]
        i-=1

    if action == 0:
        snakeY[0]-=100
    elif action == 1:
        snakeY[0]+= 100
    elif action == 2:
        snakeX[0]-=100
    else:
        snakeX[0]+=100

    reward = 0
    if snakeX[0] == ballX and snakeY[0] == ballY:
        snakeX.append(tailX)
        snakeY.append(tailY)
        reward = 10
        while True:
            ballX = np.random.randint(5)
            ballY = np.random.randint(5)

            ballX = ballX * 100
            ballY = ballY * 100

            i = 0
            while i < len(snakeX):
                if ballX == snakeX[i] and ballY == snakeY[i]:
                    break
                i+=1
            if i==len(snakeX):
                break
            Q[state][action] = reward




    else:
        for i in range(1,len(snakeX)):
            if snakeX[0] == snakeX[i] and snakeY[0] == snakeY[i]:
                collision = True
                break

        if collision == True:
            Q[state][action] = -10
            snakeX = []
            snakeY = []
            newSnakeX = 0
            newSnakeY = 0
            while True:
                newSnakeX = np.random.randint(5)
                newSnakeY = np.random.randint(5)
                if ballX == newSnakeX and ballY == newSnakeY:
                    pass
                else:
                    break
            snakeX.append(newSnakeX*100)
            snakeY.append(newSnakeY*100)
        else:
            newState = []

            i = 0
            while i < len(snakeX):
                snakeIndex = (snakeY[i] / 100) * 5 + (snakeX[i] / 100)
                newState.append(snakeIndex)
                i+=1

            for j in range(i,25):
                newState.append(-1)

            ballIndex = (ballY / 100) * 5 + (ballX / 100)
            newState.append(ballIndex)

            newState = tuple(newState)
            if newState not in Q.keys():
                Q[newState] = np.zeros(4)

            Q[state][action] = (1 - alpha)*Q[state][action] + alpha*(reward + gamma*max(Q[newState]))

    return snakeX, snakeY, ballX, ballY, collision,action



def game_loop():
    gameCounter = 0

    snakeX = []
    snakeY = []

    snakeX.append(0)
    snakeY.append(0)

    Q = dict()


    #pickle_in = open("Q5x5Grid.pickle")
    #Q = pickle.load(pickle_in)
    


    while True:
        ballX = np.random.randint(5)
        ballY = np.random.randint(5)
        if ballX == snakeX and ballY == snakeY:
            pass
        else:
            break

    ballX = ballX*100
    ballY = ballY*100

    gameExit = False

    action = np.random.randint(4)

    print ballX, ballY


    while not gameExit:


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                #np.save("Q.npy")
                quit()

        snakeX, snakeY, ballX, ballY, collision, newAction = QLearning(Q,snakeX,snakeY,ballX,ballY,action)
        #print snakeX
        #print snakeY
        action = newAction

        gameDisplay.fill(white)

        if collision == True:
            time.sleep(2)
            print "Collided"

        rect(snakeX[0], snakeY[0], 100, 100, blue)

        for i in range(1,len(snakeX)):
            rect(snakeX[i], snakeY[i], 100, 100, black)

        rect(ballX, ballY, 100, 100, red)
        pygame.display.update()
        clock.tick(60)
        time.sleep(5)
        #np.save("QAlternate.npy",Q)

        gameCounter+=1

        if gameCounter%10000 == 0:
            pickle_out = open("TpQ5x5Grid.pickle","wb")
            pickle.dump(Q,pickle_out)
            pickle_out.close()
            gameCounter = 0


def printQ():
    Q = np.load("QAlternate.npy")
    for i in range(len(Q)):
        print Q[i]

#init()
game_loop()
pygame.quit()
quit()
#printQ()