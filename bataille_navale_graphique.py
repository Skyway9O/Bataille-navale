"""
affichage jeu de bataille navale en mode interface graphique
Léo Gaspari, 20/12/2020
"""

"""Ce programme permet d'afficher un jeu de bataille navale en mode interface graphique.
Il est basé sur le moteur de jeu intitulé 'bataille_navale_main.py'.
"""

import bataille_navale_main as moteur
from tkinter import *
import random
import time

nb_bateaux_restant_tout = moteur.nb_bateaux_restant()
rectangle_coord = None



def pointeur(event):
    """Cette fonction prend en argument un event. Elle permet de dessiner un carré sous le curseuret d'indiquer si l'on peut cliqué dans la case désirée. """
    global rectangle_coord
    canvas1.delete(rectangle_coord) #supprime le carré avant tout 
    l = (event.y)//40                   # Ligne du clic
    c = (event.x)//40                   # Colonne du clic
    if l <= 9 and c <= 9 and moteur.cases_joueur[l][c] == 1: # le curseur dois être dans la grille et la case ou se situe le curseur doit contenir un bateau
        rectangle_coord = canvas1.create_rectangle(c*40, l*40, (c*40)+40, (l*40)+40, fill="red") #dessine un carré rouge dans la case du curseur
    else:
        rectangle_coord = canvas1.create_rectangle(c*40, l*40, (c*40)+40, (l*40)+40, fill="#00ff74") #dessine un carré vert dans la case du curseur si il n'y a pas de bateau



def annule_selection():
    """Cette fonction permet d'annuler le mode sélection. Elle unbind le canvas et restaure la fonctionnalité du bouton et le texte du label d'information"""
    canvas1.unbind("<Motion>") #unbind le deplacement de la souris du canvas 1
    canvas1.delete(rectangle_coord)#efface le carré sous le curseur
    bouton_bateaux.configure( text="Placer un bateau", command=selection_bateau, bg="#ffcc46")
    if moteur.nb_bateau != 0:#s'il reste des bateaux à placer
        label_info.configure(text="\nAppuyer sur le bouton 'Placer un bateau'\n")
    
    

def selection_bateau():
    """Cette fonction permet de rentrer en mode sélection dans le placement des bateaux. Elle bind le canvas1 sur la souris(ses déplacements et sur le clique gauche). Elle configure aussi le message dans le label_info."""
    if moteur.nb_bateau != 0:#s'il reste des bateaux à placer
        label_info.configure(text="Cliquez sur la grille de gauche\npour sélectionner une case\n")
        bouton_bateaux.configure(text="Selection en cours", bg="#ff4c4c", command=annule_selection ) #configure le bouton pour pouvoir annuler le mode sélection
        canvas1.bind("<Button-1>", clique_selection_bateau) #permet, au clique gauche sur le canvas1, de lancer la fonction qui va ouvrir la pop_up de configuration
        canvas1.bind("<Motion>", pointeur)
    else:
        label_info.configure(text="Vous avez déjà placez tout vos bateaux.\nCliquez sur la grille de droite pour tirer.\n")
    

def clique_selection_bateau(event):
    """Cette fonction permet de récupérer les coordonnées du clique et donc dessiner un carré dans la case de ces coordonnées. Elle modifie le label_info en fonction de ce qu'il y a dans la case.
    Elle unbind le canvas1 et lance l'ouverture de la pop_up de configuration. """
    global rectangle_selection
    l = (event.y)//40                  # Ligne du clic
    c = (event.x)//40                  # Colonne du clic
    if moteur.cases_joueur[l][c] == 1:
        label_info.configure(text="\nIl y a déjà un bateau à cette position.\n")
        return
    else:
        canvas1.unbind("<Button-1>")
        canvas1.unbind("<Motion>")
        rectangle_selection = canvas1.create_rectangle(c*40, l*40, (c*40)+40, (l*40)+40, fill="orange")
        creer_pop_up(l,c)



