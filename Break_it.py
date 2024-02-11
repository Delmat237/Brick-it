#coding:utf-8
import pygame as pg
import random as rd

class Brick():
    def __init__(self,life=5):
        self.life = life
        self.x = w//20
        self.y = h//25
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
        self.img = pg.transform.scale(img,(self.x,self.y))
                

#initialisation de la fenetre
pg.init()
#creation de la fenetre
screen_info = pg.display.Info()
# Dimension de l'ecran
w,h = screen_info.current_w,screen_info.current_h
fenetre = pg.display.set_mode((w,h),pg.RESIZABLE)
pg.display.set_caption("BREAK IT")

jouer = True
level = 1 
def jouer_une_partie():
    global jouer,level
    
    #chargement des objets
    background = pg.image.load("background.gif").convert_alpha()
    paddle = pg.image.load("paddle.gif").convert_alpha()
    blue_bricks = [Brick(5) for i in range(rd.randrange(10))]
    green_bricks = [Brick(4) for i in range(rd.randrange(15))]
    pink_bricks = [Brick(3) for i in range(rd.randrange(10))]
    purple_bricks = [Brick(2) for i in range(rd.randrange(15))]
    yellow_bricks = [Brick(1) for i in range(rd.randrange(10))]

    liste = blue_bricks + green_bricks +pink_bricks + purple_bricks + yellow_bricks
    bricks = rd.sample(liste, len(liste))
    wall = pg.image.load("wall.gif").convert_alpha()
    wall1 = pg.image.load("wall1.gif").convert_alpha()
    wall2 = pg.image.load("wall2.gif").convert_alpha()
    ball = pg.image.load("ball.gif").convert_alpha()


    #REDIMENSIONNEMENT DES objets
    background = pg.transform.scale(background,(w,h))
    paddle = pg.transform .scale(paddle,(w//10,h//25))
    wall = pg.transform .scale(wall,(h//30,h))
    wall1 = pg.transform .scale(wall1,(h//25,h//2-20))
    wall2 = pg.transform .scale(wall2,(h//25,h//2-20))
    ball = pg.transform .scale(ball,(h//30,h//30))
    lifes = [pg.transform .scale(paddle,(w//20,h//30)),pg.transform .scale(paddle,(w//20,h//30)),pg.transform .scale(paddle,(w//20,h//30))]

    background.set_alpha(100)

    # position des objets
    position_ball = pg.Vector2(w//2,h-50-h//25)
    position_paddle = pg.Vector2(w//2-paddle.get_width()//2,h-50)
    position_wall,position_wall1,position_wall2,position_wall3 = [pg.Vector2(x,y) for x,y in [(10,20),(30,w//10),(30+w//10,w//10),(w-h//30,20)]]
    column  = rd.randrange(3,10)
    row =  int(len(bricks)/column)+1
    position_bricks = [(w//2+i*Brick().x,Brick().x+j*Brick().y) for i in range(row) for j in range(column)]
    position_lifes =[(w-3*w//20,10),(w-2*w//20,10),(w-1*w//20,10)]
        
    speed = w//200
    depl_ball = pg.Vector2(0,-speed) #deplacement de la balle
    depl_paddle = 0 #deplacement du paddle
    
    font = pg.font.SysFont("bradley hand itc",35) #POLICE DE CARACTERE
    texte,mess= "SCORE : 0000",None
    police = pg.font.SysFont("algerian",45)
    pause_surface = pg.font.SysFont("bradley hand itc",35).render("PAUSE !!!",True,"green")
    gameover_surface = pg.font.SysFont("bradley hand itc",35).render("GAME OVER !!!",True,"green")
    congrat_surface = pg.font.SysFont("bradley hand itc",35).render("CONGRATULATION !!! !!!",True,"green")
    message = ''
    coeur = 3
    x,y = w//2,h #position texte defilant
    score,brick_off = 0,0 #brick_off est le numbre de brick , ceci nous permettra de savoir si le joueur a gagner
    play,pause,gameover,congratulation = False,False,False,False
    
    running = True
    while running:
        for  event in pg.event.get():
            if event.type == pg.QUIT :
                running = False
                
            elif event.type == pg.KEYDOWN :
                if event.key == pg.K_LEFT:
                    depl_paddle = -speed-1
                elif event.key == pg.K_RIGHT:
                    depl_paddle = speed+1
                    
                elif event.key == pg.K_RETURN and gameover == False:
                    play = True
                    pause = False
                elif event.key == pg.K_BACKSPACE:
                    play = False
                    pause = True
                elif event.key == pg.K_ESCAPE:
                    running = False
                    jouer = False
                elif event.key == pg.K_0: #Restart game
                       running = False
                       
            elif event.type == pg.KEYUP:
                if event.key in [pg.K_LEFT,pg.K_RIGHT]:
                    depl_paddle = 0
                    
        #controle du deplacement des objets mobile
        if position_paddle.x <=10 or position_paddle.x >= w-100:
            depl_paddle = -depl_paddle
        
        if position_ball.x <= 50 or position_ball.x >= w-50  :
            depl_ball.x =-depl_ball.x
            
        if position_ball.y <= 10:
            depl_ball.y =-depl_ball.y
            
        if position_ball.y > h-paddle.get_height():
            #on soustrait un coeur
            coeur -= 1
            if coeur :
                y,mess =h//2, f"il reste {coeur} vies" 
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
        
        rect_bricks = [pg.Rect(x,y,50,30) for x,y in position_bricks]
                
        
        #ce qui se passe lorsqu'il y'a collision
        if rect_ball.colliderect(rect_paddle):
            x1,x2,l = position_ball.x +ball.get_width()//2 , position_paddle.x , paddle.get_width()
            if x1 >= x2 and x1 <= x2+5*l/12: #si la balle rebondit sur la partie gauche du paddle
                depl_ball.x = -speed-rd.randrange(1, 2)
                depl_ball.y = -speed
            elif x1 >= x2+7*l/12 and x1 <= x2+l: #si la balle rebondit sur la partie droite du paddle
                depl_ball.x = speed+rd.randrange(1, 2)
                depl_ball.y = -speed
            elif x1 >= x2+5*l/12 and x1 <= x2 +7*l/12:
                depl_ball.x = 0
                depl_ball.y = -speed
            
        if rect_ball.colliderect(rect_wall ) or rect_ball.colliderect(rect_wall1) or\
        rect_ball.colliderect(rect_wall2) or rect_ball.colliderect(rect_wall3):
            depl_ball.x = -depl_ball.x

        for i,brick in enumerate(bricks):
            p = brick.life
            if rect_ball.colliderect(rect_bricks[i]):
                if p == 1:
                    position_bricks[i] = (w+100,h)
                    score += 5
                    brick_off += 1
                    x,y,mess = position_ball.x, position_ball.y, "+ 5"
                else:
                    bricks[i] = Brick(p-1)
                    depl_ball.x = -depl_ball.x-rd.randrange(1, 2)
                    depl_ball.y = -depl_ball.y
                    score += 1
                    x,y,mess = position_ball.x, position_ball.y, "+ 1"
                
                    
        if play:
            position_paddle.x += depl_paddle
            position_ball.x += depl_ball.x
            position_ball.y += depl_ball.y
            y -= 3

        #CREATION SURFACE DE TEXTE
        texte = "SCORE : {}".format(score)
        score_surface = font.render(texte,True,"white")
        surface_text = police.render(mess,True,"orange")
        level_text = font.render("LEVEL : {}".format(level),True,"white")
        #POSITION DU TEXTE
        position_score = (w//4-score_surface.get_width()//2,20-score_surface.get_height()//2)
        position_level = (2*w//3-level_text.get_width()//2,20-level_text.get_height()//2)
        position_text = (x-surface_text.get_width()//2,y-surface_text.get_height()//2)

        try:
            lifes[-coeur-1].set_alpha(0)
            assert(coeur > 0)
        except AssertionError:
            mess = None
            gameover = True
            play = False
        except:
            pass
        
        if brick_off == len(bricks):
            congrat = True
            play = False
            level += 1
            running = False
            message = "NEXT LEVEL ???"
            
        fenetre.fill((0,0,0)) # remplissage du background
        fenetre.blit(background,(0,0))
        #Affichage des objets 
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
        #Affichage des textes
        fenetre.blit(score_surface,position_score)
        fenetre.blit(surface_text,position_text)
        fenetre.blit(level_text,position_level)
        if pause :
            fenetre.blit(pause_surface,(w//2,h//2))    
        if gameover:
            fenetre.blit(gameover_surface,(w//2,h//2))
            running = False
            message = "RESTART GAME ???"
            
        if congratulation:
            fenetre.blit(congrat_surface,(w//2,h//2))

        # MISE A JOUR DE LA FENETRE
        pg.display.flip()
    
    #On demande à l'utilisateur s'il veut continuer si le jeu n'a pas été interrompu
    if message :
        running  = True
        #creations des boutons
        button1_rect = pg.Rect(w//3,h//2,150,60)
        button1_text = pg.font.SysFont("elephant",55).render("YES ",True,"black")
        button2_rect = pg.Rect(2*w//3,h//2,150,50)
        button2_text = pg.font.SysFont("elephant",50).render("NO ",True,"black")
        position_question = pg.Rect(w//2-45,h//2-100,90,60)
        question = pg.font.SysFont("comic sans ms",35).render(message,True,"purple")
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1 and button1_rect.collidepoint(event.pos):
                        running = False
                    elif event.button == 1 and button2_rect.collidepoint(event.pos):
                        jouer = False
                        running = False
                
            fenetre.fill("black")
            fenetre.blit(background,(0,0))
            fenetre.blit(question, (position_question.x ,position_question.y))
            fenetre.blit(pg.transform.scale(Brick(5).img,(150,60)),button1_rect)
            fenetre.blit(button1_text, (button1_rect.x ,button1_rect.y))
            fenetre.blit(pg.transform.scale(Brick(1).img,(90,60)),button2_rect)
            fenetre.blit(button2_text, (button2_rect.x ,button2_rect.y))
            pg.display.flip()
    

#Boucle principale
while jouer :
    jouer_une_partie()
    
#Fermeture de la page
pg.quit()