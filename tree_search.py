import random
import connect4 as game
#import tictactoe as game
board=game.Board()
def compute(depth):
    tree=board.initTree()
    if depth<1:return board.randomMove(tree["state"], tree["turn"])
    branches=(tree,)
    for i in range(depth):
        for j in branches:j.update(board.enumerateMoves(j["state"], j["turn"], evaluation=j["eval"][0]))
        branches=tuple(j[k] for j in branches for k in j if k not in ("state", "turn", "eval"))
    for i in range(depth-1, -1, -1):
        branches=(tree,)
        for j in range(i):branches=tuple(j[k] for j in branches for k in j if k not in ("state", "turn", "eval"))
        for j in branches:
            if len(j)>3:
                for k in j:
                    if k not in ("state", "turn", "eval"):j[k]=j[k]["eval"]
                j["eval"]=board.eval(j, i%2==0)
    print("\nEval:", tree["eval"])
    print("\nMove evals:", {i:tree[i] for i in tree if i not in ("state", "turn", "eval")})
    return random.choice(tuple(i for i in tree if i not in ("state", "turn", "eval") if tree[i][0]==tree["eval"][0]-1 and tree[i][1]==tree["eval"][1])) if tree["eval"][1]==tree["turn"]%2+1 else random.choice(tuple(i for i in tree if i not in ("state", "turn", "eval") if tree[i]==tree["eval"]))
board.play()