def switch_direction_ligne(radio1, radio2, radio3, radio4):
    """Cette fonction permet de désactiver les 2 peremiers boutons mis en argument et d'activer les deux suivants. Elle est appelé quand on décide de changer de direction principale"""
    radio1.configure(state=DISABLED)
    radio2.configure(state=DISABLED)
    radio3.configure(state=NORMAL)
    radio4.configure(state=NORMAL)
    radio3.select()



def creer_pop_up(ligne, colonne):
    """Cette fonction permet d'ouvrir une fenêtre toplevel (pop-up) qui va servir à la configuration de notre bateau"""

    #crée une popup pour configurer le placement du bateau
    pop_up = Toplevel()
    pop_up.title("infos bateau")
    pop_up.geometry("700x500")
    pop_up.grab_set() #bloc les intéraction avec la fenêtre principale
    pop_up.transient(fenetre)
    pop_up.minsize(450,500)

    frame_pop_up = Frame(pop_up)

    #placer des labels
    label_info_pop_up = Label(frame_pop_up, text="Choisissez la façon de placer votre bateau :", font=("Helvetica, 13"), fg="Black", borderwidth=3, relief="solid")
    label_info_pop_up.grid(row=0, column=0, columnspan=3, pady = 20)

    texte_direction = Label(frame_pop_up, text="Direction :", font=("Helvetica, 11"))
    texte_direction.grid(row=1, column=0, padx=20, ipady=30)

    texte_direction_secondaire = Label(frame_pop_up, text="Direction secondaire :", font=("Helvetica, 11"))
    texte_direction_secondaire.grid(row=3, column=0, padx=20)

    reste_bateaux = Label(frame_pop_up, text="Il vous reste {} bateaux. {} de 4, {} de 3 et {} de 2. ".format(moteur.nb_bateau, moteur.nb_bateau_4, moteur.nb_bateau_3, moteur.nb_bateau_2), font=("Helvetica, 11"), fg = "#b30808")
    reste_bateaux.grid(row=7, column=0, columnspan=3, pady = 30)

    texte_bateau = Label(frame_pop_up, text= "Type de bateau :", font=("Helvetica, 11"))
    texte_bateau.grid(row=8, column=0, padx=20)

    #placer des widgets switch pour la direction principale
    radioValueDirection = StringVar()

    radio_ligne = Radiobutton(frame_pop_up, text="ligne", variable=radioValueDirection, value="L")
    radio_ligne.grid(row=1, column=1, sticky=NW, ipady=30)

    radio_colonne = Radiobutton(frame_pop_up, text="colonne", variable=radioValueDirection, value="C")
    radio_colonne.grid(row=1, column=2, sticky=NW, ipady=30)

    
    #placer des widgets switch pour la direction secondaire
    radioValueDirection_secondaireA = StringVar()


    radio_nord = Radiobutton(frame_pop_up, text="Nord", variable=radioValueDirection_secondaireA, value="N")
    radio_nord.grid(row=3, column=1, sticky=NW)

    radio_est = Radiobutton(frame_pop_up, text="Est", variable=radioValueDirection_secondaireA, value="E")
    radio_est.grid(row=4, column=1, sticky=NW)

    radio_ouest = Radiobutton(frame_pop_up, text="Ouest", variable=radioValueDirection_secondaireA, value="W")
    radio_ouest.grid(row=5, column=1, sticky=NW)

    radio_sud = Radiobutton(frame_pop_up, text="Sud", variable=radioValueDirection_secondaireA, value="S")
    radio_sud.grid(row=6, column=1, sticky=NW)

    
    radio_ligne.configure(command=lambda:[switch_direction_ligne(radio_nord, radio_sud, radio_est, radio_ouest)]) #quand on clique sur le bouton de configuration en ligne, cela appèle la fonction qui va activer ou désactiver les direction secondaire qui ne peuvent pas être sélectionées
    radio_colonne.configure(command=lambda:[switch_direction_ligne(radio_est, radio_ouest, radio_nord, radio_sud)]) #idem que la ligne précédente mais pour le bouton de configuration en colonne
    radio_ligne.invoke() #permet de simuler le clique d'un joueur et donc qu'il y ai une valaur par defaut


    #placer les widgets switch pour le type de bateau
    radioValue_boat = IntVar()

    radio_bateaux_4 = Radiobutton(frame_pop_up, text="bateau de 4", variable=radioValue_boat, value=4, state=DISABLED)
    radio_bateaux_4.grid(row=8, column=1)

    radio_bateaux_3 = Radiobutton(frame_pop_up, text="bateau de 3", variable=radioValue_boat, value=3, state=DISABLED)
    radio_bateaux_3.grid(row=9, column=1)

    radio_bateaux_2 = Radiobutton(frame_pop_up, text="bateau de 2", variable=radioValue_boat, value=2, state=DISABLED)
    radio_bateaux_2.grid(row=10, column=1)

    actif = False

    if moteur.nb_bateau_4 != 0: #permet de verifier qu'il reste bien de ce type de bateau sinon on ne peux pas le selectionner
        radio_bateaux_4.configure(state=NORMAL) #permet d'activer le bouton
        actif = True
        radio_bateaux_4.select()    #permet qu'il y ai une pré-selection

    if  moteur.nb_bateau_3 != 0: #permet de verifier qu'il reste bien de ce type de bateau sinon on ne peux pas le selectionner
        radio_bateaux_3.configure(state=NORMAL) #permet d'activer le bouton
        if not(actif):
            actif = True
            radio_bateaux_3.select()    #permet qu'il y ai une pré-selection

    if  moteur.nb_bateau_2 != 0: #permet de verifier qu'il reste bien de ce type de bateau sinon on ne peux pas le selectionner
        radio_bateaux_2.configure(state=NORMAL) #permet d'activer le bouton
        if not(actif):
            actif = True
            radio_bateaux_2.select()    #permet qu'il y ai une pré-selection
    
    #placer bouton
    bouton_quitter_pop_up = Button(frame_pop_up, text="Quitter", bg="#d80000", fg="white", font=("Helvetica, 11"), command=lambda:[quitter_pop_up(pop_up)]) #appelle la fonction qui va fermer proprement la pop-up 
    bouton_quitter_pop_up.grid(row=11, column=0, pady=20, padx = 20)

    valider = Button(frame_pop_up, text="Valider", bg="Gold", font=("Helvetica, 11"), command=lambda:[verif_bateau(radioValueDirection, radioValueDirection_secondaireA, radioValue_boat, ligne, colonne, pop_up, label_info_pop_up)]) #lance la vérification que la configuration est possible
    valider.grid(row=11, column=2, columnspan=2, pady=20)

    #pack la frame
    frame_pop_up.pack(expand=YES)



