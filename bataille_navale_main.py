"""
moteur jeu de bataille navale
Léo Gaspari, 20/12/2020
"""

"""Ce programme est le moteur du jeu. Il ne permet pas d'afficher quoi que ce soit. 
Pour lancer le jeu en mode console, exécutez le script 'bataille_navale_console.py'.
Pour lancer le jeu en mode interface graphique, exécutez le script 'bataille_navale_graphique.py'.
"""

import random
import time

largeur = 10
hauteur = 10
cases_joueur = [[0 for k in range(largeur)] for i in range(hauteur) ] #grille des bateaux du joueur ainsi que les tires de l'ordinateur
cases_ordi = [[0 for k in range(largeur)] for i in range(hauteur) ] #grille des bateaux de l'ordinateur
grille_coup_joueur = [[0 for k in range(largeur)] for i in range(hauteur) ] #grille des coup du joueur

nb_bateau_4 = 2
nb_bateau_3 = 2
nb_bateau_2 = 2
nb_bateau = nb_bateau_2 + nb_bateau_3 + nb_bateau_4 #permet de compter rapidement le nombre de bateaux plaçables. Les variables sont donc modifiables afin de changer le nombre de bateaux plaçables en fonction de leur taille
nb_bateau_total = nb_bateau
liste_bateaux = [None for k in range(nb_bateau)] #permet de stocker toutes les postions de chaques cases des bateaux du joueur

nb_bateau_2_ordi = nb_bateau_2
nb_bateau_3_ordi = nb_bateau_3
nb_bateau_4_ordi = nb_bateau_4
nb_bateau_ordi = nb_bateau_2_ordi + nb_bateau_3_ordi + nb_bateau_4_ordi #permet de compter rapidement le nombre de bateaux plaçables. Les variables sont donc modifiables afin de changer le nombre de bateaux plaçables en fonction de leur taille
liste_bateaux_ordi = [None for k in range(nb_bateau_ordi)] #permet de stocker toutes les postions de chaques cases des bateaux de l'ordinateur

tour_de_jeu = 0
score_joueur = 0
score_ordi = 0

def renit(question : str):
    """Cette fonction permet de tout remettre à zéro. Elle prend en parametre une chaine de charactère qui va définir si l'on remet tout à 0 ou pas"""

    global cases_joueur, grille_coup_joueur, nb_bateau_4, nb_bateau_3, nb_bateau_2, nb_bateau, score_joueur, liste_bateaux
    global cases_ordi, nb_bateau_4_ordi, nb_bateau_3_ordi, nb_bateau_2_ordi, nb_bateau_ordi, liste_bateaux_ordi, score_ordi
    global tour_de_jeu

    cases_joueur = [[0 for k in range(largeur)] for i in range(hauteur) ] #grille des bateaux du joueur ainsi que les tires de l'ordinateur
    cases_ordi = [[0 for k in range(largeur)] for i in range(hauteur) ] #grille des bateaux de l'ordinateur
    grille_coup_joueur = [[0 for k in range(largeur)] for i in range(hauteur) ] #grille des coup du joueur

    nb_bateau_4 = 2
    nb_bateau_3 = 2
    nb_bateau_2 = 2
    nb_bateau = nb_bateau_2 + nb_bateau_3 + nb_bateau_4 #permet de compter rapidement le nombre de bateaux plaçables. Les variables sont donc modifiables afin de changer le nombre de bateaux plaçables en fonction de leur taille
    liste_bateaux = [None for k in range(nb_bateau)] #permet de stocker toutes les postions de chaques cases des bateaux du joueur

    nb_bateau_2_ordi = nb_bateau_2
    nb_bateau_3_ordi = nb_bateau_3
    nb_bateau_4_ordi = nb_bateau_4
    nb_bateau_ordi = nb_bateau_2_ordi + nb_bateau_3_ordi + nb_bateau_4_ordi #permet de compter rapidement le nombre de bateaux plaçables. Les variables sont donc modifiables afin de changer le nombre de bateaux plaçables en fonction de leur taille
    liste_bateaux_ordi = [None for k in range(nb_bateau_ordi)] #permet de stocker toutes les postions de chaques cases des bateaux de l'ordinateur

    if question == "RECOMMENCER": #si on veut tout recommencer, on remet aussi les score à 0
        tour_de_jeu = 0
        score_joueur = 0
        score_ordi = 0
    else:
        return


