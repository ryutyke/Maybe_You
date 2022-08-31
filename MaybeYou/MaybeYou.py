import math
import pygame
import random
import time

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)
red = (255, 0, 0)
red2 = (200, 0, 0)
red3 = (150, 0, 0)
gray = (160,161,157)
purple = (153,50,204)
lightgreen = (0,200,0)
lightpurple = (150,123,220)


pygame.init()

screen = pygame.display.set_mode([display_width,display_height])

pygame.display.set_caption('Maybe You')
clock = pygame.time.Clock()

font = pygame.font.Font(None, 36) 
font1 = pygame.font.Font(None, 20) #monster hp

shooteffect = pygame.mixer.Sound('fire.wav')
collideffect = pygame.mixer.Sound('collide.wav')
hurteffect = pygame.mixer.Sound('hurt.wav')
monsterdieeffect = pygame.mixer.Sound('monsterdie.wav')

#랜덤 위치 생성 블록
class Block(pygame.sprite.Sprite):

    def __init__(self, color, x, y, w, h):

        super().__init__()

        self.image = pygame.Surface([w, h])

        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.width = w
        self.height = h
        self.rect.x = x
        self.rect.y = y


class Ball(pygame.sprite.Sprite):
    speed = 1.0

    x = 387.0
    y = 550.0
    ballDamage = 1
    # degrees
    direction = 0
    level = 1
    width = 10
    height = 10

    def __init__(self, direction, x):
        super().__init__()
        self.damage = Ball.ballDamage
        
        self.direction = direction
        self.isCollide = False

        self.image = pygame.Surface([self.width, self.height])

        self.image.fill(black)

        self.rect = self.image.get_rect()

        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
        if x < 0:
            self.rect.x = 387.0
        else:
            self.x = x
            self.rect.x = x
        
        self.rect.y = self.y

    def damageUp(self):
        self.damage += self.level
        return self.damage
    def returnDamage(self):
        return self.damage
    def bounce(self, block, collidepointx, collidepointy):
        collideffect.play()
        self.isCollide = True
        if collidepointx <= block.rect.x - 8:
            self.direction = (360 - self.direction) % 360
            self.x = block.rect.x - self.width - 1
        elif collidepointx >= block.rect.x + block.width - 2:
            self.direction = (360 - self.direction) % 360
            self.x = block.rect.x + block.width + 1
        elif collidepointy <= block.rect.y -8:
            self.direction = (180 - self.direction) % 360
            self.y = block.rect.y - self.height - 1
        elif collidepointy >= block.rect.y + block.height - 2:
            self.direction = (180 - self.direction) % 360
            self.y >= block.rect.y + block.height + 10

    def update(self):
        direction_radians = math.radians(self.direction)

        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        self.rect.x = self.x
        self.rect.y = self.y

class Player(pygame.sprite.Sprite):
    statPoint = 0
    shild = 0
    level = 1
    def __init__(self, x):

        super().__init__()
        self.x = x
        self.life = 100
        self.width = 40
        self.height = 80
        self.exp = 0
        
        #self.image = pygame.Surface([self.width, self.height])
        #self.image.fill((black))

        self.image = pygame.image.load('man.png')
        self.image = pygame.transform.scale(self.image, (self.width,self.height))

        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()

        self.rect = self.image.get_rect()
        if self.x < 0:
            self.rect.x = self.screenwidth / 2 - self.width / 2  #(800, 600)
            self.rect.y = self.screenheight-self.height
        else:
            self.rect.x = self.x
            self.rect.y = self.screenheight-self.height
    
    def hit(self, damage):
        if damage - Player.shild > 0:
            hurteffect.play()
            self.life = self.life - damage

    def shoot(self, x):
        shooteffect.play()
        pos = pygame.mouse.get_pos()
        mouseV = [pos[0] - (self.rect.x + self.width/2), pos[1] - (self.rect.y + self.height / 2)]
        mouseV = [mouseV[0] / math.sqrt(mouseV[0]**2 + mouseV[1]**2), mouseV[1]/ math.sqrt(mouseV[0]**2 + mouseV[1]**2)] #단위벡터
        #[0,1] 과의 사이각
        betweenV = math.acos(0*mouseV[0] + 1*mouseV[1])
        betweenV = math.degrees(betweenV)
        if(pos[0] <= self.rect.x + self.width/2):
            return Ball(betweenV + 180, x)
        else:
            return Ball(180 - betweenV, x)
    def levelUP(self):
        self.exp = self.exp - 100
        Player.level += 1
        Player.statPoint += 1
    def getExp(self, exp):
        self.exp += exp

