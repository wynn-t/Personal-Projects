import random
import connect4 as game
#import tictactoe as game
board=game.Board()
def compute(depth):
    tree=board.initTree()
    if depth<1:return board.randomMove(tree["state"], tree["turn"])
    branches=[tree]
    for i in range(depth):
        for j in branches:
            if j["eval"]==0:j.update(board.enumerateMoves(j["state"], j["turn"]))
        branches=[j[k] for j in branches for k in j if k not in ["state", "turn", "eval"]]
    for i in range(depth-1, -1, -1):
        branches=[tree]
        for j in range(i):branches=[j[k] for j in branches for k in j if k not in ["state", "turn", "eval"]]
        for j in branches:
            if len(j)>3:j["eval"]=board.eval(j, i%2==0)
    #print("\nTree:", tree)
    #print("\nEval:", tree["eval"])
    #print("\nBranch evals:", [tree[i]["eval"] for i in tree if i not in ["state", "turn", "eval"]])
    return random.choice([i for i in tree if i not in ["state", "turn", "eval"] if tree[i]["eval"]==tree["eval"]])
board.play()
