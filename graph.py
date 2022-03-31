
#!/usr/bin/env python3
import numpy as np
from copy import deepcopy
from ai import mat_points
from game import coups_possibles, playerScore, jouer_coup, matrixToString, affichage


class Graphe:  # L'objet graphe

    def __init__(self,plateau,joueurActuel, ncoup, IA = "absolue", profondeur = 1):
        self.idMax = 0 # Indice max utilisé en tant qu'idSommet (utilisé pour la création de sommet)
        self.etatInitial = 0
        self.sommets = [[self.idMax,plateau,"None",joueurActuel]]
        self.successeurs = [[]] # [ [ [1 4], [2 9] ], [] ]
        self.IA = IA
        
        current = [self.etatInitial]
        next = []
        joueurSuivant = abs(joueurActuel-1)
        while self.profondeur() != profondeur:
            for sommet in current:
                #print("sommet " + str(sommet))
                plateau = self.get_plateau(sommet)
                coups = coups_possibles(joueurActuel,plateau)
                for coup in coups:
                    #print("coup " + str(coup))
                    nouveau_plateau = deepcopy(plateau)
                    jouer_coup(joueurActuel,matrixToString(coup),nouveau_plateau)
                    next.append(self.ajout_Sommet(nouveau_plateau,joueurSuivant,IA,sommet,matrixToString(coup),ncoup))
            current = next
            next = []
            joueurActuel = joueurSuivant
            joueurSuivant = abs(joueurActuel-1)
        return

    def ajout_Sommet(self,plateau,joueur, IA,idpredecesseur,coup, ncoup):
        self.idMax = self.idMax + 1
        nouveau_sommet = [self.idMax,plateau, "None" , joueur]
        nouveau_successeur = [idpredecesseur,coup]
        self.sommets += [nouveau_sommet] 
        self.successeurs[idpredecesseur] += [[self.idMax,coup]] 
        self.successeurs += [[]]
        #self.evaluation_sommet(ncoup,IA,self.idMax,self.coup(self.idMax),joueur)
        return self.idMax

    def get_predecesseur(self,idSommet):
        for successeur in self.successeurs:
            for element in successeur:
                if element[0] == idSommet:
                    return self.successeurs.index(successeur)
        return None

    def get_successeurs(self,idSommet):
        successeurs = []
        for element in self.successeurs[idSommet]:
            successeurs += [element[0]]
        return successeurs

    def get_plateau(self,idSommet):
        return self.sommets[idSommet][1]

    def get_coup(self,idSommet):
        for successeur in self.successeurs:
            for element in successeur:
                if element[0] == idSommet:
                    return element[1]
        return

    def profondeur(self, idSommet = 0):
        succ = self.get_successeurs(idSommet)
        if idSommet == 0 and len(succ) == 0:
            return 0
        if len(succ) == 0:
            return 0
        temp = 0
        for s in succ:
            temp = max(temp,self.profondeur(s))
        return 0.5 + temp
        
    def modifierPoids(self, Letat, Lpoids):
        n = len(Letat)
        # Pour chaque etat de E associe le poids correspondant du même indice de Lpoids.
        for k in range(n):
            self.E[Letat[k]-1][2] = Lpoids[k]
        self.g[1] = self.E

    def evaluation_positionnel(self, coupMatrix):
        return mat_points[coupMatrix]

    def evaluation_mobilite(self, idsommet, coupMatrix, currentPlayer):
        plateau = self.g[1][idsommet][2]
        return len(coups_possibles(currentPlayer, plateau))

    def evaluation_absolue(self, idsommet, coupMatrix, currentPlayer):
        plateau_bis = self.g[1][idsommet][2]
        plateau = plateau_bis.copy
        jouer_coup(currentPlayer, matrixToString(coupMatrix), plateau)
        return (playerScore(plateau)[currentPlayer] - playerScore(plateau)[abs(currentPlayer-1)])

    def evaluation_sommet(self, ncoup, ia, idsommet, coupMatrix, currentPlayer):
        if ia == "positionnelle" or (ia == "mixte" and ncoup < 24):
            return Graphe.evaluation_positionnel(coupMatrix)
        if ia == "mobilitee" or (ia == "mixte" and ncoup < 44):
            return Graphe.evaluation_mobilite(idsommet, coupMatrix, currentPlayer)
        if ia == "absolue" or (ia == "mixte" and ncoup > 43):
            return Graphe.evaluation_absolue(idsommet, coupMatrix, currentPlayer)

    def __str__(self):
        for sommet in self.sommets:
            print("---------------------------------")
            if sommet[0] != 0:
                print("Sommet n°"+ str(sommet[0])+"\nCoup qui a été joué: "+ self.get_coup(sommet[0]) + "\nSommet précedent: " + str(self.get_predecesseur(sommet[0])) + "\nPoids (selon IA \"" +self.IA + "\"): " + str(sommet[2]) + "\n\nEtat du plateau :")
            else:
                print("Etat initial\nEtat du plateau :")
            affichage(sommet[3],sommet[1])
        return ""

    # renvoie la liste [[sommets de hauteur 1], [sommets de hauteur 2], ..., [sommets de hauteur n]]
    def palier(self):
        L_paliers = [[1]]
        L_adj = self.g[2]
        n = len(self.g[1])  # le  nombre de sommets du graphe
        k = 1
        while k < n:
            L_paliers = L_paliers + [[]]
            for i in range(len(L_paliers[-2])):
                L_paliers[-1] = L_paliers[-1] + L_adj[L_paliers[-2][i]-1]
                k += len(L_adj[L_paliers[-2][i]-1])
        return L_paliers

    # Renvoie la liste des poids des sommets de la liste à indices égaux
    def poids_liste(self, L):
        pds = []
        for k in range(len(L)):
            pds = pds + [self.g[1][L[k]-1][2]]
        return pds

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
                    if len(poids > 0):
                        if ((n-k)/2 - (n-k)//2 == 0 and tmax == False) or (((n-k)/2 - (n-k)//2 != 0 and tmax)):
                            self.g[1][paliers[-(k+2)][i]-1][2] = max(poids)
                        else:
                            self.g[1][paliers[-(k + 2)][i] - 1][2] = min(poids)