class Monster1(pygame.sprite.Sprite): #지렁이
    
    def __init__(self):

        super().__init__()
        
        self.life = 5 + (Player.level - 1)
        
        self.exp = 35
        self.speed = 40
        self.width = 50
        self.height = 25
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((red))
        xList = [15 ,785 - self.width]

        self.rect = self.image.get_rect()
        self.rect.x = xList[random.randint(0,1)]
        self.rect.y = 585 - self.height
    
    def hit(self, damage):
        self.life = self.life - damage

    def move(self):
        self.ToplayerV = [400 - (self.rect.x + self.width / 2), 560 - (self.rect.y + self.height/2)]
        self.ToplayerV = [self.ToplayerV[0] / math.sqrt(self.ToplayerV[0]**2 + self.ToplayerV[1]**2), self.ToplayerV[1]/ math.sqrt(self.ToplayerV[0]**2 + self.ToplayerV[1]**2)] #단위벡터화
        self.ToplayerV = [self.ToplayerV[0] * self.speed, self.ToplayerV[1] * self.speed]
        self.rect.x += self.ToplayerV[0]
        self.rect.y += self.ToplayerV[1]

    def ReturnPower(self): #power = life
        return self.life
    
    def hptextPos(self):
        self.textpos = [self.rect.x + 13, self.rect.y + 7]
        return self.textpos

class Monster2(pygame.sprite.Sprite): #새
    
    def __init__(self):

        super().__init__()
        
        self.life = 5 + (Player.level - 1)
        self.exp = 35
        self.speed = 50
        self.width = 40
        self.height = 40
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((red2))
        xList = [15 ,785 - self.width]
        yList = [100, 150, 200, 250]

        self.rect = self.image.get_rect()
        self.rect.x = xList[random.randint(0,1)]
        self.rect.y = yList[random.randint(0,3)]
    
    def hit(self, damage):
        self.life = self.life - damage

    def move(self):
        self.ToplayerV = [400 - (self.rect.x + self.width / 2), 560 - (self.rect.y + self.height/2)]
        self.ToplayerV = [self.ToplayerV[0] / math.sqrt(self.ToplayerV[0]**2 + self.ToplayerV[1]**2), self.ToplayerV[1]/ math.sqrt(self.ToplayerV[0]**2 + self.ToplayerV[1]**2)] #단위벡터화
        self.ToplayerV = [self.ToplayerV[0] * self.speed, self.ToplayerV[1] * self.speed]
        self.rect.x += self.ToplayerV[0]
        self.rect.y += self.ToplayerV[1]

    def ReturnPower(self): #power = life
        return self.life
    def hptextPos(self):
        self.textpos = [self.rect.x + 10, self.rect.y + 10]
        return self.textpos

