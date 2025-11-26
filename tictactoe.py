import __main__, random, pygame
from pygame.locals import *
def row(l):
    for i in l:
        if i!=l[0]:return False
    return True
class Board:
    def __init__(self):
        self.state=[0]*9
        self.turn=len(self.state)-self.state.count(0)
    def initTree(self):return {"state":self.state, "turn":self.turn, "eval":0}
    def enumerateMoves(self, state, turn, reasonable=True, *, evaluation=0):
        if evaluation!=0 or self.winDetection(state)!=0:return {}
        if not reasonable:return {i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":0} for i in range(len(state)) if state[i]==0}
        result={i:{"state":temp, "turn":turn+1, "eval":[0, 1, -1][turn%2+1]} for i in range(len(state)) if state[i]==0 and self.winDetection(temp:=self.applyMove(state, turn, i))==turn%2+1}
        if len(result)==0:result={i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":0} for i in range(len(state)) if state[i]==0 and self.winDetection(self.applyMove(state, turn+1, i))==(turn+1)%2+1}
        if len(result)==0:result={i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":0} for i in range(len(state)) if state[i]==0}
        return result
    def randomMove(self, state, turn):return random.choice(list(self.enumerateMoves(state, turn, False)))
    def applyMove(self, state, turn, move):
        state=list(state)
        state[move]=turn%2+1
        return state
    def winDetection(self, state):
        for i in list(range(4))+[6]:
            if (i<3 and row(state[i:i+7:3]) or i%3==0 and row(state[i:i+3]) or i==0 and row(state[i:i+9:4]) or i==2 and row(state[i:i+5:2])) and state[i]!=0:return state[i]
        return 0
    def eval(self, branch, ownTurn):
        evals, temp=[branch[i]["eval"] for i in branch if i not in ["state", "turn", "eval"]], [1, -1][branch["turn"]%2]
        if ownTurn:return [max, max, min][temp](evals)
        else:return temp if temp in evals else sum(evals)/len(evals)
    def display(self, window, humanPlayer=1):
        window.fill((0, 0, 0))
        if status=="player":
            window.blit(pygame.font.Font(None, 50).render("Player: "+textInput, True, (255, 255, 255)), (40, 150))
            if invalidInput:window.blit(pygame.font.Font(None, 20).render("Please input either 1 or 2.", True, (255, 0, 0)), (42, 190))
        else:
            temp=self.winDetection(self.state)
            window.blit(pygame.font.Font(None, 20).render((f"{'Player' if humanPlayer!=0 else 'Computer'} {temp} wins!" if __name__=="__main__" else "The player wins!" if temp==humanPlayer else "The computer wins!") if temp!=0 else "It's a tie." if 0 not in self.state else "Click on a square to play in that square." if humanPlayer!=0 else "", True, (255, 255, 255)), (25, 15))
            for i in range(2):
                pygame.draw.rect(window, (255, 255, 255), (100*i+95, 50, 10, 300))
                pygame.draw.rect(window, (255, 255, 255), (0, 100*i+145, 300, 10))
            for i in range(len(self.state)):
                if self.state[i]==1:
                    pygame.draw.polygon(window, (255, 255, 255), ((i%3*100+25, i//3*100+70), (i%3*100+20, i//3*100+75), (i%3*100+75, i//3*100+130), (i%3*100+80, i//3*100+125)))
                    pygame.draw.polygon(window, (255, 255, 255), ((i%3*100+75, i//3*100+70), (i%3*100+80, i//3*100+75), (i%3*100+25, i//3*100+130), (i%3*100+20, i//3*100+125)))
                elif self.state[i]==2:pygame.draw.circle(window, (255, 255, 255), (i%3*100+50, i//3*100+100), 35, 7)
        pygame.display.update()
    def play(self):
        pygame.init()
        self.__init__()
        global screen, textInput, status, invalidInput
        screen, textInput, status, invalidInput, humanPlayer=pygame.display.set_mode((300, 350)), "", "player" if __name__!="__main__" else "playing", False, -1
        print()
        self.display(screen, humanPlayer)
        while True:
            move=-1
            for event in pygame.event.get():
                if event.type==QUIT or event.type==KEYUP and event.key==K_ESCAPE:
                    pygame.quit()
                    return
                elif event.type==MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and status=="playing" and (__name__=="__main__" or self.turn%2+1==humanPlayer) and event.pos[1]>=50 and 5<=event.pos[0]%100<=95 and 5<=(event.pos[1]-50)%100<=95:move=event.pos[0]//100+(event.pos[1]-50)//100*3
                elif event.type==KEYDOWN:
                    if event.key==K_RETURN:
                        if textInput=="" or status=="player" and int(textInput) not in range(3):invalidInput=True
                        elif status=="player":
                            humanPlayer, status=int(textInput), "playing"
                            self.display(screen, humanPlayer)
                    elif event.key==K_BACKSPACE:textInput, invalidInput=textInput[:-1], False
                    elif pygame.key.name(event.key).isnumeric():
                        if invalidInput:textInput=""
                        textInput+=pygame.key.name(event.key)
                        invalidInput=False
            if status=="playing" and self.winDetection(self.state)==0 and 0 in self.state:
                if __name__!="__main__" and self.turn%2+1!=humanPlayer:
                    move=__main__.compute(self.state.count(0))
                    print("\nComputer played:", move, "\n")
                if move in self.enumerateMoves(self.state, self.turn, False):
                    self.state=self.applyMove(self.state, self.turn, move)
                    self.turn+=1
            self.display(screen, humanPlayer)
if __name__=="__main__":Board().play()
