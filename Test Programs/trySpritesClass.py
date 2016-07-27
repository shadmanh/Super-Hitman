#trySprites.py

from pygame import *
from random import *
from math import *
screen=display.set_mode((800,600))

cx,cy=400,300

#---background---
back=Surface((2000,2000))
for x in range(100):
    for y in range(100):
        col=randint(0,255),randint(0,255),randint(0,255)
        for a in range(20):
            for b in range(20):
                back.set_at((x*20+a,y*20+b),col)


class Player:
    '''Player keeps track of:

    x,y - current position
    ang - current angle the Player is facing
    pic1 - sprite to display when not moving
    pic2 - sprite to alternate to when firing
    '''

    def __init__(self,x,y,ang,pic1,pic2,weapon):

        self.x = x
        self.y = y
        self.ang = ang
        self.pic1 = pic1
        self.pic2 = pic2
        self.fire = False

    def move(self,destX,destY):
        '''player angle changes based on mouse coordinates'''

        moveX = destX - 400
        moveY = destY - 300
        self.ang = atan2(-moveY, moveX)

    def draw(self,surface,delay,mb):
        '''player is rotated/drawn based on angle coordinates. If he is
        shooting, the sprite drawn alternates between the idle and firing
        sprites (pic1 and pic2)'''
        self.move(mx,my)
        
        if mb[0]==1 and delay % weapon[2] == 0:
            newpic = transform.rotate(self.pic2,degrees(self.ang)+270)
        else :
            newpic = transform.rotate(self.pic1,degrees(self.ang)+270)
        surface.blit(newpic,getCentre(newpic,player.x,player.y))

class Bullet:
    '''Bullet keeps track of:

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

    def move(self):
        '''finds the bullet end's and tip's next coordinates by using trig and
        the set distance and length of the bullet (which can be changed easily)'''

        self.ex, self.ey = self.tx + cos(self.ang) * 0, self.ty - sin(self.ang) * 0 #15 is speed of bullet
        self.tx, self.ty = self.tx + cos(self.ang) * 20, self.ty - sin(self.ang) * 20 #(15-10=)5 is length of bullet
        

    def draw(self,surface):
        '''draws bullet using it's end and tip coordinates'''

        draw.line(surface,(255,0,0),(self.ex,self.ey),(self.tx,self.ty),7)

def erase(bList):
    '''gathers list of bullets out of the screen in a list, then deletes
    them from the list of active bullets'''

    aList = []
    for b in bList:
        if b.tx > 2000 or 0 > b.tx or b.ty > 2000 or 0 > b.ty:
            aList.append(b)
    for a in aList:
        bList.remove(a)

