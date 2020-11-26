from pokemon import Pokemon,makeMove,Paralysis,battle,battles
import matplotlib.pyplot as plt




if __name__ == '__main__':
    bulby = Pokemon('Bulbasaur',5)
    bulby.setMove('Tackle')
    
    charmy = Pokemon('Charmander',5)
    charmy.setMove('Ember')
    charmy.setMove('Growl')
    
    
    
    ## hit rate testing
    
    samples = []
    for i in range(2000):
        hits = []
        for i in range(1000):
            hits.append(bulby.missAttack(charmy,bulby.moves['Tackle']))
    
     
        samples.append(sum(hits)/len(hits))

    fig,ax = plt.subplots(1)
    ax.hist(samples)

    ax.set_ylabel('Frequency',fontweight='bold',fontsize=15)
    ax.set_xlabel('Miss frequency',fontweight='bold',fontsize=15)
    ax.set_title(f'Miss frequency average: {round(sum(samples)/len(samples),5)}',fontweight='bold',fontsize=15)

    
    
    ## paralysis testing
    # Expected ~0.1
    
    thundershock = makeMove('Thundershock')
    para = []
    for i in range(10000):
        para.append(thundershock.doesParalyze())
    print(sum(para)/len(para))
    
    ## burn testing
    ## Expected ~0.1
    
    
    ember = makeMove('Ember')
    burn = []
    for i in range(10000):
        burn.append(ember.doesBurn())
    print(sum(burn)/len(burn))
    
    
    print(bulby.battleStats)
    ember.burn(bulby)
    print(bulby.battleStats)
    
    print(charmy.battleStats)
    thundershock.paralyze(charmy)
    print(charmy.battleStats)
    
    
    charmy.attack(bulby,'Growl')
    
    print(bulby.battleStats)
    
    
    ## Expected ~0.75
    
    able = []
    bulby = Pokemon('Bulbasaur')
    bulby.status = Paralysis(bulby)
    for i in range(100000):
        able.append(bulby.status.canMove())
    print(sum(able)/len(able))
    
    
    bulby = Pokemon('Squirtle',5)
    bulby.setMove('Tackle')
    bulby.setMove('Tail Whip')


    charmy = Pokemon('Bulbasaur',5)
    charmy.setMove('Scratch')
    charmy.setMove('Growl')
    
    print(battle([bulby,charmy]))
    
    
    pokemon1 = ('Pikachu',5,['Thundershock','Growl'])
    pokemon2 = ('Eevee',5,['Tackle','Tail Whip'])
    pokemons = (pokemon1,pokemon2)
    print(battles(pokemons,10000))

    
    plt.show()

    
    