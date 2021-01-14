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

    def calculateTypeModifier(self,other,move):
        """
            Calculate type modifier of an attack (super effective, not every effective)


            Args:
                other (Pokemon): Instance of the Pokemon class that is getting attacked

            Returns:


        """
        count = 0
        oppType = other.type
        moveType = move.type

        for opType in oppType:
            if moveType in types[opType]['Resistance']:
                count -=1

            if moveType in types[opType]['Weakness']:
                count +=1

        return TYPEMULTIPLIER[count]




    def calculateModifier(self,other,move):


        ## NON GEN1 FACTORS
        targets = 1
        weather = 1
        badge = 1
        critical = 1

        if move.type in self.type:
            stab = 1.5
        else:
            stab = 1

        typeM = self.calculateTypeModifier(other,move)

        rand = random.randint(217,255) / 255



        return targets*weather*badge*critical*stab*typeM*rand

    def calculateDamage(self,other,move):

        isCrit = self.is_crit_hit(move)

        if isCrit:
            level = self.level*2
            #print('Critical Hit')


            if move.category == 'Physical':
                attack = self.stats['Attack']
                defense = other.stats['Defense']

            else:
                attack = self.stats['Special']
                defense = other.stats['Special']


        else:
            level = self.level

            if move.category == 'Physical':
                attack = self.battle_stats['Attack'][0] * STATSMULTIPLIER[self.battle_stats['Attack'][1]]
                defense = other.battle_stats['Defense'][0] * STATSMULTIPLIER[other.battle_stats['Defense'][1]]
            else:
                attack = self.battle_stats['Special'][0] * STATSMULTIPLIER[self.battle_stats['Special'][1]]
                defense = other.battle_stats['Special'][0] * STATSMULTIPLIER[other.battle_stats['Special'][1]]



        modifier =  self.calculateModifier(other,move)
        power = move.power

        return math.floor(((2*level/5 + 2)*power*attack/defense/50 + 2) * modifier)


    def receiveDamage(self,damage):
        self.battle_stats['HP'] -= damage

        if self.battle_stats['HP'] < 0:
            self.battle_stats['HP'] =0


    def attack(self,other,moveName):

        if self.status.canMove():


            move = self.moves[moveName]


            ## damaging attack
            if move.category in ['Physical','Special']:
                #print(self.name + ' used '+ move.name)
                damage = self.calculateDamage(other,move)

                if not self.miss_attack(other,move):
                    other.receiveDamage(damage)

                    #print(self.name + ' inflicted ' + str(damage) + ' damage')
                    if isinstance(move,ParalyzingMove):
                        if move.doesParalyze() and isinstance(other.status,Normal):
                            move.paralyze(other)
                            #print(other.name + ' was paralyzed')
                    elif isinstance(move,BurnMove):
                        if move.doesBurn() and isinstance(other.status,Normal) and 'Fire' not in other.type:
                            move.burn(other)
                            #print(other.name + ' was burned')

                    elif isinstance(move,PoisonMove):
                        if move.doesPoison() and isinstance(other.status,Normal):
                            move.poison(other)
                            #print(other.name + ' was poisoned')



                else:
                    #print(self.name + ' missed')
                    pass
            ## stat changing move
            else:
                ## targets the opponent pokemon
                #print(self.name + ' used ' + move.name)
                if move.target:
                    if not self.miss_attack(other,move):
                        receiveStatusModifier(other,move)

                ## targets self (raises stats)
                else:
                    receiveStatusModifier(self,move)

        else:
            pass
            #print(self.name + ' is fully paralyzed')


    def getSpeed(self):
        return self.battle_stats['Speed'][0] * STATSMULTIPLIER[self.battle_stats['Speed'][1]]


def receiveStatusModifier(pokemon,move):
    if move.stages < 0:
        if pokemon.battle_stats[move.affects][1] > -6:
            pokemon.battle_stats[move.affects][1] += move.stages
            if pokemon.battle_stats[move.affects][1] < -6:
                pokemon.battle_stats[move.affects][1] = -6
    else:
        if pokemon.battle_stats[move.affects][1] < 6:
            pokemon.battle_stats[move.affects][1] += move.stages
            if pokemon.battle_stats[move.affects][1] > 6:
                pokemon.battle_stats[move.affects][1] = 6