#---Start of Peaceful AI---
class peacefulAI:
    """The peaceful AI in the large map
    x,y - current position
    sprite - sprite of the AI
    direction - direction headed (North, East, South, West or None if stationary)
    dirProb - probability of the character changing direction (the greater the
    probablity, the lesser the chance)
    """
    '''
    def __init__(self,x,y,sprite,direction):
        self.x=x
        self.y=y
        self.direction=direction
        self.sprite=sprite #the original sprite
        self.rotated=sprite #self.sprite in its rotated form
    def move(self):
        """
        moves the player
        there is a 1 in 250 chance that the AI will change to a certain direction
        the remaining chance will make the AI continue in the same direction
        """
        num=randint(1,250)
        if num==1:
            self.direction="North"
        elif num==2:
            self.direction="East"
        elif num==3:
            self.direction="South"
        elif num==4:
            self.direction="West"
        elif num==5:
            self.direction="None"

        #self.dirProb-=5
        
        if self.direction=="North":
            if self.y>=12:
                self.y-=2
        elif self.direction=="East":
            if self.x<=1988:
                self.x+=2
        elif self.direction=="South":
            if self.y<=1988:
                self.y+=2
        elif self.direction=="West":
            if self.x>=12:
                self.x-=2

        #---Rotation---
        if self.direction=="South" or self.direction=="None":
            self.rotated=transform.rotate(self.sprite,0)
        elif self.direction=="East":
            self.rotated=transform.rotate(self.sprite,90)
        elif self.direction=="North":
            self.rotated=transform.rotate(self.sprite,180)
        elif self.direction=="West":
            self.rotated=transform.rotate(self.sprite,270)
    
    def draw(self,surface):
        """
        Blits the image ont0 the screen
        """
        
        surface.blit(self.rotated,getCentre(self.rotated,self.x,self.y))
    '''
    def __init__(self,x,y,pic1,player,mode,pDir,ang):
        self.x=x
        self.y=y
        self.pic1=pic1
        #self.pic2=pic2
        self.player=player
        self.mode=mode
        #self.direction=direction
        self.pDir=pDir
        self.rotated1=pic1
        self.ang=ang
        #self.shot=shot
    def move(self,player):
        self.player=player
        """
        This function moves the AI
        """
        if distance((self.x,self.y),(self.player.x,self.player.y))>2000:
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
        else :
            self.mode="Hostile"
            ###Code from FP Basics Eg 4.py###
            dist = max(1,distance((self.x, self.y), (self.player.x, self.player.y)))
            moveX = (self.player.x - self.x)*5/dist
            moveY = (self.player.y - self.y)*5/dist
            self.ang = degrees(atan2(-moveY, moveX))
            self.x += moveX
            self.y += moveY
            ###
    def rotate(self):
        if self.mode=="Peaceful":
            if self.pDir=="South" or self.pDir=="None":
                self.rotatedP=transform.rotate(self.pic1,0)
            elif self.pDir=="East":
                self.rotatedP=transform.rotate(self.pic1,90)
            elif self.pDir=="North":
                self.rotatedP=transform.rotate(self.pic1,180)
            elif self.pDir=="West":
                self.rotatedP=transform.rotate(self.pic1,270)
            #surface.blit(self.rotated1,getCentre(self.rotated1,self.x,self.y))
        elif self.mode=="Hostile":
            #if self.shot==True:
            #self.ang=atan2(-surface.get_width()//2,surface.get_height()//2)
            #self.ang=
            self.rotatedH=transform.rotate(self.pic1,self.ang+90)
    def draw(self,surface):
        if self.mode=="Peaceful":
            surface.blit(self.rotatedP,getCentre(self.rotatedP,self.x,self.y))
        else :
            surface.blit(self.rotatedH,getCentre(self.rotatedH,self.x,self.y))
    def rectangle(self):
        """
        Returns the rectangular area that the sprite covers
        Used for collision detection
        """
        return Rect(self.x,self.y,self.rotated1.get_width(),
                    self.rotated1.get_height())


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
    while x_pos<=0 or y_pos<=0:
        side=randint(1,4)
        if side==1:
            x_pos=randint(player.x-(screen.get_width())//2,player.x
                          +(screen.get_width())//2)
            y_pos=randint(player.y-(screen.get_height())//2-255,player.y
                          -(screen.get_height())//2-50)
        elif side==2:
            x_pos=randint(player.x+(screen.get_width())//2+50,player.x+
                          (screen.get_width())//2+255)
            y_pos=randint(player.y-(screen.get_height())//2,player.y
                          +(screen.get_height())//2)
        elif side==3:
            x_pos=randint(player.x-(screen.get_width())//2,player.x
                          +screen.get_width()//2)
            y_pos=randint(player.y+(screen.get_height())//2+50,player.y
                          +(screen.get_height())//2+255)
        elif side==4:
            x_pos=randint(player.x-(screen.get_width())//2-255,player.x
                          -(screen.get_width())//2-50)
            y_pos=randint(player.y-(screen.get_height())//2,player.y
                          +(screen.get_height())//2)
    direction=choice(["North","South","East","West","None"])
    probability=1000
    sprite=choice(peacefulSprites)
    return ((x_pos,y_pos,sprite,direction))

def distance(p1,p2):
    "Simple distance formula"
    return abs(sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2))

def erasePeacefulAI(player,peacefulAIlist,bulletList):
    """
    Goes through the list of peaceful AIs and if the AI is a great distance
    away from the player, then it is removed from the list and removed from
    the map.
    A new AI will be spawned somewhere near the player
    """
    eList=[]
    for ai in peacefulAIlist:
        if distance((ai.x,ai.y),(player.x,player.y))>1500:
            eList.append(ai)
        else :
            for bullet in bulletList:
                if ai.rectangle().collidepoint(bullet.tx,bullet.ty):
                    try:
                        eList.append(ai)
                    except ValueError: pass
    for e in eList:
        try:
            peacefulAIlist.remove(e)
        except ValueError: pass #an error occurs if an AI is hit with multiple
                                #bullets
#---End of Peaceful AI---

def make(player,wNum,shots,pos):
    '''makes bullets starting in various places going in various directions
    based on the weapon chosen. After determining the specific position and
    angle of the bullet, the properties of the bullet (tip/end coordinates,
    angle) are created and added to the list of active bullets as a tuple'''

    randang = randint(8*(shots-1),8*shots)
    ammoList = [(pos[0] + cos(player.ang) * 35, pos[1] - sin(player.ang) * 35, player.ang), #machine gun
    (pos[0] + cos(player.ang+radians(-5+15*shots)) * 35, pos[1] - 
        sin(player.ang+radians(-5+15*shots)) * 35, player.ang), #dual pistols
    ((pos[0]+cos(player.ang)*35)+cos(player.ang+radians(-14+randang)) * 35,
     (pos[1]-sin(player.ang)*35)-sin(player.ang+radians(-14+randang)) * 35,
     player.ang+radians(-14+randang))] #shotgun now shoots better
    tipX,tipY = ammoList[wNum][0], ammoList[wNum][1]
    ang = ammoList[wNum][2]
    return ((tipX,tipY,tipX,tipY,ang))

def drawScene(surface,cur_pos,player,bList,delay,mb,peacefulAIlist):
    '''draws bullets in active bullet list and the player'''

    for b in bList:
        b.draw(surface)
    for ai in peacefulAIlist:
        ai.draw(surface)
    player.draw(surface,delay,mb)
    screen.blit(surface.subsurface(cur_pos[0]-400,cur_pos[1]-300,800,600),(0,0))

def getCentre(surface,h,k):
    '''returns coordinate of where to blit picture so that it is always
    in the centre'''
    x = surface.get_width()
    y = surface.get_height()
    return h-(x//2),k-(y//2)

def movePlayer(surface,keys,cur_x,cur_y):
    '''Moves the player if the WASD keys are pressed'''
    if keys[K_a]:
        if cur_x==400:
            pass
        else :
            cur_x-=5
    if keys[K_d]:
        if cur_x==1600:
            pass
        else :
            cur_x+=5
    if keys[K_w]:
        if cur_y==300:
            pass
        else :
            cur_y-=5
    if keys[K_s]:
        if cur_y==1700:
            pass
        else :
            cur_y+=5
    return cur_x,cur_y
    

#---weapons---
#contains all weapon information
#(weapon name, number of bullets being fired per shot,rate of fire)
weapons = [('m16',1,5),('dualPistols',2,15),('shotgun',5,30)]
w=0
weapon = weapons[w] #change this number to change weapon
bulletList = []
myClock = time.Clock()
shot = False
clip = 1000
delay = 0
peacefulAIlist=[]
cur_x=1000
cur_y=1000
peacefulSprites=["peaceful AI-1.png"]

running=True
while running:
    for e in event.get():
        if e.type==MOUSEBUTTONDOWN and e.button==3:
            w+=1
            if w>2:
                w=0
        if e.type==QUIT:
            running=False

    cur_screen=back.copy()

    k=key.get_pressed()
    cur_x,cur_y=movePlayer(cur_screen,k,cur_x,cur_y)
    
    #screen.fill((255,255,255))
    weapon=weapons[w]
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    dist = hypot(mx-cx, my-cy)
    pic1 = image.load('%s1.png'%weapon[0])
    pic2 = image.load('%s2.png'%weapon[0])
    player = Player(cur_x,cur_y,0,pic1,pic2,weapon)
    if mb[0] == 1:
        if clip > 0:
            shot=True
            if delay % weapon[2] == 0:
                player.move(mx,my)
                for i in range(weapon[1]):
                    bull = make(player,weapons.index(weapon),i,(cur_x,cur_y))
                    bulletList.append(Bullet(bull[0],bull[1],bull[2],bull[3],bull[4]))
                clip -= 1
            
    if delay == 29: #delay between bullets (1-30, lower is faster)
        delay = 0
        shot = False
    if shot:
        delay += 1
    for i in range(len(bulletList)):
        bulletList[i].move()
    erase(bulletList)

    #---peaceful AI---
    while len(peacefulAIlist)<5:
        ai=makePeacefulAI(screen,player,peacefulSprites)
        peacefulAIlist.append(peacefulAI(ai[0],ai[1],image.load("%s"%ai[2]),player,"Hostile",
                                         ai[3],0))
    for ai in peacefulAIlist:
        ai.move(player)
        ai.rotate()
    erasePeacefulAI(player,peacefulAIlist,bulletList)
    
    drawScene(cur_screen,(cur_x,cur_y),player,bulletList,delay-1,mb,peacefulAIlist)
    
    
    myClock.tick(30)

    display.flip()
quit()
