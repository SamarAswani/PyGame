import pygame
from pygame.locals import *

BACKGROUNDCOLOUR = (97,143,248)
PINK = (248, 24, 148)
PLAYERICON_BASE = "adventurer-run3-0"
PLAYERICON_EXT = ".png"
BLOCKICON = "rawSauce"
BLOCKICON_EXT = ".jpg"
PLAYERMOVE = 5
PLAYERICON_IMAGES = 6
BLOCKICON_IMAGES = 4
WHITE = (255,255,255)
WINDOWWIDTH = 800
WINDOWHEIGHT = 400
gravity = 0.7
SPRITEHEIGHT = 37
SPRITEWIDTH = 40
BLOCKWIDTH = 50
HighScores = open("HighScores.txt","a")
readHighScore=open("HighScores.txt","r")

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.imageCounter = 0
        self.images = []
        self.gravity = True
        self.jumps = 0
        for i in range(PLAYERICON_IMAGES):
            self.images.append(pygame.image.load(PLAYERICON_BASE+str(i)+PLAYERICON_EXT))
            self.image = self.images[self.imageCounter]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y

            self.changeX = 0
            self.changeY = 0

    def getRect(self):
        return self.rect

    def getSurface(self):
        return self.image

    def moveLeft(self):
        self.changeX = -PLAYERMOVE

    def moveRight(self):
        self.changeX = PLAYERMOVE

    def moveUp(self):
        self.changeY = PLAYERMOVE

    def moveDown(self):
        self.changeY = -PLAYERMOVE

    def stopHoriz(self):
        self.changeX = 0

    def stopVert(self):
        self.changeY =0

    def jump(self):
        if self.rect.y == (WINDOWHEIGHT - SPRITEHEIGHT):
            self.jumps = 0

        if self.jumps >=1:
            self.changeY = 0
        else:
            self.changeY = -12
            self.jumps +=1

    def getJump(self):
        return self.jumps
    def getY(self):
        return self.rect.y

    def updatePos(self):
        self.rect.x += self.changeX
        self.rect.y += self.changeY
        #if self.jumps < 3:
            #self.rect.y += self.changeY
        #else:
            #self.changeY = gravity
            #self.rect.y += self.changeY

        if self.changeX > 0:
            self.imageCounter = (self.imageCounter +1)%PLAYERICON_IMAGES
            self.image = self.images[self.imageCounter]
        if self.changeX<0:
            self.imageCounter = (self.imageCounter+1)%PLAYERICON_IMAGES
            self.image = pygame.transform.flip(self.images[self.imageCounter],True,False)

        if self.rect.x <= 0:
            self.stopHoriz()
            self.rect.x = 0
        if self.rect.x >= (WINDOWWIDTH - SPRITEWIDTH):
            self.rect.x = (WINDOWWIDTH - SPRITEWIDTH)

        if self.gravity:
            self.changeY+=gravity
            if self.rect.y > (WINDOWHEIGHT - SPRITEHEIGHT):
                self.stopVert()
                self.rect.y = (WINDOWHEIGHT - SPRITEHEIGHT)



