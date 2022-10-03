"""
A block dodging game build using pygame!

Author: Yash Indane
Email: yashindane46@gmail.com
"""

import pygame
import random
import math
import sys
import pygame.mixer

pygame.mixer.pre_init(44100, -16, 2, 2048)
pygame.mixer.init()
pygame.init()

#defining all values
sound=pygame.mixer.Sound("mario.wav")
block_brick=pygame.mixer.Sound("pop.wav")
gunshot=pygame.mixer.Sound("40_smith_wesson.wav")
music=pygame.mixer.Sound("sierra_nevada.wav")
pygame.mixer.Sound.play(music)

width=800
height=600
ORANGE=(205, 101, 0)
BLUE=(0, 0, 255)
GREEN=(0, 255, 0)
GREY=(192, 192, 192)
GOLD=(212, 175, 55)
RED=(255, 0, 0)
background=(0, 0, 0)
player_size=50
player_pos=[width/2-player_size/2, height-2*player_size]
enemy_pos=[random.randint(0, width-player_size), 0]
gem_radius=15
gem_count=0
brick_count=0
gol_count=0
gem_pos=[random.randint(gem_radius, width-2*gem_radius), -gem_radius]
gol_pos=[random.randint(gem_radius, width-2*gem_radius), -random.randint(gem_radius, height*2)]
bul_pos=[width/2-player_size/2+22, height-2*player_size-15]
SPEED=0.5
enemy_list=[enemy_pos]
score=0
gameover=True
b=False
font=pygame.font.SysFont("calibri", 35)
FPS=300

screen=pygame.display.set_mode((width, height))
pygame.display.set_caption("BLOCK BREAKER")
clock=pygame.time.Clock() #for setting fps rate


def drop_enemeis(j):
    delay=random.random()
    if (len(j)<9 and delay<0.013):
        x_pos=random.randint(0, width-player_size)
        y_pos=0
        j.append([x_pos, y_pos])


def draw_enemeis(p):
    for enemy in p:
        pygame.draw.rect(screen, BLUE, (int(enemy[0]), int(enemy[1]), player_size, player_size))


def update_en_pos(s, x):
    for idx,enemy_pos in enumerate(s, start=0):

      if (enemy_pos[1]>=0 and enemy_pos[1]<height):
         enemy_pos[1]+=SPEED
      else:
          s.pop(idx)
          x+=1
    return x     
            

def col_check(q, z, u, k, m, g):
    for a in q:
        if detect_col(a, z, u, k, m, g, q)==False:
            return False
            
        else:
            return True


        #return detect_col(a,z,u,k,m,g)


def detect_col(a, b, u, k, m, g, q): 
    p_x=a[0]
    p_y=a[1]

    e_x=b[0]
    e_y=b[1]

    if ((math.fabs(p_y-e_y)<=player_size and math.fabs(p_x-e_x)<=player_size)): #or (math.fabs(p_x-e_x)<=player_size and math.fabs(p_y-e_y)<=player_size)):
        f=u+k*15+m*25+g*5
        background=(104, 52, 52)
        screen.fill(background)
        print("GAME OVER! \t")
        print("Your score:", f)
        print("Gems earned:", k+m)
      
        return False
        
    else:
        return True

                                                                                                                                          
