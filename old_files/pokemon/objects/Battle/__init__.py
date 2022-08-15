"""
    Module for holding Pokemon battle functions
    Author: Robert Currie
    Date: January 17, 2021

"""

## library imports
import random ## rng
import math ## math operations

from pokemon.objects.Status import Poison,Burn ## necessary Statuses
from pokemon.objects.Pokemon import Pokemon ## Pokemon object


def battles(pokemons,num_battles=100,normalize=True):
    """
        Runs num_battles number of battles
        Args:
            pokemons (list(tuple(str,int,list(str)))): List of tuples of names, levels and list of moves of Pokemon battling
            num_battles (int): number of battles
            normalize (bool): normalize the number of wins to be a percentage

    """
    ## dictionary which keeps track of # of wins
    score = {pokemons[0][0]:0,pokemons[1][0]:0}

    ## loop through the number of battles
    for i in range(num_battles):
        ## list that holds the Pokemon
        pokemon = []
        ## create the Pokemon
        for i,tup in enumerate(pokemons):
            pokemon.append(Pokemon(tup[0],tup[1]))
            ## set the pokemon moves
            for move in tup[2]:
                pokemon[i].set_move(move)

        ## get the winner of the battle
        winner = battle(pokemon)
        ## increment pokemon win count
        score[winner] += 1

    ## normalize results
    if normalize:
        for key in score.keys():
            p = score[key]/num_battles
            score[key] = [p,math.sqrt(p*(1-p)/num_battles)]


    return score


def battle(pokemons):
    """
        Battle two pokemon
        Args:
            pokemons (list(Pokemon)): List of Pokemon instances
        Returns:
            str, name of the winning Pokemon

    """
    ## set the battle stats of the pokemon being battled, i.e. reset any status afflictions, etc.
    for pokemon in pokemons:
        pokemon.set_battle_stats()


    pokemon_one = pokemons[0]
    pokemon_two = pokemons[1]

    ## dictionary for holding the health of the Pokemon
    health = {pokemon_one:[pokemon_one.battle_stats['HP']],pokemon_two:[pokemon_two.battle_stats['HP']]}

    ## main battle loop
    while True:
        ## pick the moves the pokemon will use and the order they will move in
        moves = pick_move(pokemons)
        order = pick_order(pokemons,moves)

        ## battle order
        first_pokemon = order.pop()
        second_pokemon = order.pop()

        ## first attack
        first_pokemon.attack(second_pokemon,moves[first_pokemon].name) ## this is stupid as hell, should pass the move object, not the move name

        ## check if the battle is over
        if is_battle_over(pokemons):
                ## append health to dictionary
                health[pokemon_one].append(pokemon_one.battle_stats['HP'])
                health[pokemon_two].append(pokemon_two.battle_stats['HP'])
                break

        ## check if the first pokemon is burned, or poisoned
        if isinstance(first_pokemon.status,(Poison,Burn)):
            first_pokemon.status.do_damage(first_pokemon)

        ## check if the battle is over
        if is_battle_over(pokemons):
                health[pokemon_one].append(pokemon_one.battle_stats['HP'])
                health[pokemon_two].append(pokemon_two.battle_stats['HP'])
                break

        ## second attack
        second_pokemon.attack(first_pokemon,moves[second_pokemon].name) ## this is stupid as hell, should pass the move object, not the move name

        ## check if the battle is over
        if is_battle_over(pokemons):
                health[pokemon_one].append(pokemon_one.battle_stats['HP'])
                health[pokemon_two].append(pokemon_two.battle_stats['HP'])
                break

        ## check if the first pokemon is burned, or poisoned
        if isinstance(second_pokemon.status,(Poison,Burn)):
            second_pokemon.status.do_damage(second_pokemon)

        if is_battle_over(pokemons):
                health[pokemon_one].append(pokemon_one.battle_stats['HP'])
                health[pokemon_two].append(pokemon_two.battle_stats['HP'])
                break

        ## if the battle isn't over, append the health of the pokemon to the ditionary
        health[pokemon_one].append(pokemon_one.battle_stats['HP'])
        health[pokemon_two].append(pokemon_two.battle_stats['HP'])


    ## battle over
    ## check that both Pokemon don't have the same health, might change in the future for self-destruct
    assert health[pokemon_one][-1] != health[pokemon_two][-1]

    ## check who has more health (i.e. winner)
    if health[pokemon_one][-1] > health[pokemon_two][-1]:
        return pokemon_one.name
    else:
        return pokemon_two.name






