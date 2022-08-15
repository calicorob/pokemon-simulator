# library imports
from dataclasses import dataclass, field
from typing import Dict, Callable
from os.path import dirname,realpath
from pathlib import Path
import json 
import random
import math

__all__ = ['Pokemon']


PokemonStat = Dict[str,int] # TODO: move somewhere else?
categories = ['attack','defense','speed','special']

file_path = Path(dirname(realpath(__file__)))
data_path = file_path/'..'/'..'/'data'
pokemon_data_path = data_path/"pokemon.json"  # TODO: remove magic string?


def get_pokemon_data()->Dict[str,Dict]:
    with open(file=pokemon_data_path,mode='r') as file:
        data = json.load(file)
    return data

def generate_individual_values()->PokemonStat:
    health = ""
    individual_values = dict()
    for cat in categories:
        individual_values[cat] = random.choice(range(16)) # TODO: remove magic number
        health = health +  '{0:b}'.format(individual_values[cat])[-1]
    individual_values['health'] = int(health,2)
    return individual_values

def non_health_stat_equation(level:int, base_stat:int,individual_value:int)->int:
    return math.floor((base_stat + individual_value)*2*level/100 + 5)

def health_stat_equation(level:int, base_stat:int,individual_value:int)->int:
    return math.floor((base_stat + individual_value)*2 *level/100 + level+10)


def generate_stats(level:int,base_stats:PokemonStat,individual_values:PokemonStat,non_health_stat_equation:Callable,health_stat_equation:Callable)->PokemonStat:
    
    _categories = categories + ['health']
    return {
        cat: non_health_stat_equation(level=level,base_stat = base_stats[cat],individual_value = individual_values[cat])
    if cat !='health' else health_stat_equation(level=level,base_stat = base_stats[cat],individual_value = individual_values[cat]) for cat in _categories }


pokemon_data = get_pokemon_data()

@dataclass
class Pokemon:
    name : str
    level : int
    type : str = field(init=False)
    base_stats : PokemonStat = field(init=False)
    individual_values : PokemonStat = field(init=False)
    stats: PokemonStat = field(init=False)

    def __post_init__(self)->None:

        if not self.level >= 1:
            raise ValueError("Input level must be greater than 0.")
        self.name = self.name.lower()
        try:
            self.type = pokemon_data[self.name]['type']
            self.base_stats = pokemon_data[self.name]['base stats']
        except KeyError:
            raise KeyError("")

        self.individual_values = generate_individual_values()
        self.stats = generate_stats(level=self.level,base_stats=self.base_stats,individual_values=self.individual_values,health_stat_equation=health_stat_equation,non_health_stat_equation=non_health_stat_equation)

if __name__ == '__main__':
    
    pikachu = Pokemon(name='pikachu',level=20)



    print(pikachu)
    # print(file_path)
    # print(data_path)
    # print(get_pokemon_data())

    
    pass