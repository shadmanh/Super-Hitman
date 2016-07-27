#Sprite Tester
from pygame import*
import glob

screen=display.set_mode((300,300))

pics = glob.glob('*.png')
pics.sort()
for i in range(5):
    pics += [pics[0]]
pics.sort()
print(pics)
counter = 0
frame = 0
framesPerSprite = 50

running=True
while running:
    for e in event.get():
        if e.type==QUIT:
            running=False
            
    screen.fill((255,255,255))
    screen.blit(image.load(pics[frame]),(150-image.load(pics[frame]).get_width()//2,150-image.load(pics[frame]).get_height()//2))
    counter += 1
    if counter % framesPerSprite == 0:
        frame += 1
    if frame == len(pics):
        frame = 0
    if counter == framesPerSprite*len(pics):
        counter = 0

    display.flip()
quit()
