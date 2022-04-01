#!/usr/bin/env python3

from game import *
from graph import *


plateau = init()
joueurActuel = 0
graphe = Graphe(plateau,joueurActuel,0)
joueurActuel = abs(joueurActuel - 1)
graphe.get_paliers()
#print(graphe)
#print(graphe.profondeur())
#print(graphe.palier)

#print("graphe.sommets avant = ", graphe.sommets)
#print("min-max = ", graphe.min_max(True))
#print("graphe.sommets = ", [graphe.sommets[i][2] for i in range(len(graphe.sommets))])