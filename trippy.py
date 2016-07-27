#trySprites.py

from pygame import *
from random import *
from math import *
screen=display.set_mode((800,600))

pic=image.load("M161.png")
m16=image.load("M162.png")

cx,cy=400,300

class Player:
    '''
    Player keeps track of:

    x,y - current position
    ang - current angle the Player is facing
    pic - sprite to display
    '''

    def __init__(self,x,y,ang,pic):

        self.x = x
        self.y = y
        self.ang = ang
        self.pic = pic

    def move(self,destX,destY):

        moveX = destX - self.x
        moveY = destY - self.y
        self.ang = degrees(atan2(-moveY, moveX)) + 270

    def draw(self,surface):

        self.move(mx,my)
        newpic=transform.rotate(pic,self.ang)
        surface.blit(newpic,get_center(newpic,400,300))

class Bullet:
    '''
    Bullet keeps track of:

    ex,ey - current end position
    tx,ty - current tip position
    ang - current angle bullet is going from player when it was shot
    '''

    def __init__(self,ex,ey,tx,ty,ang):

        self.ex = ex
        self.ey = ey
        self.tx = tx
        self.ty = ty
        self.ang = ang

    def move(self,player):

        self.ex, self.ey = self.ex + cos(player.ang) * 50, self.ey - sin(player.ang) * 50
        self.tx, self.ty = self.tx + cos(player.ang) * 45, self.ty - sin(player.ang) * 45

    def draw(self,surface):

        draw.line(surface,(255,0,0),(self.ex,self.ey),(self.tx,self.ty),14)

    def erase(self,bList):

        if self.tx > 800 or 0 > self.tx or self.ty > 600 or 0 > self.ty:
            bList.remove(self)

def make(player):

        endX, endY = player.x + cos(player.ang), player.y - sin(player.ang)
        tipX, tipY = player.x + cos(player.ang), player.y - sin(player.ang)
        return ((endX,endY,tipX,tipY,player.ang))

def drawScene(surface,player,bList):

    player.draw(surface)
    for b in bList:
        b.draw(surface)

def get_center(surface,h,k):
    x=surface.get_width()
    y=surface.get_height()
    return h-(x//2),k-(y//2)

def get_quadrant(center,point):
    '''  y
      2  |  1
    -----|-----x
      3  |  4
    '''
    if point[0]>center[0] and point[1]<=center[1]:
        return 1
    elif point[0]<=center[0] and point[1]<center[1]:
        return 2
    elif point[0]<center[0] and point[1]>=center[1]:
        return 3
    elif point[0]>=center[0] and point[1]>center[1]:
        return 4
    else : #if the center is also the point
        return 0
    

def bullets(bulletList,bulletDistance):
    for i in range(len(bulletList)):
        draw.line(screen,(255,0,0),(cx+cos(bulletList[i][0])*(bulletDistance[i]-5),cy-sin(bulletList[i][0])*(bulletDistance[i]-5)),
                    (cx+cos(bulletList[i][0])*bulletDistance[i],cy-sin(bulletList[i][0])*bulletDistance[i]),3)
       
bulletList=[]
bulletDistance=[]
myClock=time.Clock()
ticktock=0
shot=False
clip=1000
running=True
while running:
    for e in event.get():
        if e.type==QUIT:
            running=False
    
    screen.fill((255,255,255))

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    '''if mb[0]==1:
        for i in range(0,60,5):
            if ticktock==i:
                if clip>0:
                    shot=True
                    clip-=1
                    if get_quadrant((400,300),(mx,my))==1:
                        #bulletlist.append((angle,bullet tip))
                        ang=90-degrees(acos(max(abs(cy-my),1)/(sqrt((mx-cx)**2+(my-cy)**2))))
                        bulletList.append((radians(ang),cx+cos(radians(ang))*0,cy-sin(radians(ang))*0))
                        bulletDistance.append(35)
                    elif get_quadrant((400,300),(mx,my))==2:
                        #bulletlist.append((angle,bullet tip))
                        ang=90+degrees(acos(max(abs(cy-my),1)/(sqrt((mx-cx)**2+(my-cy)**2))))
                        bulletList.append((radians(ang),cx+cos(radians(ang))*0,cy-sin(radians(ang))*0))
                        bulletDistance.append(35)
                    elif get_quadrant((400,300),(mx,my))==3:
                        #bulletlist.append((angle,bullet tip))
                        ang=270-degrees(acos(max(abs(cy-my),1)/(sqrt((mx-cx)**2+(my-cy)**2))))
                        bulletList.append((radians(ang),cx+cos(radians(ang))*0,cy-sin(radians(ang))*0))
                        bulletDistance.append(35)
                    elif get_quadrant((400,300),(mx,my))==4:
                        #bulletlist.append((angle,bullet tip))
                        ang=270+degrees(acos(max(abs(cy-my),1)/(sqrt((mx-cx)**2+(my-cy)**2))))
                        bulletList.append((radians(ang),cx+cos(radians(ang))*0,cy-sin(radians(ang))*0))
                        bulletDistance.append(35)
    else :
        ticktock=59
        
    bullets(bulletList,bulletDistance)
    for i in range(len(bulletDistance)):
        bulletDistance[i]+=30 #the speed of the bullet
        #bulletDistance[i]+=597165 -> thats for how fast the bullet travels in real life :) ... but thats so fast that you dont even see it
'''
    
    player = Player(400,300,0,pic)
    dist=(sqrt((mx-cx)**2+(my-cy)**2))
    ang=acos(max(abs(cy-my),1)/dist)
    if mb[0] == 1:
        if clip > 0:
            player.move(mx,my)
            bull = make(player)
            bulletList.append(Bullet(bull[0],bull[1],bull[2],bull[3],bull[4]))
    for i in range(len(bulletList)):
        bulletList[i].move(player)
        #bulletList[i].erase(bulletList)
    print(bulletList)
    drawScene(screen,player,bulletList)

    if ticktock==59:
        ticktock=0
    else :
        ticktock+=1
    
    myClock.tick(60)

    display.flip()
quit()