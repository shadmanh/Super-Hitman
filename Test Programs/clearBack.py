from glob import glob
from pygame import *

def clearBack(pic):
    rep = pic.get_at((0,0))
    rec = pic.get_rect()
    look = [(0,0),(pic.get_width()-1,0),(pic.get_width()-1,pic.get_height()-1),(0,pic.get_height()-1)]
    if rep[:3]!=0:
        while len(look)>0:
            x,y = look.pop()
            if rec.collidepoint((x,y)) and pic.get_at((x,y)) == rep:
                pic.set_at((x,y),(255,255,255,0))
                look += [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]
                


init()

pics = glob("*.png") + glob("*.bmp")+ glob("*.jpg")
full = []
for p in pics:
    print("working on:",p)
    pic = image.load(p)
    clearBack(pic)
    full.append(pic)

for i in range(len(pics)):
    image.save(full[i],pics[i][:-4]+".png")

quit()
