#trySprites.py

from pygame import *
from random import *
from math import *
screen=display.set_mode((800,600))

pic=image.load("sprite.png")
m16=image.load("sprite - M16 being fired.png")

cx,cy=400,300

for x in range(0,800,5):
    for y in range(0,600,5):
        col=randint(0,50)
        for a in range(5):
            for b in range(5):
                screen.set_at((x+a,y+b),(col,col,col))
copy=screen.copy()

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
    
    screen.blit(copy,(0,0))

    mx,my=mouse.get_pos()
    mb=mouse.get_pressed()
    if mb[0]==1:
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
        bulletDistance[i]+=15 #the speed of the bullet
        #bulletDistance[i]+=597165 -> thats for how fast the bullet travels in real life :) ... but thats so fast that you dont even see it


    dist=(sqrt((mx-cx)**2+(my-cy)**2))
    ang=acos(max(abs(cy-my),1)/dist)
    if shot==True:
        shot=False
        if mx<=cx and my<cy:
            newpic=transform.rotate(m16,degrees(ang))
            screen.blit(newpic,get_center(newpic,400,300))
        elif mx<cx and my>=cy:
            newpic=transform.rotate(m16,180-degrees(ang))
            screen.blit(newpic,get_center(newpic,400,300))
        elif mx>=cx and my>cy:
            newpic=transform.rotate(m16,degrees(ang)+180)
            screen.blit(newpic,get_center(newpic,400,300))
        elif mx>cx and my<=cy:
            newpic=transform.rotate(m16,360-degrees(ang))
            screen.blit(newpic,get_center(newpic,400,300))
        else :
            screen.blit(m16,(350,250))
    else :         
        if mx<=cx and my<cy:
            newpic=transform.rotate(pic,degrees(ang))
            screen.blit(newpic,get_center(newpic,400,300))
        elif mx<cx and my>=cy:
            newpic=transform.rotate(pic,180-degrees(ang))
            screen.blit(newpic,get_center(newpic,400,300))
        elif mx>=cx and my>cy:
            newpic=transform.rotate(pic,degrees(ang)+180)
            screen.blit(newpic,get_center(newpic,400,300))
        elif mx>cx and my<=cy:
            newpic=transform.rotate(pic,360-degrees(ang))
            screen.blit(newpic,get_center(newpic,400,300))
        else :
            screen.blit(pic,(350,250))

    if ticktock==59:
        ticktock=0
    else :
        ticktock+=1
    
    myClock.tick(60)

    display.flip()
quit()
    
