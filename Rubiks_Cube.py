import pygame, random
from math import ceil
from pygame.locals import *
pygame.init()
screen, layer, timer, timeElapsed, running, loading, textInput, invalidInput=pygame.display.set_mode((720, 540)), 2, pygame.time.Clock(), 0, False, True, "", False
class Cube:
    def __init__(self, size=3, scrambled=False):
        self.size, self.turnChoice=int(size), ["R", "U", "F"]+(["L", "D", "B"] if int(size)>2 else [])
        for i in range(4, self.size+1):self.turnChoice+=[str(i//2)+"Rw", str(i//2)+"Uw", str(i//2)+"Fw"] if i%2==0 else [str(i//2)+"Lw", str(i//2)+"Dw", str(i//2)+"Bw"]
        self.reset()
        if scrambled:self.scramble()
    def reset(self):self.state=[(255, 255, 255)]*self.size**2+([(255, 159, 0)]*self.size+[(0, 255, 0)]*self.size+[(255, 0, 0)]*self.size+[(0, 0, 255)]*self.size)*self.size+[(255, 255, 0)]*self.size**2
    def rotate(self, rotation, direction=1):
        for i in range(direction):
            newState=[]
            if rotation=="R":
                for j in range(self.size):newState+=self.state[j*self.size:(j+1)*self.size-1]+[self.state[(j*4+self.size+2)*self.size-1]]
                for j in range(self.size):newState+=self.state[(j*4+self.size)*self.size:(j*4+self.size+2)*self.size-1]+[self.state[(j+5*self.size+1)*self.size-1]]+self.state[j+(5*self.size-2)*self.size:j+(self.size+2)*self.size-1:-4*self.size]+[self.state[(-j+self.size)*self.size-1]]+self.state[(j*4+self.size+3)*self.size+1:(j*4+self.size+4)*self.size]
                for j in range(self.size):newState+=self.state[(j+5*self.size)*self.size:(j+5*self.size+1)*self.size-1]+[self.state[(-j*4+5*self.size-1)*self.size]]
                self.state=newState
            elif rotation=="U":
                for j in range(self.size):newState+=self.state[j+(self.size-1)*self.size::-self.size]
                self.state=newState+self.state[(self.size+1)*self.size:(self.size+4)*self.size]+self.state[self.size**2:(self.size+1)*self.size]+self.state[(self.size+4)*self.size:]
            elif rotation=="F":
                for j in range(self.size):newState+=self.state[(j*4+self.size)*self.size:(j*4+self.size+1)*self.size-1]+[self.state[j+5*self.size**2]]+self.state[j+(5*self.size-3)*self.size:j+(self.size+1)*self.size-1:-4*self.size]+[self.state[j+(self.size-1)*self.size]]+self.state[(j*4+self.size+2)*self.size+1:(j*4+self.size+4)*self.size]
                self.state=self.state[:(self.size-1)*self.size]+self.state[(5*self.size-3)*self.size-1:(self.size+1)*self.size-2:-4*self.size]+newState+self.state[(5*self.size-2)*self.size:(self.size+2)*self.size-1:-4*self.size]+self.state[(5*self.size+1)*self.size:]
            elif rotation=="L":
                for j in range(self.size):newState+=[self.state[(-j*4+5*self.size)*self.size-1]]+self.state[j*self.size+1:(j+1)*self.size]
                for j in range(self.size):newState+=self.state[j+(5*self.size-4)*self.size:j+self.size**2-1:-4*self.size]+[self.state[j*self.size]]+self.state[(j*4+self.size+1)*self.size+1:(j*4+self.size+4)*self.size-1]+[self.state[(-j+6*self.size-1)*self.size]]
                for j in range(self.size):newState+=[self.state[(j*4+self.size+1)*self.size]]+self.state[(j+5*self.size)*self.size+1:(j+5*self.size+1)*self.size]
                self.state=newState
            elif rotation=="D":
                for j in range(self.size):newState+=self.state[j+(6*self.size-1)*self.size:j+5*self.size**2-1:-self.size]
                self.state=self.state[:(5*self.size-4)*self.size]+self.state[(5*self.size-1)*self.size:5*self.size**2]+self.state[(5*self.size-4)*self.size:(5*self.size-1)*self.size]+newState
            elif rotation=="B":
                for j in range(self.size):newState+=[self.state[-j+self.size-1]]+self.state[(j*4+self.size)*self.size+1:(j*4+self.size+3)*self.size-1]+[self.state[-j+6*self.size**2-1]]+self.state[j+(5*self.size-1)*self.size:j+(self.size+3)*self.size-1:-4*self.size]
                self.state=self.state[(self.size+3)*self.size-1:(5*self.size-1)*self.size:4*self.size]+self.state[self.size:self.size**2]+newState+self.state[5*self.size**2:(6*self.size-1)*self.size]+self.state[self.size**2:(5*self.size-4)*self.size+1:4*self.size]
            elif rotation=="M":
                for j in range(2, self.size):self.rotate(str(j)+"MR", 3)
            elif rotation=="E":
                for j in range(2, self.size):self.rotate(str(j)+"MU", 3)
            elif rotation=="S":
                for j in range(2, self.size):self.rotate(str(j)+"MF")
            elif rotation[-2:]=="MR":
                for j in range(self.size):newState+=self.state[j*self.size:(j+1)*self.size-int(rotation[:-2])]+[self.state[(j*4+self.size+2)*self.size-int(rotation[:-2])]]+self.state[(j+1)*self.size-int(rotation[:-2])+1:(j+1)*self.size]
                for j in range(self.size):newState+=self.state[(j*4+self.size)*self.size:(j*4+self.size+2)*self.size-int(rotation[:-2])]+[self.state[(j+5*self.size+1)*self.size-int(rotation[:-2])]]+self.state[(j*4+self.size+2)*self.size-int(rotation[:-2])+1:(j*4+self.size+3)*self.size+int(rotation[:-2])-1]+[self.state[(-j+self.size)*self.size-int(rotation[:-2])]]+self.state[(j*4+self.size+3)*self.size+int(rotation[:-2]):(j*4+self.size+4)*self.size]
                for j in range(self.size):newState+=self.state[(j+5*self.size)*self.size:(j+5*self.size+1)*self.size-int(rotation[:-2])]+[self.state[(-j*4+5*self.size-1)*self.size+int(rotation[:-2])-1]]+self.state[(j+5*self.size+1)*self.size-int(rotation[:-2])+1:(j+5*self.size+1)*self.size]
                self.state=newState
            elif rotation[-2:]=="MU":self.state=self.state[:(self.size+4*int(rotation[:-2])-4)*self.size]+self.state[(self.size+4*int(rotation[:-2])-3)*self.size:(self.size+4*int(rotation[:-2]))*self.size]+self.state[(self.size+4*int(rotation[:-2])-4)*self.size:(self.size+4*int(rotation[:-2])-3)*self.size]+self.state[(self.size+4*int(rotation[:-2]))*self.size:]
            elif rotation[-2:]=="MF":
                for j in range(self.size):newState+=self.state[(j*4+self.size)*self.size:(j*4+self.size+1)*self.size-int(rotation[:-2])]+[self.state[j+(5*self.size+int(rotation[:-2])-1)*self.size]]+self.state[(j*4+self.size+1)*self.size-int(rotation[:-2])+1:(j*4+self.size+2)*self.size+int(rotation[:-2])-1]+[self.state[j+(self.size-int(rotation[:-2]))*self.size]]+self.state[(j*4+self.size+2)*self.size+int(rotation[:-2]):(j*4+self.size+4)*self.size]
                self.state=self.state[:(self.size-int(rotation[:-2]))*self.size]+self.state[(5*self.size-3)*self.size-int(rotation[:-2]):(self.size+1)*self.size-int(rotation[:-2])-1:-4*self.size]+self.state[(self.size-int(rotation[:-2])+1)*self.size:self.size**2]+newState+self.state[5*self.size**2:(5*self.size+int(rotation[:-2])-1)*self.size]+self.state[(5*self.size-2)*self.size+int(rotation[:-2])-1:(self.size+2)*self.size+int(rotation[:-2])-2:-4*self.size]+self.state[(5*self.size+int(rotation[:-2]))*self.size:]
            elif rotation[-2:]=="ML":self.rotate(str(self.size-int(rotation[:-2])+1)+"MR", 3)
            elif rotation[-2:]=="MD":self.rotate(str(self.size-int(rotation[:-2])+1)+"MU", 3)
            elif rotation[-2:]=="MB":self.rotate(str(self.size-int(rotation[:-2])+1)+"MF", 3)
            elif rotation[-3:]=="MRw":
                for j in range(2, int(rotation[:-3])+1):self.rotate(str(j)+"MR")
            elif rotation[-3:]=="MUw":
                for j in range(2, int(rotation[:-3])+1):self.rotate(str(j)+"MU")
            elif rotation[-3:]=="MFw":
                for j in range(2, int(rotation[:-3])+1):self.rotate(str(j)+"MF")
            elif rotation[-3:]=="MLw":
                for j in range(self.size-int(rotation[:-3])+1, self.size):self.rotate(str(j)+"MR", 3)
            elif rotation[-3:]=="MDw":
                for j in range(self.size-int(rotation[:-3])+1, self.size):self.rotate(str(j)+"MU", 3)
            elif rotation[-3:]=="MBw":
                for j in range(self.size-int(rotation[:-3])+1, self.size):self.rotate(str(j)+"MF", 3)
            elif rotation[-2:]=="Rw":
                self.rotate("R")
                self.rotate(rotation[:-2]+"MRw")
            elif rotation[-2:]=="Uw":
                self.rotate("U")
                self.rotate(rotation[:-2]+"MUw")
            elif rotation[-2:]=="Fw":
                self.rotate("F")
                self.rotate(rotation[:-2]+"MFw")
            elif rotation[-2:]=="Lw":
                self.rotate("L")
                self.rotate(rotation[:-2]+"MLw")
            elif rotation[-2:]=="Dw":
                self.rotate("D")
                self.rotate(rotation[:-2]+"MDw")
            elif rotation[-2:]=="Bw":
                self.rotate("B")
                self.rotate(rotation[:-2]+"MBw")
            elif rotation=="x":
                self.rotate("R")
                self.rotate("M", 3)
                if self.size>1:self.rotate("L", 3)
            elif rotation=="y":
                self.rotate("U")
                self.rotate("E", 3)
                if self.size>1:self.rotate("D", 3)
            elif rotation=="z":
                self.rotate("F")
                self.rotate("S")
                if self.size>1:self.rotate("B", 3)
    def scramble(self, turnChoice=...):
        custom=True
        if turnChoice==...:turnChoice, custom=self.turnChoice, False
        turnType, pTypes=0.5, [0.5]
        for i in range(15 if self.size==2 else 35 if self.size==3 else 40*self.size-100):
            if custom:turnType=random.randint(0, len(turnChoice)-1)
            else:
                while turnType in pTypes:turnType=random.randint(0, len(turnChoice)-1)
                if turnType%3!=pTypes[0]%3:pTypes=[turnType]
                else:pTypes+=[turnType]
            self.rotate(turnChoice[turnType], random.randint(1, 3))
    def drawCube(self, window, x, y, drawSize):
        for i in range(self.size):
            for j in range(self.size):pygame.draw.polygon(window, self.state[i*self.size+j], ((x+(0.4+((j+0.05)*0.6-(i+0.05)*0.4)/self.size)*drawSize, y+((i+0.05)*0.3+(j+0.05)*0.2)/self.size*drawSize), (x+(0.4+((j+0.05)*0.6-(i+0.95)*0.4)/self.size)*drawSize, y+((i+0.95)*0.3+(j+0.05)*0.2)/self.size*drawSize), (x+(0.4+((j+0.95)*0.6-(i+0.95)*0.4)/self.size)*drawSize, y+((i+0.95)*0.3+(j+0.95)*0.2)/self.size*drawSize), (x+(0.4+((j+0.95)*0.6-(i+0.05)*0.4)/self.size)*drawSize, y+((i+0.05)*0.3+(j+0.95)*0.2)/self.size*drawSize)))
        for i in range(self.size):
            for j in range(self.size):pygame.draw.polygon(window, self.state[i*4*self.size+j+(self.size+1)*self.size], ((x+(j+0.05)*0.6/self.size*drawSize, y+(0.3+((i+0.05)*0.6+(j+0.05)*0.2)/self.size)*drawSize), (x+(j+0.05)*0.6/self.size*drawSize, y+(0.3+((i+0.95)*0.6+(j+0.05)*0.2)/self.size)*drawSize), (x+(j+0.95)*0.6/self.size*drawSize, y+(0.3+((i+0.95)*0.6+(j+0.95)*0.2)/self.size)*drawSize), (x+(j+0.95)*0.6/self.size*drawSize, y+(0.3+((i+0.05)*0.6+(j+0.95)*0.2)/self.size)*drawSize)))
        for i in range(self.size):
            for j in range(self.size):pygame.draw.polygon(window, self.state[i*4*self.size+j+(self.size+2)*self.size], ((x+(0.6+(j+0.05)*0.4/self.size)*drawSize, y+(0.5+((i+0.05)*0.6-(j+0.05)*0.3)/self.size)*drawSize), (x+(0.6+(j+0.05)*0.4/self.size)*drawSize, y+(0.5+((i+0.95)*0.6-(j+0.05)*0.3)/self.size)*drawSize), (x+(0.6+(j+0.95)*0.4/self.size)*drawSize, y+(0.5+((i+0.95)*0.6-(j+0.95)*0.3)/self.size)*drawSize), (x+(0.6+(j+0.95)*0.4/self.size)*drawSize, y+(0.5+((i+0.05)*0.6-(j+0.95)*0.3)/self.size)*drawSize)))
    def drawCubeNet(self, window, x, y, width, height):
        for i in range(self.size):
            for j in range(self.size):pygame.draw.rect(window, self.state[i*self.size+j], (x+width/(4*self.size)*(j+self.size+0.1)-j*3/self.size, y+height/(3*self.size)*(i+0.1)-i*3/self.size, ceil(width*(1 if width/(4*self.size)-3/self.size-ceil(width*0.8/(4*self.size))<=1 else 0.8)/(4*self.size)), ceil(height*(1 if height/(3*self.size)-3/self.size-ceil(height*0.8/(3*self.size))<=1 else 0.8)/(3*self.size))))
        for i in range(self.size):
            for j in range(4*self.size):pygame.draw.rect(window, self.state[i*4*self.size+j+self.size**2], (x+width/(4*self.size)*(j+0.1)-j%self.size*3/self.size, y+height/(3*self.size)*(i+self.size+0.1)-i*3/self.size, ceil(width*(1 if width/(4*self.size)-3/self.size-ceil(width*0.8/(4*self.size))<=1 else 0.8)/(4*self.size)), ceil(height*(1 if height/(3*self.size)-3/self.size-ceil(height*0.8/(3*self.size))<=1 else 0.8)/(3*self.size))))
        for i in range(self.size):
            for j in range(self.size):pygame.draw.rect(window, self.state[i*self.size+j+5*self.size**2], (x+width/(4*self.size)*(j+self.size+0.1)-j*3/self.size, y+height/(3*self.size)*(i+2*self.size+0.1)-i*3/self.size, ceil(width*(1 if width/(4*self.size)-3/self.size-ceil(width*0.8/(4*self.size))<=1 else 0.8)/(4*self.size)), ceil(height*(1 if height/(3*self.size)-3/self.size-ceil(height*0.8/(3*self.size))<=1 else 0.8)/(3*self.size))))
def update():
    screen.fill((0, 0, 0))
    if loading:
        screen.blit(pygame.font.Font(None, 50).render("Cube size: "+textInput, True, (255, 255, 255)), (160, 240))
        if invalidInput:screen.blit(pygame.font.Font(None, 30).render("Please input a cube size.", True, (255, 0, 0)), (360, 280))
    else:
        cube.drawCube(screen, 30, 90, 390)
        cube.drawCubeNet(screen, 480, 360, 240, 180)
        screen.blit(pygame.font.Font(None, 20).render("Valid turns: "+("None." if cube.size<1 else "R, U, F, L, D, B, " if cube.size>1 else "")+("M, E, S, " if cube.size>2 else "")+("x, y, z. Cube notation can be searched up online." if cube.size>0 else ""), True, (255, 255, 255)), (20, 10))
        if cube.size>0:
            screen.blit(pygame.font.Font(None, 18).render("Hold Ctrl for double-turns"+(" and" if cube.size<3 else ",")+" Shift for counter-clockwise turns"+("." if cube.size<3 else (" and" if cube.size<4 else ",")+" Alt for "+("double" if cube.size<4 else "multi")+"-layer (wide) turns"+(",  A for single-layer slice" if cube.size>3 else ".")), True, (255, 255, 255)), (20, 25))
            if cube.size>3:
                screen.blit(pygame.font.Font(None, 18).render("turns, Alt+A for multi-layer slice turns, C for half-cube turns"+(" (excluding the middle layer)" if cube.size%2==1 else "")+", A+C for half-cube slice turns"+(" and Alt+C for all-slice layer-" if cube.size%2==0 else ""), True, (255, 255, 255)), (20, 40))
                screen.blit(pygame.font.Font(None, 18).render(("and Alt+C for all-slice layer-" if cube.size%2==1 else "")+"wide turns (not to be confused with full cube rotations).", True, (255, 255, 255)), (20, 55))
                screen.blit(pygame.font.Font(None, 25).render("Current multi-layer setting: "+str(layer), True, (255, 255, 255)), (435, 175))
                screen.blit(pygame.font.Font(None, 25).render("Input multi-layer setting: "+textInput, True, (255, 255, 255)), (435, 200))
                if invalidInput:
                    screen.blit(pygame.font.Font(None, 20).render("Please input a number", True, (255, 0, 0)), (550, 220))
                    screen.blit(pygame.font.Font(None, 20).render("between 2 and "+str(cube.size-1)+".", True, (255, 0, 0)), (550, 235))
            screen.blit(pygame.font.Font(None, 20).render("Press "+("Q to scramble the cube and " if cube.size>1 else "")+"W to reset to solved.", True, (255, 255, 255)), (370, 130))
        screen.blit(pygame.font.Font(None, 33).render(f"Time elapsed: {'{0:.3f}'.format(timeElapsed/1000)} seconds", True, (255, 255, 255)), (370, 80))
        screen.blit(pygame.font.Font(None, 20).render("To start, stop or reset the timer, press Space.", True, (255, 255, 255)), (370, 110))
    pygame.display.update()
update()
while True:
    for event in pygame.event.get():
        if event.type==QUIT or event.type==KEYUP and event.key==K_ESCAPE:
            pygame.quit()
            quit()
        elif event.type==KEYDOWN:
            if event.key==K_RETURN:
                if textInput=="" or not loading and (int(textInput)<2 or int(textInput)>=cube.size):invalidInput=True
                elif loading:cube, loading, textInput=Cube(int(textInput)), False, ""
                else:layer, textInput=int(textInput), ""
            elif event.key==K_BACKSPACE:textInput, invalidInput=textInput[:-1], False
            elif pygame.key.name(event.key).isnumeric():
                if invalidInput:textInput=""
                textInput+=pygame.key.name(event.key)
                invalidInput=False
            elif not loading:
                if event.key in [K_r, K_u, K_f, K_l, K_d, K_b] and cube.size>1:cube.rotate(str(cube.size-1)+pygame.key.name(event.key).upper()+"w" if cube.size>3 and event.mod&KMOD_ALT and pygame.key.get_pressed()[K_c] else str(cube.size//2)+("M"+pygame.key.name(event.key).upper()+"w" if pygame.key.get_pressed()[K_a] else pygame.key.name(event.key).upper()+"w") if cube.size>3 and pygame.key.get_pressed()[K_c] else pygame.key.name(event.key).upper() if not event.mod&KMOD_ALT and (cube.size<4 or not pygame.key.get_pressed()[K_a]) else str(layer)+("M"+pygame.key.name(event.key).upper()+"w" if cube.size>3 and event.mod&KMOD_ALT and pygame.key.get_pressed()[K_a] else pygame.key.name(event.key).upper()+"w" if event.mod&KMOD_ALT else "M"+pygame.key.name(event.key).upper()), 2 if event.mod&KMOD_CTRL else 3 if event.mod&KMOD_SHIFT else 1)
                elif event.key in [K_m, K_e, K_s] and cube.size>2:cube.rotate(pygame.key.name(event.key).upper(), 2 if event.mod&KMOD_CTRL else 3 if event.mod&KMOD_SHIFT else 1)
                elif event.key in [K_x, K_y, K_z] and cube.size>0:cube.rotate(pygame.key.name(event.key), 2 if event.mod&KMOD_CTRL else 3 if event.mod&KMOD_SHIFT else 1)
                elif event.key==K_q and cube.size>1:cube.scramble()
                elif event.key==K_w:cube.reset()
                elif event.key==K_SPACE and timeElapsed==0:running=True
                elif event.key==K_SPACE and running:running=False
                elif event.key==K_SPACE:timeElapsed=0
    timer.tick(100)
    if running:timeElapsed+=timer.get_time()
    update()