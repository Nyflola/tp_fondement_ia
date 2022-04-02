
#!/usr/bin/env python3
import numpy as np
from copy import deepcopy
from ai import mat_points
from game import coups_possibles, playerScore, jouer_coup, matrixToString, affichage, stringToMatrix


class Graphe:  # L'objet graphe

    def __init__(self,plateau,joueurActuel, ncoup, IA = "positionnelle", profondeur = 1):
        self.idMax = 0 # Indice max utilisé en tant qu'idSommet (utilisé pour la création de sommet)
        self.etatInitial = 0
        self.sommets = [[self.idMax,plateau,"None",joueurActuel]]
        self.successeurs = [[]] # [ [ [1 4], [2 9] ], [] ]
        self.IA = IA
        self.palier = [1]
        
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
        self.sommets[self.idMax][2] = self.evaluation_sommet(ncoup, IA, self.idMax, stringToMatrix(self.get_coup(self.idMax)), abs(joueur - 1))
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
        return None

    def get_poids(self, idSommet):
        return self.sommets[idSommet][2]

    def set_poids(self, idSommet, poids):
        self.sommets[idSommet][2] = poids
        return None


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

    def evaluation_positionnel(self, coupMatrix): #On regarde les points de la case que l'on vient de jouer
        if coupMatrix == None:
            return 0
        return -mat_points[coupMatrix[0]][coupMatrix[1]]

    def evaluation_mobilite(self, idsommet, currentPlayer): #On regarde le nombre de coups possibles à  ce tour (donc au plateau auquel on regarde)
        plateau = self.sommets[idsommet][1]
        return -len(coups_possibles(currentPlayer, plateau))

    def evaluation_absolue(self, idsommet, currentPlayer, idIA): #On regarde la différence de pions entre les deux joueurs du point de vue de l'IA
        plateau = self.sommets[idsommet][1]
        if currentPlayer == idIA:
            return -(playerScore(plateau)[currentPlayer] - playerScore(plateau)[abs(currentPlayer-1)])
        else:
            return (playerScore(plateau)[currentPlayer] - playerScore(plateau)[abs(currentPlayer - 1)])

    def evaluation_sommet(self, ncoup, ia, idsommet, coupMatrix, currentPlayer):
        if ia == "positionnelle" or (ia == "mixte" and ncoup < 24):
            return self.evaluation_positionnel(coupMatrix)
        if ia == "mobilitee" or (ia == "mixte" and ncoup < 44):
            return self.evaluation_mobilite(idsommet,  currentPlayer)
        if ia == "absolue" or (ia == "mixte" and ncoup > 43):
            return self.evaluation_absolue(idsommet, currentPlayer, abs(self.sommets[0][3] - 1))

    def set_poids_graphe(self):
        n = len(self.sommets)
        for k in range(n):
            player= self.sommets[k][3]
            poids_k = self.evaluation_sommet(int(2*self.profondeur(0)), self.IA, k, self.get_coup(k), player)
            self.set_poids(k, poids_k)

    def __str__(self):
        for sommet in self.sommets:
            print("---------------------------------")
            if sommet[0] != 0:
                print("Sommet n°"+ str(sommet[0])+"\nCoup qui a été joué: "+ self.get_coup(sommet[0]) + "\nSommet précedent: " + str(self.get_predecesseur(sommet[0])) + "\nPoids (selon IA \"" +self.IA + "\"): " + str(sommet[2]) + "\n\nEtat du plateau :")
            else:
                print("Etat initial\nEtat du plateau :")
            affichage(sommet[3],sommet[1])
        #print(self.palier)
        return ""

    # renvoie la liste [[sommets de hauteur 1], [sommets de hauteur 2], ..., [sommets de hauteur n]]
    def get_paliers(self):
        self.palier = [[self.sommets[0][0]]]
        L_adj = self.successeurs
        for k in range(int(2*self.profondeur(self.palier[0][0]))):
            self.palier = self.palier + [[]]
            for i in range(len(self.palier[-2])):
                for j in range(len(L_adj[self.palier[-2][i]])):
                    self.palier[-1] = self.palier[-1] + [L_adj[self.palier[-2][i]][j][0]]
        return None

    # Renvoie la liste des poids des sommets de la liste à indices égaux
    def poids_liste(self, L):
        pds = []
        for k in range(len(L)):
            pds = pds + [self.get_poids(L[k])]
        return pds

    def tour_pair(self, tour):
        return(tour//2 == tour/2)

    def inverse_liste(self, L):
        Lb = L.copy()
        Lc = []
        for k in range(len(L)):
            Lc = [Lb[k]] + Lc
        return(Lc)

    def max_avec_indice(self, L):
        maxi = [L[0], 0]
        for k in range(len(L)):
            if L[k] > maxi[0]:
                maxi = [L[k], k]
        return maxi

    def min_avec_indice(self, L):
        mini = [L[0], 0]
        for k in range(len(L)):
            if L[k] > mini[0]:
                mini = [L[k], k]
        return mini

    def min_max(self):
        n = len(self.palier)
        L = [i for i in range(len(self.sommets))]
        palier_inverse = self.inverse_liste(self.palier)
        for k in range(1, n):
            L_palier_actuel = palier_inverse[k]
            for i in L_palier_actuel:
                L_succ = self.get_successeurs(i)
                L_poids = self.poids_liste(L_succ)
                if (self.tour_pair(k) == False):
                    maxi = self.max_avec_indice(L_poids)
                    self.set_poids(maxi[1], maxi[0])
                    L[i] = L_succ[maxi[1]]
                else:
                    mini = self.min_avec_indice(L_poids)
                    self.set_poids(mini[1], mini[0])
                    L[i] = L_succ[mini[1]]

        L_coups = [0]
        for m in range(n-1):
            L_coups = L_coups + [L[L_coups[m]]]

        return L_coups

    def meilleur_coup(self):
        L = self.min_max()
        return self.get_coup(L[1])




