"""
    Module which contains Pokemon Status class definition
    Author: Robert Currie
    Date: January 16, 2021

"""


## library imports
import random ## rng
import math ## math operations

class Status(object):
    """
        Base Status class
    """
    def __init__(self):
        """
            Constructor of the base Status class
            Args:
                None
            Returns:
                Instance of the Status class

        """
        ## threshold value which controls if a pokemon can move used (status afflictions)
        ## value of 1 means it will always be able to move
        self.threshold = 1

    def can_move(self):
        """
            Checks if the status of a Pokemon allows it to move

            Args:
                None
            Returns:
                bool, True/False value for the Pokemon's ability to move

        """
        ## get random number
        rand = random.random()

        ## if the random value is below the threshold value, the Pokemon can move
        if rand <= self.threshold:
            return True ## can move
        else:
            return False ## can't move

class Poison(Status):
    """
        Poison status, if a Pokemon is poisoned it will lose 1/16th of it's max HP each turn

    """
    def __init__(self,pokemon):
        """
            Constructor of the Poison status

            Args:
                pokemon (Pokemon): Instance of the Pokemon class who is being poisoned

        """
        ## set damage
        self.damage = math.floor(pokemon.stats['HP'] / 16)
        ## set movement threshold
        self.threshold = 1
        ## if the damage is less than 1, set it do 1
        if self.damage < 1:
            self.damage = 1

    def do_damage(self,pokemon):
        """
            Inflicts poison damage on the Pokemon who is poisoned

            Args:
                pokemon (Pokemon): Instance of the Pokemon class who is poisoned

            Returns:
                None

        """
        #print(pokemon.name + 'took poison damage')
        ## inflict damage on the poisoned pokemon
        pokemon.receive_damage(self.damage)

class Paralysis(Status):
    """
        Paralysis status, if a Pokemon is paralyzed, it's speed is decreased by 25% and it has a 25% chance of not being able to move

    """
    def __init__(self,pokemon):
        """
            Constructor

            Args:
                pokemon (Pokemon): Instance of the Pokemon class that is being paralyzed

            Returns:
                Instance of the Paralysis class

        """
        ## set the speed of the pokemon being paralyzed to 75% of it's original value
        pokemon.battle_stats['Speed'][0] = math.floor(pokemon.stats['Speed'] * 0.75)
        ## set the threshold value, represents a 25% chance of not being able to move
        self.threshold = 0.75



class Burn(Status):
    """
        Burn status, if a pokemon is burned, it will take 1/16th it's total HP each turn and it's attack stat is halved

    """
    def __init__(self,pokemon):
        """
            Constructor

            Args:
                pokemon (Pokemon): Instance of the Pokemon class who is being burnt

            Returns:
                Instance of the Burn Status

        """
        ## set damage that will be inflicted each turn
        self.damage = math.floor(pokemon.stats['HP'] / 16)

        ## if the damage is less than 1, set it to 1
        if self.damage < 1:
            self.damage = 1
        self.threshold = 1

        ## halve the attack of the Pokemon who is burnt
        pokemon.battle_stats['Attack'][0] = math.floor(pokemon.stats['Attack'] * 0.5)

    def do_damage(self,pokemon):
        """
            Inflicts burn damage on the Pokemon who is burned

            Args:
                pokemon (Pokemon): Instance of the Pokemon class who is burned

            Returns:
                None

        """

        #print('Burn does' + str(self.damage) + 'damage')
        ## inflict burn damage
        pokemon.receive_damage(self.damage)

class Frozen(Status):
    def __init__(self):
        raise NotImplementedError('Frozen status not implemented yet')
        self.threshold = 0

class Normal(Status):
    """
        Normal status, pokemon who have a normal status have no afflictions
    """
    ## TODO, reset any status afflictions
    pass

class Asleep(object):
    def __init__(self):
        raise NotImplementedError("Asslep status not implemented yet")
        self.turns = random.randint(1,7)
