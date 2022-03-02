from game import *

mat_points = [[500,-150,30,10,10,30,-150,500],[-150,-250,0,0,0,0,-250,-150],[30,0,1,2,2,1,0,30],[10,0,2,16,16,2,0,0],[10,0,2,16,16,2,0,0],[30,0,1,2,2,1,0,30],[-150,-250,0,0,0,0,-250,-150],[500,-150,30,10,10,30,-150,500]]

# Retourne la valeur maximale jouable
def max_points(currentPlayer, plateau):
    L_cases = coups_possibles(currentPlayer, plateau)
    n = len(L_cases)
    L_cases_max = []
    if n != 0:
        max = mat_points[L_cases[0][0]][L_cases[0][1]]
        for k in range(1, n):
            if mat_points[L_cases[k]] > max:
                max = mat_points[L_cases[k][0]][L_cases[k][1]]
    return(max)

# Retourne le poids d'un coup, à savoir la différence de points entre les deux coups des joueurs
# Ici, le plateau sera en fait le plateau simulé après que l'IA a joué la case "case_jouée"
def poids_coup(case_jouée, currentPlayer, plateau):
    point_adverse = max_points(currentPlayer, plateau)
    point_case_jouée = mat_points[case_jouée[0]][case_jouée[1]]
    poids = point_adverse - point_case_jouée
    return(poids)

def liste_coups(currentPlayer, plateau):
    cases_possibles_ia = coups_possibles(currentPlayer, plateau)
    n = len(cases_possibles_ia)
    if n != 0:
        mat_coup_apres = plateau.copy()
        jouer_coup(currentPlayer, matrixToString(cases_possibles_ia[0]), mat_coup_apres)
        #A FINIR