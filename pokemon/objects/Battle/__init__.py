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


def battle(pokemons):
    for pokemon in pokemons:
        pokemon.setBattleStats()
        
    pokemon_one = pokemons[0]
    pokemon_two = pokemons[1]
    
    health = {pokemon_one:[pokemon_one.battleStats['HP']],pokemon_two:[pokemon_two.battleStats['HP']]}
    
    while True:
        moves = pick_move(pokemons)
        order = pick_order(pokemons,moves)
        
        first_pokemon = order.pop()
        second_pokemon = order.pop()
        
        
        first_pokemon.attack(second_pokemon,moves[first_pokemon].name) ## this is stupid as hell, should pass the move object, not the move name
        
        
        if is_battle_over(pokemons):
                health[pokemon_one].append(pokemon_one.battleStats['HP'])
                health[pokemon_two].append(pokemon_two.battleStats['HP'])
                break
                
        if isinstance(first_pokemon.status,(Poison,Burn)):
            first_pokemon.status.doDamage(first_pokemon)
            
        if is_battle_over(pokemons):
                health[pokemon_one].append(pokemon_one.battleStats['HP'])
                health[pokemon_two].append(pokemon_two.battleStats['HP'])
                break
                
        second_pokemon.attack(first_pokemon,moves[second_pokemon].name) ## this is stupid as hell, should pass the move object, not the move name
        
        
        if is_battle_over(pokemons):
                health[pokemon_one].append(pokemon_one.battleStats['HP'])
                health[pokemon_two].append(pokemon_two.battleStats['HP'])
                break
                
        if isinstance(second_pokemon.status,(Poison,Burn)):
            second_pokemon.status.doDamage(first_pokemon)
            
        if is_battle_over(pokemons):
                health[pokemon_one].append(pokemon_one.battleStats['HP'])
                health[pokemon_two].append(pokemon_two.battleStats['HP'])
                break
                
        health[pokemon_one].append(pokemon_one.battleStats['HP'])
        health[pokemon_two].append(pokemon_two.battleStats['HP'])
        
        
    assert health[pokemon_one][-1] != health[pokemon_two][-1]
                
    if health[pokemon_one][-1] > health[pokemon_two][-1]:
        
        return pokemon_one.name
    else:
        return pokemon_two.name    
    
        




def pick_move(pokemons):
    p_one = pokemons[0]
    p_two = pokemons[1]
    
    return {
        
         p_one:p_one.moves[random.choice(list(p_one.moves))]
        ,p_two:p_two.moves[random.choice(list(p_two.moves))]
        
        
    }


def pick_order(pokemons,attacks):
    p_one = pokemons[0]
    p_two = pokemons[1]
    
    
    p_one_attack = attacks[p_one]
    p_two_attack = attacks[p_two]

    
    #print(p_one_attack.priority,p_two_attack.priority)
    if p_one_attack.priority == p_two_attack.priority:
   
        #print(p_one.getSpeed(),p_two.getSpeed())
        if p_one.getSpeed() != p_two.getSpeed():
       
            order = sorted(pokemons,key=lambda x: x.getSpeed())
    
        else:
            #print('speed tie')
            name = random.choice([pokemon.name for pokemon in pokemons])
            
            if name == p_one.name:
                order = [p_two,p_one]
            else:
                order = [p_one,p_two]
            
   
            
    elif p_one_attack.priority > p_two_attack.priority:
        order = [p_two,p_one]
    else:
        order = [p_one,p_two]
        
    return order
    
def is_battle_over(pokemons):
    for pokemon in pokemons:
        if pokemon.battleStats['HP'] <= 0:
            return True
    return False    
    
    
"""
def battle(pokemons,verbose=False):

    
    
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
     """

    
    