import Menu
import random
import time
import pygame
import cv2
import numpy as np #to rotate camrera
from cvzone.HandTrackingModule import  HandDetector
from Interface.Basics.Button import  ButtonImg
import SceneManager

def Game():
#Initialize
    pygame.init()

    #Create WIndow/Display

    width, height = 1280, 720
    window = pygame.display.set_mode((width,height))
    pygame.display.set_caption("Balloon Pop")

    # Initialize clock for fps

    fps=30
    clock = pygame.time.Clock()



    # WebCam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280)#width
    cap.set(4, 720)#height


    #Images

    imgBallon = pygame.image.load('../../Resources/BalloonRed.png').convert_alpha()
    imgBalloonPop = pygame.image.load('../../Resources/BalloonPop.png').convert_alpha()

    imgBallonBlue = pygame.image.load('../../Resources/BalloonBlue.png').convert_alpha()
    imgBalloonBluePop = pygame.image.load('../../Resources/BluePop.png').convert_alpha()

    imgBallonYellow = pygame.image.load('../../Resources/BalloonYellow.png').convert_alpha()
    imgBalloonYellowPop = pygame.image.load('../../Resources/YellowPop.png').convert_alpha()

    rectBalloon = imgBallon.get_rect()
    rectBalloon.x,rectBalloon.y = 500, 300

    rectBalloonBlue = imgBallonBlue.get_rect()
    rectBalloonBlue.x,rectBalloonBlue.y = 200, 400


    rectBalloonYellow = imgBallonYellow.get_rect()
    rectBalloonYellow.x, rectBalloonYellow.y = 300, 200


    # Variables
    vie = 5
    missed = 0
    speed = 30 # we can make it more difficult
    score = 0
    startTime = time.time()
    totalTime = 10
    #Detector
    detector = HandDetector(detectionCon=0.8, maxHands=1)
    def resetBalloon():
        #change location of x and y
        rectBalloon.x = random.randint(100,img.shape[1]+20)
        rectBalloon.y = img.shape[0]+50 # y : bring it further down

    def resetBalloonBlue():

        rectBalloonBlue.x = random.randint(50,img.shape[1]+50)
        rectBalloonBlue.y = img.shape[0]+20 # y : bring it further down

    def resetBalloonYellow():

        rectBalloonYellow.x = random.randint(50,img.shape[1]+10)
        rectBalloonYellow.y = img.shape[0]+5# y : bring it further down


    def presentLoss(score):

        if score == 0:
            font = pygame.font.Font('../../Resources/Marcellus-Regular.ttf', 50)
            textLoss = font.render(f'Game Over ! You Lost !', True, (255, 255, 255))
            window.blit(textLoss, (350, 90))

        else:
            font = pygame.font.Font('../../Resources/Marcellus-Regular.ttf', 50)
            textScore = font.render(f'Your score  : {score}', True, (255, 255, 255))
            if vie <= 0 :
                textVie = font.render(f'Life number is over', True, (255, 255, 255))
                window.blit(textScore, (450, 200))
                window.blit(textVie, (420, 50))
            elif vie <= 0 and score == 0:
                textVie = font.render(f'Life number is over', True, (255, 255, 255))
                window.blit(textScore, (450, 200))
                window.blit(textVie, (450, 50))
                textTime = font.render(f'Time UP ', True, (255, 255, 255))
                window.blit(textTime, (530, 90))

            else :
                textTime = font.render(f'Time UP ', True, (255, 255, 255))
                window.blit(textTime, (530, 90))

            window.blit(textScore, (450, 200))


    #Main Loop

    start = True
    while start :
        #Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()


        # Apply LOgic of game

        timeRemain = int(totalTime - (time.time()-startTime))
        if timeRemain <= 0 or vie <= 0:

            window.fill((164,20,22))
            #show text
            buttonReplay = ButtonImg((500, 290),
                                     "../../Resources/Buttons/reply.png",
                                     pathSoundClick="../../Resources/Sounds/start.mp3",
                                     pathSoundHover="../../Resources/Sounds/hover.mp3")
            buttonQuit = ButtonImg((380, 500), "../../Resources/Buttons/quit2.png",
                                   pathSoundClick="../../Resources/Sounds/start.mp3",
                                   pathSoundHover="../../Resources/Sounds/hover.mp3")

            buttonReplay.draw(window)
            buttonQuit.draw(window)

            if buttonReplay.state == "clicked":
                cap.release()
                SceneManager.OpenScene("BallonPop")

            if buttonQuit.state == "clicked":
                pygame.quit()
            presentLoss(score)


        else :

            #OpenCV

            success, img = cap.read()

            #when our hands go to the left it goes on cam so we have to flip
            img = cv2.flip(img, 1)#1 means horizantal , 0  means vertical
            hands = detector.findHands(img,flipType=False,draw=False)#because we are already flipping it
            #speed of the balloon
            rectBalloon.y -= speed

            rectBalloonBlue.y -= speed

            rectBalloonYellow.y -= speed


            #when it reaches the top we should reset


            if rectBalloon.y < 0:
                resetBalloon()
                #change the speed everytime it resets the baloon
                speed += 1
                missed += 1
                vie -=1

            if rectBalloonYellow.y < 0:
                resetBalloonYellow()
                # change the speed everytime it resets the baloon
                speed += 1
                missed += 1
                vie -=1

            elif rectBalloonBlue.y < 0:
                resetBalloonBlue()
                #change the speed everytime it resets the baloon
                speed += 1
                missed += 1
                vie -=1


            #we will check when the hand is touching the balloon
            #check if any hand is present
            if hands:
                hand = hands[0]
                #we need the tip of index fingure
                x,y = hand['lmList'][8]
                cv2.circle(img,(x,y),15,(0, 0, 255),cv2.FILLED)


                #check if c,y are inside the balloon
                if rectBalloon.collidepoint(x,y):
                    # Show BalloonPop image
                    pop_sound = pygame.mixer.Sound('../../Resources/Sounds/pop.wav')

                    window.blit(imgBalloonPop, rectBalloon)
                    pygame.display.update()
                    resetBalloon()
                    score += 10
                    speed +=1
                    pop_sound.play()

                if rectBalloonYellow.collidepoint(x,y):
                    # Show BalloonPop image
                    pop_sound = pygame.mixer.Sound('../../Resources/Sounds/pop.wav')

                    window.blit(imgBalloonYellowPop, rectBalloonYellow)
                    pygame.display.update()
                    resetBalloonYellow()
                    score += 10
                    speed +=1
                    pop_sound.play()

                elif rectBalloonBlue.collidepoint(x,y):
                    # Show BalloonPop image
                    pop_sound = pygame.mixer.Sound('../../Resources/Sounds/pop.wav')

                    window.blit(imgBalloonBluePop, rectBalloonBlue)
                    pygame.display.update()
                    resetBalloonBlue()
                    score += 10
                    speed +=1
                    pop_sound.play()


            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            imgRGB = np.rot90(imgRGB)
            frame = pygame.surfarray.make_surface(imgRGB).convert()
            frame = pygame.transform.flip(frame, True, False)
            window.blit(frame, (0,0))

            window.blit(imgBallon,rectBalloon)
            window.blit(imgBallonBlue,rectBalloonBlue)
            window.blit(imgBallonYellow,rectBalloonYellow)



            #show text
            font = pygame.font.Font('../../Resources/Marcellus-Regular.ttf', 50)
            textScore = font.render(f'Score : {score}', True ,(164,20,22))
            textTime = font.render(f'Time : {timeRemain}', True ,(164,20,22))
            textMissed = font.render(f'Missed : {missed}', True ,(164,20,22))

            textVie = font.render(f'life : {vie}', True ,(164,20,22))


            window.blit(textScore, (35,35))
            window.blit(textTime, (1000,35))
            window.blit(textMissed, (680,35))

            window.blit(textVie, (320,35))


        #Update the display

        pygame.display.update()
        #Set the FPS
        clock.tick(fps)


if __name__ == "__main__" :
    Menu()
