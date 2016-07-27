#menu screen.py

from pygame import *
from random import *
from math import *
screen=display.set_mode((1280,720))

#--------------------------------------While Loading------------------------------
JezInc=image.load("Loading\\Jez Inc Logo.png")
And=image.load("Loading\\and.png")
ShadowGames=image.load("Loading\\shadowLogo.png")
HavePartnered=image.load("Loading\\Have Partnered.png")
JezMan=image.load("Loading\\JezMan Logo.png")
ProgrammedIn=image.load("Loading\\programmed in.png")
PythonLogo=image.load("Loading\\Python Logo.png")
WithModulesFrom=image.load("Loading\\with modules from.png")
PygameLogo=image.load("Loading\\Pygame Logo.png")

def fadeIn(surface,logo):
    for i in range(255//10):
        surface.blit(logo,(0,0))
        layer=Surface((surface.get_width(),surface.get_height()))
        layer.set_alpha(255-i*10)
        surface.blit(layer,(0,0))
        display.flip()

def fadeOut(surface,logo):
    for i in range(255//10):
        surface.blit(logo,(0,0))
        layer=Surface((surface.get_width(),surface.get_height()))
        layer.set_alpha(i*10)
        surface.blit(layer,(0,0))
        display.flip()
#---------------------------------------------------------------------------------
        

#fadeIn(screen,JezInc)
#time.wait(10)
#fadeOut(screen,JezInc)
#fadeIn(screen,And)
#time.wait(10)
#fadeOut(screen,And)
#fadeIn(screen,ShadowGames)
#time.wait(10)
#fadeOut(screen,ShadowGames)
#fadeIn(screen,HavePartnered)
#time.wait(10)
#fadeOut(screen,HavePartnered)
#fadeIn(screen,JezMan)
#time.wait(10)
#fadeOut(screen,JezMan)
#fadeIn(screen,ProgrammedIn)
#time.wait(10)
#fadeOut(screen,ProgrammedIn)
#fadeIn(screen,PythonLogo)
#time.wait(10)
#fadeOut(screen,PythonLogo)
#fadeIn(screen,WithModulesFrom)
#time.wait(10)
#fadeOut(screen,WithModulesFrom)
#fadeIn(screen,PygameLogo)
#time.wait(10)
#fadeOut(screen,PygameLogo)

#----------------------------------------------Controls Screen----------------------------
gameMap=image.load("Game Maps\Game Map.png").convert()
curPos=(1180,2450)
direction="North"
WASDkeys=image.load("Controls Screen\wasd keys.png")
RIGHTclick=image.load("Controls Screen\\right click.png")
RIGHTclick=transform.scale(RIGHTclick,(RIGHTclick.get_width()*2,RIGHTclick.get_height()*2))
LEFTclick=image.load("Controls Screen\\left click.png")
LEFTclick=transform.scale(LEFTclick,(LEFTclick.get_width()*2,LEFTclick.get_height()*2))
scroll=image.load("Controls Screen\\scroll.png")
scroll=transform.scale(scroll,(scroll.get_width()*2,scroll.get_height()*2))
pressScroll=image.load("Controls Screen\\press scroll button.png")
pressScroll=transform.scale(pressScroll,(pressScroll.get_width()*2,pressScroll.get_height()*2))

font.init()
textFont=font.SysFont("impact",30)



myClock=time.Clock()


def HelpScreen(screen,gameMap,curPos,direction,WASDkeys,
               RIGHTclick,LEFTclick,scroll,pressScroll,myClock,textFont):
    count=0
    fps=0
    fpsList=[]
    helping=True
    LEFTCLICK=textFont.render("LEFT CLICK:",True,(255,255,255))
    SHOOT=textFont.render("shoot",True,(255,255,255))

    SCROLL=textFont.render("SCROLL:",True,(255,255,255))
    CHANGEWEP=textFont.render("swap weapon",True,(255,255,255))

    RIGHTCLICK=textFont.render("RIGHT CLICK:",True,(255,255,255))
    MELEE=textFont.render("secondary attack",True,(255,255,255))

    PRESSSCROLL=textFont.render("CLICK SCROLL",True,(255,255,255))
    CHANGEMELEE=textFont.render("change melee weapon",True,(255,255,255))
    
    while helping:
        for e in event.get():
            if e.type==QUIT:
                helping=False

        #---Conditions to change current direction---
        if curPos[1]<1175:
            direction="East"
            curPos=(curPos[0],curPos[1]+2)
        elif curPos[0]>2350:
            direction="South"
            curPos=(curPos[0]-2,curPos[1])
        elif curPos[1]>3840:
            direction="West"
            curPos=(curPos[0],curPos[1]-2)
        elif curPos[0]<1170:
            direction="North"
            curPos=(curPos[0]+2,curPos[1])
        curScreen=gameMap.subsurface((curPos[0]-screen.get_width()//2, #section of map currently viewed on screen
                                       curPos[1]-screen.get_height()//2, screen.get_width(),screen.get_height())).copy()
        screen.blit(curScreen,(0,0))
        cover=Surface((screen.get_width(),screen.get_height()))
        cover.set_alpha(50)
        screen.blit(cover,(0,0))
        screen.blit(WASDkeys,(0,0))

        screen.blit(LEFTCLICK,(0,screen.get_height()-LEFTclick.get_height()-SHOOT.get_height()-LEFTCLICK.get_height()))
        screen.blit(SHOOT,(0,screen.get_height()-LEFTclick.get_height()-SHOOT.get_height()))
        screen.blit(LEFTclick,(0,screen.get_height()-LEFTclick.get_height()))

        screen.blit(SCROLL,(LEFTclick.get_width(),screen.get_height()-scroll.get_height()-SCROLL.get_height()-CHANGEWEP.get_height()))
        screen.blit(CHANGEWEP,(LEFTclick.get_width(),screen.get_height()-scroll.get_height()-CHANGEWEP.get_height()))
        screen.blit(scroll,(LEFTclick.get_width(),screen.get_height()-scroll.get_height()))

        screen.blit(RIGHTCLICK,(LEFTclick.get_width()+scroll.get_width(),screen.get_height()-RIGHTclick.get_height()-RIGHTCLICK.get_height()-MELEE.get_height()))
        screen.blit(MELEE,(LEFTclick.get_width()+scroll.get_width(),screen.get_height()-RIGHTclick.get_height()-RIGHTCLICK.get_height()))
        screen.blit(RIGHTclick,(LEFTclick.get_width()+scroll.get_width(),screen.get_height()-RIGHTclick.get_height()))

        screen.blit(PRESSSCROLL,(LEFTclick.get_width()+scroll.get_width()+RIGHTclick.get_width(),screen.get_height()-pressScroll.get_height()-PRESSSCROLL.get_height()-CHANGEMELEE.get_height()))
        screen.blit(MELEE,(LEFTclick.get_width()+scroll.get_width()+RIGHTclick.get_width(),screen.get_height()-pressScroll.get_height()-PRESSSCROLL.get_height()))
        screen.blit(pressScroll,(LEFTclick.get_width()+scroll.get_width()+RIGHTclick.get_width(),screen.get_height()-pressScroll.get_height()))

        if direction=="North":
            curPos=(curPos[0],curPos[1]-2)
        elif direction=="East":
            curPos=(curPos[0]+2,curPos[1])
        elif direction=="South":
            curPos=(curPos[0],curPos[1]+2)
        elif direction=="West":
            curPos=(curPos[0]-2,curPos[1])

            
        myClock.tick(60)
        display.flip()

#----------------------------------------------END----------------------------------------



#------------------------------------------MENU SCREEN------------------------------------
menuPage=image.load("Menu Page.png")
gun=image.load("Gun_Pointing.png")

font.init()

play=font.SysFont("impact",75).render("PLAY",True,(150,150,150))
playClicked=font.SysFont("impact",75).render("PLAY",True,(255,255,255))
playRect=Rect(screen.get_width()//2-play.get_width()//2,screen.get_height()//2,play.get_width(),
              play.get_height())
playList=(play,playClicked,playRect)
controls=font.SysFont("impact",75).render("CONTROLS",True,(150,150,150))
controlsClicked=font.SysFont("impact",75).render("CONTROLS",True,(255,255,255))
controlsRect=Rect(screen.get_width()//2-controls.get_width()//2,
                  screen.get_height()//2+play.get_height(),controls.get_width(),
                  controls.get_height())
controlsList=(controls,controlsClicked,controlsRect)
credit=font.SysFont("impact",75).render("CREDITS",True,(150,150,150))
creditsClicked=font.SysFont("impact",75).render("CREDITS",True,(255,255,255))
creditsRect=Rect(screen.get_width()//2-credit.get_width()//2,screen.get_height()//2+play.get_height()+controls.get_height(),credit.get_width(),
              credit.get_height())
creditsList=(credit,creditsClicked,creditsRect)
htp=font.SysFont("impact",75).render("HOW TO PLAY",True,(150,150,150))
htpClicked=font.SysFont("impact",75).render("HOW TO PLAY",True,(255,255,255))
htpRect=Rect(screen.get_width()//2-htp.get_width()//2,screen.get_height()//2+play.get_height()+controls.get_height()+credit.get_height(),htp.get_width(),
              htp.get_height())
htpList=[htp,htpClicked,htpRect]
optionsList=[playList,controlsList,creditsList,htpList]

class Menu:
    def __init__(self):
        self.lineList=[]
    def addLine(self,screen):
        length=randint(1,25)
        ang=randint(0,360)
        speed=randint(1,10)
        self.lineList.append(((screen.get_width()//2+cos(radians(ang))*length,
                                screen.get_height()//2-sin(radians(ang))*length),
                               (screen.get_width()//2,screen.get_height()//2),
                               length,ang,speed))
    def move(self,screen):
        removeList=[]
        for i in range(len(self.lineList)):
            startX=self.lineList[i][0][0]
            startY=self.lineList[i][0][1]
            endX=self.lineList[i][1][0]
            endY=self.lineList[i][1][1]
            length=self.lineList[i][2]
            ang=self.lineList[i][3]
            speed=self.lineList[i][4]
            self.lineList[i]=(((startX+cos(radians(ang))*speed,
                                 startY-sin(radians(ang))*speed),
                                (endX+cos(radians(ang))*speed,
                                 endY-sin(radians(ang))*speed),
                                length,ang,speed))
            if self.lineList[i][0][0]<0 or self.lineList[i][0][0]>screen.get_width():
                removeList.append(self.lineList[i])
            elif self.lineList[i][0][1]<0 or self.lineList[i][0][1]>screen.get_height():
                removeList.append(self.lineList[i])
        for item in removeList:
            self.lineList.remove(item)
    def draw(self,screen):
        for line in self.lineList:
            draw.line(screen,(255,0,0),line[0],line[1],3)

def drawOptions(screen,optionsList,mx,my):
    for option in optionsList:
        if option[2].collidepoint((mx,my)):
            screen.blit(option[0],(option[2][0],option[2][1]))
        else :
            screen.blit(option[1],(option[2][0],option[2][1]))
#-------------------------------------------------------------------------------------------

#----------------------------------------HOW TO PLAY----------------------------------------
howToPlayImg=image.load("how to play.png")
def howToPlay(screen,gun,howToPlayImg):
    showingHowToPlay=True
    back=Menu()
    while showingHowToPlay:
        for e in event.get():
            if e.type==QUIT:
                showingHowToPlay=False

        screen.fill((0,0,0))
        screen.blit(gun,(335,272))
        menu.addLine(screen)
        menu.move(screen)
        menu.draw(screen)
        screen.blit(transform.scale(howToPlayImg,(screen.get_width(),screen.get_height())),(0,0))
        display.flip()

#---------------------------------------CREDITS---------------------------------------------
#creditsFile=open("credits.txt","r")
#creditsList=creditsFile.read().split("\n")
def displayCredits(screen,gun,creditsList):
    displaying=True
    creditsFontHeight=50
    creditsFontCol=(0,0,255)
    creditsFont=font.SysFont("impact",creditsFontHeight)
    back=Menu()
    while displaying:
        for e in event.get():
            if e.type==QUIT:
                displaying=False

                
                
        screen.fill((0,0,0))
        screen.blit(gun,(335,272))
        menu.addLine(screen)
        menu.move(screen)
        menu.draw(screen)
        #for i in range(len(creditsList)):
        #    text=creditsFont.render(creditsList[i],True,creditsFontCol)
        #    screen.blit(text,(screen.get_width()//2-text.get_width()//2,50*i+10*i))
        display.flip()
        
        
        

count=0
fps=0
fpsList=[]
running=True
menu=Menu()
myClock=time.Clock()
while running:
    for e in event.get():
        if e.type==QUIT:
            running=False
        if e.type==MOUSEBUTTONDOWN and e.button==1:
            if controlsRect.collidepoint((mx,my)):
                HelpScreen(screen,gameMap,curPos,direction,WASDkeys,RIGHTclick,LEFTclick,scroll,pressScroll,
                           myClock,textFont)
            #if creditsRect.collidepoint((mx,my)):
                #displayCredits(screen,gun,creditsList)
            if htpRect.collidepoint((mx,my)):
                howToPlay(screen,gun,howToPlayImg)

    screen.fill((0,0,0))
    mx,my=mouse.get_pos()
    screen.blit(gun,(335,272))

    menu.addLine(screen)
    menu.move(screen)
    menu.draw(screen)
    screen.blit(menuPage,(screen.get_width()//2-menuPage.get_width()//2,screen.get_height()//6))

    drawOptions(screen,optionsList,mx,my)
    
    count += 1
    fps += myClock.get_fps()
    fpsList.append(myClock.get_fps())
            
    myClock.tick(60)
    display.flip()
print(fps/count)
print(max(fpsList))
print(min(fpsList))
quit()
