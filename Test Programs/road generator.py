from pygame import *
from random import *
screen=display.set_mode((700,700))

for x in range(0,700,5):
    for y in range(0,700,5):
        
        col=randint(25,125)
        col=(0,col,0)
        
        for a in range(5):
            for b in range(5):
                screen.set_at((x+a,y+b),(col))
'''
screen.fill((200,200,200))
x=100
y=400
w=400
h=250
col=200
for i in range(50):
    draw.rect(screen,(col,col,col),(x,y,w,h),1)
    x+=1
    y+=1
    w-=2
    h-=2
    col-=4
'''
#copy=screen.copy()
#image.save(copy,"brick.png")
running=True
while running:
    for e in event.get():
        if e.type==QUIT:
            running=False

    display.flip()
quit()
