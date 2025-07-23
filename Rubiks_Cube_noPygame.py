import random
class Cube:
    def __init__(self, size=3, scrambled=False):
        self.size, self.turnChoice=int(size), ["r", "u", "f"]+(["l", "d", "b"] if int(size)>2 else [])
        for i in range(4, self.size+1):self.turnChoice+=[str(i//2)+"rw", str(i//2)+"uw", str(i//2)+"fw"] if i%2==0 else [str(i//2)+"lw", str(i//2)+"dw", str(i//2)+"bw"]
        self.reset()
        if scrambled:self.scramble()
    def reset(self):self.state=["W"]*self.size**2+(["O"]*self.size+["G"]*self.size+["R"]*self.size+["B"]*self.size)*self.size+["Y"]*self.size**2
    def rotate(self, rotation, direction=1):
        for i in range(direction):
            newState=[]
            if rotation=="r":
                for j in range(self.size):newState+=self.state[j*self.size:(j+1)*self.size-1]+[self.state[(j*4+self.size+2)*self.size-1]]
                for j in range(self.size):newState+=self.state[(j*4+self.size)*self.size:(j*4+self.size+2)*self.size-1]+[self.state[(j+5*self.size+1)*self.size-1]]+self.state[j+(5*self.size-2)*self.size:j+(self.size+2)*self.size-1:-4*self.size]+[self.state[(-j+self.size)*self.size-1]]+self.state[(j*4+self.size+3)*self.size+1:(j*4+self.size+4)*self.size]
                for j in range(self.size):newState+=self.state[(j+5*self.size)*self.size:(j+5*self.size+1)*self.size-1]+[self.state[(-j*4+5*self.size-1)*self.size]]
                self.state=newState
            elif rotation=="u":
                for j in range(self.size):newState+=self.state[j+(self.size-1)*self.size::-self.size]
                self.state=newState+self.state[(self.size+1)*self.size:(self.size+4)*self.size]+self.state[self.size**2:(self.size+1)*self.size]+self.state[(self.size+4)*self.size:]
            elif rotation=="f":
                for j in range(self.size):newState+=self.state[(j*4+self.size)*self.size:(j*4+self.size+1)*self.size-1]+[self.state[j+5*self.size**2]]+self.state[j+(5*self.size-3)*self.size:j+(self.size+1)*self.size-1:-4*self.size]+[self.state[j+(self.size-1)*self.size]]+self.state[(j*4+self.size+2)*self.size+1:(j*4+self.size+4)*self.size]
                self.state=self.state[:(self.size-1)*self.size]+self.state[(5*self.size-3)*self.size-1:(self.size+1)*self.size-2:-4*self.size]+newState+self.state[(5*self.size-2)*self.size:(self.size+2)*self.size-1:-4*self.size]+self.state[(5*self.size+1)*self.size:]
            elif rotation=="l":
                for j in range(self.size):newState+=[self.state[(-j*4+5*self.size)*self.size-1]]+self.state[j*self.size+1:(j+1)*self.size]
                for j in range(self.size):newState+=self.state[j+(5*self.size-4)*self.size:j+self.size**2-1:-4*self.size]+[self.state[j*self.size]]+self.state[(j*4+self.size+1)*self.size+1:(j*4+self.size+4)*self.size-1]+[self.state[(-j+6*self.size-1)*self.size]]
                for j in range(self.size):newState+=[self.state[(j*4+self.size+1)*self.size]]+self.state[(j+5*self.size)*self.size+1:(j+5*self.size+1)*self.size]
                self.state=newState
            elif rotation=="d":
                for j in range(self.size):newState+=self.state[j+(6*self.size-1)*self.size:j+5*self.size**2-1:-self.size]
                self.state=self.state[:(5*self.size-4)*self.size]+self.state[(5*self.size-1)*self.size:5*self.size**2]+self.state[(5*self.size-4)*self.size:(5*self.size-1)*self.size]+newState
            elif rotation=="b":
                for j in range(self.size):newState+=[self.state[-j+self.size-1]]+self.state[(j*4+self.size)*self.size+1:(j*4+self.size+3)*self.size-1]+[self.state[-j+6*self.size**2-1]]+self.state[j+(5*self.size-1)*self.size:j+(self.size+3)*self.size-1:-4*self.size]
                self.state=self.state[(self.size+3)*self.size-1:(5*self.size-1)*self.size:4*self.size]+self.state[self.size:self.size**2]+newState+self.state[5*self.size**2:(6*self.size-1)*self.size]+self.state[self.size**2:(5*self.size-4)*self.size+1:4*self.size]
            elif rotation=="m":
                for j in range(2, self.size):self.rotate(str(j)+"mr", 3)
            elif rotation=="e":
                for j in range(2, self.size):self.rotate(str(j)+"mu", 3)
            elif rotation=="s":
                for j in range(2, self.size):self.rotate(str(j)+"mf")
            elif rotation[-2:]=="mr":
                layer=2 if rotation[:-2]=="" else int(rotation[:-2])
                for j in range(self.size):newState+=self.state[j*self.size:(j+1)*self.size-layer]+[self.state[(j*4+self.size+2)*self.size-layer]]+self.state[(j+1)*self.size-layer+1:(j+1)*self.size]
                for j in range(self.size):newState+=self.state[(j*4+self.size)*self.size:(j*4+self.size+2)*self.size-layer]+[self.state[(j+5*self.size+1)*self.size-layer]]+self.state[(j*4+self.size+2)*self.size-layer+1:(j*4+self.size+3)*self.size+layer-1]+[self.state[(-j+self.size)*self.size-layer]]+self.state[(j*4+self.size+3)*self.size+layer:(j*4+self.size+4)*self.size]
                for j in range(self.size):newState+=self.state[(j+5*self.size)*self.size:(j+5*self.size+1)*self.size-layer]+[self.state[(-j*4+5*self.size-1)*self.size+layer-1]]+self.state[(j+5*self.size+1)*self.size-layer+1:(j+5*self.size+1)*self.size]
                self.state=newState
            elif rotation[-2:]=="mu":
                layer=2 if rotation[:-2]=="" else int(rotation[:-2])
                self.state=self.state[:(self.size+4*layer-4)*self.size]+self.state[(self.size+4*layer-3)*self.size:(self.size+4*layer)*self.size]+self.state[(self.size+4*layer-4)*self.size:(self.size+4*layer-3)*self.size]+self.state[(self.size+4*layer)*self.size:]
            elif rotation[-2:]=="mf":
                layer=2 if rotation[:-2]=="" else int(rotation[:-2])
                for j in range(self.size):newState+=self.state[(j*4+self.size)*self.size:(j*4+self.size+1)*self.size-layer]+[self.state[j+(5*self.size+layer-1)*self.size]]+self.state[(j*4+self.size+1)*self.size-layer+1:(j*4+self.size+2)*self.size+layer-1]+[self.state[j+(self.size-layer)*self.size]]+self.state[(j*4+self.size+2)*self.size+layer:(j*4+self.size+4)*self.size]
                self.state=self.state[:(self.size-layer)*self.size]+self.state[(5*self.size-3)*self.size-layer:(self.size+1)*self.size-layer-1:-4*self.size]+self.state[(self.size-layer+1)*self.size:self.size**2]+newState+self.state[5*self.size**2:(5*self.size+layer-1)*self.size]+self.state[(5*self.size-2)*self.size+layer-1:(self.size+2)*self.size+layer-2:-4*self.size]+self.state[(5*self.size+layer)*self.size:]
            elif rotation[-2:]=="ml":self.rotate(str(self.size-(2 if rotation[:-2]=="" else int(rotation[:-2]))+1)+"mr", 3)
            elif rotation[-2:]=="md":self.rotate(str(self.size-(2 if rotation[:-2]=="" else int(rotation[:-2]))+1)+"mu", 3)
            elif rotation[-2:]=="mb":self.rotate(str(self.size-(2 if rotation[:-2]=="" else int(rotation[:-2]))+1)+"mf", 3)
            elif rotation[-3:]=="mrw":
                for j in range(2, (2 if rotation[:-3]=="" else int(rotation[:-3]))+1):self.rotate(str(j)+"mr")
            elif rotation[-3:]=="muw":
                for j in range(2, (2 if rotation[:-3]=="" else int(rotation[:-3]))+1):self.rotate(str(j)+"mu")
            elif rotation[-3:]=="mfw":
                for j in range(2, (2 if rotation[:-3]=="" else int(rotation[:-3]))+1):self.rotate(str(j)+"mf")
            elif rotation[-3:]=="mlw":
                for j in range(self.size-(2 if rotation[:-3]=="" else int(rotation[:-3]))+1, self.size):self.rotate(str(j)+"mr", 3)
            elif rotation[-3:]=="mdw":
                for j in range(self.size-(2 if rotation[:-3]=="" else int(rotation[:-3]))+1, self.size):self.rotate(str(j)+"mu", 3)
            elif rotation[-3:]=="mbw":
                for j in range(self.size-(2 if rotation[:-3]=="" else int(rotation[:-3]))+1, self.size):self.rotate(str(j)+"mf", 3)
            elif rotation[-2:]=="rw":
                self.rotate("r")
                self.rotate(str(2 if rotation[:-2]=="" else int(rotation[:-2]))+"mrw")
            elif rotation[-2:]=="uw":
                self.rotate("u")
                self.rotate(str(2 if rotation[:-2]=="" else int(rotation[:-2]))+"muw")
            elif rotation[-2:]=="fw":
                self.rotate("f")
                self.rotate(str(2 if rotation[:-2]=="" else int(rotation[:-2]))+"mfw")
            elif rotation[-2:]=="lw":
                self.rotate("l")
                self.rotate(str(2 if rotation[:-2]=="" else int(rotation[:-2]))+"mlw")
            elif rotation[-2:]=="dw":
                self.rotate("d")
                self.rotate(str(2 if rotation[:-2]=="" else int(rotation[:-2]))+"mdw")
            elif rotation[-2:]=="bw":
                self.rotate("b")
                self.rotate(str(2 if rotation[:-2]=="" else int(rotation[:-2]))+"mbw")
            elif rotation=="x":
                self.rotate("r")
                self.rotate("m", 3)
                if self.size>1:self.rotate("l", 3)
            elif rotation=="y":
                self.rotate("u")
                self.rotate("e", 3)
                if self.size>1:self.rotate("d", 3)
            elif rotation=="z":
                self.rotate("f")
                self.rotate("s")
                if self.size>1:self.rotate("b", 3)
    def scramble(self):
        turnType, pTypes=0.5, [0.5]
        for i in range(15 if self.size==2 else 35 if self.size==3 else 40*self.size-100):
            while turnType in pTypes:turnType=random.randint(0, len(self.turnChoice)-1)
            if turnType%3!=pTypes[0]%3:pTypes=[turnType]
            else:pTypes+=[turnType]
            self.rotate(self.turnChoice[turnType], random.randint(1, 3))
    def display(self):
        for i in range(self.size):
            print(end="\n   "+"   "*self.size)
            for j in range(self.size):print(self.state[i*self.size+j], end="  ")
        print()
        for i in range(self.size):
            print(end="\n ")
            for j in range(4):
                for k in range(self.size):print(self.state[i*4*self.size+j*self.size+k+self.size**2], end="  ")
                print(end="  ")
        print()
        for i in range(self.size):
            print(end="\n   "+"   "*self.size)
            for j in range(self.size):print(self.state[i*self.size+j+5*self.size**2], end="  ")
while True:
    try:cube=Cube(int(input("\nInput cube size: ")))
    except ValueError:print("Please input an integer.")
    else:break
print("\nCube initialized:")
cube.display()
print("\n\nInput \"scramble\" to scramble the cube and \"reset\" to reset to a solved state.\nTurn input is not case sensitive.\nMultiple turns can be inputted at once separated by spaces.\n\nValid turns: "+("None." if cube.size<1 else "R, U, F, L, D, B, " if cube.size>1 else "")+("(n)Rw, (n)Uw, (n)Fw, (n)Lw, (n)Dw, (n)Bw, " if cube.size>2 else "")+("(n)MR(w), (n)MU(w), (n)MF(w), (n)ML(w), (n)MD(w), (n)MB(w), " if cube.size>3 else "")+("M, E, S, " if cube.size>2 else "")+("x, y, z. Cube notation can be searched up online." if cube.size>0 else "")+"\n\nSuffixes: 2 for double-turns, ' for counter-clockwise turns.\nUse \"quit\" or \"exit\" to terminate the program.")
while True:
    for i in input("\n\nInput turns: ").lower().split():
        if i=="quit" or i=="exit":quit()
        elif i=="reset":
            cube.reset()
            print("\nCube resetted to solved state")
        elif i=="scramble":
            cube.scramble()
            print("\nCube scrambled")
        else:
            try:
                if (i[:-1] if i[-1]=="'" or i[-1]=="2" else i) in ([] if cube.size<1 else ["x", "y", "z"]+(["r", "u", "f", "l", "d", "b"] if cube.size>1 else [])+(["rw", "uw", "fw", "lw", "dw", "bw", "m", "e", "s"] if cube.size>2 else [])+(["mr", "mu", "mf", "ml", "md", "mb", "mrw", "muw", "mfw", "mlw", "mdw", "mbw"] if cube.size>3 else [])) or cube.size>3 and ((i[-4:] if i[-1]=="'" or i[-1]=="2" else i[-3:]) in ["mrw", "muw", "mfw", "mlw", "mdw", "mbw"] and 1<int(i[:-4] if i[-1]=="'" or i[-1]=="2" else i[:-3])<cube.size or (i[-3:] if i[-1]=="'" or i[-1]=="2" else i[-2:]) in ["rw", "uw", "fw", "lw", "dw", "bw", "mr", "mu", "mf", "ml", "md", "mb"] and 1<int(i[:-3] if i[-1]=="'" or i[-1]=="2" else i[:-2])<cube.size):cube.rotate(i[:-1] if i[-1]=="'" or i[-1]=="2" else i, 2 if i[-1]=="2" else 3 if i[-1]=="'" else 1)
            except ValueError:print("\nPlease input a valid turn.")
    cube.display()