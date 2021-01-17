"""
    Initialization file for the Pokemon Battle Simulator library
    Author: Robert Currie
    Last Updated: January 13, 2021


"""

## import Pokemon objects
from pokemon.objects.Pokemon import(

    Pokemon

)

## import function for adding moves
from pokemon.objects.Moves import(

    make_move

)


## import Paralysis status (for some reason?)
from pokemon.objects.Status import(
    Paralysis
)


## import functions for running battle simulations
from pokemon.objects.Battle import(
     battles
    ,battle
)