def lance_verif_ordi(type_boat : int):
    """
    Cette fonction prend en parametre le type de bateau que l'ordinateur va générer.
    Elle va donc tirer aléatoirement la direction principale (ligne ou colonne) puis le point de départ du bateau. Puis en fonction de de la direction principale, elle va tirer au sort une direction secondaire (Nord, Sud ou Est, West)
    Ensuite elle va lancer la fonction verif_cases avec en paramètre les éléments tirés au sort ainsi que les autres éléments requis
    """
    LorC = random.choice(["L", "C"])
    ligne = random.randint(1,hauteur)
    colonne = random.randint(1,largeur)
    if LorC == "L":
        direction_secondaire = random.choice(["E", "W"])
    else:
        direction_secondaire = random.choice(["N", "S"])

    verif_cases(ligne, colonne, LorC, direction_secondaire, type_boat, "ordi")



"""def lance_verif_joueur(ligne, colonne, LorC, direction_secondaire, type_boat):
    
    Cette fonction permet juste de passer en parametre dans la fonction verif_cases le joueur.
    
    verif_cases(ligne, colonne, LorC, direction_secondaire, type_boat, "joueur")"""



def verif_cases(ligne : int, colonne : int, LorC : str, direction_secondaire : str, type_boat : int, joueur : str):
    """Prend en paramètre une ligne, une colonne, une direction principale ( ligne ou colonne ), une direction secondaire ( Nord, Sud, Ouest, Est), un type de bateau et le joueur qui veut exécuter cette fonction.
    Cette fonction va donc vérifier si le bateau voulu peut se placer dans la grille dans la direction voulu et aux coordonnées voulu. Si il n'y a pas de bateaux déjà présents à l'emplacement voulu et que le bateau est dans la grille, cette fonction va en appeler une autre.
    Cette fonction ne renvoie rien sauf pour des messages d'erreurs"""
    global liste_bateaux_ordi, liste_bateaux

    create_boat = [None for k in range(type_boat)]
    index = 0 #index du tableau des cases du bateau
    
    placable = 0 #variable qui va montrer si le bateau peut se placer ( palacable = 1 )
    if (nb_bateau if joueur == "joueur" else nb_bateau_ordi) != 0:
        if LorC == "L": #vérifie si l'orientation principale est en ligne
            test_dans_grille_ligne = (((colonne - 1) + type_boat) <= largeur if direction_secondaire == "E" else ((colonne+1) - type_boat) >= 1) #teste si le bateau rentre dans la grille en fonction de l'orientaion gauche ou droite
            if test_dans_grille_ligne:
                for k in range((colonne - 1), (((colonne - 1) + type_boat) if direction_secondaire == "E" else ((colonne - 1) - type_boat)), (1 if direction_secondaire == "E" else -1)): #regarde les cases du point de départ donné en paramètre jusqu'à celle de la fin du bateau (droite ou gauche en fonction de la direction secondaire)
                    if (cases_ordi[ligne - 1][k] if joueur == "ordi" else cases_joueur[ligne - 1][k]) == 0 and placable != 2: #regarde si la case est vide (0) et que placable est différent de 2 , c-a-d que les cases testées précédement sont vide
                        placable = 1 #la case est libre 
                        create_boat[index] = [ligne - 1, k] #ajoute la case aux autres cases du bateau
                        index += 1 #comme une case vient d'être ajouté aux cases du bateau, on augmente l'index de 1
                    else:
                        placable = 2 #prend la valeur 2 car la case n'est pas vide
                           
        elif LorC == "C": #vérifie si l'orientation principale est en colonne
            test_dans_grille_colonne = (((ligne - 1) + type_boat) <= hauteur if direction_secondaire == "S" else ((ligne + 1) - type_boat) >= 1) #teste si le bateau rentre dans la grille en fonction de l'orientaion haut ou bas
            if test_dans_grille_colonne:
                for k in range((ligne - 1), (((ligne - 1) + type_boat) if direction_secondaire == "S" else ((ligne - 1) - type_boat)), (1 if direction_secondaire == "S" else -1)): #idem que la boucle précédente mais pour une direction principale en colonne
                    if (cases_ordi[k][colonne - 1] if joueur == "ordi" else cases_joueur[k][colonne - 1]) == 0 and placable != 2: #regarde si la case est vide (0) et que placable est différent de 2 , c-a-d que les cases testées précédement sont vide
                        placable = 1 #la case est libre 
                        create_boat[index] = [k, colonne -1]#ajoute la case aux autres cases du bateau
                        index += 1 #comme une case vient d'être ajouté aux cases du bateau, on augmente l'index de 1
                    else:
                        placable = 2#prend la valeur 2 car la case n'est pas vide
        else:
            return 

        if joueur == "ordi": #on regarde qui est le joueur
            if placable == 1: # si toutes les cases étaient vide et donc que l'on peut placer le bateau
                liste_bateaux_ordi[nb_bateau_total - nb_bateau_ordi] = create_boat #ajoute le bateau placé dans la liste de tous les bateaux de l'ordinateur à une index précise calculé en fonction du nombre de bateau qu'il resta a placer
                positionner(LorC, ligne, colonne, type_boat, direction_secondaire, joueur) #apelle la fonction qui va dessiner les bateau dans la grille
                
            else:
                lance_verif_ordi(type_boat) #si on ne peut pas placer le bateau, on réessaye avec de nouveaux paramètres

        elif joueur == "joueur": #on regarde qui est le joueur
            if placable == 1:
                liste_bateaux[nb_bateau_total - nb_bateau] = create_boat #ajoute le bateau placé dans la liste de tous les bateaux du joueur à une index précise calculé en fonction du nombre de bateau qu'il resta a placer
                positionner(LorC, ligne, colonne, type_boat, direction_secondaire , joueur)
            else:
                return "Le bateau ne peut pas se placer de cette façon."

    else:
        return "Vous n'avez plus de bateaux."



