#trySprites.py

from pygame import *
from random import *
from math import *

#---------------------VARIABLES THAT DO NOT CHANGE----------------------

resx,resy = 1280,720 #resolution size
cx,cy = resx//2,resy//2 #center coordinates, also half size of resolution
bx,by = 2500,2500 #background size
screen=display.set_mode((resx,resy))

#---weapons---
#contains all weapon information
#(weapon name, number of bullets being fired per shot,rate of fire
#(the lower it is, the faster the gun shoots))
weapons = [('m16',1,5),('dualPistols',2,15),('shotgun',5,30)]

clip = 1000 #starting number of bullets of each clip
bLen = 15 #bullet length
bWid = 7 #bullet width
bSpeed = 40 #bullet speed
viewDelay = 8 #reduction of aim sensitivity
myClock = time.Clock()
peacefulSprites=["peaceful AI-1.png"] #list of images for peaceful ai sprites

#-------------------------VARIABLES THAT CAN CHANGE----------------------

running=True #flag for if program is running
w=0 #selected weapon can change by changing this variable
weapon = weapons[w]
bulletList = [] #list of active bullets in play in the game
shot = False #flag checking if player is currently shooting
delay = 0 #counter keeping track of current frame number (0-29)
peacefulAIList=[] #list of active civilians on screen
cur_x = 1000 #starting player coordinates in accordance to map
cur_y = 1000 #(starts in the middle)

#-------------------------------BACKGROUND-------------------------------

