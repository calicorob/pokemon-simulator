"""
    Module which contains Pokemon class definition
    Author: Robert Currie
    Date: January 16, 2021

"""

## library imports

import math ## math operations
import random ## RNG
import json  ## reading moves, pokemon attributes, etc.


## import Pokemon and attributes
from pokemon.data import POKEMON as pokemon ## dictionary of pokemon and their attributes
from pokemon.data import MOVES as moves ## dictionary of moves and their attributes
from pokemon.data import TYPES as types ## dictionary of types and their attributes

from pokemon.data import TYPEMULTIPLIER ## dictionary of multipliers for type effectiveness
from pokemon.data import STATSMULTIPLIER ## dictionary of status multiplers for status effects


from pokemon.objects.Status import Normal
from pokemon.objects.Moves import make_move,ParalyzingMove,BurnMove,PoisonMove


class Pokemon(object):
    """
        Pokemon object which can damage and affect other Pokemon objects
    """
    def __init__(self,name,level=1):

        """
            Constructor

            Args:
                name (string): Name of the Pokemon
                level (int): level of the Pokemon

        """


        ## BASE STATS & TYPE

        ## checking a valid level was passed
        assert all(


            [isinstance(level,int),level>0]


        ), "Invalid level passed"

        ## set the name of the Pokemon
        self.name = name

        ## set the level of the Pokemon
        self.level = level

        ## set the type of the Pokemon
        self.type = pokemon[self.name]['Type']
        self.base_stats = pokemon[self.name]['Base Stats']



        ## INDIVIDUAL VALUES

        ## set the individual values for the pokemon
        self.IV = {}

        ## string which holds characters which determine what IV the health of the Pokemon has
        health = ""

        ## Loop through the different attributes and set a random value
        for cat in ['Attack','Defense','Speed','Special']:
            self.IV[cat] = random.choice(range(16))

            ## build a string of binary values to set the HP IV
            health = health + '{0:b}'.format(self.IV[cat])[-1]
        ## set the HP IV
        self.IV['HP'] = int(health,2)


        ## ALL STATS EXCEPT FOR HEALTH SINCE IT'S A SPECIAL CASE

        ## dictionary to hold the stats of the Pokemon
        self.stats = {}
        ## loop through the attributes and set thier value
        for cat in ['Attack','Defense','Speed','Special']:
            base_stat = self.base_stats[cat]
            iv_stat = self.IV[cat]
            self.stats[cat] = math.floor((base_stat + iv_stat)*2 *self.level/100 + 5 )

        ## Set Accuracy and Evasion (always 1 to start)
        self.stats['Accuracy'] = 1
        self.stats['Evasion'] = 1



        ## HEALTH STAT

        base_stat = self.base_stats['HP']
        iv_stat = self.IV['HP']
        self.stats['HP'] = math.floor((base_stat + iv_stat)*2 *self.level/100 + self.level+10)


        self.set_battle_stats()


          ## MOVES
        ## dictionary to hold the moveset of the Pokemon
        self.moves = {}


    def __repr__(self):
        """
            Returns the string representation of the Pokemon instance

            Args:
                None
            Returns:
                string, name of the Pokemon

        """
        return self.name


    def set_move(self,move):
        """
            Add a move to the Pokemon

            Args:
                move (str): name of the move to be added

            Returns:
                None

        """

        ## check that the move exists
        assert move in moves.keys(), "Move was not found"

        ## check that the pokemon doesn't already have 4 moves
        if len(self.moves) <= 4:
            self.moves[move] = make_move(move)
        else:
            print(self.name + " already has 4 moves!")


    def set_battle_stats(self):
        """
            Sets or resets the Battle Stats for the Pokemon (no status affects) and sets the Status of the Pokemon to Normal

            Args:
                None

            Returns:
                None
        """

        ## dictionary to hold the battle stats
        self.battle_stats = {}

        ## loop through the attributes, setting the battle stat to the initial value
        for cat in ['Attack','Defense','Speed','Special','Accuracy','Evasion']:
            self.battle_stats[cat] = [self.stats[cat],0]

        self.battle_stats['HP'] = self.stats['HP']


        ## set the status of the Pokemon to Normal
        self.status = Normal()


    def miss_attack(self,other,move):
        """
            Checks if an attack is successful in hitting

            Args:
                other (Pokemon): Instance of the Pokemon class that is being attacked
                move (Move): Instance of the Move class that is being used on other

            Returns:
                bool, whether or not the attack hits

        """

        ## getting
        accuracy = self.battle_stats['Accuracy'][0]
        evasion = other.battle_stats['Evasion'][0]

        ## threshold value
        threshold = math.floor(move.accuracy*255)*accuracy*evasion

        ## random value between 0 and 255
        rand = random.randint(0,255)

        ## checks if the random number is less than the threshold value
        ## without any accuracy / evasion changes, attacks should hit 255/256
        if rand < threshold:
            return False ## attack hits
        else:
            return True ## attack misses


    def is_crit_hit(self,move):
        """
            Checks if a an attack is a critical hit

            Args:
                move (Move): Instance of the Move class being used

            Returns:
                bool, whether or not the attack was a critical hit

        """

        ## get the speed of the pokemon and the move crit ratio
        speed = self.base_stats['Speed']
        crit_ratio = move.crit_ratio

        ## calculate the threshold value
        threshold = math.floor(speed*crit_ratio/2)

        ## random number between 0 and 255
        rand = random.randint(0,255)

        ## if the random number is less than threshold, a critical hit occurs
        if rand < threshold:
            return True
        else:
            return False

    def calculate_type_modifier(self,other,move):
        """
            Calculate type modifier of an attack (super effective, not every effective)


            Args:
                other (Pokemon): Instance of the Pokemon class that is getting attacked
                move (Move): Instance of the Move class that is being used to attack other
            Returns:
                float, damage modifier of type weakness / resistance


        """
        ## counter, used to keep track of super effective and double super effective moves
        count = 0

        opp_type = other.type
        move_type = move.type

        ## loop through the attack types
        for op_type in opp_type:
            ## if the move type is found in the other pokemon's resistances, decrease counter by 1
            if move_type in types[op_type]['Resistance']:
                count -=1
            ## if the move type is found in the other pokemon's weaknesses, increase counter by 1
            if move_type in types[op_type]['Weakness']:
                count +=1

        ## return type multiplier
        return TYPEMULTIPLIER[count]

    def calculate_modifier(self,other,move):
        """
            Calculates damage modifier of an attack

            Args:
                other (Pokemon): Instance of the Pokemon class being attacked
                move (Move): Instance of the Move class being used to attack other

            Returns:
                float, damage modifier of the pokemon being attacked

        """

        ## NON GEN1 FACTORS
        targets = 1
        weather = 1
        badge = 1
        critical = 1

        ## if the attack is the same type as the pokemon attacking, it gets a STAB (same type attack bonus)
        if move.type in self.type:
            stab = 1.5
        else:
            stab = 1

        ## calculates type modifier
        type_modifier = self.calculate_type_modifier(other,move)

        ## RNG
        rand = random.randint(217,255) / 255

        ## return modifier
        return targets*weather*badge*critical*stab*typeM*rand

    def calculate_damage(self,other,move):
        """
            Calculates the damage of an attack against an opponent Pokemon

            Args:
                other (Pokemon): Instance of the Pokemon class being attacked
                move (Move): Instance of the Move class being used to attack

            Returns:
                float, damage done to other

        """

        ## is the attack a critical hit
        is_crit = self.is_crit_hit(move)

        ## if the move is a critical hit, increase damage done by 2, by pass all stat multiplers
        if is_crit:
            level = self.level*2
            #print('Critical Hit')

            ## if the move is a physical attack, get the attack and defense stat of the attacking and defending pokemon, respectively
            if move.category == 'Physical':
                attack = self.stats['Attack']
                defense = other.stats['Defense']
            ## if the move is a special attack, get the special of the attacking and defending pokemon
            else:
                attack = self.stats['Special']
                defense = other.stats['Special']

        ## attack is not a critical hit
        else:
            level = self.level

            ## if the move is a physical attack, get the attack and defense stat of the attacking and defending pokemon, respectively
            if move.category == 'Physical':
                attack = self.battle_stats['Attack'][0] * STATSMULTIPLIER[self.battle_stats['Attack'][1]]
                defense = other.battle_stats['Defense'][0] * STATSMULTIPLIER[other.battle_stats['Defense'][1]]
            ## if the move is a special attack, get the special of the attacking and defending pokemon
            else:
                attack = self.battle_stats['Special'][0] * STATSMULTIPLIER[self.battle_stats['Special'][1]]
                defense = other.battle_stats['Special'][0] * STATSMULTIPLIER[other.battle_stats['Special'][1]]


        ## calculate the RNG multiplier
        modifier =  self.calculate_modifier(other,move)
        ## get the move power
        power = move.power

        ## return the damage
        return math.floor(((2*level/5 + 2)*power*attack/defense/50 + 2) * modifier)


    def receive_damage(self,damage):
        """
            Receive incoming damage from an attack or status afflictions

            Args:
                damage (float): damage being done

            Returns:
                None


        """
        ## subtract the damage done from the pokemon's HP
        self.battle_stats['HP'] -= damage

        ## if the heath dip belows 0, set to 0
        if self.battle_stats['HP'] < 0:
            self.battle_stats['HP'] =0


    def attack(self,other,move_name):
        """
            Attack an opposing Pokemon

            Args:
                other (Pokemon): Instance of the Pokemon class being attacked by self
                move_name (str): name of the attack being used on other


        """
        ## check if the status allows the Pokemon to attack (e.g. not paralyzed or frozen)
        if self.status.can_move():

            ## get the Move instance from the self's move dictionary
            move = self.moves[move_name]


            ## damaging attack
            if move.category in ['Physical','Special']:
                #print(self.name + ' used '+ move.name)
                damage = self.calculate_damage(other,move)

                ## check if the move misses
                if not self.miss_attack(other,move):
                    other.receive_damage(damage)

                    #print(self.name + ' inflicted ' + str(damage) + ' damage')

                    ## check if the move is a ParalyzingMove, BurnMove, Poison move and whether or not the other pokemon is affected
                    if isinstance(move,ParalyzingMove):
                        if move.does_paralyze() and isinstance(other.status,Normal):
                            move.paralyze(other)
                            #print(other.name + ' was paralyzed')
                    elif isinstance(move,BurnMove):
                        if move.does_burn() and isinstance(other.status,Normal) and 'Fire' not in other.type:
                            move.burn(other)
                            #print(other.name + ' was burned')

                    elif isinstance(move,PoisonMove):
                        if move.does_poison() and isinstance(other.status,Normal):
                            move.poison(other)
                            #print(other.name + ' was poisoned')


                ## attack is missed
                else:
                    #print(self.name + ' missed')
                    pass

            ## stat changing move
            else:
                ## targets the opponent pokemon
                #print(self.name + ' used ' + move.name)
                if move.target:
                    if not self.miss_attack(other,move):
                        receive_status_modifier(other,move)

                ## targets self (raises stats)
                else:
                    receive_status_modifier(self,move)

        else:
            pass
            #print(self.name + ' is fully paralyzed')


    def get_speed(self):
        """
            Returns the speed of self

            Args:
                None

            Returns:
                float, current speed of self

        """
        return self.battle_stats['Speed'][0] * STATSMULTIPLIER[self.battle_stats['Speed'][1]]


def receive_status_modifier(pokemon,move):
    """
        Changes an attribute of a Pokemon

        Args:
            pokemon (Pokemon): Instance of the Pokemon class whose status is being changed
            move (Move): Instance of the Move class changing the pokemon's status

        Returns:
            None

        Notes:
            Could be turned into a method?


    """
    ## if the move decreases the pokemon's stats
    if move.stages < 0:
        ## if the status being affected isn't already at it's lowest
        if pokemon.battle_stats[move.affects][1] > -6:
            pokemon.battle_stats[move.affects][1] += move.stages

            ## if the status goes beyond the maximum change, set it to the maximum change
            if pokemon.battle_stats[move.affects][1] < -6:
                pokemon.battle_stats[move.affects][1] = -6
    ## increases a pokemon's stats
    else:
        ## check the status isn't at it's max value
        if pokemon.battle_stats[move.affects][1] < 6:
            pokemon.battle_stats[move.affects][1] += move.stages
            ## if the status is beyond it's max value, set it to the max value
            if pokemon.battle_stats[move.affects][1] > 6:
                pokemon.battle_stats[move.affects][1] = 6