class Monster3(pygame.sprite.Sprite): #큰애
    
    def __init__(self):

        super().__init__()
        
        self.life = 20 + (Player.level - 1)
        self.exp = 60
        self.speed = 30
        self.width = 65
        self.height = 65
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((red3))
        xList = [15 ,785 - self.width]
        yList = [100, 150, 200, 250]

        self.rect = self.image.get_rect()
        self.rect.x = xList[random.randint(0,1)]
        self.rect.y = yList[random.randint(0,3)]
    
    def hit(self, damage):
        self.life = self.life - damage

    def move(self):
        self.ToplayerV = [400 - (self.rect.x + self.width / 2), 560 - (self.rect.y + self.height/2)]
        self.ToplayerV = [self.ToplayerV[0] / math.sqrt(self.ToplayerV[0]**2 + self.ToplayerV[1]**2), self.ToplayerV[1]/ math.sqrt(self.ToplayerV[0]**2 + self.ToplayerV[1]**2)] #단위벡터화
        self.ToplayerV = [self.ToplayerV[0] * self.speed, self.ToplayerV[1] * self.speed]
        self.rect.x += self.ToplayerV[0]
        self.rect.y += self.ToplayerV[1]

    def ReturnPower(self): #power = life
        return self.life
    def hptextPos(self):
        self.textpos = [self.rect.x + 10, self.rect.y + 10]
        return self.textpos

def gamequit():
    pygame.quit()
    quit()
def BallLevelUp():
    if Player.statPoint > 0:
        Player.statPoint -= 1
        Ball.ballDamage += 3
def ShildLevelUp():
    if Player.statPoint > 0:
        Player.statPoint -= 1
        Player.shild += 2
def BallIncreaseUP():
    if Player.statPoint > 0:
        Player.statPoint -= 1
        Ball.level += 1
        
def text_objects(text,font, color):
    textSurface = font.render(text, True , color)
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse=pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    smallText= pygame.font.Font('freesansbold.ttf',20)

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        textSurf, textRect = text_objects(msg, smallText, purple)
        textRect.center = ( x+(w/2), y+(h/2))
        screen.blit(textSurf, textRect)
        if click[0] == 1 and action !=None:
            action()

    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
        textSurf, textRect = text_objects(msg, smallText, lightpurple)
        textRect.center = ( x+(w/2), y+(h/2))
        screen.blit(textSurf, textRect)

def introscreen():
    
    Ball.ballDamage = 1
    Player.statPoint = 0
    Player.shild = 0
    Ball.level = 1
    Player.level = 1

    pygame.mixer.music.load('introbgm.mp3')
    pygame.mixer.music.play(-1)

    logo = pygame.image.load("logo.png")
    logo = pygame.transform.scale(logo, (400,150))
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamequit()
        screen.fill(black)

        screen.blit(logo, (200, 20))

        button("Single",270,310,105,30,black,black,singleplay)
        button("Two Players",270,430,105,30,black,black,twoplay)
        button("Quit",470,490,55,30,black,black,gamequit)
        button("Rule",470,370,55,30,black,black,rulescreen)
       
        pygame.display.update()
        clock.tick(15)


def rulescreen():
     rule = pygame.image.load("rule.png")
     rule = pygame.transform.scale(rule, (750,450))
     intro = True
     while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamequit()
        screen.fill(black)
        screen.blit(rule, (10,10))

        button("Back",220,530,55,30,black,black,introscreen)
        
        pygame.display.update()
        clock.tick(15)

def gameoverscreen(winner):

    gameover=True
    while gameover:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamequit()
        screen.fill(black)
        largeText = pygame.font.Font('freesansbold.ttf',80)
        if winner == -1:
            TextSurf, TextRect = text_objects("GameOver",largeText, lightpurple)
            TextRect.center = ((display_width/2),(display_height/5))
            screen.blit(TextSurf, TextRect)
        else:
            TextSurf, TextRect = text_objects(str(winner)+" Win!!",largeText, lightpurple)
            TextRect.center = ((display_width/2),(display_height/5))
            screen.blit(TextSurf, TextRect)

        button("Intro",370,280,55,30,black,black,introscreen)
        button("Quit",370,380,55,30,black,black,gamequit)
    
        pygame.display.update()
        clock.tick(15)