def quitter_pop_up(pop_up):
    """cette fonction permet de quitter la pop_up proprement en remettant la fenêtre principale oppérationnelle et avec les bonnes configuration des boutons"""
    canvas1.delete(rectangle_selection)
    canvas1.delete(rectangle_coord)
    bouton_bateaux.configure( text="Placer un bateau", command=selection_bateau, bg="#ffcc46")
    fenetre.update()
    pop_up.destroy()



def verif_bateau(entree_direction, entree_direction_secondaire, entree_type_bateau, ligne, colonne, pop_up, label_info_pop_up):
    """Cette fonction vérifie que la configuration donnée en argument est possible. Si non, elle affiche un message d'erreur dans la fenêtre pop-up."""
    global nb_bateaux_restant_tout
    direction = str(entree_direction.get()) #on récupère les valeurs des radioboutons de la direction principale
    direction_secondaire = str(entree_direction_secondaire.get()) #on récupère les valeurs des radioboutons de la direction secondaire
    type_bateau = int(entree_type_bateau.get()) #on récupère les valeurs des radioboutons du type de bateau
    message = moteur.verif_cases(ligne+1, colonne+1, direction, direction_secondaire, type_bateau,"joueur") #on vérifie

    if message != None: #si il y a un message d'erreur
        label_info_pop_up.configure(text=message+"\nSaisissez des informations correctes", fg="red")

    else:
        if moteur.nb_bateau != 0: #s'il reste des bateaux à placer
            bouton_bateaux.configure( text="Placer un bateau", command=selection_bateau, bg="#ffcc46")
            label_info.configure(text="\nAppuyer sur le bouton 'Placez un bateau'\n")
            label_bateau_reste_placer.configure(text="Il vous reste {}\nbateaux à placer".format(moteur.nb_bateau)) #rafraichit dans la fenêtre principale le label avec le nombre de bateaux à placer
        elif moteur.nb_bateau == 0: #s'il ne reste plus de bateaux à placer
            bouton_bateaux.configure(state=DISABLED) #on désactive le bouton de sélection
            label_bateau_reste_placer.grid_remove() #on retire le texte qui permet d'affiche le nombre de bateaux restant à placer

        canvas1.delete(rectangle_selection) #on supprime le carré de sélection
        pop_up.destroy() #on détruit la pop-up
        nb_bateaux_restant_tout = moteur.nb_bateaux_restant() #regarde combien de bateau il reste au joueur (permet de dire combien sont déjà placer)
        label_bateaux_restant_joueur.configure(text="Bateaux restant joueur :\n"+str(nb_bateaux_restant_tout[0])) 
        dessiner_bateau() #appelle la fonction qui va dessiner le bateau sur la grille


