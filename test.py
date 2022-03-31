#!/usr/bin/env python3

from game import *
from graph import *


plateau = init()
joueurActuel = 0
graphe = Graphe(plateau,joueurActuel,0)
joueurActuel = abs(joueurActuel - 1)
print(graphe)
print(graphe.profondeur())