from pygame import *
import glob
screen=display.set_mode((1280,720))

'''JezInc=image.load("Jez Inc Logo.png")
And=image.load("and.png")
ShadowGames=image.load("shadowLogo.png")
HavePartnered=image.load("Have Partnered.png")
JezMan=image.load("JezMan Logo.png")
ProgrammedIn=image.load("programmed in.png")
PythonLogo=image.load("Python Logo.png")
WithModulesFrom=image.load("with modules from.png")
PygameLogo=image.load("Pygame Logo.png")'''

logos = glob.glob('*.png')

def fadeIn(surface,logo):
    for i in range(255//4):
        surface.blit(logo,(0,0))
        layer=Surface((surface.get_width(),surface.get_height()))
        layer.set_alpha(255-i*4)
        surface.blit(layer,(0,0))
        display.flip()

def fadeOut(surface,logo):
    for i in range(255//4):
        surface.blit(logo,(0,0))
        layer=Surface((surface.get_width(),surface.get_height()))
        layer.set_alpha(i*4)
        surface.blit(layer,(0,0))
        display.flip()

running=True
while running:
    for e in event.get():
        if e.type==QUIT:
            running=False
    for i in range(len(logos)):
        fadeIn(screen,image.load(logos[i]))
        time.wait(10)
        fadeOut(screen,image.load(logos[i]))
        
quit()
