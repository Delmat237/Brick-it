#coding:utf-8
import pygame as pg
import random as rd

class Brick():
    def __init__(self,life=5):
        self.life = life
        if life == 5:
            img = pg.image.load("blue_brick.gif").convert_alpha()
        elif life == 4:
            img = pg.image.load("green_brick.gif").convert_alpha()
        elif life == 3:
            img = pg.image.load("pink_brick.gif").convert_alpha()
        elif life == 2:
            img = pg.image.load("purple_brick.gif").convert_alpha()
        elif life == 1:
            img = pg.image.load("yellow_brick.gif").convert_alpha()

        #redimensionnement
        self.img = pg.transform.scale(img,(50,30))
                
#initialisation de la fenetre
pg.init()
#creation de la fenetre
w,h = 800,600
fenetre = pg.display.set_mode((w,h))
pg.display.set_caption("BREAK IT")

#chargement des objets
paddle = pg.image.load("paddle.gif").convert_alpha()
blue_bricks = [Brick(5) for i in range(8)]
green_bricks = [Brick(4) for i in range(10)]
pink_bricks = [Brick(3) for i in range(4)]
purple_bricks = [Brick(2) for i in range(15)]
yellow_bricks = [Brick(1) for i in range(15)]

liste = blue_bricks + green_bricks +pink_bricks + purple_bricks + yellow_bricks
bricks = rd.sample(liste, len(liste))
wall = pg.image.load("wall.gif").convert_alpha()
wall1 = pg.image.load("wall1.gif").convert_alpha()
wall2 = pg.image.load("wall2.gif").convert_alpha()
ball = pg.image.load("ball.gif").convert_alpha()


#REDIMENSIONNEMENT DES objets
paddle = pg.transform .scale(paddle,(100,30))
wall = pg.transform .scale(wall,(20,h))
wall1 = pg.transform .scale(wall1,(30,h//2-20))
wall2 = pg.transform .scale(wall2,(30,h//2-20))
ball = pg.transform .scale(ball,(20,20))
lifes = [pg.transform .scale(paddle,(50,20)),pg.transform .scale(paddle,(50,20)),pg.transform .scale(paddle,(50,20))]

# position des objets
position_ball = pg.Vector2(w//3,h//3)
position_paddle = pg.Vector2(w//2,h-50)
position_wall,position_wall1,position_wall2,position_wall3 = [pg.Vector2(x,y) for x,y in [(10,20),(30,80),(150,80),(w-20,20)]]
speed = 2 
depl_ball = pg.Vector2(0,1) #deplacement de la balle
depl_paddle = 0 #deplacement du paddle
position_bricks = [(w//2+i*50,50+j*30) for i in range(6) for j in range(9)]
rect_bricks = [pg.Rect(x,y,50,30) for x,y in position_bricks]
position_lifes =[(w-3*55,10),(w-2*55,10),(w-1*55,10)]
score = 0
play = False
font = pg.font.SysFont("bradley hand itc",35) #POLICE DE CARACTERE
texte = "SCORE : 0000"
coeur = 3

running = True
while running:
    for  event in pg.event.get():
        if event.type == pg.QUIT :
            running = False
        elif event.type == pg.KEYDOWN :
            if event.key == pg.K_LEFT:
                depl_paddle = -speed
            elif event.key == pg.K_RIGHT:
                depl_paddle = speed
            elif event.key == pg.K_RETURN:
                play = True
            elif event.key == pg.K_BACKSPACE:
                play = False
            elif event.key == pg.K_SPACE:
                coeur -= 1
        elif event.type == pg.KEYUP:
            if event.key in [pg.K_LEFT,pg.K_RIGHT]:
                depl_paddle = 0
                
    #controle du deplacement des objets mobile
    if position_paddle.x <=50 or position_paddle.x >= w-100:
        depl_paddle = -depl_paddle
    
    if position_ball.x <= 50 or position_ball.x >= w-50  :
        depl_ball.x =-depl_ball.x
    if position_ball.y <= 10:
        depl_ball.y =-depl_ball.y
    if position_ball.y > h-paddle.get_height():
        #on soustrait un coeur
        coeur -= 1
        #repositionne la balle
        position_ball.x = w//3
        position_ball.y = h//3 
    
    #position des objets
    rect_ball = ball.get_rect().move(position_ball.x,position_ball.y) 
    rect_paddle = paddle.get_rect().move(position_paddle.x,position_paddle.y)
    rect_wall = wall.get_rect().move(position_wall.x,position_wall.y)
    rect_wall1 = wall1.get_rect().move(position_wall1.x,position_wall1.y)
    rect_wall2 = wall2.get_rect().move(position_wall2.x,position_wall2.y)
    rect_wall3 = wall.get_rect().move(position_wall3.x,position_wall3.y)
    
            
    
    #ce qui se passe lorsqu'il y'a collision
    if rect_ball.colliderect(rect_paddle):
        x1,x2,l = position_ball.x +ball.get_width()//2 , position_paddle.x , paddle.get_width()
        if x1 >= x2 and x1 <= x2+5*l/12: #si la balle rebondit sur la partie gauche du paddle
            depl_ball.x = -speed/2
            depl_ball.y = -speed/2
        elif x1 >= x2+7*l/12 and x1 <= x2+l: #si la balle rebondit sur la partie droite du paddle
            depl_ball.x = speed/2
            depl_ball.y = -speed/2
        elif x1 >= x2+5*l/12 and x1 <= x2 +7*l/12:
            depl_ball.x = 0
            depl_ball.y = -speed/2
        
        
        
    if rect_ball.colliderect(rect_wall ) or rect_ball.colliderect(rect_wall1) or\
       rect_ball.colliderect(rect_wall2) or rect_ball.colliderect(rect_wall3):
        depl_ball.x = -depl_ball.x

    for i,brick in enumerate(bricks):
        p = brick.life
        if rect_ball.colliderect(rect_bricks[i]):
            score += 1
            if p == 1:
                position_bricks[i] = (w+100,h)
            else:
                bricks[i] = Brick(p-1)
                depl_ball.x = -depl_ball.x
                depl_ball.y = -depl_ball.y
            
            
                 
                
    if play:
        position_paddle.x += depl_paddle
        position_ball.x += depl_ball.x
        position_ball.y += depl_ball.y
    
    #CREATION SURFACE DE TEXTE
    texte = "SCORE : {}".format(score)
    score_surface = font.render(texte,True,"white")
    #POSITION DU TEXTE
    position_score = (150-score_surface.get_width()//2,20-score_surface.get_height()//2)
    try:
        lifes[-coeur-1].set_alpha(0)
        assert(coeur > 0)
    except AssertionError:
        break
    except:
        pass
    
    fenetre.fill((0,0,0)) # remplissage du background
    fenetre.blit(paddle,(position_paddle.x,position_paddle.y))
    for i,brick in enumerate(bricks):
        fenetre.blit(brick.img,(position_bricks[i]))
            
    fenetre.blit(wall,(position_wall.x,position_wall.y))
    fenetre.blit(wall1,(position_wall1.x,position_wall1.y))
    fenetre.blit(wall2,(position_wall2.x,position_wall2.y))
    fenetre.blit(wall,(position_wall3.x,position_wall3.y))
    fenetre.blit(ball,(position_ball.x,position_ball.y)) 
    for i,life in enumerate(lifes):
        fenetre.blit(life,position_lifes[i])
        
    fenetre.blit(score_surface,position_score)
    
    # MISE A JOUR DE LA FENETRE
    pg.display.flip()
#Fermeture de la page
pg.quit()