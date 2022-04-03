#!/usr/bin/env python3

from copy import deepcopy
import os
from platform import system
from time import sleep,time
import random
from ai import *
from game import *
from graph import Graphe

profondeur_IA = 1

def calcul_temps(IA1="absolue",IA2="positionnelle"):
    temp_generation_arbre_IA1 = 0
    temps_min_max_IA1 = 0
    nb1 = 0
    moyenne_gen_arbre_IA1 = 0
    moyenne_min_max_IA1 = 0
    temp_generation_arbre_IA2 = 0
    temps_min_max_IA2 = 0
    nb2 = 0
    moyenne_gen_arbre_IA2 = 0
    moyenne_min_max_IA2 = 0

    debut_de_partie = time()
    global profondeur_IA
    tour_IA1 = random.choice([0,1])
    plateau = init()
    currentPlayer = 0
    ncoup = 0
    liste_coups = []
    while not isGameOver(currentPlayer,plateau):
        if currentPlayer == tour_IA1:
            print("Tour IA1, coup n°%d" %(ncoup),end="\r")
            deb = time()
            graphe = Graphe(deepcopy(plateau),currentPlayer,ncoup,IA1,profondeur_IA)
            fin = time()
            temp_generation_arbre_IA1 += fin - deb
            deb = time()
            coup = graphe.meilleur_coup()
            fin = time()
            temps_min_max_IA1 += fin - deb
            nb1 += 1
            if coup != None:
                jouer_coup(currentPlayer,coup,plateau)
            liste_coups.append(coup)
        else:
            print("Tour IA2, coup n°%d, coup possible %d" %(ncoup,len(coups_possibles(currentPlayer,plateau))),end="\r")
            deb = time()
            graphe = Graphe(deepcopy(plateau),currentPlayer,ncoup,IA2,profondeur_IA)
            fin = time()
            temp_generation_arbre_IA2 += fin - deb
            deb = time()
            coup = graphe.meilleur_coup()
            fin = time()
            temps_min_max_IA2 += fin - deb
            nb2 += 1
            if coup != None:
                jouer_coup(currentPlayer,coup,plateau)
            liste_coups.append(coup)
        ncoup += 1
        currentPlayer = (currentPlayer + 1) % 2
    score = playerScore(plateau)
    if score[tour_IA1] > score[abs(tour_IA1-1)]:
        print("\nL'IA n°1 a gagné! %d vs %d" %(score[tour_IA1],score[abs(tour_IA1-1)]))
    else:
        if score[0] == score[1]:
            print("\nLes IAs sont égalitées! %d vs %d" %(score[tour_IA1],score[abs(tour_IA1-1)]))
        else:
            print("\nL'IA n°2 a gagné! %d vs %d" %(score[abs(tour_IA1-1)],score[tour_IA1]))
    fin_de_partie = time()
    clear()
    print("""Statistiques :

Pour l'IA n°1 (%s):
Temps de génération total des graphes: %.4f secs.
Temps de calcul total min max: %.4f secs.
Temps de génération moyen d'un graphe: %.4f secs.
Temps de calcul moyen min max: %.4f secs.

Pour l'IA n°2 (%s):
Temps de génération total des graphes: %.4f secs.
Temps de calcul total min max: %.4f secs.
Temps de génération moyen d'un graphe: %.4f secs.
Temps de calcul moyen min max: %.4f secs.

Temps de partie: %.4f secs.
Nombre de coups: %d""" % (IA1,temp_generation_arbre_IA1,temps_min_max_IA1,temp_generation_arbre_IA1 / nb1,
 temps_min_max_IA1 / nb1, IA2,temp_generation_arbre_IA2,temps_min_max_IA2,temp_generation_arbre_IA2/nb2,
 temps_min_max_IA2/nb2,fin_de_partie-debut_de_partie,len(liste_coups)))
    #print("Résumé des coups joués : " + str(liste_coups))
    return

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
    global profondeur_IA
    clear()
    print("Pour quitter et revenir au menu principal, utilisez le raccourci \"Ctrl + c\"")
    pause()
    clear()
    liste_coups = []
    try:
        menu="""Qui souhaitez voir commencer ?

1) Vous
2) IA
3) Aléatoire

Votre choix: """
        menu_erreur="""Qui souhaitez-vous voir commencer ?

        1) Vous
        2) IA
        3) Aléatoire

        Votre choix (Entre 1 et 3!): """
        choix = input(menu)
        if choix == "1":
            joueur = 0
        if choix == "2":
            joueur = 1
        if choix == "3":
            joueur = random.choice([0,1])
        while choix != "1" and choix != "2" and choix != "3":
            clear()
            choix = input(menu_erreur)
            if choix == "1":
                joueur = 0
            if choix == "2":
                joueur = 1
            if choix == "3":
                random.choice([0,1])
        clear()

        plateau = init()
        currentPlayer = 0
        ncoup = 0
        while not isGameOver(currentPlayer,plateau):
            if currentPlayer == joueur:
                clear()
                affichage(currentPlayer,plateau)
                if len(coups_possibles(currentPlayer,plateau)) == 0:
                    print("Pas de coup possible. Appuyez sur entrée pour continuer")
                    input()
                else:
                    print(str(len(coups_possibles(currentPlayer,plateau))) + " coup(s) possible(s)")   
                    coup = input("Votre coup : ")
                    while not (coup.upper() in [matrixToString(element) for element in coups_possibles(currentPlayer,plateau)]):
                        clear()
                        affichage(currentPlayer,plateau)
                        print(str(len(coups_possibles(currentPlayer,plateau))) + " coup(s) possible(s)")
                        coup = input("Coup non valide.\nRessayez : ")
                    jouer_coup(currentPlayer,coup,plateau)
                    liste_coups.append(coup.upper())
            else:
                clear()
                print("Tour IA")
                affichage(currentPlayer,plateau)
                graphe = Graphe(deepcopy(plateau),currentPlayer,ncoup,IA,profondeur_IA)
                print("Arbre généré")
                coup = graphe.meilleur_coup()
                if coup == None:
                    print("L'IA n'a pas de coups possibles")
                else:
                    print("L'IA joue " + str(coup))
                    jouer_coup(currentPlayer,coup,plateau)
                liste_coups.append(coup.upper())
                pause()
            ncoup += 1
            currentPlayer = (currentPlayer + 1) % 2
        score = playerScore(plateau)
        if score[joueur] > score[abs(joueur-1)]:
            print("\nVous avez gagné!")
        else:
            if score[0] == score[1]:
                print("\nVous êtes égalités!")
            else:
                print("\nL'IA a gagné!")
        print("Résumé des coups joués : " + str(liste_coups))
    except KeyboardInterrupt:
        x = 3
        print("")
        while x > 0:
            print("Retour au menu principal dans " + str(x) + " seconde(s)...", end='\r')
            sleep(1)
            x -= 1
        menu_principal()
    return

