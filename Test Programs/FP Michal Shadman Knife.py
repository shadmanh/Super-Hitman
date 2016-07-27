from pygame import *
from math import *
from random import *

#---------------------VARIABLES THAT DO NOT CHANGE----------------------

resx,resy = 1280,720 #resolution size
cx,cy = resx//2,resy//2 #center coordinates, also half size of resolution
#The above actually change (ssshhhh don't tell anyone!) but they aren't constantly
#changing. The only reason they are privileged to be here is because they're
#needed in the next line :P
screen=display.set_mode((resx,resy),HWSURFACE|DOUBLEBUF|RESIZABLE)

font.init()

#---weapons---
#contains all weapon information
#(weapon image names (idle and firing), number of bullets fired per shot,rate of fire (the lower it is,
#the faster the gun shoots), damage per bullet)
weapons = [((image.load('Player\m161.png'),image.load('Player\m162.png')),1,10,10),
           ((image.load('Player\dualPistols1.png'),image.load('Player\dualPistols2.png')),2,30,20),
           ((image.load('Player\shotgun1.png'),image.load('Player\shotgun2.png')),5,60,15)]

meleeList = [('boomerang',image.load('boomerang.png'))]
knifeSprites = []
for i in range(6):
    knifeSprites.append(image.load('Player\knife%d.png'%i))
meleeList.append(knifeSprites)
meleeList[1] = ('knife',meleeList[1])

coin = image.load("Coin.png") #coin image
clip = 1000 #starting number of bullets of each clip
bLen = 20 #bullet length
bWid = 7 #bullet width
bSpeed = 40 #bullet speed
sprSpeed = 0.5 #speed of melee attacks
dynamicView = True #setting for if dynamic view is turned on/off
viewDelay = 8 #reduction of aim sensitivity
myClock = time.Clock()
peacefulSprites=[(image.load("Civilians\peaceful AI-1.png"),image.load("Civilians\peaceful AI-1-shot.png"))]
#list of images for peaceful ai sprites
maxCoinDrop=101 #the most $ that an AI can drop
minCoinDrop=1 #the least $ that an AI can drop
fadeSpeed=2 #speed at which onscreen info about pickups fade away
enemySpritesPistol=[] #list on enemy sprites that carry a pistol
for i in range(3):
    enemySpritesPistol.append((image.load("Enemies\e%sPistols1.png"%(str(i+1))),
                                image.load("Enemies\e%sPistols2.png"%(str(i+1)))))
#---Constants for shooter AI---
ammoPistol=36
healthPistol=100
#for each weapon list : [number of bullets per shot,rate of fire,damage per bullet]
pistol=[1,30,20,enemySpritesPistol]
weaponsAI=[pistol]
AIspeed=5
knifeDmg = 5 #damage X 12 used per swipe

#-------------------------VARIABLES THAT CAN CHANGE------------------------

running = True #flag for if program is running
count = 0
fps = 0
fpsList = []
w = 0 #selected primary weapon can change by changing this variable
n = 1 #selected secondary weapon can change by changing this variable
weapon = weapons[w] #selected weapon inside weapon list
bulletList = [] #list of active bullets in play in the game
shot = False #flag checking if player is currently shooting
bCol = (218,165,32)
delay = 0 #counter keeping track of current frame number (0-29) used in primary weapon sprites
secDelay = 0 #counter for secondary weapon sprites
peacefulAIList=[] #list of active civilians on screen
civHealth = 100 #civilian health
cur_x = 0 #default player coordinates in accordance to map
cur_y = 0
coinList=[] #the positions of dropped money by AIs and how much each is worth
money=0 #the amount of money that the player has
collectedCoinList=[] #list of coins that have been collected
#purpose is to display the amount for a little while after it has been collected
melSpr = image.load('Player\knife1.png') #default melee sprite
secondary = False #flag for if player is using secondary weapon or not
knife = False #flag for if player is knifing or not
dmgTip = (0,0) #default melee knife tip used for damage
deadList=[]
shooterAIList=[]

