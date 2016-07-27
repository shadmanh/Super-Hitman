#menu screen.py

from pygame import *
from random import *
from math import *
screen=display.set_mode((1280,720))
img=image.load("Menu Page.png")
gun=image.load("Gun_Pointing.png")

font.init()

play=font.SysFont("impact",75).render("PLAY",True,(100,100,100))
playClicked=font.SysFont("impact",75).render("PLAY",True,(255,255,255))
playRect=Rect(screen.get_width()//2-play.get_width()//2,screen.get_height()//2,play.get_width(),
              play.get_height())
controls=font.SysFont("impact",75).render("CONTROLS",True,(100,100,100))
controlsClicked=font.SysFont("impact",75).render("CONTROLS",True,(255,255,255))
controlsRect=Rect(screen.get_width()//2-controls.get_width()//2,
                  screen.get_height()//2+play.get_height(),controls.get_width(),
                  controls.get_height())


#((startX,startY),(endX,endY),length)
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

    screen.fill((0,0,0))
    mx,my=mouse.get_pos()
    screen.blit(gun,(335,272))

    menu.addLine(screen)
    menu.move(screen)
    menu.draw(screen)
    screen.blit(img,(screen.get_width()//2-img.get_width()//2,screen.get_height()//6))

    if playRect.collidepoint((mx,my)):
        screen.blit(playClicked,(screen.get_width()//2-play.get_width()//2,screen.get_height()//2))
    else :
        screen.blit(play,(screen.get_width()//2-play.get_width()//2,screen.get_height()//2))

    if controlsRect.collidepoint((mx,my)):
        screen.blit(controlsClicked,(screen.get_width()//2-controls.get_width()//2,
                              screen.get_height()//2+play.get_height()))
    else :
        screen.blit(controls,(screen.get_width()//2-controls.get_width()//2,
                              screen.get_height()//2+play.get_height()))
    
    count += 1
    fps += myClock.get_fps()
    fpsList.append(myClock.get_fps())
            
    myClock.tick(60)
    display.flip()
print(fps/count)
print(max(fpsList))
print(min(fpsList))
quit()
