import __main__, random, pygame
from pygame.locals import *
pygame.init()
screen=pygame.display.set_mode((300, 350))
def unique(l):
    l=list(l)
    for i in range(len(l)-1, -1, -1):
        if l[i] in l[:i]:l.pop(i)
    return l
class Board:
    def __init__(self):
        self.state=[0]*9
        self.turn=len(self.state)-self.state.count(0)
    def initTree(self):return {"state":self.state, "turn":self.turn, "eval":0}
    def enumerateMoves(self, state, turn, reasonable=True):
        if self.winDetection(state)!=0:return {}
        if not reasonable:return {i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":[0, 1, -1][self.winDetection(self.applyMove(state, turn, i))]} for i in range(len(state)) if state[i]==0}
        result={i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":[0, 1, -1][self.winDetection(self.applyMove(state, turn, i))]} for i in range(len(state)) if state[i]==0 and self.winDetection(self.applyMove(state, turn, i))==turn%2+1}
        if len(result)==0:result={i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":0} for i in range(len(state)) if state[i]==0 and self.winDetection(self.applyMove(state, turn+1, i))==(turn+1)%2+1}
        if len(result)==0:result={i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":0} for i in range(len(state)) if state[i]==0}
        return result
    def randomMove(self, state, turn):return random.choice(list(self.enumerateMoves(state, turn, False)))
    def applyMove(self, state, turn, move):
        state=list(state)
        state[move]=turn%2+1
        return state
    def winDetection(self, state):
        for i in range(len(state)):
            if (i<3 and len(unique(state[i:i+7:3]))==1 or i%3==0 and len(unique(state[i:i+3]))==1 or i==0 and len(unique(state[i:i+9:4]))==1 or i==2 and len(unique(state[i:i+5:2]))==1) and state[i]!=0:return state[i]
        return 0
    def eval(self, branch, ownTurn):
        evals, temp=[branch[i]["eval"] for i in branch if i not in ["state", "turn", "eval"]], 1 if branch["turn"]%2==0 else -1
        if ownTurn:return [max, max, min][temp](evals)
        else:return temp if temp in evals else sum(evals)/len(evals)
    def display(self, window, humanPlayer=1):
        window.fill((0, 0, 0))
        window.blit(pygame.font.Font(None, 20).render((f"Player {self.winDetection(self.state)} wins!" if __name__=="__main__" else "The player wins!" if self.winDetection(self.state)==humanPlayer else "The computer wins!") if self.winDetection(self.state)!=0 else "It's a tie." if 0 not in self.state else "Click on a square to play in that square.", True, (255, 255, 255)), (25, 15))
        for i in range(2):
            pygame.draw.rect(window, (255, 255, 255), (100*i+95, 50, 10, 300))
            pygame.draw.rect(window, (255, 255, 255), (0, 100*i+145, 300, 10))
        for i in range(len(self.state)):
            if self.state[i]==1:
                pygame.draw.polygon(window, (255, 255, 255), ((i%3*100+25, i//3*100+70), (i%3*100+20, i//3*100+75), (i%3*100+75, i//3*100+130), (i%3*100+80, i//3*100+125)))
                pygame.draw.polygon(window, (255, 255, 255), ((i%3*100+75, i//3*100+70), (i%3*100+80, i//3*100+75), (i%3*100+25, i//3*100+130), (i%3*100+20, i//3*100+125)))
            elif self.state[i]==2:pygame.draw.circle(window, (255, 255, 255), (i%3*100+50, i//3*100+100), 35, 7)
        pygame.display.update()
    def play(self, humanPlayer=1):
        print()
        self.display(screen, humanPlayer)
        while True:
            move=-1
            for event in pygame.event.get():
                if event.type==QUIT or event.type==KEYUP and event.key==K_ESCAPE:
                    pygame.quit()
                    quit()
                if event.type==MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] and (__name__=="__main__" or self.turn%2+1==humanPlayer) and event.pos[1]>=50:move=event.pos[0]//100+(event.pos[1]-50)//100*3
            if self.winDetection(self.state)==0 and 0 in self.state:
                if self.winDetection(self.state)==0 and __name__!="__main__" and self.turn%2+1!=humanPlayer:
                    move=__main__.compute(self.state.count(0))
                    print("\nComputer played:", move, "\n")
                if move in self.enumerateMoves(self.state, self.turn, False):
                    self.state=self.applyMove(self.state, self.turn, move)
                    self.turn+=1
            self.display(screen, humanPlayer)
if __name__=="__main__":
    board=Board()
    board.play()