def game_IA_vs_IA(IA1,IA2):  
    try:
        clear()
        global profondeur_IA
        tour_IA1 = random.choice([0,1])
        plateau = init()
        currentPlayer = 0
        ncoup = 0
        liste_coups = []
        print("""--------------------------
-     Début de partie    -
--------------------------""")
        affichage(currentPlayer,plateau)
        sleep(2)
        while not isGameOver(currentPlayer,plateau):
            if currentPlayer == tour_IA1:
                clear()
                print("""--------------------------
-       Tour IA n°1      -
--------------------------""")
                affichage(currentPlayer,plateau)
                graphe = Graphe(deepcopy(plateau),currentPlayer,ncoup,IA1,profondeur_IA)
                coup = graphe.meilleur_coup()
                if coup == None:
                    print("L'IA n°1 n'a pas de coups possibles")
                else:
                    print("L'IA n°1 joue " + str(coup))
                    jouer_coup(currentPlayer,coup,plateau)
                liste_coups.append(coup)
                sleep(2)
            else:
                clear()
                print("""--------------------------
-       Tour IA n°2      -
--------------------------""")
                affichage(currentPlayer,plateau)
                graphe = Graphe(deepcopy(plateau),currentPlayer,ncoup,IA2,profondeur_IA)
                coup = graphe.meilleur_coup()
                if coup == None:
                    print("L'IA n°1 n'a pas de coups possibles")
                else:
                    print("L'IA n°1 joue " + str(coup))
                    jouer_coup(currentPlayer,coup,plateau)
                liste_coups.append(coup)
                sleep(2)
            ncoup += 1
            currentPlayer = (currentPlayer + 1) % 2
        score = playerScore(plateau)
        if score[tour_IA1] > score[abs(tour_IA1-1)]:
            print("\nL'IA n°1 a gagné!")
        else:
            if score[0] == score[1]:
                print("\nLes IAs sont égalitées!")
            else:
                print("\nL'IA n°2 a gagné!")
        print("Résumé des coups joués : " + str(liste_coups))
    except KeyboardInterrupt:
        x = 3
        print("")
        while x > 0:
            print("Retour au menu principal dans " + str(x) + " seconde(s)...", end='\r')
            sleep(1)
            x -= 1
        menu_principal()
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

