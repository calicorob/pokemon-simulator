"""
    Module which holds the Move Class
    Author: Robert Currie
    Date: January 17, 2021

"""
## library imports

import random ## rng
import math ## math operations

from pokemon.data import MOVES as moves ## moves dictionary
from pokemon.objects.Status import Paralysis, Burn,Poison ## Statuses



class Move(object):
    """
        Base Move class

    """
    def __init__(self,name):
        """
            Base move class Constructor
            Args:
                name (str): Name of the move
            Returns:
                Instance of the Move class

        """
        ## setting class variables
        self.name = name
        self.type = moves[name]['Type']
        self.category = moves[name]['Category']
        self.accuracy = moves[name]['Accuracy']
        self.PP = moves[name]['PP']
        self.priority = moves[name]['Priority']


class NormalMove(Move):
    """
        NormalMove class
    """
    def __init__(self,name):
        """
            Constructor for the NormalMove class
            Args:
                Name (str): Name of the move being constructed
            Returns:
                Instance of the NormalMove class

        """
        ## initialize base class variables
        super().__init__(name)
        ## move power and crit ratio
        self.power = moves[name]['Power']
        self.crit_ratio = moves[name]['CritRatio']

class PhysicalMove(Move):
    """
        PhysicalMove class, physical moves use the Pokemon's attack stat for it's attack power

    """
    def __init__(self,name):
        """
            Constructor for the PhysicalMove class
            Args:
                Name (str): Name of the move being constructed
            Returns:
                Instance of the PhysicalMove class

        """
        ## initialize base class variables
        super().__init__(name)
        ## move power and crit ratio
        self.power = moves[name]['Power']
        self.crit_ratio = moves[name]['CritRatio']

class SpecialMove(Move):
    """
        SpecialMove class, special moves use the Pokemon's special stat for it's attack power

    """
    def __init__(self,name):
        """
            Constructor for the SpecialMove class
            Args:
                Name (str): Name of the move being constructed
            Returns:
                Instance of the SpecialMove class

        """
        super().__init__(name)
        self.power = moves[name]['Power']
        self.crit_ratio = moves[name]['CritRatio']

class ParalyzingMove(Move):
    """
        ParalyzingMove class, paralyzing moves have a chance to paralyze the defending pokemon
    """
    def __init__(self,name):
        """
            Constructor for the ParalyzingMove class
            Args:
                Name (str): Name of the move being constructed
            Returns:
                Instance of the ParalyzingMove class

        """
        ## initialize base class variables
        super().__init__(name)
        ## move power and crit ratio
        self.power = moves[name]['Power']
        self.crit_ratio = moves[name]['CritRatio']
        ## chance to paralyze
        self.chance = moves[name]['Chance']


    def does_paralyze(self):
        """
            Checks if the attack will paralyze the attacking Pokemon

            Args:
                None

            Returns:
                bool, True/False depending if the pokemon is paralyzed or not

        """
        ## chance the attack paralyzes
        threshold = self.chance

        ## random number
        rand = random.random()
        ## if the random number is higher than the chance of paralysis, don't paralyze
        if rand > threshold:
            return False ## doesn't paralyze
        else:
            return True ## paralyzes


    def paralyze(self,pokemon):
        """
            Sets the status of the Pokemon to paralyzed

            Args:
                pokemon (Pokemon): Instance of the Pokemon class being paralyzed

            Returns:
                None

        """
        ## set the status of the pokemon to paralyzed
        pokemon.status = Paralysis(pokemon)

class BurnMove(Move):
    """
        BurnMove class, burn moves have a chance to burn the Pokemon being attacked

    """
    def __init__(self,name):
        """
            Constructor for the BurnMove class
            Args:
                Name (str): Name of the move being constructed
            Returns:
                Instance of the BurnMove class

        """
        ## initialize base class variables
        super().__init__(name)
        ## power and crit ratio
        self.power = moves[name]['Power']
        self.crit_ratio = moves[name]['CritRatio']
        ## chance the move burns
        self.chance = moves[name]['Chance']

    def does_burn(self):
        """
            Checks if the attack will burn the defending Pokemon
            Args:
                None
            Returns:
                None

        """
        ## chance the attack will burn
        threshold = self.chance
        ## random number
        rand = random.random()

        ## if the random number is higher than the threshold, the attack doesn't burn
        if rand > threshold:
            return False ## doesn't burn
        else:
            return True

    def burn(self,pokemon):
        """
            Burn the defending pokemon, sets the status of the Pokemon to Burn

            Args:
                pokemon (Pokemon): Instance of the Pokemon being burned

            Returns:
                None

        """
        ## set the status of the defending Pokemon to Burn
        pokemon.status = Burn(pokemon)

class PoisonMove(Move):
    """
        PoisonMove, poison moves have a chance to poison defending Pokemon

    """
    def __init__(self,name):
        """
            Constructor for the PoisonMove class
            Args:
                Name (str): Name of the move being constructed
            Returns:
                Instance of the PoisonMove class

        """
        ## initialize base class variable
        super().__init__(name)
        ## power and crit ratio
        self.power = moves[name]['Power']
        self.crit_ratio = moves[name]['CritRatio']
        ## chance the move has to poison
        self.chance = moves[name]['Chance']
    def does_poison(self):

        """
            Checks if the attack poisons the defending Pokemon
            Args:
                None
            Returns:
                None

        """
        ## chance to poison
        threshold = self.chance
        ## random number
        rand = random.random()

        ## if the random number is higher than the chance to poison, don't poison
        if rand > threshold:
            return False ## doesn't poison
        else:
            return True

    def poison(self,pokemon):
        """
            Poison the defending Pokemon, sets the status of the Pokemon to Poison
            Args:
                pokemon (Pokemon): Instance of the Pokemon class being poisoned
            Returns:
                None

        """
        ## set the status of the Pokemon to Poisoned
        pokemon.status = Poison(pokemon)


class StatusMove(Move):
    """
        StatusMove, changes the status of the offending pokemon

    """
    def __init__(self,name):
        """
            Constructor for the StatusMove class
            Args:
                Name (str): Name of the move being constructed
            Returns:
                Instance of the StatusMove class

        """
        ## initialize base class variable
        super().__init__(name)
        ## class variables
        self.affects = moves[name]['Affects']
        self.stages = moves[name]['Stages']
        self.target = moves[name]['Target']

def make_move(name):
    """

        Helper function which creates moves
        Args:
            name (str): Name of the move being created

        Returns:
            Move

    """
    ## get the move category
    cat = moves[name]['Category']

    ## check if the move has an afflition
    try:
        aff = moves[name]['Affliction']
    except KeyError:
        aff = None

    ## if the move has an affliction, return the appropriate Move
    if aff:
        if aff == 'Burn':
            return BurnMove(name)
        elif aff == 'Paralysis':
            return ParalyzingMove(name)
        elif aff == 'Poison':
            return PoisonMove(name)

    ## no affliction
    else:
        ## if it's a Physical or Special category, return a normal attacking move, otherwise it's a Status Move
        if cat == 'Physical' or cat == 'Special':
            return NormalMove(name)
        else:
            return StatusMove(name)
