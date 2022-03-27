#!/usr/bin/env python3
import numpy as np
from ai import mat_points
from game import coups_possibles, playerScore, jouer_coup, matrixToString


class Graphe: # L'objet graphe

    def __init__(self, EI, E, Adj, plateau): 
        self.EI = EI # EI = [etat initial 1]
        self.E = E # E = [[indice etat, le plateau, le poids, le joueur qui joue], ...]
        self.Adj = Adj # Adj = [[successeurs de 1], [successeurs de 2], ...]
        self.g = [[], [], []]
        self.plateau = plateau

    def creation(self):
        self.g = [self.EI, self.E, self.Adj]
    #def ajoutEtatInitial(self, element):
    #self.EI = self.EI + [element]
    #self.g[0] = self.EI

    def ajoutEtat(self, element, plateau, poids, joueur):
        self.E = self.E + [[element, plateau, poids, joueur]]
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

    #renvoie la liste [[sommets de hauteur 1], [sommets de hauteur 2], ..., [sommets de hauteur n]]
    def palier(self):
        L_paliers = [[1]]
        L_adj = self.g[2]
        n = len(self.g[1]) #le  nombre de sommets du graphe
        k = 1
        while k < n:
            L_paliers = L_paliers + [[]]
            for i in range(len(L_paliers[-2])):
                L_paliers[-1] = L_paliers[-1] + L_adj[L_paliers[-2][i]-1]
                k += len(L_adj[L_paliers[-2][i]-1])
        return L_paliers

    def poids_liste(self, L):
        pds = []
        for k in range(len(L)):
            pds = pds + [self.g[1][L[k]-1][2]]
        return pds

    #def predecesseur(self, sommet, graphe):
    #    for i in range(graphe[2]):
    #        for k in range(graphe[2][i]):
    #            if graphe[2][i][k] == sommet:
    #                return graphe[2][i][k]

    def min_max(self, ia, joueurTour):
        paliers = Graphe.palier()
        tmax = False
        n = len(paliers)
        if ia == joueurTour:
            tmax = True
        if len(paliers) == 1:
            return self.g[1][0][2]
        else:
            for k in range(len(paliers)-1):
                for i in range(len(paliers[-(k+2)])):
                    poids = Graphe.poids_liste(self.g[2][paliers[-(k+2)][i]-1])
                    if len(poids>0):
                        if ((n-k)/2 - (n-k)//2 == 0 and tmax == False) or (((n-k)/2 - (n-k)//2 != 0 and tmax)):
                            self.g[1][paliers[-(k+2)][i]-1][2] = - max(poids) #il faut inverser le signe du poids en fonction du point de vue qu'on prend (+ si c'est l'ia, - si c'est l'adversaire)
                        else:
                            self.g[1][paliers[-(k + 2)][i] - 1][2] = - min(poids)







        

    
#print(P)
#EI = [1]
#E = [[1, [], None], [2, [], None], [3, [], None]] #le plateau en 2ème position
#Adj = [[2, 3], [], []]

#Graphe_othello = Graphe(EI, E, Adj)
#Graphe_othello.creation()
#graphe = Graphe_othello.g

#print(graphe)

#Graphe_othello.ajout(4, [], 1, None, False)

#Graphe_othello.ajoutEtat(4, None)
#Graphe_othello.ajoutPredecesseur(4, 1)
#graphe = Graphe_othello.ajoutEtat(4, None)
#graphe = Graphe_othello.ajoutEtatInitial(4)
#graphe = Graphe_othello.ajoutSuccesseur([1, 2, 3])

#graphe = Graphe_othello.g
#print(graphe)
    
#Graphe_othello.modifierPoids([2, 4], [8, 9])
#graphe = Graphe_othello.g
#print(graphe)

