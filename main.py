#!/usr/bin/env python3

import os
from platform import system
from time import sleep
from ai import *
from game import *

def clear():
    if system() == 'Linux':
        os.system('clear')
    else:
        if system() == 'Windows':
            os.system('cls')

def pause():
    input("\nAppuyez sur une entrée pour continuer...")
    return


def game_IA(IA):
    return

def menu_IA():
    clear()
    menu = """--------------------------
-         Othello        -
--------------------------

1) IA absolue
2) IA positionnelle
3) IA mobilitée
4) IA mixte
5) Quitter

Choix: """
    menu_erreur = """--------------------------
-         Othello        -
--------------------------

1) IA absolue
2) IA positionnelle
3) IA mobilitée
4) IA mixte
5) Quitter

Choix (Entre 1 et 5!): """
    
    choix = input(menu)
    if choix == "1":
        clear()
        game_IA("absolue")
    if choix == "2":
        clear()
        game_IA("positionelle")
    if choix == "3":
        clear()
        game_IA("mobilitee")
    if choix == "4":
        clear()
        game_IA("mixte")
    if choix == "5":
        clear()
        exit(0)

    while choix != "1" and choix != "2" and choix != "3":
        clear()
        choix = input(menu_erreur)
        if choix == "1":
            clear()
            game_IA("absolue")
        if choix == "2":
            clear()
            game_IA("positionelle")
        if choix == "3":
            clear()
            game_IA("mobilitee")
        if choix == "4":
            clear()
            game_IA("mixte")
        if choix == "5":
            clear()
            exit(0)
    return

def menu_principal():
    clear()
    menu = """--------------------------
-         Othello        -
--------------------------

1) Jouer "Joueur vs Joueur"
2) Jouer "Joueur vs IA"
3) Quitter

Choix: """
    menu_erreur = """--------------------------
-         Othello        -
--------------------------

1) Jouer "Joueur vs Joueur"
2) Jouer "Joueur vs IA"
3) Quitter

Choix (Entre 1 et 3!): """
    
    choix = input(menu)
    if choix == "1":
        clear()
        print("Pour quitter et revenir au menu principal, utilisez le raccourci \"Ctrl + c\"")
        pause()
        clear()
        game()
    if choix == "2":
        clear()
        menu_IA()
    if choix == "3":
        clear()
        exit(0)

    while choix != "1" and choix != "2" and choix != "3":
        clear()
        choix = input(menu_erreur)
        if choix == "1":
            clear()
            print("Pour quitter et revenir au menu principal, utilisez le raccourci \"Ctrl + c\"")
            pause()
            clear()
            game()
        if choix == "2":
            clear()
            menu_IA()
        if choix == "3":
            clear()
            exit(0)

def menu_principal():
    clear()
    menu = """--------------------------
-         Othello        -
--------------------------

1) Jouer "Joueur vs Joueur"
2) Jouer "Joueur vs IA"
3) Quitter

Choix: """
    menu_erreur = """--------------------------
-         Othello        -
--------------------------

1) Jouer "Joueur vs Joueur"
2) Jouer "Joueur vs IA"
3) Quitter

Choix (Entre 1 et 3!): """
    
    choix = input(menu)
    if choix == "1":
        clear()
        print("Pour quitter et revenir au menu principal, utilisez le raccourci \"Ctrl + c\"")
        pause()
        clear()
        game()
    if choix == "2":
        clear()
        menu_IA()
    if choix == "3":
        clear()
        exit(0)

    while choix != "1" and choix != "2" and choix != "3":
        clear()
        choix = input(menu_erreur)
        if choix == "1":
            clear()
            print("Pour quitter et revenir au menu principal, utilisez le raccourci \"Ctrl + c\"")
            pause()
            clear()
            game()
        if choix == "2":
            clear()
            menu_IA()
        if choix == "3":
            clear()
            exit(0)

def game():
    try:
        plateau = init()
        currentPlayer = 0
        ncoup = 0
        while not isGameOver(currentPlayer,plateau):
            clear()
            affichage(currentPlayer,plateau)
            if len(coups_possibles(currentPlayer,plateau)) == 0:
                print("Pas de coup possible. Appuyez sur entrée pour continuer")
                input()
            else:
                print(str(len(coups_possibles(currentPlayer,plateau))) + " coup(s) possible(s)")   
                coup = input("Votre coup : ")
                print((coup.upper() in [matrixToString(element) for element in coups_possibles(currentPlayer,plateau)]))
                while not (coup.upper() in [matrixToString(element) for element in coups_possibles(currentPlayer,plateau)]):
                    clear()
                    affichage(currentPlayer,plateau)
                    print(str(len(coups_possibles(currentPlayer,plateau))) + " coup(s) possible(s)")
                    coup = input("Coup non valide.\nRessayez : ")
                jouer_coup(currentPlayer,coup,plateau)
            
            if currentPlayer == 1:
                ncoup += 1
            currentPlayer = (currentPlayer + 1) % 2
        score = playerScore(plateau)
        if score[0] > score[1]:
            print("\nLes blancs ont gagné!")
        else:
            if score[0] == score[1]:
                print("\nLes joueurs sont égalités!")
            else:
                print("\nLes noirs ont gagné!")
    except KeyboardInterrupt:
        x = 3
        print("")
        while x > 0:
            print("Retour au menu principal dans " + str(x) + " seconde(s)...", end='\r')
            sleep(1)
            x -= 1
        menu_principal()

if __name__ == '__main__':
    menu_principal()