"""
affichage jeu de bataille navale en mode console
Léo Gaspari, 20/12/2020
"""

"""Ce programme permet d'afficher en mode console un jeu de bataille navale.
Il est basé sur la moteur de jeu intitulé 'bataille_navale_main.py'.
"""

import bataille_navale_main as moteur
import random

def affiche():
    """Cette fonction permet de dessiner dans la console la grille des bateaux du joueur ainsi que les tirs adverses"""
    coord = ord("A")
    print("\nVotre grille avec vos bateaux et les tirs adverses :\n")
    print("-----------------------------------------")
    for k in range(moteur.hauteur):
        for i in range(moteur.largeur):
            if moteur.cases_joueur[k][i] == 0:
                print("|   ", end="")
            elif moteur.cases_joueur[k][i] == 1:
                print("| 1 ", end="")
            elif moteur.cases_joueur[k][i] == "X":
               print("| X ", end="") 
            elif moteur.cases_joueur[k][i] == "O":
               print("| O ", end="") 
        print("| {}\n-----------------------------------------".format(chr(coord)))
        coord += 1
    print("  1   2   3   4   5   6   7   8   9   10  ")
    #affichage_grille_tire()
        

def affichage_grille_tire():
    """Cette fonction permet de dessiner dans la console la grille des tirs du joueur"""
    coord = ord("A")
    print("\nVotre grille de tir :\n")
    print("-----------------------------------------")
    for k in range(moteur.hauteur):
        for i in range(moteur.largeur):
            if moteur.grille_coup_joueur[k][i] == 0:
                print("|   ", end="")
            elif moteur.grille_coup_joueur[k][i] == "X":
               print("| X ", end="") 
            elif moteur.grille_coup_joueur[k][i] == "O":
               print("| O ", end="") 
        print("| {}\n-----------------------------------------".format(chr(coord)))
        coord += 1
    print("  1   2   3   4   5   6   7   8   9   10  ")


def affiche_ordi():
    """Cette fonction permet de dessiner la grille des bateaux de l'ordinateur. Cette fonction n'est pas appelé dans le programme principle mais elle sert de débug"""
    coord = ord("A")
    print("-----------------------------------------")
    for k in range(moteur.hauteur):
        for i in range(moteur.largeur):
            if moteur.cases_ordi[k][i] == 0:
                print("|   ", end="")
            elif moteur.cases_ordi[k][i] == 1:
                print("| 1 ", end="")
            elif moteur.cases_ordi[k][i] == "X":
               print("| X ", end="") 
            elif moteur.cases_ordi[k][i] == "O":
               print("| O ", end="") 
        print("| {}\n-----------------------------------------".format(chr(coord)))
        coord += 1
    print("  1   2   3   4   5   6   7   8   9   10  ")



def afficher_compteur(compteur : tuple):
    """Cette fonction affiche en console le score du joueur et de l'ordinateur ainsi que le nombre de bateaux restant à chacun.
    Cette fonction va donc prendre en paramètre un tuple avec ce nombre de bateaux (d'abord ceux restant du joueur, puis ceux restant de l'odinateur)"""
    print("\nVous : {}\tOrdinateur : {}".format(moteur.score_joueur, moteur.score_ordi))
    print("Il vous reste {} bateaux. Il reste {} bateaux à l'ordinateur".format(compteur[0], compteur[1]))
    




def convertisseur(coord):
    """Cette fonction permet de ne pas utiliser de dictionnaire. Elle permet à partir de coordonnées du type 'A1', de connaitre des coordonnées en chiffre( A1 = 1ère ligne et 1ère colonne )"""
    chaine = coord.upper()
    if ord(chaine[0]) <= ord("J"): #si le premier caractère en unicode possède une valeur plus petite ou égale à J en unicode (car 10 lignes/colonnes)
        if len(chaine) == 3: #si la chaine est de 3 de longueur
            verif = ((ord(chaine[1]) + ord(chaine[2])) == ord("1") + ord("0")) #on vérifie que la chaine est du type "lettre + 10"
            if verif == True and chaine[1] == "1" and chaine[2] == "0": #si le booléen précédent est vrai
                return ((ord(chaine[0]) - ord("A")) + 1), 10 #alors on retourne un tuple contenant les coordonnées
        elif len(chaine) == 2: #si la longueur de la chaine est égale à 2
            verif = (ord("1") <= ord(chaine[1]) <= ord("9")) #si le deuxième élément de la chaine est un chiffre entre 1 et 9
            if verif == True:
                return ((ord(chaine[0]) - ord("A")) + 1), int(chaine[1]) #alors on retourne un tuple contenant les coordonnées
    return "Ces coordonnées n'existent pas." #message d'erreur