def dessiner_bateau():
    """Cette fonction permet de dessiner tout les bateaux sur la grille. Elle parcourt la liste de bateaux et les affiche un par un"""
    rectangle_bateau = None
    canvas1.delete(rectangle_bateau)

    couleur = 75 #permet de créé un dégradé de couleur pour mieux différencier les bateaux
    for k in moteur.liste_bateaux: #percours la liste de tous les bateaux
        couleur += 10 #crée une petite différence de couleur
        if k != None: #si il s'agit bien d'un bateau
            for i in k:#on parcours toutes les cases du bateaux k
                rectangle_bateau = canvas1.create_rectangle(i[1]*40, i[0]*40, (i[1]*40)+40, (i[0]*40)+40, fill="#{:x}{:x}{:x}".format(couleur,couleur,couleur)) #on dessine à la case i un rectangle gris 

    fenetre.update() #rafraichit la fenêtre
    if moteur.nb_bateau == 0: #s'il ne reste plus de bateaux à placer au joueur
        label_info.configure(text="Maintenant, au tour de l'ordinateur.\n Patientez...\n")
        moteur.ordi_place_bateaux() #place le placement des bateaux de l'ordinateur

        bouton_bateaux.configure( text="Placer un bateau", command=selection_bateau, bg="#ffcc46")#rénitialise le bouton de sélection
        fenetre.update()
        time.sleep(2.5)#fait croire que l'ordinateur "réfléchit" à comment placer ses bateaux
        nb_bateaux_restant_tout = moteur.nb_bateaux_restant()
        label_bateaux_restant_ordi.configure(text="Bateaux restant ordi :\n"+str(nb_bateaux_restant_tout[1]))
        label_info.configure(text="Vous avez tous les deux placé tous vos bateaux!\nLe jeu peut donc commencer. \nCliquez sur la grille de droite pour tirer.")
        jeu_principal() #appelle la fonction dui va permettre de tirer 



