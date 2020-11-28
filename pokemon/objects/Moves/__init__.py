import random
import math

from pokemon.data import MOVES as moves
from pokemon.objects.Status import Paralysis, Burn



class Move(object):
    def __init__(self,name):
        self.name = name
        
        self.type = moves[name]['Type']
        self.category = moves[name]['Category']
        self.accuracy = moves[name]['Accuracy']
        self.PP = moves[name]['PP']
        self.priority = moves[name]['Priority']
        
        
class NormalMove(Move):
    def __init__(self,name):
        super().__init__(name)
        self.power = moves[name]['Power']
        self.critRatio = moves[name]['CritRatio']
        
class PhysicalMove(Move):
    def __init__(self,name):
        super().__init__(name)
        self.power = moves[name]['Power']
        self.critRatio = moves[name]['CritRatio']
        
class SpecialMove(Move):
    def __init__(self,name):
        super().__init__(name)
        self.power = moves[name]['Power']
        self.critRatio = moves[name]['CritRatio']
                
class ParalyzingMove(Move):
    def __init__(self,name):
        super().__init__(name)
        self.power = moves[name]['Power']
        self.critRatio = moves[name]['CritRatio']
        self.chance = moves[name]['Chance']
        
        
    def doesParalyze(self):
        threshold = self.chance
        
        rand = random.random()
        
        if rand > threshold:
            return False ## doesn't paralyze
        else:
            return True ## paralyzes
        
        
    def paralyze(self,pokemon):
        pokemon.status = Paralysis(pokemon)
        
class BurnMove(Move):
    def __init__(self,name):
        super().__init__(name)
        self.power = moves[name]['Power']
        self.critRatio = moves[name]['CritRatio']
        self.chance = moves[name]['Chance']
        
    def doesBurn(self):
        threshold = self.chance
        rand = random.random()
        
        if rand > threshold:
            return False ## doesn't burn
        else:
            return True
        
    def burn(self,pokemon):
        pokemon.status = Burn(pokemon)
        

class StatusMove(Move):
    def __init__(self,name):
        super().__init__(name)
        self.affects = moves[name]['Affects']
        self.stages = moves[name]['Stages']
        self.target = moves[name]['Target']
        
def makeMove(name):
    
    cat = moves[name]['Category']
    
    try:
        aff = moves[name]['Affliction']
    except KeyError:
        aff = None
        
    if aff:
        if aff == 'Burn':
            return BurnMove(name)
        elif aff == 'Paralysis':
            return ParalyzingMove(name)
        
    else:
        
        if cat == 'Physical' or cat == 'Special':
            return NormalMove(name)
        else:
            return StatusMove(name)