def positionner(LorC : str, ligne : int, colonne : int, type_boat : int, direction_secondaire : str, joueur : str):
    """Parametres : si l'on veut placer en ligne ou en colonne le bateau, le point de l'avant du bateau avec la ligne et la colonne, le type de bateau, la direction secondaire (Nord, Est, Sud, Ouest) et le joueur (ordinateur ou joueur).
    Cette fonction va donc placer le bateau sur la grille du joueur mis en paramètre et décompter sur le nombre de bateau total.
    Cette fonction ne renvoie rien
    """
    global nb_bateau_4_ordi, nb_bateau_3_ordi, nb_bateau_2_ordi, nb_bateau_ordi, cases_ordi, nb_bateau_4, nb_bateau_3, nb_bateau_2, nb_bateau, cases_joueur # importe toutes les variables des bateaux et des grilles

    if LorC == "L": #si la direction principale est en ligne
        borne_max = ((colonne - 1) + type_boat) if direction_secondaire == "E" else ((colonne - 1) - type_boat) #il s'agit de la fin du bateau à partir des coordonnées données en paramètre
        pas = (1 if direction_secondaire == "E" else -1)
        if type_boat == 4: #si le bateau est un bateau de 4
            if (nb_bateau_4_ordi if joueur == "ordi" else nb_bateau_4) != 0: #si il rest des bateaux de ce type en fonction du joueur
                for k in range((colonne - 1), borne_max, pas): #parcours les cases des coordonnées données jusqu'à la fin du bateau
                    if joueur == "ordi":
                        cases_ordi[ligne-1][k] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases de l'ordinateur (place le bateau dans la grille)
                    elif joueur == "joueur":
                        cases_joueur[ligne-1][k] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases du joueur (place le bateau dans la grille)
                if joueur == "ordi":
                    nb_bateau_4_ordi = nb_bateau_4_ordi - 1 #retranche 1 au nombre de bateau de ce type à l'ordinateur
                elif joueur == "joueur":
                    nb_bateau_4 = nb_bateau_4 - 1#retranche 1 au nombre de bateau de ce type au joueur

        elif type_boat == 3: #si le bateau est un bateau de 3
            if (nb_bateau_3_ordi if joueur == "ordi" else nb_bateau_3) != 0: #si il rest des bateaux de ce type en fonction du joueur
                for k in range((colonne - 1), borne_max, pas): #parcours les cases des coordonnées données jusqu'à la fin du bateau
                    if joueur == "ordi":
                        cases_ordi[ligne-1][k] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases de l'ordinateur (place le bateau dans la grille)
                    elif joueur == "joueur":
                        cases_joueur[ligne-1][k] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases du joueur (place le bateau dans la grille)
                if joueur == "ordi":
                    nb_bateau_3_ordi = nb_bateau_3_ordi - 1 #retranche 1 au nombre de bateau de ce type à l'ordinateur
                elif joueur == "joueur":
                    nb_bateau_3 = nb_bateau_3 - 1 #retranche 1 au nombre de bateau de ce type au joueur

        elif type_boat == 2: #si le bateau est un bateau de 2
            if (nb_bateau_2_ordi if joueur == "ordi" else nb_bateau_2) != 0: #si il rest des bateaux de ce type en fonction du joueur
                for k in range((colonne - 1), borne_max, pas): #parcours les cases des coordonnées données jusqu'à la fin du bateau
                    if joueur == "ordi":
                        cases_ordi[ligne-1][k] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases de l'ordinateur (place le bateau dans la grille)
                    elif joueur == "joueur":
                        cases_joueur[ligne-1][k] = 1  #ajoute la case d'un bateau à sa place dans toutes les cases du joueur (place le bateau dans la grille)
                if joueur == "ordi":
                    nb_bateau_2_ordi = nb_bateau_2_ordi - 1 #retranche 1 au nombre de bateau de ce type à l'ordinateur
                elif joueur == "joueur":
                    nb_bateau_2 = nb_bateau_2 - 1 #retranche 1 au nombre de bateau de ce type au joueur

    elif LorC == "C": #si la direction principale est en colonne
        borne_max = ((ligne - 1) + type_boat) if direction_secondaire == "S" else ((ligne - 1) - type_boat)
        pas = (1 if direction_secondaire == "S" else -1)
        if type_boat == 4:
            if (nb_bateau_4_ordi if joueur == "ordi" else nb_bateau_4) != 0:
                for k in range((ligne - 1), borne_max, pas):
                    if joueur == "ordi":
                        cases_ordi[k][colonne - 1] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases de l'ordinateur (place le bateau dans la grille)
                    elif joueur == "joueur":
                        cases_joueur[k][colonne - 1] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases du joueur (place le bateau dans la grille)
                if joueur == "ordi":
                    nb_bateau_4_ordi = nb_bateau_4_ordi - 1 #retranche 1 au nombre de bateau de ce type à l'ordinateur
                elif joueur == "joueur":
                    nb_bateau_4 = nb_bateau_4 - 1 #retranche 1 au nombre de bateau de ce type au joueur

        elif type_boat == 3:
            if (nb_bateau_3_ordi if joueur == "ordi" else nb_bateau_3) != 0:
                for k in range((ligne - 1), borne_max, pas):
                    if joueur == "ordi":
                        cases_ordi[k][colonne - 1] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases de l'ordinateur (place le bateau dans la grille)
                    elif joueur == "joueur":
                        cases_joueur[k][colonne - 1] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases du joueur (place le bateau dans la grille)
                if joueur == "ordi":
                    nb_bateau_3_ordi = nb_bateau_3_ordi - 1 #retranche 1 au nombre de bateau de ce type à l'ordinateur
                elif joueur == "joueur":
                    nb_bateau_3 = nb_bateau_3 - 1 #retranche 1 au nombre de bateau de ce type au joueur

        elif type_boat == 2:
            if (nb_bateau_2_ordi if joueur == "ordi" else nb_bateau_2) != 0:
                for k in range((ligne - 1), borne_max, pas):
                    if joueur == "ordi":
                        cases_ordi[k][colonne - 1] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases de l'ordinateur (place le bateau dans la grille)
                    elif joueur == "joueur":
                        cases_joueur[k][colonne - 1] = 1 #ajoute la case d'un bateau à sa place dans toutes les cases du joueur (place le bateau dans la grille)
                if joueur == "ordi":
                    nb_bateau_2_ordi = nb_bateau_2_ordi - 1 #retranche 1 au nombre de bateau de ce type à l'ordinateur
                elif joueur == "joueur":
                    nb_bateau_2 = nb_bateau_2 - 1 #retranche 1 au nombre de bateau de ce type au joueur


    if joueur == "ordi":
        nb_bateau_ordi = nb_bateau_ordi - 1
    elif joueur == "joueur":
        nb_bateau = nb_bateau - 1 



