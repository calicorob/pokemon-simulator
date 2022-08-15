# library imports
from dataclasses import dataclass, field
from typing import Dict
from os.path import dirname,realpath
from pathlib import Path
import json 

__all__ = ['Pokemon']


PokemonStat = Dict[str,int] # TODO: move somewhere else?


file_path = Path(dirname(realpath(__file__)))
data_path = file_path/'..'/'..'/'data'
pokemon_data_path = data_path/"pokemon.json"  # TODO: remove magic string?


def get_pokemon_data()->Dict[str,Dict]:
    with open(file=pokemon_data_path,mode='r') as file:
        data = json.load(file)
    return data

pokemon_data = get_pokemon_data()

@dataclass
class Pokemon:
    name : str
    level : int
    type : str = field(init=False)
    base_stats : PokemonStat = field(init=False)

    def __post_init__(self)->None:

        if not self.level >= 1:
            raise ValueError("Input level must be greater than 0.")
        self.name = self.name.lower()
        try:
            self.type = pokemon_data[self.name]['type']
            self.base_stats = pokemon_data[self.name]['base stats']
        except KeyError:
            raise KeyError("")

if __name__ == '__main__':
    
    pikachu = Pokemon(name='pikachu',level=1)



    print(pikachu)
    # print(file_path)
    # print(data_path)
    # print(get_pokemon_data())

    
    pass