if __name__ == "__main__":
    while gameover:
        for event in pygame.event.get(): #for loop to track events in game
            if (event.type==pygame.QUIT):
                sys.exit()

            if(event.type==pygame.KEYDOWN):
                
                x=player_pos[0]
                u=bul_pos[0]
                v=bul_pos[1]
            
                
                if(event.key==pygame.K_LEFT):
                    if player_pos[0]>0:
                        x-=50
                        u-=50
                    else:
                        pass    
                        
                    
                if(event.key==pygame.K_RIGHT):
                    
                    if player_pos[0]+player_size<width:
                        x+=50
                        u+=50
                        
                    else:
                        pass 
                if event.key==pygame.K_SPACE:
                    pygame.mixer.Sound.play(gunshot)

                    b=True
                else:
                    b=False    
                

            elif event.type==pygame.KEYUP:
                if event.key==pygame.K_SPACE:
                    #b=False
                    u=x+22
                    v=player_pos[1]
                else:
                    pass    
                    
                #for getting the bullet to new location of player!
                bul_pos[1]=v  
                bul_pos[0]=u
                player_pos[0]=x
                

        screen.fill(background)

        drop_enemeis(enemy_list)
        score=update_en_pos(enemy_list, score)
        
        if score<25:
            FPS=150
        elif score<60:
            FPS=250
        elif score<100:
            FPS=350
        elif score<160:
            FPS=480
        elif score<250:
            FPS=600  
        elif score>=250:
            FPS=750

        if gem_pos[1]<height:
            gem_pos[1]+=2
        else:
            gem_pos[1]=-gem_radius
            gem_pos[0]=random.randint(gem_radius, width-2*gem_radius)

        if gol_pos[1]<height:
            gol_pos[1]+=2
        else:
            gol_pos[1]=-gem_radius#-random.randint(gem_radius,height*2)                                                                                                                              
            gol_pos[0]=random.randint(gem_radius, width-2*gem_radius)    

        if ((player_pos[1]-gol_pos[1]==gem_radius) and (player_pos[0]-gem_radius<gol_pos[0] and player_pos[0]+player_size+gem_radius>gol_pos[0])):
            gol_count+=1
            pygame.mixer.Sound.play(sound)
            gol_pos[1]=-gem_radius#-random.randint(gem_radius,height*2)
            gol_pos[0]=random.randint(gem_radius, width-2*gem_radius)

        else:
            pass 

        if ((player_pos[1]-gem_pos[1]==gem_radius) and (player_pos[0]-gem_radius<gem_pos[0] and player_pos[0]+player_size+gem_radius>gem_pos[0])):
                
            gem_count+=1
            pygame.mixer.Sound.play(sound)
            gem_pos[1]=-gem_radius
            gem_pos[0]=random.randint(gem_radius, width-2*gem_radius)

        else:
            pass

        g="Gems:"+str(gem_count+gol_count)
        label1=font.render(g, 1, GREEN)
        screen.blit(label1, (width-150, height-540))

        pygame.draw.rect(screen, ORANGE, (int(player_pos[0]), int(player_pos[1]), player_size, player_size))
        if b:
            
            try:
                pygame.draw.rect(screen, RED, (int(bul_pos[0]), int(bul_pos[1]), 7, 15))
            except TypeError:
                pass  
            
            for m in enemy_list:
                if ((bul_pos[1]-m[1]+player_size<=player_size) and ((bul_pos[0]>=m[0]-7) and (bul_pos[0]<=m[0]+player_size))):
                        pygame.mixer.Sound.play(block_brick)
                        bul_pos[1]=v  
                        bul_pos[0]=u

                        
                        m[0]=random.randint(0, width-player_size)
                        m[1]=-player_size
                        
                        
                        brick_count+=1
                        b=False
                        break
                        
                else:
                    pass
                    
                    
            try:

                    bul_pos[1]-=player_size*0.2
                    if bul_pos[1]<=0:
                        
                    
                        bul_pos[1]=v  
                        bul_pos[0]=u
                        b=False
                        
            except TypeError:
                pass         

        
        d="Score:"+str(score+(gem_count*15)+(gol_count*25)+(brick_count*5))
        label=font.render(d, 1, GREEN)
        screen.blit(label, (width-150, height-580))       

        gameover=col_check(enemy_list, player_pos, score, gem_count, gol_count, brick_count)
        draw_enemeis(enemy_list)       

        pygame.draw.circle(screen, GREY, (gem_pos[0], gem_pos[1]), gem_radius)
        pygame.draw.circle(screen, GOLD, (gol_pos[0], gol_pos[1]), gem_radius)
        
        clock.tick(FPS)
        pygame.display.update()
