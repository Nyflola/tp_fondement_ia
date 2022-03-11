#!/usr/bin/env python3
import numpy as np

class Graphe: # L'objet graphe

    def __init__(self, EI, E, Adj): 
        self.EI = EI # EI = [etat initial 1]
        self.E = E # E = [[indice etat, le plateau, le poids], ...]
        self.Adj = Adj # Adj = [[successeurs de 1], [successeurs de 2], ...]
        self.g = [[], [], []]

    def creation(self):
        self.g = [self.EI, self.E, self.Adj]
    #def ajoutEtatInitial(self, element):
    #self.EI = self.EI + [element]
    #self.g[0] = self.EI

    def ajoutEtat(self, element, plateau, poids):
        self.E = self.E + [[element, plateau, poids]]
        self.g[1] = self.E 

    def ajoutPredecesseur(self, element, pred): # element = element à  ajouter et pred = son predecesseur (indice)
        self.Adj[pred-1] = self.Adj[pred-1] + [element]
        self.Adj = self.Adj + [[]] # instancier la liste des successeurs de element
        self.g[2] = self.Adj

    def ajout(self, element, plateau, pred, poids, initial):
        Graphe.ajoutEtat(self, element, plateau, poids)
        Graphe.ajoutPredecesseur(self, element, pred)
        #if initial:
        #Graphe.ajoutEtatInitial(self, element)

    def modifierPoids(self, Letat, Lpoids):
        n = len(Letat)
        for k in range(n): # Pour chaque etat de E associe le poids correspondant du même indice de Lpoids.
            self.E[Letat[k]-1][2] = Lpoids[k] 
        self.g[1] = self.E
        

    
#print(P)
EI = [1]
E = [[1, [], None], [2, [], None], [3, [], None]] #le plateau en 2ème position
Adj = [[2, 3], [], []]

Graphe_othello = Graphe(EI, E, Adj)
Graphe_othello.creation()
graphe = Graphe_othello.g

print(graphe)

Graphe_othello.ajout(4, [], 1, None, False)

#Graphe_othello.ajoutEtat(4, None)
#Graphe_othello.ajoutPredecesseur(4, 1)
#graphe = Graphe_othello.ajoutEtat(4, None)
#graphe = Graphe_othello.ajoutEtatInitial(4)
#graphe = Graphe_othello.ajoutSuccesseur([1, 2, 3])

graphe = Graphe_othello.g
print(graphe)
    
Graphe_othello.modifierPoids([2, 4], [8, 9]) 
graphe = Graphe_othello.g         
print(graphe)