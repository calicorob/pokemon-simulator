from pokemon import Pokemon,makeMove,Paralysis,battle,battles
import matplotlib.pyplot as plt

import math


def hit_rate_testing(runs:int=2000,attacks:int=1000,verbose:bool=True)->None:
    bulby = Pokemon('Bulbasaur',5)
    bulby.setMove('Tackle')
    
    charmy = Pokemon('Charmander',5)
    charmy.setMove('Ember')
    charmy.setMove('Growl')
    
    samples = []
    
    for i in range(runs):
        hits = []
        for j in range(attacks):
            hits.append(bulby.missAttack(charmy,bulby.moves['Tackle']))
            
        samples.append(sum(hits)/len(hits))
        
        
    if verbose:
        fig,ax = plt.subplots(1)
        ax.hist(samples)

        ax.set_ylabel('Frequency',fontweight='bold',fontsize=15)
        ax.set_xlabel('Miss frequency',fontweight='bold',fontsize=15)
        ax.set_title(f'Miss frequency average: {round(sum(samples)/len(samples),5)}',fontweight='bold',fontsize=15)    
        
       
    print(sum(samples)/len(samples))

    
    
def paralysis_testing(runs:int=10000)->None:
    thundershock = makeMove('Thundershock')
    para = []
    for i in range(runs):
        para.append(thundershock.doesParalyze())
    print(sum(para)/len(para))
    
    
def burn_testing(runs:int=10000)->None:
    
    ember = makeMove('Ember')
    burn = []
    for i in range(runs):
        burn.append(ember.doesBurn())
    print(sum(burn)/len(burn))
    
    
def burn_status_affliction()->None:
    bulby = Pokemon('Bulbasaur',5)
    ember = makeMove('Ember')
    atk = bulby.battleStats['Attack'][0]
    ember.burn(bulby)
    
    assert math.floor(atk/2) == bulby.battleStats['Attack'][0]
    assert bulby.battleStats['Attack'][1] == 0
    
def paralysis_status_affliction()->None:
    charmy = Pokemon('Charmander',5)
    thundershock = makeMove('Thundershock')
    
    spd = charmy.battleStats['Speed'][0]
    thundershock.paralyze(charmy)
    
    assert math.floor(spd*0.75) == charmy.battleStats['Speed'][0]
    assert charmy.battleStats['Speed'][1] == 0
    
def status_affliction()->None:
    bulby = Pokemon('Bulbasaur',5)
    bulby.setMove('Tackle')
    
    charmy = Pokemon('Charmander',5)
    charmy.setMove('Ember')
    charmy.setMove('Growl')
    
    
    charmy.attack(bulby,'Growl')
    
    assert bulby.battleStats['Attack'][1] == -1
    
    
def paralysis_movement(runs:int=10000)->None:
    able = []
    bulby = Pokemon('Bulbasaur')
    bulby.status = Paralysis(bulby)
    for i in range(runs):
        able.append(bulby.status.canMove())
    print(sum(able)/len(able))
    
    
def test_battle()->None:
    bulby = Pokemon('Squirtle',5)
    bulby.setMove('Tackle')
    bulby.setMove('Tail Whip')


    charmy = Pokemon('Bulbasaur',5)
    charmy.setMove('Scratch')
    charmy.setMove('Growl')
    
    print(battle([bulby,charmy]))
    
def test_priority()->None:
    ember = makeMove('Ember')
    print(ember.priority)
    
    quickAttack = makeMove('Quick Attack')
    print(quickAttack.priority)
    
    
def test_battles(runs:int=10000)->None:
    pokemon1 = ('Pikachu',5,['Thundershock','Growl'])
    pokemon2 = ('Eevee',5,['Tackle','Tail Whip'])
    pokemons = (pokemon1,pokemon2)
    print(battles(pokemons,runs))
    
def test_battles(runs:int=10000)->None:
    pokemon1 = ('Weedle',5,['Poison Sting','String Shot'])
    pokemon2 = ('Eevee',5,['Tackle','Tail Whip'])
    pokemons = (pokemon1,pokemon2)
    print(battles(pokemons,runs))
    
    
    
    
    

if __name__ == '__main__':
    
    ## hit rate testing
    ## Expected ~0.004
    
    #hit_rate_testing()

    ## paralysis testing
    ## Expected ~0.1
    
    #paralysis_testing()
    
    
    ## burn testing
    ## Expected ~0.1
    
    #burn_testing()
    
    
    #burn_status_affliction()
    #paralysis_status_affliction()
    #status_affliction()
    
    ## Expected ~0.75
    
    #paralysis_movement()
    
    
    test_battle()
    
    test_battles()
    
    #test_priority()
    
   
    
    
    
    
  
    
    
    
    
    
    
    
    

    
    plt.show()

    
    