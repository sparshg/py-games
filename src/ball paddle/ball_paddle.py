import pygame

pygame.init()

blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
black = (0, 0, 0)

ball = 10
length = 500
width = 500

rectx = 250
recty = 250

brickw = 45
brickL = 10

new_x1 = 0
new_y1 = 0

clock = pygame.time.Clock()

brickx1 = width // 2 - brickw // 2
bricky1 = length - brickL - 5

brick_ki_tezi = 5

rect_changex = -3
rect_changey = -2

display = pygame.display.set_mode((width, length))
pygame.display.set_caption("BRICK BALL GAME ")

game_over = False

while not game_over:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True          

    keys = pygame.key.get_pressed()

    if keys[pygame.K_RIGHT] and brickx1 <= width - brickw:
        new_x1 = brick_ki_tezi
        new_y1 = 0

        brickx1 += new_x1

    if keys[pygame.K_LEFT] and -brickx1 < 0:
        new_x1 = -brick_ki_tezi
        new_y1 = 0

        brickx1 += new_x1

    rectx += rect_changex
    recty += rect_changey

    if rectx >= 500 or rectx < 0:
        rect_changex = rect_changex * -1
    if recty < 0:
        rect_changey = -rect_changey
    if recty >= 500:
        game_over = True

    if rectx in range(brickx1, brickx1 + brickw) and recty in range(bricky1 - brickL, bricky1):
        print("CONTACT")
        #rect_changex = rect_changex * -1
        rect_changey = rect_changey * -1
    

    display.fill(black)
    pygame.draw.rect(display, blue, [brickx1, bricky1, brickw, brickL] ) 
    pygame.draw.rect(display, green, [rectx, recty, ball, ball])       
    pygame.display.flip()

    clock.tick(60)
    