def tirer(ligne : int, colonne : int, joueur : str) -> str:
    """Prend en parametre une ligne et une colonne (point d'intersection) ainsi que le type du joueur (ordinateur ou humain)
    Cette fonction va donc vérifier que la case où l'on veut tirer est libre ( que l'on a pas déjà tiré dessus), car sinon on peut retirer ( de même quand on a toucé un bateau ), puis ensuite elle va vérifier si il y a un 
    bateau ou non à la case visé. On ajoute ensuite à la grille le tire et si il a touché ou non.
    Elle fait de même avec les deux joueur à une seule différence, si l'ordinateur touche un bateau, une nouvelle fonction est appelée.
    Cette fonction renvoie seulement des messages d'erreur quand nécessaire."""
    global grille_coup_joueur, liste_bateaux_ordi, liste_bateaux, tour_de_jeu
    test_dans_grille = (ligne <= hauteur and ligne >= 1 and colonne >= 1 and colonne <= largeur)
    nb_bateau_restant = nb_bateaux_restant() #permet de garder en mémoire le nombre de bateaux restant à l'ordinateur avant le coup
    if test_dans_grille:
        if joueur == "joueur" :
            if grille_coup_joueur[ligne - 1][colonne - 1] == 0: #vérifie que c'est une case qui n'a pas encore été visé
                if cases_ordi[ligne-1][colonne-1] == 1: #vérifie s'il y a un bateau sur la case visé
                    grille_coup_joueur[ligne - 1][colonne - 1] = "X" #ajoute un X sur le grille des coups du joueur pour montrer qu'un bateau a été touché
                    for k in liste_bateaux_ordi:#on parcours la liste des cases des bateaux 
                        if [ligne - 1, colonne - 1] in k: #si la case touchée est dans le bateau k
                            index_a = liste_bateaux_ordi.index(k) #stocke l'index du bateau dans la liste des bateaux 
                            index_b = liste_bateaux_ordi[index_a].index([ligne - 1, colonne - 1]) #stocke l'index de la case visé dans celle du bateau
                            del liste_bateaux_ordi[index_a][index_b] #permet de supprimer la case du bateau dans la liste des bateaux de l'ordinateur
                    nb_bateau_restant_bis = nb_bateaux_restant() #permet de garder en mémoire le nombre de bateaux restant de l'ordinateur après le coup du joueur
                    if nb_bateau_restant[1] != nb_bateau_restant_bis[1]:#permet de savoir si le joueur a coulé un bateaux ou pas si les deux variables sont différentes
                        return "Vous avez touché et coulé un bateau ! Rejouer !"
                    else: 
                        return "Vous avez touché un bateau ! Rejouer !"
                elif cases_ordi[ligne - 1][colonne - 1] == 0: #si la case visée est vide, on affiche un rond pour "plouf"
                    grille_coup_joueur[ligne - 1][colonne - 1] = "O"
                    tour_de_jeu += 1 #ajoute 1 au tour de jeu
                    return "Loupé ! Recommencez au prochain tour !"

            else: return "Vous avez déjà tiré ici"

        elif joueur == "ordi" and tour_de_jeu%2 != 0: #vérifie que c'est bien à l'ordinateur de jouer 
            if cases_joueur[ligne - 1][colonne - 1] == 1: #vérifie s'il y a un bateau sur la case visé
                cases_joueur[ligne - 1][colonne - 1] = "X" #ajoute un X sur le grille du joueur pour montrer qu'un bateau a été touché
                for k in liste_bateaux: #on parcours la liste des cases des bateaux 
                    if [ligne - 1, colonne - 1] in k: #si la case touchée est dans le bateau k
                        index_a = liste_bateaux.index(k) #stocke l'index du bateau dans la liste des bateaux
                        index_b = liste_bateaux[index_a].index([ligne - 1, colonne - 1]) #stocke l'index de la case visé dans celle du bateau
                        del liste_bateaux[index_a][index_b] #permet de supprimer la case du bateau dans la liste des bateaux du joueur
                time.sleep(1) #permet de faire croire que l'ordinateur "réfléchit" avant de tirer
                
                intelligence_ordi(ligne, colonne) #appelle la fonction d'intelligence de l'ordinateur qui va lui permettre de retirer (comme l'ordinateur viens de toucher)
            elif cases_joueur[ligne - 1][colonne - 1] == 0:  #si la case visée est vide, on affiche un rond pour "plouf"
                cases_joueur[ligne - 1][colonne - 1] = "O"
                tour_de_jeu += 1 #ajoute 1 au tour de jeu
                time.sleep(1) #permet de faire croire que l'ordinateur "réfléchit" avant de tirer
                
            else:
                tirer(random.randint(1, hauteur), random.randint(1, largeur), "ordi") #la case visée a déjà été visée. Donc l"ordinateur retire

    elif joueur == "joueur": #vérifie qui joue
        return "Cette case n'est pas dans la grille. Retirez !" #message d'erreur 
    elif joueur == "ordi": #vérifie qui joue
        tirer(random.randint(1, hauteur), random.randint(1, largeur), "ordi") #fait retirer l'ordinateur au lieu d'un message d'erreur



