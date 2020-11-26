import json

with open(r"pokemon/data/pokemon.json") as file:
    POKEMON = json.load(file)
    
with open(r"pokemon/data/moves.json") as file:
    MOVES = json.load(file)

with open(r"pokemon/data/types.json") as file:
    TYPES = json.load(file)
    
## for super / not effective 
TYPEMULTIPLIER = {-2:0.25,-1:0.5,0:1,1:2,2:4}
## for stat changes
STATSMULTIPLIER = {-6:0.25,-5:0.28,-4:0.33,-3:0.4,-2:0.5,-1:0.66,0:1,1:1.5,2:2,3:2.5,4:3,5:3.5,6:4}