def start():
    """Appelez cette fonction pour commencer le jeu. C'est elle qui va permettre d'afficher et de commander e placement des bateaux"""
    affiche()
    while moteur.nb_bateau != 0:
        print("\nIl vous reste {} bateaux. {} de 4, {} de 3 et {} de 2. \n".format(moteur.nb_bateau, moteur.nb_bateau_4, moteur.nb_bateau_3, moteur.nb_bateau_2))
        coord_saisi = input("Où voulez-vous placez votre bateau (ligne puis colonne. Ex: D6) ? ")
        coord = convertisseur(coord_saisi)
        if type(coord) == tuple:
            direction0 = input("Dans quelle direction voulez-vous que le bateau se place ( L pour ligne, C pour colonne ) ? ")
            direction = direction0.upper()
            if direction == "L" or direction == "C":
                if direction == "L":
                    direction_secondaire0 = input("Dans quelle direction voulez-vous placez le bateau ( E pour Est, W pour Ouest ) ? ")
                elif direction == "C":
                    direction_secondaire0 = input("Dans quelle direction voulez-vous placez le bateau ( N pour Nord, S pour Sud ) ? ")
                direction_secondaire = direction_secondaire0.upper()
                if (direction == "L" and (direction_secondaire == "E" or direction_secondaire == "W")) or (direction == "C" and (direction_secondaire == "S" or direction_secondaire == "N")):
                    type_bateau = int(input("Quel type de bâteau voulez vous placez ? "))
                    if type_bateau == 2 or type_bateau == 3 or type_bateau == 4:
            
                        a = moteur.verif_cases(coord[0], coord[1], direction, direction_secondaire, type_bateau, "joueur")
                        affiche()
                        
                        if a != None:
                            print("\n", a)

                    else:
                        print("Ce type de bateau n'existe pas.")
                else:
                    print("Cette direction n'est pas disponible.")
            else:
                print("Cette direction n'existe pas.")
        else:
            print(coord)

    moteur.ordi_place_bateaux()
    jeu_principal()


def jeu_principal():
    """Cette fonction permet le déroulement du jeu. Contrairement à 'start()', cette fonction asure le déroulement des tirs du joueur et de l'ordinateur et d'afficher les message d'erreurs si nécessaire ainsi que les grille et les scores"""
    compteur = moteur.nb_bateaux_restant()
    affichage_grille_tire()
    while ((compteur[0] != 0) and (compteur[1] != 0)):
        tire = input("Où voulez-vous tirer (ligne puis colonne. Ex: D6) ? ")
        coord = convertisseur(tire)
        if type(coord) == tuple:
            resultat = moteur.tirer(coord[0],coord[1],"joueur")
            affichage_grille_tire()
            if resultat != None:
                print(resultat)
                if moteur.tour_de_jeu %2 != 0:
                    print("Au tour de l'ennemi...")
                    moteur.tirer(random.randint(1,10),random.randint(1,10),"ordi")
                    affiche()
                    compteur = moteur.nb_bateaux_restant()    
                    afficher_compteur(compteur)

                else:
                    compteur = moteur.nb_bateaux_restant()
                    afficher_compteur(compteur)

                    
        else:
            print(coord)
        
    print(moteur.score(compteur[0], compteur[1])) #affiche qui a gagné ainsi que les nouveaux scores
    good = False #permet de stopper la boucle while suivante
    while good == False:
        rejouer = input("Voulez-vous rejouer, recommencer tout ou quitter ? \nTapez REJOUER pour rejouer, RECOMMENCER à 0 pour recommencer ou QUITTER pour quitter :\n ")
        rejouer.upper()
        if rejouer == "REJOUER" or rejouer == "RECOMMENCER": 
            moteur.renit(rejouer) #ce référer à la définition de la fonction
            good = True #on stop la boucle
            start() #relance le jeu
        elif rejouer == "QUITTER":
            good = True #on stop la boucle
            return #permet de quitter la fonction et donc quitter le jeu
        else:
            print("Cette commande n'existe pas. Veyez recommencer.") #message d'erreur



start() #enlever/mettre le commentaire pour lancer/ne pas lancer le jeu à l'exécution