def intelligence_ordi(ligne : int, colonne : int):
    """Cette fonction prend en paramètre la ligne et la colonne (donc la case) de la case ou l'on a tiré. 
    Cette fonction va donc, en fonction de cette cases et des autres tirs autours, décider de la prochaine cases où l'ordinateur va tirer."""
    
    verif1 = ((cases_joueur[ligne-2][colonne-1] != "X" and cases_joueur[ligne-2][colonne-1] != "O") if (ligne-2) >= 0 else False)#vérifie si la case du haut n'a pas déjà été tiré et touché seulement si elle appratient bien à la grille. Si elle a déjà été tiré et touché ou que la case tiré est hos de la grille, verif1 = False
    verif2 = ((cases_joueur[ligne][colonne-1] != "X" and cases_joueur[ligne][colonne-1] != "O") if ligne <= (hauteur-1) else False)#idem mais pour la case du bas
    verif3 = ((cases_joueur[ligne-1][colonne-2] != "X" and cases_joueur[ligne-1][colonne-2] != "O") if (colonne-2) >= 0 else False)#idem mais pour la case de gauche
    verif4 = ((cases_joueur[ligne-1][colonne] != "X" and cases_joueur[ligne-1][colonne] != "O") if colonne <= (largeur-1) else False)#idem mais pour la case de droite

    
    if (colonne-2) >= 0 and cases_joueur[ligne-1][colonne-2] == "X": #si la case à gauche du tir est dans la grille et si la case à gauche du tir à est une case où il y a un bateau touché
        tirer(ligne, colonne+1, "ordi") #tir donc sur la case à droite du tir
    elif colonne <= (largeur-1) and cases_joueur[ligne-1][colonne] == "X": #si la case à droite du tir est dans la grille et si la case à droite du tir à est une case où il y a un bateau touché
        tirer(ligne, colonne-1, "ordi") #tir donc sur la case à gauche du tir
    elif (ligne-2) >= 0 and cases_joueur[ligne-2][colonne-1] == "X": #si la case au-dessus du tir est dans la grille et si la case au-dessus du tir à est une case où il y a un bateau touché
        tirer(ligne+1, colonne, "ordi") #tir donc sur la case au-dessus du tir
    elif ligne <= (hauteur-1) and cases_joueur[ligne][colonne-1] == "X": #si la case es dessous du tir est dans la grille et si la case en dessous du tir à est une case où il y a un bateau touché
        tirer(ligne-1, colonne, "ordi") #tir donc sur la case en dessous du tir
    elif verif1 or verif2 or verif3 or verif4: #si les autres condition ne sont pas vérifié, donc qu'il n'y a aucun tir sur un bateau autour du tir, et que au moins un des booléens est vrai
        tab_aleatoire = "" #créé une chaine de caractère
        if verif1: #si vrai (voir précédement)
            tab_aleatoire = tab_aleatoire + "S" #on ajoute la direction Sud à la chaine de charactère tab_aleatoire
        if verif2: #si vrai (voir précédement)
            tab_aleatoire = tab_aleatoire + "N" #on ajoute la direction Nord à la chaine de charactère tab_aleatoire
        if verif3: #si vrai (voir précédement)
            tab_aleatoire = tab_aleatoire + "W" #on ajoute la direction Ouest à la chaine de charactère tab_aleatoire
        if verif4: #si vrai (voir précédement)
            tab_aleatoire = tab_aleatoire + "E" #on ajoute la direction Est à la chaine de charactère tab_aleatoire

        sens = random.choice(tab_aleatoire) #choisit aléatoirement un direction dans celle disponible (vérifié précédement)
        if sens == "S": #si le sens tiré au sort est le Sud
            tirer(ligne+1, colonne, "ordi") #alors on tir juste au dessus de la case tirée
        elif sens == "N": #si le sens tiré au sort est le Nord
            tirer(ligne-1, colonne, "ordi") #alors on tir juste en dessous de la case tirée
        elif sens == "E": #si le sens tiré au sort est l'Est
            tirer(ligne, colonne+1, "ordi") #alors on tir à droite de la case tirée
        elif sens == "W": #si le sens tiré au sort est l'Ouest
            tirer(ligne, colonne-1, "ordi") #alors on tir à gauche de la case tirée