def jeu_principal():
    """Cette fonction permet, une fois que les bateaux sont tous placés, de commencer à jouer. Le canvas2 (zone de tir) est bind afin de pouvoir cliquer dessus pour tirer.
    Quand un joueur a gagné, c'est cette fonction qui va mettre à jour le label_info et rafraichir les scores"""
    global nb_bateaux_restant_tout
    fenetre.update()
    nb_bateaux_restant_tout =  moteur.nb_bateaux_restant() #calcul le nombre de bateau restant de chaque joueur

    if nb_bateaux_restant_tout[0] != 0 and nb_bateaux_restant_tout[1] != 0: #s'il reste des bateaux aux joueurs
        if moteur.tour_de_jeu % 2 == 0: #si c'est au tour du joueur
            canvas2.bind("<Button-1>",coord_tir) #bind la grille des tirs (celle de droite)

        elif moteur.tour_de_jeu %2 !=0: #si c'est au tour de l'ordinateur
            label_info.configure(text="\nAu tour de l'ennemi...\n")
            fenetre.update()
            moteur.tirer(random.randint(1,10),random.randint(1,10),"ordi") #fait tirer l'ordinateur
            dessiner_tirs_ordi() #dessine le(s) tir(s) de l'ordinateur

    elif nb_bateaux_restant_tout[1] == 0: #si l'ordinateur n'a plus de bateaux
        label_info.configure(text="\nVous avez gagné !\n")
        gagner()

    elif nb_bateaux_restant_tout[0] == 0: #si le joueur n'a plus de bateaux
        label_info.configure(text="\nC'est l'ordinateur qui a gagné !\n")
        gagner()



def coord_tir(event):
    """Cette fonction permet au joueur d'afficher un cercle sur la case de tir."""
    global nb_bateaux_restant_tout

    l = (event.y)//40                  # Ligne du clic
    c = (event.x)//40                  # Colonne du clic
    canvas2.unbind("<Button-1>") #permet de ne pas pouvoir cliquer quand c'est l'odinateur qui joue
    
    reponse = moteur.tirer(l+1, c+1, "joueur") #permet de stocker le message obtenu quand on a tiré

    nb_bateaux_restant_tout =  moteur.nb_bateaux_restant()
    label_bateaux_restant_ordi.configure(text="Bateaux restant ordi :\n"+str(nb_bateaux_restant_tout[1]))
    
    if nb_bateaux_restant_tout != 0:
        label_info.configure(text="\n"+reponse+"\n") #permet d'afficher le message obtenu après avoir tiré dans le label d'information
    fenetre.update()
    
    dessiner_tirs_joueur(l,c) #dessine les tirs du joueur
    fenetre.update()
    if reponse == "Loupé ! Recommencez au prochain tour !": #quand le prochain tour est celui de l'ordinateur
        time.sleep(1.5) #permet de mettre un petit délai avnt que le message ne s'efface
    if nb_bateaux_restant_tout[0] != 0 or nb_bateaux_restant_tout[1] != 0: #tant qu'il reste au moins 1 bateaux au deux joueur
        jeu_principal()



def dessiner_tirs_joueur(y,x):
    """Cette fonction permet de dessiner le tir du joueur au coordonnées données en arguments"""
    if moteur.grille_coup_joueur[y][x] == "X": #si un bateau est touché
        rond_touche = canvas2.create_oval(x*40, y*40, (x*40)+40, (y*40)+40, fill="#e11800") #affiche un rond rouge pour "touché"
    elif moteur.grille_coup_joueur[y][x] == "O": #si c'est un tir dans l'eau
        rond_rate = canvas2.create_oval(x*40, y*40, (x*40)+40, (y*40)+40, fill="#defffb") #affiche un rond blanc/bleu pour "raté"
            


def dessiner_tirs_ordi():
    """Cette fonction permet de dessiner les tous tirs de l'ordinateur sur la grille des bateaux du joueur """
    global nb_bateaux_restant_tout
    for y in range(moteur.hauteur):
        for x in range(moteur.largeur):
            if moteur.cases_joueur[y][x] == "X": #si un bateau est touché
                rond_touche = canvas1.create_oval(x*40, y*40, (x*40)+40, (y*40)+40, fill="#e11800") #affiche un rond rouge pour "touché"
                fenetre.update()
                
            elif moteur.cases_joueur[y][x] == "O": #si c'est un tir dans l'eau
                rond_rate = canvas1.create_oval(x*40, y*40, (x*40)+40, (y*40)+40, fill="#defffb") #affiche un rond blanc/bleu pour "raté"
                fenetre.update()
            
    nb_bateaux_restant_tout =  moteur.nb_bateaux_restant()
    label_bateaux_restant_joueur.configure(text="Bateaux restant joueur :\n"+str(nb_bateaux_restant_tout[0]))            
    if nb_bateaux_restant_tout[0] == 0:
       gagner() 
    else:
        label_info.configure(text="\nÀ vous de tirer !\n")

    fenetre.update()
    jeu_principal()



