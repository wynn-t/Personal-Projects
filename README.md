Some files in this repository require the Pygame module, run "pip install pygame" to install it.

esoLang.py - My interpreter for Brainf**k, including an attempt at providing a general framework for an esoteric programming language interpreter.
fileNamer.java - The automatic file namer/class renaming tool I wrote to help with assignments in APCSA class, incorporating several safety features. Shared with friends so they may benefit from it.
sorting.py - A showcase of my thought process, when I was deriving Insertion Sort and Merge Sort more than 2 years ago.

The following files require the Pygame module:
connect4.py - Contains the game mechanics for connect 4. Run this to play a human vs human game.
DFS.py - Contains the Depth-First Search algorithm which I wrote to play strategy games, as a significant optimization to the Breadth-First Search algorithm I wrote in tree_search.py by allowing transposition tables. Currently requires either connect4.py or tictactoe.py to run properly.
Rubiks_Cube.py - The CPT I submitted for APCSP. Features state vectors representing rotations and a random move scrambler. The basis of my virtual Rubik's cube on Desmos.
tictactoe.py - Contains the game mechanics for tictactoe. Run this to play a human vs human game.
tree_search.py - Contains my original Breadth-First Search derivation that solved the NYT Connections question, with some modifications made so that it would be compatible with connect4.py and tictactoe.py. Currently requires either connect4.py or tictactoe.py to run properly.