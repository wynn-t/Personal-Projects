import __main__
import random
def unique(l):
    l=list(l)
    for i in range(len(l)-1, -1, -1):
        if l[i] in l[:i]:l.pop(i)
    return l
class Board:
    def __init__(self):
        self.state=[0]*42
        self.turn=len(self.state)-self.state.count(0)
    def initTree(self):return {"state":self.state, "turn":self.turn, "eval":0}
    def enumerateMoves(self, state, turn, reasonable=True):
        if self.winDetection(state)!=0:return {}
        if not reasonable:return {i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":[0, 1, -1][self.winDetection(self.applyMove(state, turn, i))]} for i in range(7) if state[i]==0}
        result={i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":[0, 1, -1][self.winDetection(self.applyMove(state, turn, i))]} for i in range(7) if state[i]==0 and self.winDetection(self.applyMove(state, turn, i))==turn%2+1}
        if len(result)==0:result={i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":0} for i in range(7) if state[i]==0 and self.winDetection(self.applyMove(state, turn+1, i))==(turn+1)%2+1}
        if len(result)==0:
            for i in range(7):
                if state[i]==0:temp=self.applyMove(state, turn, i)
                if state[i]==0 and (temp[i]!=0 or temp[i]==0 and self.winDetection(self.applyMove(temp, turn+1, i))!=(turn+1)%2+1):
                    temp2=False
                    for j in range(5):
                        if state[j*7+i]==0 and state[j*7+i+7]==0 and self.winDetection(state[:j*7+i]+[turn%2+1]+state[j*7+i+1:])==turn%2+1 and self.winDetection(state[:j*7+i+7]+[turn%2+1]+state[j*7+i+8:])==turn%2+1:
                            result[i], temp2={"state":temp, "turn":turn+1, "eval":1 if turn%2==0 else -1}, True
                            break
                    if temp2:
                        for j in dict(result):
                            if j not in ["state", "turn", "eval", i]:result.pop(j)
                        break
                    result[i], count={"state":temp, "turn":turn+1, "eval":0}, 0
                    for j in range(7):
                        if temp[j]==0 and self.winDetection(self.applyMove(temp, turn, j))==turn%2+1:count+=1
                    if count>1:result[i]["eval"]=1 if turn%2==0 else -1
                    for j in range(len(temp)-7):
                        if temp[j]==0 and temp[j+7]==0 and self.winDetection(temp[:j]+[turn%2+1]+temp[j+1:])==turn%2+1 and self.winDetection(temp[:j+7]+[turn%2+1]+temp[j+8:])==turn%2+1:
                            result[i]["eval"]=1 if turn%2==0 else -1
                            break
        if len(result)==0:result={i:{"state":self.applyMove(state, turn, i), "turn":turn+1, "eval":0} for i in range(7) if state[i]==0}
        return result
    def randomMove(self, state, turn):return random.choice(list(self.enumerateMoves(state, turn, False)))
    def applyMove(self, state, turn, move):
        state=list(state)
        state[max([i for i in range(move, len(state), 7) if state[i]==0])]=turn%2+1
        return state
    def winDetection(self, state):
        for i in range(len(state)):
            if (i<21 and len(unique(state[i:i+22:7]))==1 or i%7<4 and len(unique(state[i:i+4]))==1 or i<18 and i%7<4 and len(unique(state[i:i+25:8]))==1 or i<21 and i%7>2 and len(unique(state[i:i+19:6]))==1) and state[i]!=0:return state[i]
        return 0
    def eval(self, branch, ownTurn):
        if branch["eval"]!=0:return branch["eval"]
        evals, temp=[branch[i]["eval"] for i in branch if i not in ["state", "turn", "eval"]], 1 if branch["turn"]%2==0 else -1
        if ownTurn:return [max, max, min][temp](evals)
        else:return temp if temp in evals else sum(evals)/len(evals)
    def display(self):
        print()
        for i in range(7):print(end=f" {i} "+("\n\n" if i==6 else "|"))
        for i in range(6):
            for j in range(7):print(end=f" {' 12'[self.state[7*i+j]]} "+("\n" if j==6 else "|"))
            if i!=5:print("---+"*6+"---")
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
                difficulty, slots=6, self.state[:7].count(0)
                move=__main__.compute(difficulty if difficulty<6 else 5 if self.turn<15 else 6 if self.turn<25 else 7 if slots>5 else 8 if slots==5 else 9 if slots==4 else 12)
                print("Computer played:", move)
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
