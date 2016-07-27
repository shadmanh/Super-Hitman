#peaceful AI class

from random import *

class peacefulAI:
    """The peaceful AI in the large map
    x,y - current position
    sprite - sprite of the AI
    direction - direction headed (North, East, South, West or None if stationary)
    dirProb - probability of the character changing direction (the greater the
    probablity, the lesser the chance)
    """

    def __init__(self,x,y,sprite,direction,dirProb):
        self.x=x
        self.y=y
        self.direction=direction
        self.dirProb=dirProb
    def move(self,x,y,direction):
        num=randint(1,self.dirProb)
        if num==1:
            direction="North"
        elif num==2:
            direction="East"
        elif num==3:
            direction="South"
        elif num==4:
            direction="West"
        elif num==5:
            direction="None"

        self.dirProb-=5
        self.direction=direction
        
        if direction=="North":
            self.y-=2
        elif direction=="East":
            self.x+=1
        elif direction=="South":
            self.y+=1
        elif direction=="West":
            self.x-=1
    def draw(self,surface,direction):
        if direction=="North":
            newpic=transform.rotate(self.sprite,0)
        elif direction=="East":
            newpic=transform.rotate(self.sprite,270)
        elif direction=="South":
            newpic=transform.rotate(self.sprite,180)
        elif direction=="West":
            newpic=transform.rotate(self.sprite,90)
        surface.blit(newpic,getCentre(newpic,x,y))
    #def rectangle(self,


def makePeacefulAI(screen,player,peacefulSprites):
    """Makes a peaceful AI"""
    side=randint(1,4) #the side in relation to the player that the AI will be spawned
    """
    1 is to the top
    2 is to the right
    3 is to the bottom
    4 is to the left
    """
    x_pos=0
    y_pos=0
    while x_pos<0 or y_pos<0:           
        if side==1:
            x_pos=randint(player.x-screen.get_width()//2,player.x
                          +screen.get_width()//2)
            y_pos=randint(player.y-screen.get_height//2-255,player.y
                          -screen.get_height//2-5)
        elif side==2:
            x_pos=randint(player.x+screen.get_height//2+255,player.x
                          +screen.get_height//2+5)
            y_pos=randint(player.y-screen.get_width()//2,player.y
                          +screen.get_width()//2)
        elif side==3:
            x_pos=randint(player.x-screen.get_width()//2,player.x
                          +screen.get_width()//2)
            y_pos=randint(player.y+screen.get_height//2+255,player.y
                          +-screen.get_height//2+5)
        elif side==4:
            x_pos=randint(player.x-screen.get_height//2-255,player.x
                          -screen.get_height//2-5)
            y_pos=randint(player.y-screen.get_width()//2,player.y
                          +screen.get_width()//2)
    direction=choice("North","South","East","West","None")
    probability=1000
    sprite=choice(peacefulSprites)
    sprite=image.load(sprite)
    return x_pos,y_pos,sprite,direction,probability

def distance(p1,p2):
    return abs(sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2))

def erasePeacefulAI(player,peacefulAIlist):
    "Doesnt include bullet collisions"
    eList=[]
    for ai in peacefulAIlist:
        if distance((ai.x,ai.y),(player.x,player.y))>1500:
            eList.append(ai)
    for e in eList:
        peacefulAIlist.remove(e)


#---Collision test for peaceful AIs---
#Modification of erasePeacefulAI function

def erasePeacefulAI(player,peacefulAIlist,bulletList):
    "With bullet collisions"
    eList=[]
    for ai in peacefulAIlist:
        if distance((ai.x,ai.y),(player.x,player.y))>1500:
            eList.append(ai)
        else :
            for bullet in bulletList:
                if (ai.rectangle).collidepoint(bullet.tx,bullet.ty):
                  eList.append(ai)
    for e in eList:
        peacefulAIlist.remove(e)

#---Class for enemies that shoot at the player---
class enemyShooter:
    """
    This is the class for the AI enemies that shoot at the player
    x - x coordinate of the enemy
    y - y coordinate of the enemy
    pic1 - sprite of the enemy when they are not shooting their gun
    pic2 - sprite when they are shooting their gun
    player - the class for the player
    mode - "Hostile" or "Peaceful"
        Hostile - the AI attempts to shoot the player
        Peaceful - the AI is too far from the player and therefore doesnt engage him
    pDir - direction when the AI is in peaceful mode
    """
    def __init__(self,x,y,pic1,pic2,player,mode,direction,pDir,ang,shot,weapon):
        self.x=x
        self.y=y
        self.pic1=pic1
        self.pic2=pic2
        self.player=player
        self.mode=mode
        self.direction=direction
        self.pDir=pDir
        self.rotated1=pic1
        self.ang=ang
        self.shot=shot
        self.dist=distance((self.x,self.y),(self.player.x,self.player.y))
        self.weapon=weapon
    def move(self):
        self.player=player
        """
        This function moves the AI
        """
        self.dist=distance((self.x,self.y),(self.player.x,self.player.y))
        if dist>2000:
            self.mode="Peaceful"
            """
            moves the player
            there is a 1 in 250 chance that the AI will change to a certain direction
            the remaining chance will make the AI continue in the same direction
            """
            num=randint(1,250)
            if num==1:
                self.pDir="North"
            elif num==2:
                self.pDir="East"
            elif num==3:
                self.pDir="South"
            elif num==4:
                self.pDir="West"
            elif num==5:
                self.pDir="None"
            
            if self.pDir=="North":
                if self.y>=12:
                    self.y-=2
            elif self.pDir=="East":
                if self.x<=1988:
                    self.x+=2
            elif self.pDir=="South":
                if self.y<=1988:
                    self.y+=2
            elif self.pDir=="West":
                if self.x>=12:
                    self.x-=2
            #---Rotation---
            if self.pDir=="South" or self.pDir=="None":
                self.rotatedP=transform.rotate(self.pic1,0)
            elif self.pDir=="East":
                self.rotatedP=transform.rotate(self.pic1,90)
            elif self.pDir=="North":
                self.rotatedP=transform.rotate(self.pic1,180)
            elif self.pDir=="West":
                self.rotatedP=transform.rotate(self.pic1,270)
        else :
            self.mode="Hostile"
            if dist>250:
                ###Code from FP Basics Eg 4.py###
                dist = max(1,distance(self.x, self.y, target.x, target.y))
                moveX = (self.player.x - self.x)*5/dist
                moveY = (self.player.y - self.y)*5/dist
                self.ang = degrees(atan2(-moveY, moveX))
                self.x += moveX
                self.y += moveY
                ###
            
    def shoot(self):
        if self.dist<400:
            
    def draw(self,surface):
        if self.mode=="Peaceful":
            surface.blit(self.rotatedP,getCentre(self.rotatedP,self.x,self.y))
        else :
            self.rotatedH=transform.rotate(self.pic1,self.ang+90)
            surface.blit(self.rotatedH,getCentre(self.rotatedH,self.x,self.y))
    def rectangle(self):
        """
        Returns the rectangular area that the sprite covers
        Used for collision detection
        """
        return Rect(self.x,self.y,self.rotated1.get_width(),
                    self.rotated1.get_height())