def nb_bateaux_restant() -> tuple:
    """Cette fonction ne prend rien en paramètre. Elle va regarder le nombre de bateau qu'il reste à chaque joueur
    Cette fonction renvoie le nombre de bateaux restant du joueur puis le nombre de bateaux restant de l'ordinateur"""
    compteur_joueur = 0 #compteur de bateaux restant au joueur
    compteur_ordi = 0 #compteur de bateau restant à l'ordinateur
    for bateaux in liste_bateaux: #parcours la liste de bateau du joueur
        if bateaux != [] and bateaux != None: #si le bateau n'est pas vide (ou détruit entièrement) et qu'il s'agit bien d'u bateau( quand on ne les a pas encore palcé tous les bateaux, la valeur est None à chaque emplacement)
            compteur_joueur += 1#on ajoute 1 au compteur

    for bateaux in liste_bateaux_ordi: #parcours la liste de bateau de l'ordinateur
        if bateaux != [] and bateaux != None: #si le bateau n'est pas vide (ou détruit entièrement) et qu'il s'agit bien d'u bateau( quand on ne les a pas encore palcé tous les bateaux, la valeur est None à chaque emplacement)
            compteur_ordi += 1#on ajoute 1 au compteur
    
    return compteur_joueur, compteur_ordi
    

