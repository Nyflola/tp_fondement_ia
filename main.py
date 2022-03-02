#!/usr/bin/env python3

import os
from ai import *
from game import *

def main():
    plateau = init()
    currentPlayer = 0
    while not isGameOver(currentPlayer,plateau):
        os.system('clear')
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