def gagner():
    """Cette fonction permet de rafraichir les scores"""
    moteur.score(nb_bateaux_restant_tout[0], nb_bateaux_restant_tout[1])
    label_score.configure(text="Vous : {}\tOrdinateur : {}\n".format(moteur.score_joueur, moteur.score_ordi))
    bouton_bateaux.configure(text="Nouvelle manche", state=NORMAL, command=rejouer) #configure le bouton pour pouvoir rejouer
    fenetre.update()


def rejouer():
    """Permet de rénitialiser tout les label, bouton, canvas, etc... mais sans effacer les scores."""
    global nb_bateaux_restant_tout
    moteur.renit("REJOUER") #permet de remettre toutes les valeurs du moteur à 0 sauf les scores
    canvas1.unbind("<Button-1>")
    canvas1.unbind("<Motion>")
    canvas2.unbind("<Button-1>")
    canvas1.delete('all')
    canvas2.delete('all')
    for i in range(moteur.hauteur):
        canvas1.create_line(0, 40*i, 400, 40*i, width=1)
        canvas1.create_line(40*i, 0, 40*i, 400, width=1)
    for i in range(moteur.hauteur):
        canvas2.create_line(0, 40*i, 400, 40*i, width=1)
        canvas2.create_line(40*i, 0, 40*i, 400, width=1)
    nb_bateaux_restant_tout = moteur.nb_bateaux_restant()
    bouton_bateaux.configure(state=NORMAL, bg="#ffcc46", text="Placer un bateau", command=selection_bateau)
    bouton_bateaux.update()
    label_info.configure(text = "\nAppuyer sur le bouton 'Placez un bateau'\n")
    label_bateaux_restant_joueur.configure(text="Bateaux restant joueur :\n"+str(nb_bateaux_restant_tout[0]))
    label_bateaux_restant_ordi.configure(text="Bateaux restant ordi :\n"+str(nb_bateaux_restant_tout[1]))
    label_bateau_reste_placer.configure(text="Il vous reste {}\nbateaux à placer".format(moteur.nb_bateau))
    label_bateau_reste_placer.grid()
    label_score.configure(text="Vous : {}\tOrdinateur : {}\n".format(moteur.score_joueur, moteur.score_ordi))




def recommencer():
    """Permet de rénitialiser tout les label, bouton, canvas, etc...avec les scores aussi."""
    global nb_bateaux_restant_tout
    moteur.renit("RECOMMENCER") #permet de remettre toutes les valeurs du moteur à 0, y compris les scores
    canvas1.unbind("<Button-1>")
    canvas1.unbind("<Motion>")
    canvas2.unbind("<Button-1>")
    canvas1.delete('all')
    canvas2.delete('all')
    for i in range(moteur.hauteur):
        canvas1.create_line(0, 40*i, 400, 40*i, width=1)
        canvas1.create_line(40*i, 0, 40*i, 400, width=1)
    for i in range(moteur.hauteur):
        canvas2.create_line(0, 40*i, 400, 40*i, width=1)
        canvas2.create_line(40*i, 0, 40*i, 400, width=1)
    nb_bateaux_restant_tout = moteur.nb_bateaux_restant()
    bouton_bateaux.configure(state=NORMAL, bg="#ffcc46", text="Placer un bateau", command=selection_bateau)
    bouton_bateaux.update()
    label_info.configure(text = "\nAppuyer sur le bouton 'Placez un bateau'\n")
    label_bateaux_restant_joueur.configure(text="Bateaux restant joueur :\n"+str(nb_bateaux_restant_tout[0]))
    label_bateaux_restant_ordi.configure(text="Bateaux restant ordi :\n"+str(nb_bateaux_restant_tout[1]))
    label_bateau_reste_placer.configure(text="Il vous reste {}\nbateaux à placer".format(moteur.nb_bateau))
    label_bateau_reste_placer.grid()
    label_score.configure(text="Vous : {}\tOrdinateur : {}\n".format(moteur.score_joueur, moteur.score_ordi))



