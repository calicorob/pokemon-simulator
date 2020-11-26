import json

with open(r"pokemon/data/pokemon.json") as file:
    POKEMON = json.load(file)
    
with open(r"pokemon/data/moves.json") as file:
    MOVES = json.load(file)

with open(r"pokemon/data/types.json") as file:
    TYPES = json.load(file)