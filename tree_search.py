import random
import tictactoe as game
board=game.Board()
def compute(depth):
    tree=board.initTree()
    branches=[tree]
    for i in range(depth):
        for j in branches:j.update(board.enumerateMoves(j["state"], j["turn"]))
        branches=[j[k] for j in branches for k in j if k not in ["state", "turn", "eval"]]
    for i in range(depth-1, -1, -1):
        branches=[tree]
        for j in range(i):branches=[j[k] for j in branches for k in j if k not in ["state", "turn", "eval"]]
        for j in branches:
            if len(j)>3:j["eval"]=board.eval(j, i%2==0)
    #print(f"\n{tree["eval"]}")
    return random.choice([i for i in tree if i not in ["state", "turn", "eval"] if tree[i]["eval"]==tree["eval"]])
humanPlayer=-1
while humanPlayer not in [1, 2]:
    try:humanPlayer=int(input("Input player (1/2): "))
    except ValueError:print("Please input a number.")
    else:
        if humanPlayer not in [1, 2]:print("Please input either 1 or 2.")
board.play(humanPlayer)
