"""
    Holds the Pokemon stat, Pokemon move and Pokemon type data
    Author: Robert Currie
    Date: January 17, 2021
"""

import json ## for data loading

## pokemon stat data
with open(r"pokemon/data/pokemon.json") as file:
    POKEMON = json.load(file)
## pokemon move data
with open(r"pokemon/data/moves.json") as file:
    MOVES = json.load(file)
## pokemon types data
with open(r"pokemon/data/types.json") as file:
    TYPES = json.load(file)

## for super / not effective
TYPEMULTIPLIER = {-2:0.25,-1:0.5,0:1,1:2,2:4}
## for stat changes
STATSMULTIPLIER = {-6:0.25,-5:0.28,-4:0.33,-3:0.4,-2:0.5,-1:0.66,0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}