def singleplay():

    pygame.mixer.music.stop()
    pygame.mixer.music.load('mainbgm.mp3')
    pygame.mixer.music.play(-1)

    #background = pygame.image.load('back1.png')
    background = pygame.Surface(screen.get_size())

    blocks = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    players = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()
    monsters = pygame.sprite.Group()

    monster = Monster1()
    monsters.add(monster)
    allsprites.add(monster)

    player = Player(-1)
    players.add(player)
    allsprites.add(player)

    block = Block(black, 0, 0, 15, 600)
    blocks.add(block)
    allsprites.add(block)
    block = Block(black, 785, 0, 15, 600)
    blocks.add(block)
    allsprites.add(block)
    block = Block(black, 0, 0, 800, 60)
    blocks.add(block)
    allsprites.add(block)
    block = Block(black, 0, 585, 800, 15)
    blocks.add(block)
    allsprites.add(block)


    playerTurn = True

    game_over = False
    ExistBall = False

    exit_program = False
    score = 0
    damage = 1
    block_x = 0
    block_y = 0
    block_w = 0
    block_h = 0

    while exit_program != True:

        clock.tick(2000)

        screen.fill(white)

        if playerTurn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_program = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (not game_over) and (not ExistBall):
                        mouse=pygame.mouse.get_pos()
                        if mouse[1] > 60:
                            ball = player.shoot(-1)
                            allsprites.add(ball)
                            balls.add(ball)
                            ExistBall = True
            # bullet 데미지 가져오는 함수, 그만큼 플레이어 피 깎아주는 함수.
            if(ExistBall):
                for rectangle in blocks:
                    if pygame.sprite.collide_rect(ball, rectangle):
                        ball.bounce(rectangle, ball.x, ball.y)
                        damage = ball.damageUp()
    
                if pygame.sprite.spritecollide(ball, players, False):
                    if ball.isCollide == True:
                        BulletDamage = ball.returnDamage()
                        player.hit(BulletDamage)
                        ball.kill()
                        ExistBall = False
                        damage = Ball.ballDamage
                        playerTurn = False
                for monster in monsters:
                    if pygame.sprite.collide_rect(monster, ball):
                        BulletDamage = ball.returnDamage()
                        monster.hit(BulletDamage)
                        ball.kill()
                        ExistBall = False
                        damage = Ball.ballDamage
                        playerTurn = False
                        if monster.life <= 0:
                            player.getExp(monster.exp)
                            if player.exp >= 100:
                                player.levelUP()
                            monster.kill()
                            monsterdieeffect.play()
                            score += 1
                ball.update()

            allsprites.draw(screen)
            for monster in monsters:
                textpos = monster.hptextPos()
                hp = monster.ReturnPower()
                text = font1.render(str(hp), True, black)
                screen.blit(text, textpos)
            text = font.render("Player's HP: "+str(player.life), True, white)
            screen.blit(text, [10, 5])
            text = font.render("Level: "+str(Player.level), True, white)
            screen.blit(text, [10, 30])
            text = font.render("("+str(player.exp)+" / 100)", True, white)
            screen.blit(text, [130, 30])
            text = font.render("Bullet Power: "+str(damage), True, white)
            screen.blit(text, [500, 5])
            text = font.render("Score: "+str(score), True, white)
            screen.blit(text, [270, 5])
            text = font.render("Stat Point: "+str(player.statPoint), True, white)
            screen.blit(text, [270, 30])

            text = font.render(str(Ball.ballDamage), True, white)
            screen.blit(text, [520, 34])            
            text = font.render(str(Player.shild), True, white)
            screen.blit(text, [610, 34])
            text = font.render(str(Ball.level), True, white)
            screen.blit(text, [720, 34])
            button("Damage",450,40,50,10,black,black,BallLevelUp)
            button("Shild",550,40,50,10,black,black,ShildLevelUp)
            button("Increase",650,40,50,10,black,black,BallIncreaseUP)
            
        if player.life <= 0:
            game_over = True
            gameoverscreen(-1)
        if playerTurn == False:
        
            for a in blocks:
                a.kill()

            #몬스터 턴
            #1. 몬스터 이동
            for monster in monsters:
                monster.move()
                if pygame.sprite.collide_rect(monster, player):
                    power = monster.ReturnPower()
                    monster.kill()
                    if power > Player.shild:
                        player.hit(power - Player.shild)
            #2. 몬스터 생성
            rand = random.randint(0,2)
            if(rand == 0):
                monster = Monster1()
            elif(rand == 1):
                monster = Monster2()
            else:
                monster = Monster3()
            monsters.add(monster)
            allsprites.add(monster)

            playerTurn = True
        

            for a in range(Player.level):
                keepDo = True
                while(keepDo):
                    block_x = random.randint(15,770)
                    block_y = random.randint(60,570)
                    block_w = random.randint(15,300)
                    block_h = random.randint(15,300)
                    block = Block(green, block_x, block_y, block_w, block_h)
                    blocks.add(block)
                    allsprites.add(block)
                    if pygame.sprite.spritecollide(player, blocks, False):
                        block.kill()
                        #for a in blocks:
                        #    a.kill()
                    elif pygame.sprite.spritecollide(block, monsters, False):
                        block.kill()
                        #for a in blocks:
                        #    a.kill()
                    else:
                        keepDo = False
            
            block = Block(black, 0, 0, 15, 600)
            blocks.add(block)
            allsprites.add(block)
            block = Block(black, 785, 0, 15, 600)
            blocks.add(block)
            allsprites.add(block)
            block = Block(black, 0, 0, 800, 60)
            blocks.add(block)
            allsprites.add(block)
            block = Block(black, 0, 585, 800, 15)
            blocks.add(block)
            allsprites.add(block)

        pygame.display.flip()

    pygame.quit()

