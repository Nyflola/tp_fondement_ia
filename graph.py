#!/usr/bin/env python3
import numpy as np
from ai import mat_points
from game import coups_possibles, playerScore, jouer_coup, matrixToString


class Graphe: # L'objet graphe

    def __init__(self, EI, E, Adj, plateau): 
        self.EI = EI # EI = [etat initial 1]
        self.E = E # E = [[indice etat, le plateau, le poids], ...]
        self.Adj = Adj # Adj = [[successeurs de 1], [successeurs de 2], ...]
        self.g = [[], [], []]
        self.plateau = plateau

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

    def evaluation_positionnel(self, coupMatrix):
        return mat_points[coupMatrix]

    def evaluation_mobilite(self, idsommet, coupMatrix, currentPlayer):
        plateau = self.g[1][idsommet][2]
        return len(coups_possibles(currentPlayer,plateau))
    
    def evaluation_absolue(self, idsommet, coupMatrix, currentPlayer):
        plateau_bis = self.g[1][idsommet][2]
        plateau = plateau_bis.copy
        jouer_coup(currentPlayer, matrixToString(coupMatrix), plateau)
        return (playerScore(plateau)[currentPlayer] - playerScore(plateau)[abs(currentPlayer-1)])

    def evaluation_sommet(self, ncoup, ia, idsommet, coupMatrix, currentPlayer):
        if ia == "positionnel" or (ia == "mixte" and ncoup < 24):
            return Graphe.evaluation_positionnel(coupMatrix)
        if ia == "mobilité" or (ia == "mixte" and ncoup < 44):
            return Graphe.evaluation_mobilite(idsommet, coupMatrix, currentPlayer)
        if ia == "absolue" or (ia == "mixte" and ncoup > 43):
            return Graphe.evaluation_absolue(idsommet, coupMatrix, currentPlayer)





        

    
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

