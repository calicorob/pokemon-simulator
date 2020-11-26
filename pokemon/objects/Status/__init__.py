import random
import math

class Status(object):
    def __init__(self):
        self.threshold = 1
        
    def canMove(self):
        rand = random.random()
        
        if rand <= self.threshold:
            return True ## can move
        else:
            return False ## can't move

class Poison(Status):
    def __init__(self,pokemon):
        self.damage = math.floor(pokemon.stats['HP'] / 16)
        if self.damage < 1:
            self.damage = 1
        
    def doDamage(self,pokemon):
        pokemon.receiveDamage(self.damage)
        
class Paralysis(Status):
    def __init__(self,pokemon):
        pokemon.battleStats['Speed'][0] = math.floor(pokemon.stats['Speed'] * 0.75)
        self.threshold = 0.75
        
            

class Burn(Status):
    def __init__(self,pokemon):
        self.damage = math.floor(pokemon.stats['HP'] / 16)
        if self.damage < 1:
            self.damage = 1
        self.threshold = 1
    
        pokemon.battleStats['Attack'][0] = math.floor(pokemon.stats['Attack'] * 0.5)
        
    def doDamage(self,pokemon):
        #print('Burn does' + str(self.damage) + 'damage')
        pokemon.receiveDamage(self.damage)

class Frozen(Status):
    def __init__(self):
        self.threshold = 0

class Normal(Status):
    pass

class Asleep(object):
    def __init__(self):
        self.turns = random.randint(1,7)