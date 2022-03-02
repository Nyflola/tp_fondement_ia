#!/usr/bin/env python3

import os


nbLigne = 8
nbColonne = 8

# Conversion d'un coup de forme string (ex: "a1") sous format matrice (ex: [0,0])
def stringToMatrix(coupString):
    return [int(coupString[1]) - 1, ord(coupString.upper()[0]) - ord('A')]

# Conversion d'un coup de forme matrice (ex: [0,0]) sous format string (ex: "a1")
def matrixToString(coupMatrix):
    return chr(coupMatrix[1]+ ord('A')) + str(coupMatrix[0] + 1)

# Affiche le plateau dans la console
def affichage(joueur,plateau):
    numLigne = 1
    print("    a b c d e f g h")
    for ligne in range(nbLigne):
        print(str(numLigne) + " |", end=" ")
        for colonne in range(nbColonne):
            if plateau[ligne][colonne] != None:
                if plateau[ligne][colonne] == 0:
                    print("B", end=" ")
                else:
                    print("N", end=" ")
            else:
                if coup_valide(joueur,[ligne,colonne],plateau):
                    print("x", end=" ")
                else:
                    print(".", end=" ")
        if ligne == 0:
            score = playerScore(plateau)
            print("|\tScore: (Blancs) " + str(score[0]) + " vs " + str(score[1]) + " (Noirs)")
        else:
            if ligne == 2:
                if joueur == 0:
                    print("|\tTrait aux blancs")
                else:
                    print("|\tTrait aux noirs")
            else:
                print("|")
        numLigne = numLigne + 1
    print("")
    return

# Retourne tous les coups possibles
def coups_possibles(currentPlayer,plateau):
    coups = []
    for i in range(nbLigne):
        for j in range(nbColonne):
            if coup_valide(currentPlayer,[i,j],plateau):
                coups.append([i,j])
    return coups

# Initialise le plateau
def init():
    global nbLigne
    global nbColonne
    plateau = [[None for x in range(nbColonne)] for y in range(nbLigne)]
    plateau[3][3] = 0
    plateau[4][4] = 0
    plateau[4][3] = 1
    plateau[3][4] = 1

    return plateau

def debug():
    plateau = [[0,0,0,0,0,1,1,1],[0,0,0,0,1,0,1,1],[0,0,0,0,0,1,1,0],[0,0,0,0,1,1,0,0],[0,0,0,0,1,0,0,0],[1,0,0,0,1,0,0,0],[1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,None]]
    return plateau

# Indique si le coup est valide
def coup_valide(joueur, coupMatrix, plateau):
    global nbLigne
    global nbColonne

    if coupMatrix[0] < 0 or coupMatrix[0] >= 8 or coupMatrix[1] < 0 or coupMatrix[1] >= 8 or plateau[coupMatrix[0]][coupMatrix[1]] != None:
        return False

    voisins = []
    for i in range(-1,2):
        if coupMatrix[0] + i >= 0 and coupMatrix[0] + i < 8:
            for j in range(-1,2):
                if coupMatrix[1] + j >= 0 and coupMatrix[1] + j < 8:
                    if not (i ==  0 and j == 0):
                        voisins.append([coupMatrix[0] + i,coupMatrix[1] + j])

    for voisin in voisins:
        ligne = voisin[0] - coupMatrix[0]
        colonne = voisin[1] - coupMatrix[1]

        current_pawn_i = coupMatrix[0] + ligne
        current_pawn_j = coupMatrix[1] + colonne
        nb_pion = 0
        while current_pawn_i >= 0 and current_pawn_i < 8 and current_pawn_j >= 0 and current_pawn_j < 8 and plateau[current_pawn_i][current_pawn_j] != joueur and plateau[current_pawn_i][current_pawn_j] != None:
            current_pawn_i = current_pawn_i + ligne
            current_pawn_j = current_pawn_j + colonne
            nb_pion += 1
            #print(current_pawn_i,current_pawn_j)
            if current_pawn_i >= 0 and current_pawn_i < 8 and current_pawn_j >= 0 and current_pawn_j < 8 and plateau[current_pawn_i][current_pawn_j] == joueur:
                return True
    return False

