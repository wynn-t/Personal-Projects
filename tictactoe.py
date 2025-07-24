import __main__
import random
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
    def display(self):
        print()
        for i in range(3):
            for j in range(3):print(end=f" {[3*i+j, 'X', 'O'][self.state[3*i+j]]} {'||\n'[j]}")
            if i!=2:print("---+---+---")
        print("\n")
    def play(self, humanPlayer=1):
        if __name__=="__main__" or humanPlayer==1:self.display()
        for i in range(self.state.count(0)):
            if __name__=="__main__" or self.turn%2+1==humanPlayer:
                move=-1
                while move not in self.enumerateMoves(self.state, self.turn, False):
                    try:move=int(input("Select a move by entering the corresponding number: "))
                    except ValueError:print("Please input an integer.")
                    else:
                        if move not in self.enumerateMoves(self.state, self.turn, False):print("Please select an available move.")
            else:
                move=__main__.compute(self.state.count(0))
                print("\nComputer played:", move)
            self.state=self.applyMove(self.state, self.turn, move)
            self.turn+=1
            if __name__=="__main__" or self.turn%2+1==humanPlayer or self.turn==len(self.state) or self.winDetection(self.state)!=0:self.display()
            if self.winDetection(self.state)!=0:
                if __name__=="__main__":print(f"Player {self.winDetection(self.state)} wins!\n")
                elif self.winDetection(self.state)==humanPlayer:print("The player wins!\n")
                else:print("The computer wins!\n")
                break
        else:print("It's a tie.\n")
if __name__=="__main__":
    board=Board()
    board.play()