def twoplay():

    pygame.mixer.music.stop()
    pygame.mixer.music.load('mainbgm.mp3')
    pygame.mixer.music.play(-1)
    #background = pygame.image.load('back1.png')
    background = pygame.Surface(screen.get_size())

    blocks = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    players = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()

    player1 = Player(100)
    players.add(player1)
    allsprites.add(player1)

    player2 = Player(700)
    players.add(player2)
    allsprites.add(player2)

    block = Block(black, 0, 0, 15, 600)
    blocks.add(block)
    allsprites.add(block)
    block = Block(black, 785, 0, 15, 600)
    blocks.add(block)
    allsprites.add(block)
    block = Block(black, 0, 0, 800, 60)
    blocks.add(block)
    allsprites.add(block)
    block = Block(black, 0, 585, 800, 15)
    blocks.add(block)
    allsprites.add(block)


    player1Turn = False
    player2Turn = False

    player1Win = False
    player2Win = False

    game_over = False
    ExistBall = False

    exit_program = False
    damage = 1
    block_x = 0
    block_y = 0
    block_w = 0
    block_h = 0

    while exit_program != True:

        clock.tick(2000)

        screen.fill(white)

        if player1Turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_program = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (not game_over) and (not ExistBall):
                        mouse=pygame.mouse.get_pos()
                        if mouse[1] > 60:
                            ball = player1.shoot(110)
                            allsprites.add(ball)
                            balls.add(ball)
                            ExistBall = True
            if(ExistBall):
                for rectangle in blocks:
                    if pygame.sprite.collide_rect(ball, rectangle):
                        ball.bounce(rectangle, ball.x, ball.y)
                        damage = ball.damageUp()
    
                if pygame.sprite.spritecollide(player1, balls, False):
                    if ball.isCollide == True:
                        BulletDamage = ball.returnDamage()
                        player1.hit(BulletDamage)
                        ball.kill()
                        ExistBall = False
                        damage = Ball.ballDamage
                        if player1Turn:
                            player1Turn = False
                            player2Turn = True
                        else:
                            player2Turn = False

                        
                if pygame.sprite.spritecollide(player2, balls, False):
                    if ball.isCollide == True:
                        BulletDamage = ball.returnDamage()
                        player2.hit(BulletDamage)
                        ball.kill()
                        ExistBall = False
                        damage = Ball.ballDamage
                        if player1Turn:
                            player1Turn = False
                            player2Turn = True
                        else:
                            player2Turn = False
                
                ball.update()

            allsprites.draw(screen)

            text = font.render("Player1's HP: "+str(player1.life), True, white)
            screen.blit(text, [10, 5])
            text = font.render("Player2's HP: "+str(player2.life), True, white)
            screen.blit(text, [580, 5])
            text = font.render("Bullet Power: "+str(damage), True, white)
            screen.blit(text, [300, 5])
        elif player2Turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_program = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if (not game_over) and (not ExistBall):
                        mouse=pygame.mouse.get_pos()
                        if mouse[1] > 60:
                            ball = player2.shoot(710)
                            allsprites.add(ball)
                            balls.add(ball)
                            ExistBall = True
            # bullet 데미지 가져오는 함수, 그 만큼 플레이어 피 깎아주는 함수.
            if(ExistBall):
                for rectangle in blocks:
                    if pygame.sprite.collide_rect(ball, rectangle):
                        ball.bounce(rectangle, ball.x, ball.y)
                        damage = ball.damageUp()
    
                if pygame.sprite.spritecollide(player1, balls, False):
                    if ball.isCollide == True:
                        BulletDamage = ball.returnDamage()
                        player1.hit(BulletDamage)
                        ball.kill()
                        ExistBall = False
                        damage = Ball.ballDamage
                        if player1Turn:
                            player1Turn = False
                            player2Turn = True
                        else:
                            player2Turn = False

                        
                if pygame.sprite.spritecollide(player2, balls, False):
                    if ball.isCollide == True:
                        BulletDamage = ball.returnDamage()
                        player2.hit(BulletDamage)
                        ball.kill()
                        ExistBall = False
                        damage = Ball.ballDamage
                        if player1Turn:
                            player1Turn = False
                            player2Turn = True
                        else:
                            player2Turn = False
                
                ball.update()

            allsprites.draw(screen)
            
            text = font.render("Player1's HP: "+str(player1.life), True, white)
            screen.blit(text, [10, 5])
            text = font.render("Player2's HP: "+str(player2.life), True, white)
            screen.blit(text, [580, 5])
            text = font.render("Bullet Power: "+str(damage), True, white)
            screen.blit(text, [300, 5])
            
        if player1.life <= 0:
            game_over = True
            player2Win = True
            gameoverscreen("player2")
            
        if player2.life <= 0:
            game_over = True
            player1Win = True
            gameoverscreen("player1")

        if player1Turn == False and player2Turn == False:
            for a in blocks:
                a.kill()

            for a in range(3):
                keepDo = True
                while(keepDo):
                    block_x = random.randint(15,770)
                    block_y = random.randint(60,570)
                    block_w = random.randint(15,300)
                    block_h = random.randint(15,300)
                    block = Block(green, block_x, block_y, block_w, block_h)
                    blocks.add(block)
                    allsprites.add(block)
                    if pygame.sprite.spritecollide(block, players, False):
                        block.kill()
                    else:
                        keepDo = False
            
            block = Block(black, 0, 0, 15, 600)
            blocks.add(block)
            allsprites.add(block)
            block = Block(black, 785, 0, 15, 600)
            blocks.add(block)
            allsprites.add(block)
            block = Block(black, 0, 0, 800, 60)
            blocks.add(block)
            allsprites.add(block)
            block = Block(black, 0, 585, 800, 15)
            blocks.add(block)
            allsprites.add(block)
            player1Turn = True

        pygame.display.flip()

    pygame.quit()

introscreen()