#création de la fenêtre
fenetre = Tk()
fenetre.title("bataille navale")
fenetre.geometry("1100x600")
fenetre.minsize(1100, 600)

#cree une frame
frame = Frame(fenetre)

#cree un label
label_info = Label(frame, text = "\nAppuyer sur le bouton 'Placez un bateau'\n", font=("Helvetica, 13"), borderwidth=3, relief="solid", justify= "center")
label_info.grid(row=0, column=5, columnspan=2, pady= 30, sticky= NW)

label_score = Label(frame, text="Vous : {}\tOrdinateur : {}\n".format(moteur.score_joueur, moteur.score_ordi), font=("Helvetica, 13"))
label_score.grid(row=0, column=1, columnspan=2, ipady=30)

coord_x1 = Label(frame, text= " 1        2        3        4        5        6        7        8        9       10", font=("Helvetica, 11"))
coord_x1.grid(row=12, column=1, columnspan=2)

coord_x2 = Label(frame, text= " 1        2        3        4        5        6        7        8        9       10", font=("Helvetica, 11"))
coord_x2.grid(row=12, column=5, columnspan=2)


for x in range(1, moteur.hauteur+1):
    templabel = Label(frame, text=chr(ord("A")+x-1 ), font=("Helvetica, 13"))
    templabel.grid(row=x, column=0)

for x in range(1, moteur.hauteur+1):
    templabel = Label(frame, text=chr(ord("A")+x-1 ), font=("Helvetica, 13"))
    templabel.grid(row=x, column=7) 

labeltest = Label(frame, text="")
labeltest.grid(row=2, column=3)

label_bateaux_restant_joueur = Label(frame, text="Bateaux restant joueur :\n"+str(nb_bateaux_restant_tout[0]), font=("Helvetica, 13"))
label_bateaux_restant_joueur.grid(row=4, column=3, rowspan=2 )

label_bateaux_restant_ordi = Label(frame, text="Bateaux restant ordi :\n"+str(nb_bateaux_restant_tout[1]), font=("Helvetica, 13"))
label_bateaux_restant_ordi.grid(row=6, column=3, rowspan=2 )

label_bateau_reste_placer = Label(frame, text="Il vous reste {}\nbateaux à placer".format(moteur.nb_bateau), font=("Helvetica", "13", "bold"))
label_bateau_reste_placer.grid(row=2, column=3, rowspan=2)

#cree canvas
canvas1 = Canvas(frame, highlightthickness = 1, highlightbackground="Black", width = 400, height= 400, bg="#3d8fec")
canvas1.grid(row=1, column=1, columnspan=2, rowspan=10)



for i in range(moteur.hauteur):
    canvas1.create_line(0, 40*i, 400, 40*i, width=1)
    canvas1.create_line(40*i, 0, 40*i, 400, width=1)


canvas2 = Canvas(frame, highlightthickness = 1, highlightbackground="Black", width = 400, height= 400, bg="#3d8fec")
canvas2.grid(row=1, column=5, columnspan=2, rowspan=10)

for i in range(moteur.hauteur):
    canvas2.create_line(0, 40*i, 400, 40*i, width=1)
    canvas2.create_line(40*i, 0, 40*i, 400, width=1)

#cree boutons
bouton_bateaux = Button(frame, text="Placer un bateau", font=("Helvetica, 12"), command=selection_bateau, bg="#ffcc46")
bouton_bateaux.grid(row=13, column=1)

bouton_quitter = Button(frame, text="Quitter", font=("Helvetica, 12"), bg= "#df3f18", command=fenetre.destroy, fg="white")
bouton_quitter.grid(row=13, column=3)

bouton_recommencer = Button(frame, text="Nouvelle partie", bg="#18dfca", font=("Helvetica, 12"), command=recommencer)
bouton_recommencer.grid(row=13, column=6)


#pack la fenêtre
frame.pack(expand=YES)



fenetre.mainloop()