import pygame
import time
import random
from pygame.constants import KEYDOWN, WINDOWHITTEST 

pygame.init()                               

blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

lambai = 300
chodai = 300

score = 0
saanp = 10
saanp_ki_tezi = 10

display = pygame.display.set_mode((chodai, lambai))
pygame.display.set_caption("SAANP KA KHEL ")

tiktok = pygame.time.Clock() 

font = pygame.font.SysFont("none", 30)
score_font = pygame.font.SysFont("comicsansms", 20)

def aapka_score(score, colour):
    msg = score_font.render("YOUR SCORE: " + str(score), True, colour)
    display.blit(msg, [0, 0])

def haar_gye_aap(message, colour):
    msg = font.render(message, True, colour)
    display.blit(msg, [15, 150])
    
def draw_snake(saanp, saanp_list):
    for x in saanp_list:
        pygame.draw.rect(display, blue, [x[0], x[1], saanp, saanp]) 

def gameloop():
    new_x1 = 0
    new_y1 = 0

    x1 = lambai / 2
    y1 = chodai / 2 

    saanp_ki_lambai = 1
    saanp_ki_list = []

    game_running = True
    game_closed = False


    foodx = round(random.randrange(0, chodai - saanp)/ 10 ) * 10
    foody = round(random.randrange(0, lambai - saanp)/ 10 ) * 10
 
    while not game_closed:

        while game_running == False:
                haar_gye_aap("GAME OVER, Press Q to quit or R to restart", red)
                aapka_score( saanp_ki_lambai - 1, red)
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_closed = True
                        game_running = True
                    if event.type == KEYDOWN:
                        if event.key == pygame.K_q:
                            game_closed = True
                            game_running = True
                        elif event.key == pygame.K_r:
                            gameloop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_closed = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    new_x1 = 0
                    new_y1 = -saanp_ki_tezi
                elif event.key == pygame.K_d:
                    new_x1 = saanp_ki_tezi
                    new_y1 = 0
                elif event.key == pygame.K_a:
                    new_x1 = -saanp_ki_tezi
                    new_y1 = 0
                elif event.key == pygame.K_s:
                    new_x1 = 0
                    new_y1 = saanp_ki_tezi
                #print(event)

        if x1 > chodai or x1 < 0 or y1 > lambai or y1 < 0:
            game_running = False

        x1 += new_x1
        y1 += new_y1
 
        display.fill(black)
        pygame.draw.rect(display, green, [foodx, foody, saanp, saanp])

        saanp_head = []
        saanp_head.append(x1)
        saanp_head.append(y1)
        saanp_ki_list.append(saanp_head)

        if len(saanp_ki_list) > saanp_ki_lambai:
            print(saanp_ki_list)
            del saanp_ki_list[0]

        for x in saanp_ki_list[:-1]:
            if x == saanp_head:
                game_running = False

        draw_snake(saanp, saanp_ki_list) 
        aapka_score(saanp_ki_lambai - 1, red)

        pygame.display.update()
        
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, chodai - saanp) / 10) * 10
            foody = round(random.randrange(0, lambai - saanp) / 10) * 10
            saanp_ki_lambai += 1
            print("ITEDAKIMASU")
            
        tiktok.tick(saanp_ki_tezi)

            


            

    pygame.quit()


gameloop()




