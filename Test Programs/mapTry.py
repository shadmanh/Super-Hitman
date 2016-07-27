from pygame import *
from math import *
from random import *
screen=display.set_mode((1280,720))

collide=image.load("Collision Check of Map.png").convert()
top=image.load("Top of Map.png")
bottom=image.load("Background of Map.png").convert_alpha()
gameMap=image.load("newMap.png").convert()
gameMapCopy=gameMap.copy()
"""
for y in range(0,top.get_height(),5):
    for x in range(0,top.get_width(),5):
        if collide.get_at((x,y))==(255,255,255):
            screen.blit(bottom.subsurface(x-screen.get_width()//2,y-screen.get_height()//2,
                                          screen.get_width(),screen.get_height()),(0,0))
            screen.blit(top.subsurface(x-screen.get_width()//2,y-screen.get_height()//2,
                                          screen.get_width(),screen.get_height()),(0,0))
            display.flip()
            #time.wait()
            #print(time.Clock().get_fps())

quit()
"""

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

        moveX = destX - 640
        moveY = destY - 360
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
        surface.blit(newpic,getCentre(newpic,surface.get_width()//2,surface.get_height()//2))
        

class Bullet:
    '''Bullet keeps track of:

    ex,ey - current end position
    tx,ty - current tip position
    ang - current angle bullet is going from player when it was shot
    weapon - the weapon that was shot to create the bullet, current significance
    is to get the amount of damage that it causes to an enemy
    (its the tuple of the weapon in the weapons list)
    '''

    def __init__(self,ex,ey,tx,ty,ang,damage):

        self.ex = ex
        self.ey = ey
        self.tx = tx
        self.ty = ty
        self.ang = ang
        self.damage=damage

    def move(self):
        '''finds the bullet end's and tip's next coordinates by using trig and
        the set distance and length of the bullet (which can be changed easily)'''

        self.ex, self.ey = self.tx + cos(self.ang) * 10, self.ty - sin(self.ang) * 10 #15 is speed of bullet
        self.tx, self.ty = self.tx + cos(self.ang) * 30, self.ty - sin(self.ang) * 30 #(15-10=)5 is length of bullet
        

    def draw(self,surface,player):
        '''draws bullet using it's end and tip coordinates'''
        if fitOnscreen(surface,(player.x,player.y),(self.tx,self.ty)):
            new_tx=surface.get_width()//2-(player.x-self.tx)
            new_ex=surface.get_width()//2-(player.x-self.ex)
            new_ty=surface.get_height()//2-(player.y-self.ty)
            new_ey=surface.get_height()//2-(player.y-self.ey)
            draw.line(surface,(255,0,0),(new_tx,new_ty),(new_ex,new_ey),7)
        

def make(player,wNum,shots,pos,damage):
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
    return ((tipX,tipY,tipX,tipY,ang,damage))
class peacefulAI:
    """The peaceful AI in the large map
    x,y - current position
    sprite - sprite of the AI
    direction - direction headed (North, East, South, West or None if stationary)
    dirProb - probability of the character changing direction (the greater the
    probablity, the lesser the chance)
    """
    def __init__(self,x,y,sprite,direction,health):
        self.x=x
        self.y=y
        self.direction=direction
        self.sprite=sprite #the original sprite
        self.rotated=sprite #self.sprite in its rotated form
        self.health=health
        self.maxHealth=health #the amount of health they start off with
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
            if collide.get_at((self.x,self.y-2))[:3]!=(0,0,0):
                self.y-=2
        elif self.direction=="East":
            if collide.get_at((self.x+2,self.y))[:3]!=(0,0,0):
                self.x+=2
        elif self.direction=="South":
            if collide.get_at((self.x,self.y+2))[:3]!=(0,0,0):
                self.y+=2
        elif self.direction=="West":
            if collide.get_at((self.x-2,self.y))[:3]!=(0,0,0):
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
    
    def draw(self,surface,player):
        """
        Blits the image ont0 the screen
        """
        sx=surface.get_width()//2-(player.x-self.x) #x-coordinate relative to the screen
        sy=surface.get_height()//2-(player.y-self.y) #y-coordinate relative to the screen
        surface.blit(self.rotated,getCentre(self.rotated,sx,sy))

        width=int(self.rotated.get_width()/self.maxHealth*self.health)
        height=10
        col=(255-int(width*2.5),5+int(width*2.5),0)
        draw.rect(surface,col,(sx-self.rotated.get_width()//2,
                                   sy-self.rotated.get_height()//2-10,
                                   width,height))
    def rectangle(self):
        """
        Returns the rectangular area that the sprite covers
        Used for collision detection
        """
        return Rect(self.x-self.rotated.get_width()//2,self.y-self.rotated.get_height()//2,
                    self.rotated.get_width(),self.rotated.get_height())
    def reduceHealth(self,bulDamage):
        """
        Reduces the AIs health based on how much damage the bullet deals
        """
        self.health-=bulDamage
        

def makePeacefulAI(surface,mainMap,player,peacefulSprites):
    """Makes a peaceful AI"""
    side=randint(1,4) #the side in relation to the player that the AI will be spawned
    """
    1 is to the top
    2 is to the right
    3 is to the bottom
    4 is to the left
    surface - the screen
    """
    x_pos=0
    y_pos=0
    while collide.get_at((x_pos,y_pos))==(0,0,0) or fitOnscreen(surface,(player.x,player.y),(x_pos,y_pos))==True: #while the pos is in the black part of the map
        """
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
        """
        x_pos=randint(surface.get_width()//2,mainMap.get_width()-surface.get_width()//2) #less chance of them
        y_pos=randint(surface.get_height()//2,mainMap.get_height()-surface.get_height()//2)
    direction=choice(["North","South","East","West","None"])
    probability=1000
    sprite=choice(peacefulSprites)
    health=1000 #the amount of health each one has
    return ((x_pos,y_pos,sprite,direction,health))

def distance(p1,p2):
    "Simple distance formula"
    return abs(sqrt((p2[0]-p1[0])**2+(p2[1]-p1[1])**2))

def erase(player,peacefulAIlist,bulletList):
    bList=[]
    pList=[]
    for ai in peacefulAIlist:
        for bullet in bulletList:
            if ai.rectangle().collidepoint(bullet.tx,bullet.ty):
                ai.reduceHealth(bullet.damage)
                bList.append(bullet)
                if ai.health<1:
                    pList.append(ai)
    for bullet in bulletList: #checks for collisions on the map
        if collide.get_at((int(bullet.tx),int(bullet.ty)))==(0,0,0):
            bList.append(bullet)
            
    for b in bList: #removes all the bullets that collide with buildings or
                    #AIs
        try:
            bulletList.remove(b)
        except ValueError: pass #crashes if the bullet has already been erased
                                #in the erase() function
    for p in pList: #erases all of the peaceful AIs that have been shot
        try:
            peacefulAIlist.remove(p)
        except ValueError: pass #an error occurs if an AI is hit with multiple
                                #bullets

def drawScene(surface,cur_pos,player,bList,delay,mb,peacefulAIlist):
    '''draws bullets in active bullet list and the player'''
    
    for b in bList:
        b.draw(surface,player)
    
    for ai in peacefulAIlist:
        ai.draw(surface,player)
    
    player.draw(surface,delay,mb)
    screen.blit(surface,(0,0))
    #screen.blit(top.subsurface(player.x-screen.get_width()//2,
    #                               player.y-screen.get_height()//2,
    #                               1280,720),(0,0))

def getCentre(surface,h,k):
    '''returns coordinate of where to blit picture so that it is always
    in the centre'''
    x = surface.get_width()
    y = surface.get_height()
    return h-(x//2),k-(y//2)

def fitOnscreen(surface,center,point):
    """
    Checks to see whether or not a certain object is in the current screen
    For an object to appear onscreen, it can be up to 50 px off of it
    in case that its diameter is large enough that a portion of it should
    be seen by the player
    center - the center of the screen (player.x,player.y)
    point - the center of the object in question
    """
    if (point[0]>=center[0]-surface.get_width()//2-50
        and point[0]<=center[0]+surface.get_width()//2+50
        and point[1]>=center[1]-surface.get_height()//2-50
        and point[1]<=center[1]+surface.get_height()//2+50):
            return True
    else : return False

def movePlayer(keys,cur_x,cur_y):
    '''Moves the player if the WASD keys are pressed'''
    if keys[K_a]:
        if collide.get_at((cur_x-5,cur_y))[:3]==(0,0,0):
            pass
        else :
            cur_x-=5
    if keys[K_d]:
        if collide.get_at((cur_x+5,cur_y))[:3]==(0,0,0):
            pass
        else :
            cur_x+=5
    if keys[K_w]:
        if collide.get_at((cur_x,cur_y-5))[:3]==(0,0,0):
            pass
        else :
            cur_y-=5
    if keys[K_s]:
        if collide.get_at((cur_x,cur_y+5))[:3]==(0,0,0):
            pass
        else :
            cur_y+=5
    return cur_x,cur_y

cx,cy=screen.get_width()//2,screen.get_height()//2
weapons = [((image.load('m161.png'),image.load('m162.png')),1,10,10),
           ((image.load('dualPistols1.png'),image.load('dualPistols2.png')),2,30,20),
           ((image.load('shotgun1.png'),image.load('shotgun2.png')),5,60,15)]
myClock = time.Clock()
w=0
delay = 0
clip = 1000
cur_x=0
cur_y=0
shot = False
bulletList = []
peacefulAIlist=[]
count=0
fps=0
fpsList=[]
peacefulSprites=[image.load("peaceful AI-1.png")]

while collide.get_at((cur_x,cur_y))==(0,0,0):
    cur_x=randint(0,gameMap.get_width())
    cur_y=randint(0,gameMap.get_height())

running=True
while running:
    for e in event.get():
        if e.type==MOUSEBUTTONDOWN and e.button==3:
            w+=1
            if w>2:
                w=0
        if e.type==QUIT:
            running=False


    k=key.get_pressed()
    cur_x,cur_y=movePlayer(k,cur_x,cur_y)
    weapon=weapons[w]
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    dist = hypot(mx-cx, my-cy)
    pic1 = weapon[0][0]
    pic2 = weapon[0][1]
    player = Player(cur_x,cur_y,0,pic1,pic2,weapon)

    if mb[0] == 1:
        if clip > 0:
            shot=True
            if delay % weapon[2] == 0:
                player.move(mx,my)
                for i in range(weapon[1]):
                    bull = make(player,weapons.index(weapon),i,(cur_x,cur_y),
                                weapons[w][3])
                    bulletList.append(Bullet(bull[0],bull[1],bull[2],bull[3],bull[4],
                                             bull[5]))
                clip -= 1
            
    if delay == 59: #delay between bullets (1-30, lower is faster)
        delay = 0
        shot = False
    if shot:
        delay += 1
    for i in range(len(bulletList)):
        bulletList[i].move()
    
    
    #---peaceful AI---
    while len(peacefulAIlist)<10:
        ai=makePeacefulAI(screen,gameMap,player,peacefulSprites)
        peacefulAIlist.append(peacefulAI(ai[0],ai[1],ai[2],
                                         ai[3],ai[4]))
    for ai in peacefulAIlist:
        ai.move()

    erase(player,peacefulAIlist,bulletList)
    
    onscreen=gameMap.subsurface((cur_x-screen.get_width()//2,
                                 cur_y-screen.get_height()//2,
                                 screen.get_width(),screen.get_height())).copy()
    drawScene(onscreen,(cur_x,cur_y),player,bulletList,delay-1,mb,peacefulAIlist)
    
    count+=1
    fps+=myClock.get_fps()
    fpsList.append(myClock.get_fps())
    myClock.tick(1000)
    display.flip()
print(fps)
print(count)
print(fps/count)
print(max(fpsList))
print(min(fpsList))
quit()
