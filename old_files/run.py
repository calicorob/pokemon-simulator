"""
    Testing script
    Author: Robert Currie
    Date: January 17, 2021

"""

## library imports
from pokemon import Pokemon,make_move,Paralysis,battle,battles ## for battles and testing
import matplotlib.pyplot as plt ## plotting
import math ## math operations


def hit_rate_testing(runs:int=2000,attacks:int=1000,verbose:bool=True)->None:
    """
        Hit rate testing function, expected hit rate should be ~99.6 hit rate

        Args:
            runs (int): Number of samples
            attacks (int): Number of attacks in a sample
            verbose (bool): Controls verbosity of results

        Returns:
            float, miss rate

    """
    ## make test pokemon
    bulby = Pokemon('Bulbasaur',5)
    bulby.set_move('Tackle')
    charmy = Pokemon('Charmander',5)
    charmy.set_move('Ember')
    charmy.set_move('Growl')

    ## holds sample results
    samples = []

    ## loop through runs
    for i in range(runs):
        ## holds hit / misses
        hits = []
        for j in range(attacks):
            hits.append(bulby.miss_attack(charmy,bulby.moves['Tackle']))

        ## appends hit rate
        samples.append(sum(hits)/len(hits))

    ## displays histogram of samples
    if verbose:
        fig,ax = plt.subplots(1)
        ax.hist(samples)

        ax.set_ylabel('Frequency',fontweight='bold',fontsize=15)
        ax.set_xlabel('Miss frequency',fontweight='bold',fontsize=15)
        ax.set_title(f'Miss frequency average: {round(sum(samples)/len(samples),5)}',fontweight='bold',fontsize=15)


    print(sum(samples)/len(samples))
    return sum(samples)/len(samples)



def paralysis_testing(runs:int=10000)->None:
    """
        Tests the paralysis rate of Thundershock

        Args:
            runs (int): number of thundershocks to use

        Returns:
            float, paralysis rate

    """
    ## make a thundershock move
    thundershock = make_move('Thundershock')
    ## holds results
    para = []
    ## loop through number of runs, keeping track of how many time thundershock paralyzes
    for i in range(runs):
        para.append(thundershock.does_paralyze())
    print(sum(para)/len(para))
    return sum(para)/len(para)


def burn_testing(runs:int=10000)->None:
    """
        Tests the burn rate of Ember

        Args:
            runs (int): number of embers to use
        Returns:
            float, burn rate

    """

    ## make an Ember move
    ember = make_move('Ember')
    ## holds results
    burn = []
    ## loop through number of runs, keeping track of how many time Ember burns
    for i in range(runs):
        burn.append(ember.does_burn())
    print(sum(burn)/len(burn))

    return sum(burn)/len(burn)


def burn_status_affliction()->None:
    """
        Checks that a burnt pokemon's attack is halved

        Args:
            None

        Returns:
            None

    """

    ## make pokemon and burn it
    bulby = Pokemon('Bulbasaur',5)
    ember = make_move('Ember')
    atk = bulby.battle_stats['Attack'][0]
    ember.burn(bulby)

    ## checks the pokemon's attack is halved but it doesn't have an attack modifier applied
    assert math.floor(atk/2) == bulby.battle_stats['Attack'][0]
    assert bulby.battle_stats['Attack'][1] == 0

def paralysis_status_affliction()->None:
    """
        Checks that a paralyzed pokemon's speed is 3/4 it's original value

        Args:
            None

        Returns:
            None

    """

    ## make pokemon and paralyze it
    charmy = Pokemon('Charmander',5)
    thundershock = make_move('Thundershock')
    spd = charmy.battle_stats['Speed'][0]
    thundershock.paralyze(charmy)

    ## checks the pokemon's speed is 3/4 it's original value and it's speed modifier isn't affected
    assert math.floor(spd*0.75) == charmy.battle_stats['Speed'][0]
    assert charmy.battle_stats['Speed'][1] == 0

def status_affliction()->None:
    """
        Checks a growl status affliction is applied properly

        Args:
            None
        Returns:
            None


    """

    ## make pokemon for testing
    bulby = Pokemon('Bulbasaur',5)
    bulby.set_move('Tackle')

    charmy = Pokemon('Charmander',5)
    charmy.set_move('Ember')
    charmy.set_move('Growl')

    ## use growl and ensure the defending pokemon's attack stat stage is lowered by 1
    charmy.attack(bulby,'Growl')
    assert bulby.battle_stats['Attack'][1] == -1


def paralysis_movement(runs:int=10000)->None:
    """
        Checks the rate at which paralyzed pokemon can move
        Args:
            runs (int): number of possible movements
        Returns:
            float, rate at which paralyzed pokemon is able to move

    """
    ## holds results
    able = []
    ## make pokemon
    bulby = Pokemon('Bulbasaur')
    bulby.status = Paralysis(bulby)
    ## loop through and record when it's able to move and not
    for i in range(runs):
        able.append(bulby.status.can_move())
    print(sum(able)/len(able))
    return sum(able)/len(able)


def test_battle()->None:
    """
        Test a battle

        Args:
            None
        Returns:
            None

    """

    ## make the two Pokemon
    bulby = Pokemon('Squirtle',5)
    bulby.set_move('Tackle')
    bulby.set_move('Tail Whip')

    charmy = Pokemon('Bulbasaur',5)
    charmy.set_move('Scratch')
    charmy.set_move('Growl')

    ## print battle result
    print(battle([bulby,charmy]))

def test_priority()->None:
    """
        Test the priority attribute of Moves

        Args:
            None
        Returns:
            None

    """
    ember = make_move('Ember')
    print(ember.priority)

    quick_attack = make_move('Quick Attack')
    print(quick_attack.priority)



def test_battles(runs:int=10000,normalize=True)->None:
    """
        Test running multiple battles
        Args:
            runs (int): number of battles
            normalize (bool): whether or not to normalize the final results

    """
    ## make pokemon
    pokemon1 = ('Weedle',5,['Poison Sting','String Shot'])
    pokemon2 = ('Eevee',5,['Tackle','Tail Whip'])
    pokemons = (pokemon1,pokemon2)
    ## run battles
    print(battles(pokemons,runs,normalize=normalize))






if __name__ == '__main__':

    ## hit rate testing
    ## Expected ~0.004
    hit_rate_testing()

    ## paralysis testing
    ## Expected ~0.1

    paralysis_testing()


    ## burn testing
    ## Expected ~0.1
    burn_testing()


    burn_status_affliction()
    paralysis_status_affliction()
    status_affliction()

    ## Expected ~0.75
    paralysis_movement()


    test_battle()

    test_battles(normalize=True)
    test_battles(normalize=False)

    test_priority()

















    plt.show()