# Retourne les pions récemment capturés
def update_board(coupMatrix,plateau):
    voisins = []
    for i in range(-1,2):
        if coupMatrix[0] + i >= 0 and coupMatrix[0] + i < 8:
            for j in range(-1,2):
                if coupMatrix[1] + j >= 0 and coupMatrix[1] + j < 8:
                    if not (i ==  0 and j == 0) and plateau[coupMatrix[0] + i][coupMatrix[1] + j] != None:
                        voisins.append([coupMatrix[0] + i,coupMatrix[1] + j])
    
    to_flip = []
    temp = []
    joueur = plateau[coupMatrix[0]][coupMatrix[1]]
    for voisin in voisins:
        ligne = voisin[0] - coupMatrix[0]
        colonne = voisin[1] - coupMatrix[1]

        current_pawn_i = coupMatrix[0] + ligne
        current_pawn_j = coupMatrix[1] + colonne
        nb_pion = 0
        temp = [[current_pawn_i,current_pawn_j]]
        while current_pawn_i >= 0 and current_pawn_i < 8 and current_pawn_j >= 0 and current_pawn_j < 8 and plateau[current_pawn_i][current_pawn_j] != joueur and plateau[current_pawn_i][current_pawn_j] != None:
            current_pawn_i = current_pawn_i + ligne
            current_pawn_j = current_pawn_j + colonne
            nb_pion += 1
            if current_pawn_i >= 0 and current_pawn_i < 8 and current_pawn_j >= 0 and current_pawn_j < 8 and plateau[current_pawn_i][current_pawn_j] == joueur:
                for element in temp:
                    to_flip.append(element)
            temp.append([current_pawn_i,current_pawn_j])
    for coup in to_flip:
        plateau[coup[0]][coup[1]] = joueur
        
    #print([matrixToString(element) for element in to_flip])
    return

# Permet au joueur actuel de jouer un coup valide
def jouer_coup(joueur, coupString, plateau):
    #print("ouiiiiiiiiii")
    coupMatrix = stringToMatrix(coupString)
    #print("Je joue " + coupString)
    plateau[coupMatrix[0]][coupMatrix[1]] = joueur
    update_board(coupMatrix,plateau)

# Indique si la partie est fini
def isGameOver(currentPlayer,plateau):
    if len(coups_possibles(currentPlayer,plateau)) == 0 and len(coups_possibles((currentPlayer + 1)%2,plateau)) == 0:
        return True
    return False

# Retourne le score de chaque joueur
def playerScore(plateau):
    score_white = 0
    score_black = 0
    for i in range(nbLigne):
        for j in range(nbColonne):
            if plateau[i][j] == 0:
                score_white += 1
            else:
                if plateau[i][j] == 1:
                    score_black += 1
    return [score_white,score_black]

def main():
    plateau = debug()

    #J1 commence (J1 Blanc, J2 Noir)
    currentPlayer = 0

    while not isGameOver(currentPlayer,plateau):
        os.system('clear')
        #print([matrixToString(element) for element in coups_possibles(currentPlayer,plateau)])
        affichage(currentPlayer,plateau)
        if len(coups_possibles(currentPlayer,plateau)) == 0:
            print("Pas de coup possible. Appuyez sur entrée pour continuer")
            input()
        else:
            print(str(len(coups_possibles(currentPlayer,plateau))) + " coup(s) possible(s)")   
            coup = input("Votre coup : ")
            print((coup.upper() in [matrixToString(element) for element in coups_possibles(currentPlayer,plateau)]))
            while not (coup.upper() in [matrixToString(element) for element in coups_possibles(currentPlayer,plateau)]):
                os.system('clear')
                affichage(currentPlayer,plateau)
                print(str(len(coups_possibles(currentPlayer,plateau))) + " coup(s) possible(s)")
                coup = input("Coup non valide.\nRessayez : ")
            jouer_coup(currentPlayer,coup,plateau)
            
        currentPlayer = (currentPlayer + 1) % 2
    score = playerScore(plateau)
    if score[0] > score[1]:
        print("\nLes blancs ont gagné!")
    else:
        if score[0] == score[1]:
            print("\nLes joueurs sont égalités!")
        else:
            print("\nLes noirs ont gagné!")

main()