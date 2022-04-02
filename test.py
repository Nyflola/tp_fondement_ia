#!/usr/bin/env python3

from game import *
from graph import *

"""
plateau = init()
joueurActuel = 0
graphe = Graphe(plateau,joueurActuel,0)
joueurActuel = abs(joueurActuel - 1)
graphe.get_paliers()
#print(graphe)
#print(graphe.profondeur())
#print(graphe.palier)
graphe.set_poids_graphe()

#print("graphe.sommets = ", [graphe.sommets[i][2] for i in range(len(graphe.sommets))])
print("graphe.sommets = ", [graphe.sommets[i][2] for i in range(len(graphe.sommets))])
print("graphe.sommets avant = ", graphe.sommets)
#print("min-max = ", graphe.min_max())
#print("graphe.sommets = ", [graphe.sommets[i][2] for i in range(len(graphe.sommets))])

print("Il faut jouer le coup : ", graphe.meilleur_coup()) """

plateau = init()
joueurActuel = 0
graphe = Graphe(plateau,joueurActuel,0)
joueurActuel = abs(joueurActuel - 1)
print(graphe)