def score(nb_bateaux_joueur : int, nb_bateaux_ordi) -> str:
    """Prend en paramètre le nombre de bateau res : inttant de chaque joueur. 
    En fonction de cela, si il n'en resta plus un seul à l'un des deux joeur, les scores vont être mis à jour
    Cette fonction renvoie qui a gagné si un des paramètres est égal à 0"""
    global score_joueur, score_ordi
    if nb_bateaux_ordi == 0: #si le nombre de bateaux de l'ordinateur est à 0
        score_joueur += 1 #ajpute 1 au score du joueur
        return "Vous avez gagné ! Vous avez {} point(s) et l'ordinateur a {} point(s).".format(score_joueur, score_ordi)
    elif nb_bateaux_joueur == 0: #si le nombre de bateaux du joueur est à 0
        score_ordi += 1 #ajpute 1 au score de l'ordinateur
        return "C'est l'ordinateur qui a gagné ... Vous ferez mieux la prochaine fois. Vous avez {} point(s) et l'ordinateur a {} point(s).".format(score_joueur, score_ordi)



def ordi_place_bateaux():
    """Permet de faire placer les bateaux de l'ordinateur en partant des plus grand
    Rajouter des ligne comme si dessous si le nombre de bateau est modifié"""
    lance_verif_ordi(4)
    lance_verif_ordi(4)
    lance_verif_ordi(3)
    lance_verif_ordi(3)
    lance_verif_ordi(2)
    lance_verif_ordi(2)