def menu_IA_vs_IA():
    clear()
    menu = """--------------------------
-         Othello        -
--------------------------

IA n°1

1) IA absolue
2) IA positionnelle
3) IA mobilitée
4) IA mixte
5) Quitter

Choix: """
    menu_erreur = """--------------------------
-         Othello        -
--------------------------

IA n°1

1) IA absolue
2) IA positionnelle
3) IA mobilitée
4) IA mixte
5) Quitter

Choix (Entre 1 et 5!): """
    
    choix = input(menu)
    if choix == "1":
        IA1 = "absolue"
    if choix == "2":
        IA1 = "positionelle"
    if choix == "3":
        IA1 = "mobilitee"
    if choix == "4":
        IA1 = "mixte"
    if choix == "5":
        clear()
        exit(0)

    while choix != "1" and choix != "2" and choix != "3":
        clear()
        choix = input(menu_erreur)
        if choix == "1":
            A1 = "absolue"
        if choix == "2":
            IA1 = "positionelle"
        if choix == "3":
            IA1 = "mobilitee"
        if choix == "4":
            IA1 = "mixte"
        if choix == "5":
            clear()
            exit(0)

    clear()
    menu = """--------------------------
-         Othello        -
--------------------------

IA n°2

1) IA absolue
2) IA positionnelle
3) IA mobilitée
4) IA mixte
5) Quitter

Choix: """
    menu_erreur = """--------------------------
-         Othello        -
--------------------------

IA n°2

1) IA absolue
2) IA positionnelle
3) IA mobilitée
4) IA mixte
5) Quitter

Choix (Entre 1 et 5!): """
    
    choix = input(menu)
    if choix == "1":
        IA2 = "absolue"
    if choix == "2":
        IA2 = "positionelle"
    if choix == "3":
        IA2 = "mobilitee"
    if choix == "4":
        IA2 = "mixte"
    if choix == "5":
        clear()
        exit(0)

    while choix != "1" and choix != "2" and choix != "3":
        clear()
        choix = input(menu_erreur)
        if choix == "1":
            IA2 = "absolue"
        if choix == "2":
            IA2 = "positionelle"
        if choix == "3":
            IA2 = "mobilitee"
        if choix == "4":
            IA2 = "mixte"
        if choix == "5":
            clear()
            exit(0)
    clear()
    print("Pour quitter et revenir au menu principal, utilisez le raccourci \"Ctrl + c\"")
    pause()
    clear()
    game_IA_vs_IA(IA1,IA2)

def menu_principal():
    clear()
    menu = """--------------------------
-         Othello        -
--------------------------

1) Jouer "Joueur vs Joueur"
2) Jouer "Joueur vs IA"
3) Regarder "IA vs IA"
4) Quitter

Choix: """
    menu_erreur = """--------------------------
-         Othello        -
--------------------------

1) Jouer "Joueur vs Joueur"
2) Jouer "Joueur vs IA"
3) Regarder "IA vs IA"
4) Quitter

Choix (Entre 1 et 4!): """
    
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
        menu_IA_vs_IA()
    if choix == "4":
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
            menu_IA_vs_IA()
        if choix == "4":
            clear()
            exit(0)

def game():
    try:
        plateau = init()
        currentPlayer = 0
        ncoup = 0
        liste_coups = []
        while not isGameOver(currentPlayer,plateau):
            clear()
            affichage(currentPlayer,plateau)
            if len(coups_possibles(currentPlayer,plateau)) == 0:
                print("Pas de coup possible. Appuyez sur entrée pour continuer")
                input()
            else:
                print(str(len(coups_possibles(currentPlayer,plateau))) + " coup(s) possible(s)")   
                coup = input("Votre coup : ")
                while not (coup.upper() in [matrixToString(element) for element in coups_possibles(currentPlayer,plateau)]):
                    clear()
                    affichage(currentPlayer,plateau)
                    print(str(len(coups_possibles(currentPlayer,plateau))) + " coup(s) possible(s)")
                    coup = input("Coup non valide.\nRessayez : ")
                jouer_coup(currentPlayer,coup,plateau)
                liste_coups.append(coup.upper())
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
        print("Résumé des coups joués : " + str(liste_coups))
    except KeyboardInterrupt:
        x = 3
        print("")
        while x > 0:
            print("Retour au menu principal dans " + str(x) + " seconde(s)...", end='\r')
            sleep(1)
            x -= 1
        menu_principal()

if __name__ == '__main__':
    #menu_principal()
    calcul_temps()