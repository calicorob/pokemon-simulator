import random 
import math

from pokemon.objects.Status import Poison,Burn
from pokemon.objects.Pokemon import Pokemon


def battles(pokemons,numBattles=100):
    score = {pokemons[0][0]:0,pokemons[1][0]:0}
    
    for i in range(numBattles):
        pokemon = []
        for i,tup in enumerate(pokemons):
            pokemon.append(Pokemon(tup[0],tup[1]))
        
            for move in tup[2]:
                pokemon[i].setMove(move)
        
        winner = battle(pokemon)
        score[winner] += 1
        
        
    for key in score.keys():
        p = score[key]/numBattles
        score[key] = [p,math.sqrt(p*(1-p)/numBattles)]
        
        
    return score

def battle(pokemons,verbose=False):
    """
        pokemons: list of pokemon to do battle
    
    """
    
    
    def getOrder(pokemons):
    
        if pokemons[0].getSpeed() != pokemons[1].getSpeed():
            lst = sorted(pokemons,key=lambda x: x.getSpeed())
        else:
            lst = [random.choice(pokemons)]
            if pokemons[0] not in lst:
                lst.append(pokemons[0])
            else:
                lst.append(pokemons[1])
                
        return lst
    
    def isBattleOver(pokemons):
        for pokemon in pokemons:
            if pokemon.battleStats['HP'] <= 0:
                return True
        return False
    
    
    
    for pokemon in pokemons:
        pokemon.setBattleStats()
        
    health = {pokemons[0]:[pokemons[0].battleStats['HP']],pokemons[1]:[pokemons[1].battleStats['HP']]}
    
    while True:
        order = getOrder(pokemons)
        
        firstToGo = order.pop()
        secondToGo = order.pop()
        
        firstToGo.attack(secondToGo,random.choice(list(firstToGo.moves))) ## this is stupid as hell will change later but lazy now
        
        if isBattleOver(pokemons):
                health[pokemons[0]].append(pokemons[0].battleStats['HP'])
                health[pokemons[1]].append(pokemons[1].battleStats['HP'])
                break
                
        if isinstance(firstToGo.status,(Poison,Burn)):
            firstToGo.status.doDamage(firstToGo)
        
        if isBattleOver(pokemons):
                health[pokemons[0]].append(pokemons[0].battleStats['HP'])
                health[pokemons[1]].append(pokemons[1].battleStats['HP'])
                break
                
        secondToGo.attack(firstToGo,random.choice(list(secondToGo.moves))) ## this is stupid as hell will change later but lazy now
        
        if isBattleOver(pokemons):
                health[pokemons[0]].append(pokemons[0].battleStats['HP'])
                health[pokemons[1]].append(pokemons[1].battleStats['HP'])
                break
                
        if isinstance(secondToGo.status,(Poison,Burn)):
            secondToGo.status.doDamage(secondToGo)
        
        if isBattleOver(pokemons):
                health[pokemons[0]].append(pokemons[0].battleStats['HP'])
                health[pokemons[1]].append(pokemons[1].battleStats['HP'])
                break
                
        health[pokemons[0]].append(pokemons[0].battleStats['HP'])
        health[pokemons[1]].append(pokemons[1].battleStats['HP'])
                
    if health[pokemons[0]][-1] > health[pokemons[1]][-1]:
        
        return pokemons[0].name
    else:
        return pokemons[1].name
    #return health      
            
    
    