back=Surface((bx,by))
for x in range(bx//20):
    for y in range(by//20):
        col=randint(0,255),randint(0,255),randint(0,255)
        for a in range(bx//100):
            for b in range(by//100):
                back.set_at((x*(bx//100)+a,y*(by//100)+b),col)

#---------------------------------CLASSES--------------------------------

class Player:
    '''Player keeps track of:

    x,y - current position
    ang - current angle the Player is facing
    pic1 - sprite to display when not moving
    pic2 - sprite to alternate to when firing
    fire - flag for if the player is shooting
    '''

    def __init__(self,x,y,ang,pic1,pic2,weapon):

        self.x = x
        self.y = y
        self.ang = ang
        self.pic1 = pic1
        self.pic2 = pic2
        self.fire = False

    def move(self,destX,destY,hScreenX,hScreenY):
        '''player angle changes based on mouse coordinates'''

        moveX = destX - hScreenX
        moveY = destY - hScreenY
        self.ang = atan2(-moveY, moveX)

    def draw(self,surface,delay,mb):
        '''player is rotated/drawn based on angle coordinates. If he is
        shooting, the sprite drawn alternates between the idle and firing
        sprites (pic1 and pic2)'''
        self.move(mx,my,cx,cy)

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

    def move(self,speed,length):
        '''finds the bullet end's and tip's next coordinates by using trig and
        the set distance and length of the bullet (which can be changed easily)'''

        self.ex, self.ey = self.tx + cos(self.ang) * (speed-length), self.ty - sin(self.ang) * (speed-length)
        self.tx, self.ty = self.tx + cos(self.ang) * speed, self.ty - sin(self.ang) * speed


    def draw(self,surface,thick):
        '''draws bullet using it's end and tip coordinates'''

        draw.line(surface,(255,0,0),(self.ex,self.ey),(self.tx,self.ty),thick)

#---Start of Peaceful AI---
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
        self.sprite=sprite #the original sprite
        self.rotated=sprite #self.sprite in its rotated form

    def move(self):
        """
        moves the player
        there is a 1 in 250 chance that the AI will change directions
        the remaining chance will make the AI continue in the same direction
        """
        num=randint(1,250)
        directions = ['North','East','South','West','None']
        for i in range(5):
            if num == i:
                self.direction = directions[i]

        #self.dirProb-=5

        if self.direction=="North" and self.y>=12:
                self.y-=2
        elif self.direction=="East" and self.x<=1988:
                self.x+=2
        elif self.direction=="South" and self.y<=1988:
                self.y+=2
        elif self.direction=="West" and self.x>=12:
                self.x-=2

    def draw(self,surface):
        """
        Rotates the image to the direction that it is walking and then
        blits it onto the given surface, which should be the main map
        """
        if self.direction=="South" or self.direction=="None":
            self.rotated=transform.rotate(self.sprite,0)
        elif self.direction=="East":
            self.rotated=transform.rotate(self.sprite,90)
        elif self.direction=="North":
            self.rotated=transform.rotate(self.sprite,180)
        elif self.direction=="West":
            self.rotated=transform.rotate(self.sprite,270)
        surface.blit(self.rotated,getCentre(self.rotated,self.x,self.y))

    def rectangle(self):
        """
        Returns the rectangular area that the sprite covers
        Used for collision detection
        """
        return Rect(self.x,self.y,self.rotated.get_width(),
                    self.rotated.get_height())

def erase(bList):
    '''gathers list of bullets out of the screen in a list, then deletes
    them from the list of active bullets'''

    aList = []
    for b in bList:
        if b.tx > 2000 or 0 > b.tx or b.ty > 2000 or 0 > b.ty:
            aList.append(b)
    for a in aList:
        bList.remove(a)


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
                          -(screen.get_height())//2-5)
        elif side==2:
            x_pos=randint(player.x+(screen.get_width())//2+5,player.x+
                          (screen.get_width())//2+255)
            y_pos=randint(player.y-(screen.get_height())//2,player.y
                          +(screen.get_height())//2)
        elif side==3:
            x_pos=randint(player.x-(screen.get_width())//2,player.x
                          +screen.get_width()//2)
            y_pos=randint(player.y+(screen.get_height())//2+5,player.y
                          +(screen.get_height())//2+255)
        elif side==4:
            x_pos=randint(player.x-(screen.get_width())//2-255,player.x
                          -(screen.get_width())//2-5)
            y_pos=randint(player.y-(screen.get_height())//2,player.y
                          +(screen.get_height())//2)
    direction = choice(["North","South","East","West","None"])
    probability = 1000
    sprite = choice(peacefulSprites)
    return ((x_pos,y_pos,sprite,direction,probability))

def distance(p1,p2):
    "Simple distance formula"
    return hypot(p2[0]-p1[0],p2[1]-p1[1])

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
                if ai.rectangle().collidepoint(bullet.tx,bullet.ty) or distance((ai.x,ai.y),(bullet.ex,bullet.ey))<50:
                    try:
                        eList.append(ai)
                        bulletList.remove(bullet)
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

def drawScene(surface,cur_pos,player,bList,delay,mb,peacefulAIList,mx,my,cenx,ceny,rx,ry,viewDel):
    '''draws bullets in active bullet list and the player'''

    for b in bList:
        b.draw(surface,bWid)
    for ai in peacefulAIList:
        ai.draw(surface)
    player.draw(surface,delay,mb)
    dist = distance((cur_pos[0],cur_pos[1]),(mx,my)) #distance between player and mouse coordinates
    screen.blit(surface.subsurface(cur_pos[0]+(dist//viewDel)*cos(player.ang)-cenx,cur_pos[1]-(dist//viewDel)*sin(player.ang)-ceny,rx,ry),(0,0))
    

def getCentre(surface,h,k):
    '''returns coordinate of where to blit picture so that it is always
    in the centre'''
    x = surface.get_width()
    y = surface.get_height()
    return h-(x//2),k-(y//2)

def movePlayer(surface,keys,cur_x,cur_y):
    '''Moves the player if the WASD keys are pressed'''
    if keys[K_a] and cur_x != cx:
        cur_x-=5
    if keys[K_d] and cur_x != bx-cx:
        cur_x+=5
    if keys[K_w] and cur_y != cy:
        cur_y-=5
    if keys[K_s] and cur_y != by-cy:
        cur_y+=5
    return cur_x,cur_y

while running:
    for e in event.get():
        if e.type==MOUSEBUTTONDOWN and e.button==3:
            w+=1
            if w>2:
                w=0
        if e.type==QUIT or key.get_pressed()[27]:
            running=False

    cur_screen=back.copy()

    k = key.get_pressed()
    cur_x,cur_y = movePlayer(cur_screen,k,cur_x,cur_y)

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
                player.move(mx,my,cx,cy)
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
        bulletList[i].move(bSpeed,bLen)
    erase(bulletList)

    #---peaceful AI---
    while len(peacefulAIList)<5:
        ai = makePeacefulAI(screen,player,peacefulSprites)
        peacefulAIList.append(peacefulAI(ai[0],ai[1],image.load("%s"%ai[2]),
                                         ai[3],ai[4]))
    for ai in peacefulAIList:
        ai.move()
    erasePeacefulAI(player,peacefulAIList,bulletList)
    drawScene(cur_screen,(cur_x,cur_y),player,bulletList,delay-1,mb,peacefulAIList,mx,my,cx,cy,resx,resy,viewDelay)


    myClock.tick(60)

    display.flip()
quit()
