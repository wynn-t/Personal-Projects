import random
import connect4 as game
#import tictactoe as game
board=game.Board()
def compute(depth):
    global cache
    global initDepth
    tree, cache, initDepth=board.initTree(), {}, depth
    if depth<1:return board.randomMove(tree["state"], tree["turn"])
    search(depth, tree)
    #print("\nCache:", cache)
    #print("\nTree:", tree)
    print("\nEval:", tree["eval"])
    print("\nBranch evals:", {i:tree[i]["eval"] for i in tree if i not in ["state", "turn", "eval"]})
    return random.choice([i for i in tree if i not in ["state", "turn", "eval"] if tree[i]["eval"]==tree["eval"]])
def search(depth, node):
    state=tuple(node["state"])
    if state not in cache:
        node.update(board.enumerateMoves(node["state"], node["turn"], evaluation=node["eval"]))
        if depth>1:
            for i in node:
                if i not in ["state", "turn", "eval"]:node[i]=search(depth-1, node[i])
        if len(node)>3:node["eval"]=board.eval(node, (initDepth-depth)%2==0)
        cache[state]={i:node[i] for i in ["state", "turn", "eval"]}
    return cache[state]
board.play()