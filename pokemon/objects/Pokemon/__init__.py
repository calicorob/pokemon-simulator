import math
import random
import json 


from pokemon.data import POKEMON as pokemon
from pokemon.data import MOVES as moves
from pokemon.data import TYPES as types

from pokemon.data import TYPEMULTIPLIER as typeMultiplier
from pokemon.data import STATSMULTIPLIER as statsMultiplier


from pokemon.objects.Status import Normal
from pokemon.objects.Moves import makeMove,ParalyzingMove,BurnMove,PoisonMove


class Pokemon(object):
    
    def __init__(self,name,level=1):
        
        ## BASE STATS & TYPE
        self.name = name
        self.level = level
        self.type = pokemon[self.name]['Type']
        self.baseStats = pokemon[self.name]['Base Stats']
        
        
        
        ## INDIVIDUAL VALUES
      
        self.IV = {}
        health = ""
        for cat in ['Attack','Defense','Speed','Special']:
            self.IV[cat] = random.choice(range(16))
            health = health + '{0:b}'.format(self.IV[cat])[-1]       
        self.IV['HP'] = int(health,2)
        
        
            
        ## ALL STATS EXCEPT FOR HEALTH SINCE IT'S A SPECIAL CASE    
        
        self.stats = {}
        for cat in ['Attack','Defense','Speed','Special']:
            baseStat = self.baseStats[cat]
            ivStat = self.IV[cat]
            self.stats[cat] = math.floor((baseStat + ivStat)*2 *self.level/100 + 5 )
            
        self.stats['Accuracy'] = 1
        self.stats['Evasion'] = 1
            
            
            
        ## HEALTH STAT 
            
        baseStat = self.baseStats['HP']
        ivStat = self.IV['HP']
        self.stats['HP'] = math.floor((baseStat + ivStat)*2 *self.level/100 + self.level+10)
        
        
        self.setBattleStats()
            
    
          ## MOVES
        self.moves = {}
     
    
    def __repr__(self):
        return self.name
        
        
    def setMove(self,move):
        if len(self.moves) <= 4:
            self.moves[move] = makeMove(move)
        else:
            print(self.name + " already has 4 moves!")
            
            
    def setBattleStats(self):
        self.battleStats = {}
            
        for cat in ['Attack','Defense','Speed','Special','Accuracy','Evasion']:
            self.battleStats[cat] = [self.stats[cat],0]
            
    
        self.battleStats['HP'] = self.stats['HP']
            
        self.status = Normal()
            
            
    def missAttack(self,other,move):
        
        accuracy = self.battleStats['Accuracy'][0]
        evasion = other.battleStats['Evasion'][0]
        
        threshold = math.floor(move.accuracy*255)*accuracy*evasion
        
        rand = random.randint(0,255)
        
        if rand < threshold:
            return False ## attack hits
        else:
            return True ## attack misses
        
        
    def isCritHit(self,move):
        speed = self.baseStats['Speed']
        critRatio = move.critRatio
        
        
        threshold = math.floor(speed*critRatio/2)
        rand = random.randint(0,255)
        
        if rand < threshold:
            return True
        else:
            return False 
        
    def calculateTypeModifier(self,other,move):
        count = 0
        oppType = other.type
        moveType = move.type
        
        for opType in oppType:
            if moveType in types[opType]['Resistance']:
                count -=1
                
            if moveType in types[opType]['Weakness']:
                count +=1
                
        return typeMultiplier[count]
                
        
            
        
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
        
        isCrit = self.isCritHit(move)
        
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
                attack = self.battleStats['Attack'][0] * statsMultiplier[self.battleStats['Attack'][1]]
                defense = other.battleStats['Defense'][0] * statsMultiplier[other.battleStats['Defense'][1]]
            else:
                attack = self.battleStats['Special'][0] * statsMultiplier[self.battleStats['Special'][1]]
                defense = other.battleStats['Special'][0] * statsMultiplier[other.battleStats['Special'][1]]
                
                
        
        modifier =  self.calculateModifier(other,move)
        power = move.power
        
        return math.floor(((2*level/5 + 2)*power*attack/defense/50 + 2) * modifier)
                
        
    def receiveDamage(self,damage):
        self.battleStats['HP'] -= damage
        
        if self.battleStats['HP'] < 0:
            self.battleStats['HP'] =0

        
    def attack(self,other,moveName):
        
        if self.status.canMove():
            
        
            move = self.moves[moveName]


            ## damaging attack
            if move.category in ['Physical','Special']:
                #print(self.name + ' used '+ move.name)
                damage = self.calculateDamage(other,move)

                if not self.missAttack(other,move):
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
                            # print(other.name _ ' was poisoned')
                    
                    
                    
                else:
                    #print(self.name + ' missed')
                    pass
            ## stat changing move 
            else:
                ## targets the opponent pokemon
                #print(self.name + ' used ' + move.name)
                if move.target:
                    if not self.missAttack(other,move):
                        receiveStatusModifier(other,move)

                ## targets self (raises stats)
                else:
                    receiveStatusModifier(self,move)

        else:
            pass
            #print(self.name + ' is fully paralyzed')
            
                
    def getSpeed(self):
        return self.battleStats['Speed'][0] * statsMultiplier[self.battleStats['Speed'][1]]
    
    
def receiveStatusModifier(pokemon,move):
    if move.stages < 0:
        if pokemon.battleStats[move.affects][1] > -6:
            pokemon.battleStats[move.affects][1] += move.stages
            if pokemon.battleStats[move.affects][1] < -6:
                pokemon.battleStats[move.affects][1] = -6
    else:
        if pokemon.battleStats[move.affects][1] < 6:
            pokemon.battleStats[move.affects][1] += move.stages
            if pokemon.battleStats[move.affects][1] > 6:
                pokemon.battleStats[move.affects][1] = 6
                
                