def pick_move(pokemons):
    """
        Pick the moves the battling Pokemon will use
        Args:
            pokemons (list(Pokemon)): List of Pokemon instances
        Returns:
            dictionary, Pokemon, move name key value pair

    """

    p_one = pokemons[0]
    p_two = pokemons[1]
    ## randomly pick a move
    return {

         p_one:p_one.moves[random.choice(list(p_one.moves))]
        ,p_two:p_two.moves[random.choice(list(p_two.moves))]


    }


def pick_order(pokemons,attacks):
    """
        Pick the order the battling Pokemon will move in
        Args:
            pokemons (list(Pokemon)): List of Pokemon instances battling
            attacks (dictionary(Move)): Dictionary of Pokemon, Move key value pairing
        Returns:
            list of Pokemon in the order they will attack in (reverse order, i.e. last in the list goes first)

    """
    p_one = pokemons[0]
    p_two = pokemons[1]

    p_one_attack = attacks[p_one]
    p_two_attack = attacks[p_two]


    ## check if the priority of the attacks are the same
    if p_one_attack.priority == p_two_attack.priority:

        #print(p_one.get_speed(),p_two.get_speed())
        ## check if one pokemon is faster
        if p_one.get_speed() != p_two.get_speed():
            ## if one pokemon is faster, sort by speed
            order = sorted(pokemons,key=lambda x: x.get_speed())
        ## speed tie
        else:
            #print('speed tie')
            ## random choice
            name = random.choice([pokemon.name for pokemon in pokemons])

            ## set the order based on the pokemon name chosen
            if name == p_one.name:
                order = [p_two,p_one]
            else:
                order = [p_one,p_two]


    ## if the priority is higher for one pokemon, that pokemon goes first
    elif p_one_attack.priority > p_two_attack.priority:
        order = [p_two,p_one]
    else:
        order = [p_one,p_two]

    return order

def is_battle_over(pokemons):
    """
        Checks if the battle is over between two battling Pokemon
        Args:
            pokemons (list(Pokemon)): List of Pokemon instances battling
        Returns:
            bool, True/False depending on if one Pokemon has 0 HP

    """
    ## loop through and check if a pokemon has 0 HP
    for pokemon in pokemons:
        if pokemon.battle_stats['HP'] <= 0:
            return True
    return False

## old battle
"""
def battle(pokemons,verbose=False):



    def getOrder(pokemons):

        if pokemons[0].get_speed() != pokemons[1].get_speed():
            lst = sorted(pokemons,key=lambda x: x.get_speed())
        else:
            lst = [random.choice(pokemons)]
            if pokemons[0] not in lst:
                lst.append(pokemons[0])
            else:
                lst.append(pokemons[1])

        return lst

    def isBattleOver(pokemons):
        for pokemon in pokemons:
            if pokemon.battle_stats['HP'] <= 0:
                return True
        return False



    for pokemon in pokemons:
        pokemon.set_battle_stats()

    health = {pokemons[0]:[pokemons[0].battle_stats['HP']],pokemons[1]:[pokemons[1].battle_stats['HP']]}

    while True:
        order = getOrder(pokemons)

        firstToGo = order.pop()
        secondToGo = order.pop()

        firstToGo.attack(secondToGo,random.choice(list(firstToGo.moves))) ## this is stupid as hell will change later but lazy now

        if isBattleOver(pokemons):
                health[pokemons[0]].append(pokemons[0].battle_stats['HP'])
                health[pokemons[1]].append(pokemons[1].battle_stats['HP'])
                break

        if isinstance(firstToGo.status,(Poison,Burn)):
            firstToGo.status.do_damage(firstToGo)

        if isBattleOver(pokemons):
                health[pokemons[0]].append(pokemons[0].battle_stats['HP'])
                health[pokemons[1]].append(pokemons[1].battle_stats['HP'])
                break

        secondToGo.attack(firstToGo,random.choice(list(secondToGo.moves))) ## this is stupid as hell will change later but lazy now

        if isBattleOver(pokemons):
                health[pokemons[0]].append(pokemons[0].battle_stats['HP'])
                health[pokemons[1]].append(pokemons[1].battle_stats['HP'])
                break

        if isinstance(secondToGo.status,(Poison,Burn)):
            secondToGo.status.do_damage(secondToGo)

        if isBattleOver(pokemons):
                health[pokemons[0]].append(pokemons[0].battle_stats['HP'])
                health[pokemons[1]].append(pokemons[1].battle_stats['HP'])
                break

        health[pokemons[0]].append(pokemons[0].battle_stats['HP'])
        health[pokemons[1]].append(pokemons[1].battle_stats['HP'])

    if health[pokemons[0]][-1] > health[pokemons[1]][-1]:

        return pokemons[0].name
    else:
        return pokemons[1].name
    #return health
     """