#---------------------------------FONT--------------------------------------
moneyFontHeight=50
moneyFontCol=(0,255,0)
moneyFont=font.SysFont("impact",moneyFontHeight)
collectedCoinFontHeight=40
collectedCoinFontCol=(255,255,0)
collectedCoinFont=font.SysFont("impact",collectedCoinFontHeight)

#----------------------------------MAP--------------------------------------
#loads all map images

collide=image.load("Game Maps\Collide Check.png").convert()
gameMap=image.load("Game Maps\Game Map.png").convert()
gameMapCopy=gameMap.copy()

#---------------------------------CLASSES-----------------------------------

class Player:
    '''Player keeps track of:

    x,y - current position
    ang - current angle the Player is facing
    pic1 - sprite to display when not moving
    pic2 - sprite to alternate to when firing
    fire - flag for if the player is shooting
    money - the amount of money they start off with
    '''

    def __init__(self,x,y,ang,pic1,pic2,weapon,money):

        self.x = x
        self.y = y
        self.ang = ang
        self.pic1 = pic1
        self.pic2 = pic2
        self.fire = False
        self.money=money

    def rotate(self,destX,destY,hScreenX,hScreenY):
        '''Player angle changes based on mouse coordinates'''

        moveX = destX - hScreenX
        moveY = destY - hScreenY
        self.ang = atan2(-moveY, moveX)

    def collectMoney(self,coinList,coin,collectedCoinList):
        """Checks to see if the player comes in contact with any coins laying on the ground
        If he does then he picks them up (obviously)"""
        for curCoin in coinList:
            if distance((player.x,player.y),curCoin[0]) <= coin.get_width()//2+40: #width and height of coin are ==
                player.money += curCoin[1] #the players money total increases based on the coins amount
                collectedCoinList.append((curCoin[0],curCoin[1],255)) #255 is the alpha that it
                                                      #will be blitted at
        for c in collectedCoinList:
            try :
                coinList.remove((c[0],c[1])) #removes the collected coins
            except ValueError: pass #occurs if the item has already been erased

    def draw(self,surface,delay,mb,secondary,meleeDelay,secWeap,meleeSprite,mx,my,cx,cy):
        '''Player is rotated/drawn based on angle coordinates. If he is
        shooting, the sprite drawn alternates between the idle and firing
        sprites (pic1 and pic2)'''

        self.rotate(mx,my,cx,cy)

        if secondary:
            if secWeap == 'knife':
                newPic = transform.rotate(meleeSprite,degrees(self.ang)+270)
        else:
            if mb[0]==1 and delay % weapon[2] == 0 or mb[0]==1 and (delay-1) % weapon[2] == 0 or mb[0]==1 and (delay-2) % weapon[2] == 0:
                newPic = transform.rotate(self.pic2,degrees(self.ang)+270)
            else:
                newPic = transform.rotate(self.pic1,degrees(self.ang)+270)
        surface.blit(newPic,getCentre(newPic,surface.get_width()//2,surface.get_height()//2))

class Bullet:
    '''Bullet keeps track of:

    ex,ey - current end position
    tx,ty - current tip position
    ang - current angle bullet is going from player when it was shot
    '''

    def __init__(self,ex,ey,tx,ty,ang,damage):

        self.ex = ex
        self.ey = ey
        self.tx = tx
        self.ty = ty
        self.ang = ang
        self.damage=damage

    def move(self,speed,length):
        '''finds the bullet end's and tip's next coordinates by using trig and
        the set distance and length of the bullet (which can be changed easily)'''

        self.ex, self.ey = self.tx + cos(self.ang) * (speed-length), self.ty - sin(self.ang) * (speed-length)
        self.tx, self.ty = self.tx + cos(self.ang) * speed, self.ty - sin(self.ang) * speed


    def draw(self,surface,player,width,bulCol):
        '''draws bullet using it's end and tip coordinates'''
        if fitOnscreen(surface,(player.x,player.y),(self.tx,self.ty)):
            new_tx=surface.get_width()//2-(player.x-self.tx)
            new_ex=surface.get_width()//2-(player.x-self.ex)
            new_ty=surface.get_height()//2-(player.y-self.ty)
            new_ey=surface.get_height()//2-(player.y-self.ey)
            draw.line(surface,bulCol,(new_tx,new_ty),(new_ex,new_ey),width)

class peacefulAI:
    """The peaceful AI keeps track of:

    x,y - current position
    sprite - sprite of the AI
    direction - direction headed (North, East, South, West or None if stationary)
    health - current amount of health
    maxHealth - default amount of starting health
    money - the amount of money that they are carrying
    shot - whether they have just been shot
    count - serves as a count for when the ai is hit to display the shot sprite
    """

    def __init__(self,x,y,sprites,direction,health,money):
        self.x=x
        self.y=y
        self.direction=direction
        self.sprite=sprites[0] #the original sprite
        self.spriteShot=sprites[1]
        self.rotated=self.sprite #self.sprite in its rotated form
        self.rotatedShot=self.spriteShot
        self.health=health
        self.maxHealth=health #the amount of health they start off with
        self.money=money
        self.shot=False
        self.count=0

    def move(self):
        """Moves the civilian
        There is a 4 in 250 chance that the AI will change directions
        the remaining chance will make the AI continue in the same direction
        """
        num=randint(1,250)
        directions = ['North','East','South','West','None']
        for i in range(5):
            if num-1 == i:
                self.direction = directions[i]

        if self.direction=="North" and collide.get_at((self.x,self.y-2))[:3]!=(0,0,0):
                self.y-=2 #moves AI in set direction if possible
        elif self.direction=="East" and collide.get_at((self.x+2,self.y))[:3]!=(0,0,0):
                self.x+=2
        elif self.direction=="South" and collide.get_at((self.x,self.y+2))[:3]!=(0,0,0):
                self.y+=2
        elif self.direction=="West" and collide.get_at((self.x-2,self.y))[:3]!=(0,0,0):
                self.x-=2

        #---Rotation of sprite image for different directions---
        if self.direction=="South" or self.direction=="None":
            self.rotated=transform.rotate(self.sprite,0)
            self.rotatedShot=transform.rotate(self.spriteShot,0)
        elif self.direction=="East":
            self.rotated=transform.rotate(self.sprite,90)
            self.rotatedShot=transform.rotate(self.spriteShot,90)
        elif self.direction=="North":
            self.rotated=transform.rotate(self.sprite,180)
            self.rotatedShot=transform.rotate(self.spriteShot,180)
        elif self.direction=="West":
            self.rotated=transform.rotate(self.sprite,270)
            self.rotatedShot=transform.rotate(self.spriteShot,270)
    
    def draw(self,surface,player):
        'Blits the civilian onto the screen and draws health bar'

        sx=surface.get_width()//2-(player.x-self.x) #x-coordinate relative to the screen
        sy=surface.get_height()//2-(player.y-self.y) #y-coordinate relative to the screen
        if self.shot==True: #if he is being shot
            self.count+=0.2 #adds to the count
            if self.count==1: 
                self.shot=False #if the shot sprite has been blitted for the correct
                #number of frames, then it reverts to the original state
                self.count=0
            surface.blit(self.rotatedShot,getCentre(self.rotatedShot,sx,sy))
        else :
            surface.blit(self.rotated,getCentre(self.rotated,sx,sy))

        width=int(self.rotated.get_width()/self.maxHealth*self.health) #width will be the
        #same whether it is self.rotated of self.rotatedShot
        height=10
        col=(255-int(width*2.5),5+int(width*2.5),0)
        draw.rect(surface,col,(sx-self.rotated.get_width()//2, #draws health bar
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
        'Reduces the AIs health based on how much damage the bullet deals'
        self.health -= bulDamage
        self.shot=True

class enemyShooter:
    """
    This is the class for the AI enemies that shoot at the player
    x - x coordinate of the enemy
    y - y coordinate of the enemy
    regSprite - sprite of the enemy when they are not shooting their gun
    shootingSprite - sprite when they are shooting their gun
    player - the class for the player
    ang - the angle they are facing
    dist - distance from the player
    weapon - the weapon that they are carrying
    rotatedReg/rotatedShoot - the rotated versions of the sprites
    shot - if they are shooting or not
    """
    def __init__(self,x,y,player,ang,weapon,speed):
        self.x=x
        self.y=y
        
        self.regSprite,self.shootingSprite=choice(weapon[3])
        self.player=player
        self.rotatedReg=self.regSprite
        self.rotatedShooting=self.shootingSprite
        self.ang=ang
        self.shot=False
        self.dist=distance((self.x,self.y),(self.player.x,self.player.y))
        self.weapon=weapon
        self.ammo=weapon[2]
        self.speed=speed

    def move(self,player,collide):
        """
        This function moves the AI
        """
        self.player=player
        self.dist=distance((self.x,self.y),(self.player.x,self.player.y))
        if self.dist>350:
            #---Code from FP Basics Eg 4.py---
            dist=max(self.dist,1)
            moveX=(self.player.x-self.x)*ai.speed/dist
            moveY=(self.player.y-self.y)*ai.speed/dist
            self.ang=degrees(atan2(-moveY,moveX))
            if collide.get_at((int(self.x+moveX),int(self.y+moveY)))[:3]!=(0,0,0):
                self.x+=moveX
                self.y+=moveY
        elif self.dist<250:
            dist=max(self.dist,1)
            moveX=(self.player.x-self.x)*ai.speed/dist
            moveY=(self.player.y-self.y)*ai.speed/dist
            self.ang=degrees(atan2(-moveY,moveX))
            if collide.get_at((int(self.x-moveX),int(self.y-moveY)))[:3]!=(0,0,0):
                self.x-=moveX
                self.y-=moveY
        else :
            self.ang=degrees(atan2(-(self.player.y-self.y),self.player.x-self.x))
        if blockedPath(collide,player,self)==True:
            pass
            
    #def shoot(self):
    #    if self.dist<400:
            
    def draw(self,surface):
        sx=surface.get_width()//2-(player.x-self.x) #x-coordinate relative to the screen
        sy=surface.get_height()//2-(player.y-self.y) #y-coordinate relative to the screen
        self.rotatedReg=transform.rotate(self.regSprite,self.ang-90)
        if fitOnscreen(surface,(self.player.x,self.player.y),(self.x,self.y)):
            surface.blit(self.rotatedReg,getCentre(self.rotatedReg,sx,sy))
    def rectangle(self):
        """
        Returns the rectangular area that the sprite covers
        Used for collision detection
        """
        return Rect(self.x,self.y,self.rotated1.get_width(),
                    self.rotated1.get_height())

#--------------------------------------FUNCTIONS-------------------------------------

def makePeacefulAI(screen,mainMap,collide,player,peacefulSprites,health,maxCoinDrop,minCoinDrop):
    'Makes a peaceful AI by accepting surface, map, player, different civilian sprites and starting health'
    money=randint(minCoinDrop,maxCoinDrop) #the amount of money they drop
    if money==maxCoinDrop:
        """If the maxCoinDrop is chosen, then the AI will carry a large amountof money,
        which can vary from 1-4 times the maxCoinDrop value"""
        money=maxCoinDrop*randint(1,4)
    x_pos,y_pos = 0,0
    while collide.get_at((x_pos,y_pos))==(0,0,0) or fitOnscreen(screen,(player.x,player.y),(x_pos,y_pos))==True:
        x_pos = randint(screen.get_width()//2,mainMap.get_width()-screen.get_width()//2) #A random position available
        y_pos = randint(screen.get_height()//2,mainMap.get_height()-screen.get_height()//2) #for a civilian to spawn
    direction = choice(["North","South","East","West","None"]) #on and first direction is created
    sprites = choice(peacefulSprites) #random civilian sprite is chosen for civilian
    return (x_pos,y_pos,sprites,direction,health,money)

def makeShooterAI(screen,mainMap,collide,player,weapon,health,speed):
    x_pos,y_pos=0,0
    while collide.get_at((x_pos,y_pos))==(0,0,0) or fitOnscreen(screen,(player.x,player.y),(x_pos,y_pos))==True:
        x_pos = randint(screen.get_width()//2,mainMap.get_width()-screen.get_width()//2) #A random position available
        y_pos = randint(screen.get_height()//2,mainMap.get_height()-screen.get_height()//2) #for them to spawn off screen
    MoveX=x_pos-player.x
    MoveY=y_pos-player.y
    ang=degrees(atan2(-MoveY,MoveX))
    return (x_pos,y_pos,player,ang,weapon,speed)

def distance(p1,p2):
    'Simple distance formula'
    return hypot(p2[0]-p1[0],p2[1]-p1[1])

def erase(player,peacefulAIlist,bulletList,coinList,deadList,damageTip,secondary,secWeap,knifeDamage):
    'Checks to see which bullets/AIs should be removed'
    bList,pList = [],[]
    for ai in peacefulAIlist:
        for bullet in bulletList:
            if ai.rectangle().collidepoint(bullet.tx,bullet.ty):
                ai.reduceHealth(bullet.damage) #decreases ai health if shot
                bList.append(bullet)
        if secondary:
            if secWeap == 'knife':
                if ai.rectangle().collidepoint(damageTip)==True:
                    ai.reduceHealth(knifeDamage)
        if ai.health<1:
            pList.append(ai)
            coinList.append(((ai.x,ai.y),ai.money))
            deadList.append(((ai.x,ai.y),ai.rotatedShot,255))
    for bullet in bulletList: #checks for collisions on the map
        if collide.get_at((int(bullet.tx),int(bullet.ty)))==(0,0,0):
            bList.append(bullet)
    for b in bList: #removes all the bullets that collide with buildings or AIs
        try:
            bulletList.remove(b)
        except ValueError: pass #crashes if the bullet has already been erased
                                #in the erase() function
    for p in pList: #erases all of the peaceful AIs that have lost all health
        try:
            peacefulAIlist.remove(p)
        except ValueError: pass #an error occurs if an AI is hit with multiple
                                #bullets

def make(player,wNum,shots,pos,damage):
    '''Makes bullets starting in various places going in various directions
    based on the weapon chosen. After determining the specific position and
    angle of the bullet, the properties of the bullet (tip/end coordinates,
    angle) are created and added to the list of active bullets as a tuple'''

    randang = randint(8*(shots-1),8*shots)
    ammoList = [(pos[0] + cos(player.ang) * 35, pos[1] - sin(player.ang) * 35, player.ang), #machine gun bullets
    (pos[0] + cos(player.ang+radians(-5+15*shots)) * 35, pos[1] -
        sin(player.ang+radians(-5+15*shots)) * 35, player.ang), #dual pistol bullets
    ((pos[0]+cos(player.ang)*35)+cos(player.ang+radians(-14+randang)) * 35,
     (pos[1]-sin(player.ang)*35)-sin(player.ang+radians(-14+randang)) * 35,
     player.ang+radians(-14+randang))] #shotgun bullets
    tipX,tipY = ammoList[wNum][0], ammoList[wNum][1]
    ang = ammoList[wNum][2]
    return ((tipX,tipY,tipX,tipY,ang,damage))

def gunRun(mb,magazine,shot,delay,secondary,weaponsList,weapon,player,mx,my,cx,cy,cur_x,cur_y,bList,bulletSpeed,bulletLength):
    'Handles bullet creating, bullet moving and player shooting sprite selection procedures'

    if mb[0] == 1 and magazine > 0 and secondary == False:
        shot = True
        if delay % weapon[2] == 0:
            player.rotate(mx,my,cx,cy)
            for i in range(weapon[1]):
                bull = make(player,weaponsList.index(weapon),i,(cur_x,cur_y),weapon[3])
                bList.append(Bullet(bull[0],bull[1],bull[2],bull[3],bull[4],bull[5]))
            magazine -= 1

    for i in range(len(bList)):
        bList[i].move(bulletSpeed,bulletLength)

    return(shot)

def getDelay(count,shot):
    'Calculates bullets and sees if player is still shooting or not'

    if count == 29: #counter for each frame
        count = 0 #helps calculate fire rate for each weapon
        shot = False
    if shot:
        count += 1
    return(count,shot)

def drawScene(surface,cur_pos,player,bList,delay,mb,peacefulAIList,mx,my,rx,ry,
              viewDel,bulletWidth,bulCol,coinList,coin,moneyFont,moneyFontCol,collectedCoinList,
              collectedCoinFont,collectedCoinFontHeight,collectedCoinFontCol,fadeSpeed,deadList,shooterAIList,
              secondary,meleeDelay,secWeap,meleeSprite,cx,cy):
    'Draws bullets in active bullet list, civilians and the player plus the HUD'

    for b in bList:
        b.draw(surface,player,bulletWidth,bulCol)
    drawDead(surface,deadList,player)
    for ai in peacefulAIList:
        ai.draw(surface,player)
        rectX=surface.get_width()//2-(player.x-ai.x)
        rectY=surface.get_height()//2-(player.y-ai.y)
        if fitOnscreen(screen,(player.x,player.y),(ai.x,ai.y)):
            draw.rect(screen,(255,0,0),(getCentre(ai.sprite,rectX,rectY)[0],getCentre(ai.sprite,rectX,rectY)[1],
                                        ai.sprite.get_width(),ai.sprite.get_height()))
        #draw.rect(surface,(255,0,0),ai.rectangle())
    for ai in shooterAIList:
        ai.draw(surface)
    for curCoin in coinList:
        if fitOnscreen(surface,(player.x,player.y),curCoin[0]):
            surface.blit(coin,getCentre(coin,surface.get_width()//2-(player.x-curCoin[0][0]),
                                              surface.get_height()//2-(player.y-curCoin[0][1])))
    player.draw(surface,delay,mb,secondary,meleeDelay,secWeap,meleeSprite,mx,my,cx,cy)
    #dist = distance((cur_pos[0],cur_pos[1]),(mx,my)) #distance between player and mouse coordinates
    #screen.blit(surface.subsurface(cur_pos[0]+(dist//viewDel)*cos(player.ang)-cenx,
    #cur_pos[1]-(dist//viewDel)*sin(player.ang)-ceny,rx,ry),(0,0))
    drawCoinText(surface,collectedCoinFontCol,collectedCoinList,coin,collectedCoinFont,
                 collectedCoinFontHeight,collectedCoinFontCol,player,fadeSpeed)

    surface.blit(moneyFont.render("$ %s"%player.money,True,moneyFontCol),(0,0))
    screen.blit(surface,(0,0))
    

def getCentre(surface,h,k):
    'returns coordinate of where to blit picture so that it is always in the centre'
    x = surface.get_width()
    y = surface.get_height()
    return h-(x//2),k-(y//2)

def drawCoinText(surface,col,collectedCoinList,coin,collectedCoinFont,
                 collectedCoinFontHeight,collectedCoinFontCol,player,fadeSpeed):
    """
    Draws the amount of money that was collected from a coin onscreen to be brief
    for every coin collected, it blits the amount onscreen and then adds it
    back into the list with its alpha slightly reduced and its position moving
    towards the top left of the screen, then it removes the old coin tuples from
    the list
    """   
    length=len(collectedCoinList)
    toAdd=[] #the local variable that holds all the new coin tuples
    for c in collectedCoinList:
        if fitOnscreen(surface,(player.x,player.y),c[0])==True:
            text=collectedCoinFont.render("$ %s"%c[1],True,col)
            try:
                toBlit=surface.subsurface(surface.get_width()//2-(player.x-c[0][0]-coin.get_width()//2),
                                       surface.get_height()//2-(player.y-c[0][1]-coin.get_height()//2),
                                         text.get_width(),text.get_height()).copy()
                #since rendered font surfaces dont seem to be able to change alpha, we have to make a
                #surface of what its supposed to be blitted over, and then blit the text onto, change the
                #alpha and finally blit the new surface onto the screen
                toBlit.blit(text,(0,0))
                toBlit.set_alpha(c[2])
            
                surface.blit(toBlit,(surface.get_width()//2-(player.x-c[0][0]-coin.get_width()//2),
                                       surface.get_height()//2-(player.y-c[0][1]-coin.get_height()//2)))
            except ValueError: #error is raised if the text is partly onscreen and partly off
                pass 
        if c[2]-5>0: #if the alpha for the next time it will be blitted is >0
            toAdd.append(((c[0][0]-2,c[0][1]-2),c[1],c[2]-fadeSpeed)) #adds the text and modifies
                                                                      #its properties slightly 
        
    for i in range(length):
        try: #error occurs if an object is not appended to toAdd because its alpha is 0
            collectedCoinList.append(toAdd[i]) #adds the new coin info
        except IndexError: pass
        collectedCoinList.remove(collectedCoinList[0]) #removes the old coin info

def fitOnscreen(surface,center,point):
    """Checks to see whether or not a certain object is in the current screen
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

def blockedPath(surface,player,ai):
    for i in range(int(ai.dist/ai.speed)):
        x=int(ai.x+i*4*cos(radians(ai.ang)))
        y=int(ai.y-i*4*sin(radians(ai.ang)))
        if surface.get_at((x,y))[:3]==(0,0,0):
            return True
    return False
        

def drawDead(surface,deadList,player):
    length=len(deadList)
    toAdd=[]
    for dead in deadList:
        if fitOnscreen(surface,(player.x,player.y),dead[0]):
            try:
                img=dead[1]
                toBlit=surface.subsurface(getCentre(img,surface.get_width()//2-(player.x-dead[0][0]),
                                                    surface.get_height()//2-(player.y-dead[0][1]))[0],
                                           getCentre(img,surface.get_width()//2-(player.x-dead[0][0]),
                                                     surface.get_height()//2-(player.y-dead[0][1]))[1],
                                             img.get_width(),img.get_height()).copy()           
                toBlit.blit(img,(0,0))
                toBlit.set_alpha(dead[2])
                surface.blit(toBlit,getCentre(toBlit,surface.get_width()//2-(player.x-dead[0][0]),
                                              surface.get_height()//2-(player.y-dead[0][1])))
            except ValueError: pass
        if dead[2]-5>0:
            toAdd.append((dead[0],dead[1],dead[2]-5))
    for i in range(length):
        del deadList[0]
        try:
            deadList.append(toAdd[i])
        except IndexError: pass
        

def movePlayer(keys,cur_x,cur_y):
    "Moves the player if the WASD keys are pressed and if it's possible (checks collisions using collision map)"
    if keys[K_a] and collide.get_at((cur_x-5,cur_y))[:3]!=(0,0,0):
        cur_x-=5
    if keys[K_d] and collide.get_at((cur_x+5,cur_y))[:3]!=(0,0,0):
        cur_x+=5
    if keys[K_w] and collide.get_at((cur_x,cur_y-5))[:3]!=(0,0,0):
        cur_y-=5
    if keys[K_s] and collide.get_at((cur_x,cur_y+5))[:3]!=(0,0,0):
        cur_y+=5
    return cur_x,cur_y

#def thrower(surface,player,fling):
    'Throws boomerang'

def meleeAtk(surface,player,weapon,count,spriteSpeed):
    'Executes melee attacks and chooses melee sprites to display'
    if weapon[0] == 'knife':
        spr = weapon[1][int(count)]
        count += spriteSpeed #returns sprites for knife animation
        if count == 6:
            count = 0
        knifeTip = (int(cur_x+50*(cos(radians((degrees(player.ang)-30)+(15*secDelay))))),int(cur_y-50*(sin(radians((degrees(player.ang)-30)+(15*secDelay))))))
        return (count,spr,knifeTip)

while collide.get_at((cur_x,cur_y)) == (0,0,0): #chooses a random spot the player can spot
    cur_x = randint(0,gameMap.get_width())
    cur_y = randint(0,gameMap.get_height())

while running:
    for e in event.get():
        if e.type==MOUSEBUTTONDOWN:
            if e.button ==2:
                n += 1
                if n > 2:
                    n = 0
            if e.button == 3:
                secondary = True
            if e.button == 4:
                w -= 1 #changes weapons when mouse is scrolled
                if w < 0:
                    w = 2
            if e.button == 5:
                w += 1 #changes weapons when mouse is scrolled
                if w > 2:
                    w = 0
        if e.type==VIDEORESIZE:
            screen=display.set_mode(e.dict['size'],HWSURFACE|DOUBLEBUF|RESIZABLE)
            resx,resy = e.dict['size'] #resolution size
            cx,cy = resx//2,resy//2 #center coordinates, also half size of resolution
        if e.type==QUIT:
            running=False

#--------------------------------------------CONSTANTLY CHANGING VARIABLES----------------------------------------------

    k = key.get_pressed()
    cur_x,cur_y = movePlayer(k,cur_x,cur_y)
    weapon = weapons[w]
    secWeapon = meleeList[n]
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    pic1,pic2 = weapon[0][0], weapon[0][1]

#----------------------------------------------FUNCTIONS CONSTANTLY USED------------------------------------------------

    player = Player(cur_x,cur_y,0,pic1,pic2,weapon,money)

    if k[K_KP_PLUS]:
        bSpeed += 1
    if k[K_KP_MINUS]:
        bSpeed -= 1
    #if k[K_p]

    #thrower(screen,player,fling)
    shot = gunRun(mb,clip,shot,delay,secondary,weapons,weapon,player,mx,my,cx,cy,cur_x,cur_y,bulletList,bSpeed,bLen)
    delay,shot = getDelay(delay,shot)[0],getDelay(delay,shot)[1]
    if secondary:
        if secWeapon[0] == 'knife':
            player.rotate(mx,my,cx,cy)
            secDelay,melSpr,dmgTip = meleeAtk(screen,player,secWeapon,secDelay,sprSpeed)[0],\
                                meleeAtk(screen,player,secWeapon,secDelay,sprSpeed)[1],\
                                meleeAtk(screen,player,secWeapon,secDelay,sprSpeed)[2]
    if secDelay == 0: #returns melee frame number to choose melee sprite number for the next frame
        secondary = False #and melee frame to draw for the current frame and knife tip to calculate damage

    while len(peacefulAIList)<10: #spawns 30 random civilians in 30 random positions on the city map
        ai = makePeacefulAI(screen,gameMap,collide,player,peacefulSprites,civHealth,maxCoinDrop,minCoinDrop)
        peacefulAIList.append(peacefulAI(ai[0],ai[1],ai[2],ai[3],ai[4],ai[5]))

    while len(shooterAIList)<5:
        ai = makeShooterAI(screen,gameMap,collide,player,choice(weaponsAI),healthPistol,AIspeed)
        shooterAIList.append(enemyShooter(ai[0],ai[1],ai[2],ai[3],ai[4],ai[5]))

    for ai in peacefulAIList: #moves civilians
        ai.move()

    for ai in shooterAIList:
        ai.move(player,collide)

    player.collectMoney(coinList,coin,collectedCoinList) #collects any money that the player happens to walk over

    erase(player,peacefulAIList,bulletList,coinList,deadList,dmgTip,secondary,secWeapon[0],knifeDmg) #erases bullets that already collided and civilians who've lost all health
    onscreen = gameMap.subsurface((cur_x-screen.get_width()//2, #section of map currently viewed on screen
                                   cur_y-screen.get_height()//2, screen.get_width(),screen.get_height())).copy()
    drawScene(onscreen,(cur_x,cur_y),player,bulletList,delay-1,mb,peacefulAIList,mx,my,resx,resy,viewDelay,bWid,bCol,
              coinList,coin,moneyFont,moneyFontCol,collectedCoinList,collectedCoinFont,
              collectedCoinFontHeight,collectedCoinFontCol,fadeSpeed,deadList,shooterAIList,secondary,secDelay,
              secWeapon[0],melSpr,mx,my)
    #draws all elements on screen (E.g. background, player, AIs, bullets)

    money=player.money #allows the players total money to be carried over to the next loop of the game
    
    count += 1
    fps += myClock.get_fps()
    fpsList.append(myClock.get_fps())
    myClock.tick(60)
    display.flip()

print(fps/count)
print(max(fpsList))
print(min(fpsList))
quit()


#--------------------------------------Notes------------------------------------
#---Screen Resizing Feature---
"""We didn't come up with the code for it all by ourselves.
There was a sample program in the pygame.com cookbook at
http://www.pygame.org/wiki/WindowResizing?parent=CookBook
where we got the code to do it which we modified and adjusted to fit into
our program"""
