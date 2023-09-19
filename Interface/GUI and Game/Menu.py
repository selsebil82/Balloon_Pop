import pygame
import SceneManager
from Interface.Basics.Button import  ButtonImg

def Menu():
    #Initialize
    pygame.init()
    pygame.event.clear()

    #Create Window/Display
    width, height = 1280, 720
    window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Balloon Pop")

    #Initialize Clock for FPS
    fps = 30
    clock = pygame.time.Clock()

    #Images
    imgBackground = pygame.image.load("../../Resources/background.jpg").convert()
    imgPop = pygame.image.load("../../Resources/pp1.png").convert_alpha()
    # Buttons
    buttonStart = ButtonImg((160, 260), "../../Resources/Buttons/start3.png", pathSoundClick ="../../Resources/Sounds/start.mp3", pathSoundHover = "../../Resources/Sounds/hover.mp3")
    buttonQuit = ButtonImg((160, 450), "../../Resources/Buttons/quit2.png", pathSoundClick ="../../Resources/Sounds/start.mp3", pathSoundHover = "../../Resources/Sounds/hover.mp3")


    #Main Loop
    start = True
    while start :
        #Get Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                start = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s :
                    SceneManager.OpenScene("Game")


        #Apply Logic
        #Draw Background/Buttons
        window.blit(imgBackground,(0,0))
        pop_x = imgBackground.get_width() - imgPop.get_width()
        window.blit(imgPop, (pop_x, 0), special_flags=pygame.BLEND_RGB_ADD)

        font = pygame.font.Font('../../Resources/Marcellus-Regular.ttf', 20)
        textStart = font.render(f'Developped by Trabelsi selsebil', True, (255,255,255))

        window.blit(textStart,(400 , 680))

        buttonStart.draw(window)
        buttonQuit.draw(window)

        if buttonStart.state == "clicked":
            SceneManager.OpenScene("BallonPop")


        if buttonQuit.state == "clicked":
            pygame.quit()




        #Update Display
        pygame.display.update()
        #Set FPS
        clock.tick(fps)


if __name__ == "__main__":
    Menu()