class Block (pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.reset = False
            self.imageCounter = 0
            self.images = []
            for i in range(BLOCKICON_IMAGES):
                image = pygame.image.load(BLOCKICON+str(i)+BLOCKICON_EXT)
                image = pygame.transform.scale(image, (50, 50))
                self.images.append(image)

            self.image = self.images[self.imageCounter]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.gravity = True
            self.changeX = -3
            self.changeY = 0
            self.score = 0

        def getRect(self):
            return self.rect

        def getSurface(self):
            return self.image

        def stopHoriz(self):
            self.changeX = 0

        #def move(self):
            #self.changeX = -3

        def getHoriz(self):
            return self.rect.x

        def resetBlock(self):
            self.reset = True


        def updatePos(self):
            if (self.reset == False):
                self.rect.x += self.changeX
                self.rect.y = (WINDOWHEIGHT - 50)
            else:
                self.rect.x = 900
                self.imageCounter = (self.imageCounter +1)%BLOCKICON_IMAGES
                self.image = self.images[self.imageCounter]
                self.reset=False
                self.changeX -=0.5




def menu(HighScores, readHighScore):
  windowsurface = pygame.display.set_mode((WINDOWWIDTH,WINDOWHEIGHT))
  myFont = pygame.font.SysFont("Calibri", 70)
  pygame.mouse.set_visible(True)
  pScores=[]
  max=0
  for line in readHighScore:
      pScores.append(line.strip())

  for i in pScores:
      temp = int(i)
      if temp > max:
          max = temp
      else:
          continue
  print("Highscore: ",max)

  while True:
    # fill the background which will over write everything
    windowsurface.fill(BACKGROUNDCOLOUR)

    # blit anything required onto the screen
    pygame.draw.rect(windowsurface, PINK, ((WINDOWWIDTH/4), (WINDOWHEIGHT/10), (WINDOWWIDTH/2), (WINDOWHEIGHT/3)))
    playText = myFont.render(("Start game"), True, (WHITE))
    playText_rect = playText.get_rect(center =(WINDOWWIDTH/2,WINDOWHEIGHT/3.5))
    windowsurface.blit(playText, playText_rect)

    pygame.draw.rect(windowsurface, PINK, ((WINDOWWIDTH/4), (WINDOWHEIGHT/1.8), (WINDOWWIDTH/2), (WINDOWHEIGHT/3)))
    playText1 = myFont.render(("Muliplayer"), True, (WHITE))
    playText_rect1 = playText.get_rect(center =(WINDOWWIDTH/2,WINDOWHEIGHT/1.4))
    windowsurface.blit(playText1, playText_rect1)

    # update the screen to show what has been drawn/blitted/buffered
    pygame.display.update()


    # main event handling loop
    for event in pygame.event.get():
      if event.type == QUIT:
        exit()

      if event.type == pygame.MOUSEBUTTONDOWN:
        mouseX, mouseY = pygame.mouse.get_pos()

        if mouseX >= (WINDOWWIDTH/4) and mouseX <= ((WINDOWWIDTH/4)+(WINDOWWIDTH/2)) and mouseY >= (WINDOWHEIGHT/10) and mouseY <= ((WINDOWHEIGHT/10)+(WINDOWHEIGHT/3)):
          playGame(windowsurface, HighScores)

        if mouseX >= (WINDOWWIDTH/4) and mouseX <= ((WINDOWWIDTH/4)+(WINDOWWIDTH/2)) and mouseY >= (WINDOWHEIGHT/1.8) and mouseY <= ((WINDOWHEIGHT/1.8)+(WINDOWHEIGHT/3)):
          playGameMultiplayer(windowsurface, HighScores)

        else:
          print("Click outside rectangle")

def playGame(windowsurface, HighScores):
    gameOver = False

    players = [Player(100,100), Block(700,100)]
    score = 0
    multiplayer = False

    while not gameOver:
    # fill the background which will over write everything
        windowsurface.fill(BACKGROUNDCOLOUR)
        myFont = pygame.font.SysFont("Calibri", 50)
        playText = myFont.render("Score: "+ str(score), True, (WHITE))
        playText_rect = playText.get_rect(center =(WINDOWWIDTH/1.2,WINDOWHEIGHT/6.5))
        windowsurface.blit(playText, playText_rect)
        ground = False

        p = players[0]
        pBlock = players[1]

        if p.getY() == (WINDOWHEIGHT - SPRITEHEIGHT):
            ground = True

        col = pygame.sprite.collide_rect(p, pBlock)
        if col == True:
            HighScores.write(str(score)+'\n')
            GameOver(windowsurface, score, HighScores, multiplayer)

        if (pBlock.getHoriz() <= 2):
            pBlock.resetBlock()
            score +=1



        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                if (event.key == K_DOWN or event.key == K_s):
                    p.moveUp()
                if (event.key == K_UP or event.key == K_w) and (((p.getJump()) <1) or ground == True):
                    p.jump()
                if (event.key == K_LEFT or event.key == K_a):
                    p.moveLeft()
                if (event.key == K_RIGHT or event.key == K_d):
                    p.moveRight()

            if event.type == KEYUP:
                if (event.key == K_UP or event.key == K_w):
                    p.stopVert()
                if (event.key == K_DOWN or event.key == K_s):
                    p.stopVert()
                if (event.key == K_RIGHT or event.key == K_d):
                    p.stopHoriz()
                if (event.key == K_LEFT or event.key == K_a):
                    p.stopHoriz()

        p.updatePos()
        pBlock.updatePos()

# blit the players
        for p in players:
            windowsurface.blit(p.getSurface(), p.getRect())

# update the screen to show what has been drawn/blitted/buffered
        pygame.display.update()

def playGameMultiplayer(windowsurface, HighScores):
    gameOver = False

    players = [Player(100,100), Block(700,100), Player(150,100)]
    score = 0
    multiplayer = True

    while not gameOver:
    # fill the background which will over write everything
        windowsurface.fill(BACKGROUNDCOLOUR)
        myFont = pygame.font.SysFont("Calibri", 50)
        playText = myFont.render("Score: "+ str(score), True, (WHITE))
        playText_rect = playText.get_rect(center =(WINDOWWIDTH/1.2,WINDOWHEIGHT/6.5))
        windowsurface.blit(playText, playText_rect)
        ground = False
        ground1 = False

        p = players[0]
        p1 = players[2]
        pBlock = players[1]

        if p.getY() == (WINDOWHEIGHT - SPRITEHEIGHT):
            ground = True
        if p1.getY() == (WINDOWHEIGHT - SPRITEHEIGHT):
            ground1 = True

        col = pygame.sprite.collide_rect(p, pBlock)
        if col == True:
            HighScores.write(str(score)+'\n')
            GameOver(windowsurface, score, HighScores, multiplayer)
        col1 = pygame.sprite.collide_rect(p1, pBlock)
        if col1 == True:
            HighScores.write(str(score)+'\n')
            GameOver(windowsurface, score, HighScores, multiplayer)

        if (pBlock.getHoriz() <= 2):
            pBlock.resetBlock()
            score +=1


        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == KEYDOWN:
                if (event.key == K_DOWN):
                    p.moveUp()
                if (event.key == K_UP) and (((p.getJump()) <1) or ground == True):
                    p.jump()
                if (event.key == K_LEFT):
                    p.moveLeft()
                if (event.key == K_RIGHT):
                    p.moveRight()
                if (event.key == K_s):
                    p1.moveUp()
                if (event.key == K_w) and (((p1.getJump()) <1) or ground1 == True):
                    p1.jump()
                if (event.key == K_a):
                    p1.moveLeft()
                if (event.key == K_d):
                    p1.moveRight()

            if event.type == KEYUP:
                if (event.key == K_UP):
                    p.stopVert()
                if (event.key == K_DOWN):
                    p.stopVert()
                if (event.key == K_RIGHT):
                    p.stopHoriz()
                if (event.key == K_LEFT):
                    p.stopHoriz()
                if (event.key == K_w):
                    p1.stopVert()
                if (event.key == K_s):
                    p1.stopVert()
                if (event.key == K_d):
                    p1.stopHoriz()
                if (event.key == K_a):
                    p1.stopHoriz()

        p.updatePos()
        pBlock.updatePos()
        p1.updatePos()

# blit the players
        for p in players:
            windowsurface.blit(p.getSurface(), p.getRect())

# update the screen to show what has been drawn/blitted/buffered
        pygame.display.update()



def GameOver(windowsurface, score, HighScores, multiplayer):
    myFont = pygame.font.SysFont("Calibri", 35)
    pygame.mouse.set_visible(True)
    while True:
        windowsurface.fill(BACKGROUNDCOLOUR)
        pygame.draw.rect(windowsurface, PINK, ((WINDOWWIDTH/5.7), (WINDOWHEIGHT/8), (WINDOWWIDTH/1.5), (WINDOWHEIGHT/3)))
        playText = myFont.render(("Score: " + str(score)), True, (WHITE))
        playText_rect = playText.get_rect(center =(WINDOWWIDTH/3,WINDOWHEIGHT/5))
        playText1 = myFont.render(("Game Over (Click here to restart)"), True, (WHITE))
        playText1_rect = playText.get_rect(center =(WINDOWWIDTH/3,WINDOWHEIGHT/3))
        windowsurface.blit(playText, playText_rect)
        windowsurface.blit(playText1, playText1_rect)

        # update the screen to show what has been drawn/blitted/buffered
        pygame.display.update()

        # main event handling loop
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouseX, mouseY = pygame.mouse.get_pos()

                if mouseX >= (WINDOWWIDTH/5.7) and mouseX <= ((WINDOWWIDTH/5.7)+(WINDOWWIDTH/1.5)) and mouseY >= (WINDOWHEIGHT/8) and mouseY <= ((WINDOWHEIGHT/8)+(WINDOWHEIGHT/3)):
                  if multiplayer == True:
                      playGameMultiplayer(windowsurface, HighScores)
                  else:
                      playGame(windowsurface, HighScores)




# MAIN PROGRAM
pygame.init()
menu(HighScores, readHighScore)
