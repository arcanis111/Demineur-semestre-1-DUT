# Information : l'affichage des scores se fait sur l'invite de commande (ou en ouvrant le fichier texte)
#On importe les modules nécessaires
from tkinter import *
from tkinter.messagebox import *
from tkinter import simpledialog
from random import randint
import time
from datetime import datetime


#procédure generateur : générer les grilles nécessaires, avec comme paramètres : la longueur et la largeur de la grille, le nombre de bombes et le temps 
def generateur(long, larg, bombmax,t1):
    # On intialise les 2 tableaux
    Grille=[] # Tableau de référence, qui entiérement complété dès le départ
    Grille2=[] # Tableau de jeu, qui sera vide au départ
    
    # On génère les tableaux à doubles entrées
    for i in range(long):  #Pour i allant de 0 à la (longeur-1)
        Grille.append(["0"] * larg) #A chaque ligne, on ajoute au tableau larg fois "0"
        Grille2.append([" "] * larg) #A chaque ligne, on ajoute au tableau larg fois une case vide
        
    bombpos=0 #On initialise le nombre de bombes posé
    #On mets les bombes aléatoirement dans la grille
    while bombpos<bombmax: # Tant qu'on n'a pas posé le nombre de bombes demandé
        Y = randint(0, long-1) #La variable Y prend une valeur aléatoire comprise entre 0 et long-1
        X = randint(0, larg-1) #La variable X prend une valeur aléatoire comprise entre 0 et larg-1
        if Grille[Y][X]!="B": #S'il n'y pas déjà une bombe à l'emplacement correspondant aux coordonnées Y et X
            Grille[Y][X] = "B" # On met une bombe à ces coordonnées
            bombpos+=1 #On incrémente le nombre de bombes posées        

    #On mets, dans chaque case du tableau, le chiffre correspondant aux nombre de bombes se trouvant dans les 8 cases autour     
    for i in range(long): # On parcourt la longueur du tableau
        for j in range(larg): # On parcourt la largeur du tableau
            bombesvoisines = 0 # On initialise la variable bombevoisines, pour chaque case
            if Grille[i][j] != "B": #Si la case ne contient pas de bombe, on fait le traitement, sinon on passe à la suivante
                if j < larg-1:#droite #Si on ne se trouve pas tout à droite (sinon on sortirait du tableau)
                    if Grille[i][j+1] == "B":  # si la case se trouvant à droite contient une bombe
                        bombesvoisines += 1 # On incrémente bombesvoisines
                if j > 0: #Si on ne se trouve pas tout à gauche (sinon on sortirait du tableau)
                    if Grille[i][j-1] == "B": # si la case se trouvant à gauche contient une bombe
                        bombesvoisines += 1 # On incrémente bombesvoisines
                if i > 0: #Si on n'est pas tout en haut (1ère ligne)
                    if j > 0: #Si on ne se trouve pas tout à gauche 
                        if Grille[i-1][j-1] == "B":  #si la case se trouvant en haut à gauche contient une bombe
                            bombesvoisines += 1 # On incrémente bombesvoisines
                    if Grille[i-1][j] == "B": #si la case se trouvant en haut contient une bombe
                        bombesvoisines += 1  #On incrémente bombesvoisines
                    if j < larg-1: #Si on ne se trouve pas tout à droite
                        if Grille[i-1][j+1] == "B":  #si la case se trouvant en haut à droite contient une bombe
                            bombesvoisines += 1 #On incrémente bombesvoisines
                if i < long-1: #Si on n'est pas tout en bas (dernière ligne)
                    if j > 0: #Si on ne se trouve pas tout à gauche 
                        if Grille[i+1][j-1] == "B": #si la case se trouvant en bas à gauche contient une bombe
                            bombesvoisines += 1 #On incrémente bombesvoisines
                    #bas
                    if Grille[i+1][j] == "B": #si la case se trouvant en bas à gauche contient une bombe
                        bombesvoisines += 1 #On incrémente bombesvoisines
                    if j < larg-1: #Si on ne se trouve pas tout à droite
                        if Grille[i+1][j+1] == "B": #si la case se trouvant en bas à droite contient une bombe
                            bombesvoisines += 1 #On incrémente bombesvoisines  
                Grille[i][j] = bombesvoisines # On met le nombre de bombe dans la case
    affichage(Grille,Grille2,larg,long,bombmax,t1) # On fait appel à la fonction affichage


#procédure creuser avec comme paramètres, x et y, les coordonnées de la case où l'on a cliqué, la grille de référence et la grille de jeu, long, larg et bombmax
def creuser(x,y,Grille,Grille2,long,larg,bombmax):
        grillecreuse = Grille[x][y] # On met la valeur se trouvant à la position x et y du tableau de référence dans la variable grillecreuse
        if Grille2[x][y] == str(grillecreuse) or Grille2[x][y]=="P": #Si on a déja creusé à cette endroit ou qu'un drapeau est posé 
            return # On ne fait rien                 
        else: # Sinon
            Grille2[x][y] = str(grillecreuse) # On met la valeur de grillecreuse dans le tableau  de jeu
        if grillecreuse == 0: # On met la valeur de grillecreuse est 0
            for i in range(max(0, x-1), min(x+2, long)): #On parcourt la ligne de la case  
                for j in range(max(0, y-1), min(y+2, larg)): #On parcourt la colonne de la case  
                    creuser(i,j,Grille,Grille2,long,larg,bombmax) # On fait un appel récursif de la fonction creuser, sur la case de coordonnées i et j
        return 

# procédure poserdreapeau
def poserdrapeau(x,y,Grille,Grille2,long,larg,bombmax):
        if  Grille2[x][y]==" " : # Si la case de la grille de jeu est vide
            Grille2[x][y]="P" # On pose un drapeau
        elif Grille2[x][y]=="P":  # Si la case de la grille de jeu contient déjà un drapeau
            Grille2[x][y]=" " #On enlève le drapeau
        return

#procédure cliqueG : clique gauche, associé à l'action "creuser"
def cliqueG(x,y,Grille,Grille2,long,larg,bombmax,t1,Grille3):
    creuser(x,y,Grille,Grille2,long,larg,bombmax) # On creuse aux coordonnées indiquées
    # On rafraichi ensuite l'affichage, en changeant le texte contenu dans les boutons
    for i in range(long):
        for j in range(larg):
            couleur = "white"
            #On fonction du contenu de la case, on va changer la couleur de fond du bouton
            if Grille2[i][j] == "0" : 
                couleur = "lightyellow"
            elif Grille2[i][j] == "1" :
                couleur = "palegoldenrod"
            elif Grille2[i][j]== "2" :
                couleur = "lightcoral"
            elif Grille2[i][j] == "3" :
                couleur = "red"
            elif Grille2[i][j] == "P" :
                couleur = "blue"
            Grille3[i][j].config(text=Grille2[i][j],background=couleur) #Chaque bouton prend la valeur de la grille de jeu (grille2) correpondant aux mêmes coordonnées 
    
    verifvictoire(Grille,Grille2,larg,long,bombmax,t1) # On vérifie si on a gagné ou perdu
    return

#procédure cliqueD : clique droit, associé à l'action "poser un drapeau"
def cliqueD(x,y,Grille,Grille2,long,larg,bombmax,t1,Grille3):
    poserdrapeau(x,y,Grille,Grille2,long,larg,bombmax) # On pose un drapeau, si possible, aux coordonnées x et y

    for i in range(long):
        for j in range(larg):
            couleur = "white"
            if Grille2[i][j] == "0" :
                couleur = "lightyellow"
            elif Grille2[i][j] == "1" :
                couleur = "palegoldenrod"
            elif Grille2[i][j]== "2" :
                couleur = "lightcoral"
            elif Grille2[i][j] == "3" :
                couleur = "red"
            elif Grille2[i][j] == "P" :
                couleur = "blue"
            Grille3[i][j].config(text=Grille2[i][j],background=couleur) 
    return

# procédure verifvictoire : permet de vérifier l'état du jeu
def verifvictoire(Grille,Grille2,larg,long,bombmax,t1):
    nbremplie=0 # On initialise la variable nbremplie ,correspondant au nombre de cases remplies
    for i in range(long): #On parcourt la longueur du tableau
        for j in range(larg): #On parcourt la largeur du tableau
            if Grille2[i][j]!=" " and Grille2[i][j]!="P" and Grille2[i][j]!="B": #Si la case n'est pas vide, n'est pas un drapeau et une bombe
                nbremplie += 1 # On incrémente nbremplie
            elif Grille2[i][j]=="B": #Si la case contient une bombe
                showinfo("Perdu", "Vous avez perdu!") #On affiche qu'on a perdu
                nouvellepartie() # On relance une nouvelle partie
            
    #Conditions de victoire
    if nbremplie==(long*larg)-bombmax: # Si toutes les cases, sauf celles contenant une bombe, ont été creusées
        t2=time.time() #On prend le temps de fin de partie
        t3=int(t2-t1) # On calcule le temps qu'à duré la partie
        showinfo("Gagne","Vous avez gagné" ) # On affiche qu'on a gagné
        showinfo("Score en secondes",t3 ) # On affiche le score
        nom = simpledialog.askstring("Entrer", "Entrer votre nom")
        gestionscore(str(long),str(larg),str(bombmax),nom,str(t3))
        nouvellepartie() # On relance une nouvelle partie
    return

# Procédure affichage : générer une grille de bouton pour l'interface graphique
def affichage(Grille,Grille2,larg,long,bombmax,t1):
    
    #Configurations des lignes et des colonnes
    Grid.rowconfigure(fenetre, 0, weight=1) 
    Grid.columnconfigure(fenetre, 0, weight=1) 

    #On créée et on configure le "frame"
    frame=Frame(fenetre)
    frame.grid(row=0, column=0, sticky=N+S+E+W)
    Grille3=[]
    for i in range(long):  #Pour i allant de 0 à la (longeur-1)
        Grille3.append(["0"] * larg) #A chaque x, on ajoute au tableau larg fois "0"

    # On génère la grille de boutons
    for i in range(long): #On parcourt la longueur
        Grid.rowconfigure(frame, i, weight=1) 
        for j in range(larg):  #On parcourt la largeur
         Grid.columnconfigure(frame, j, weight=1)
         couleur = "white"
         #On crée un bouton, avec la valeur correspondant à la grille 2, une couleur de fond, un relief quand on passe la souris dessus
         #Une commande : celle ci utilise une "mini fonction" lambda qui permet d'associer à chaque bouton ses coordonnées, ou fait ensuite appel à la fonction cliqueG avec ces coordonnées
         Grille3[i][j] = Button(frame,text=Grille2[i][j], background=couleur, overrelief="sunken",command=lambda x=i, y=j: cliqueG(x,y,Grille,Grille2,long,larg,bombmax,t1,Grille3))
         
         #On ajoute une autre commande au bouton, lorqu'on utilise le clic droit    
         Grille3[i][j].bind("<Button-3>", lambda event,x=i,y=j: cliqueD(x,y,Grille,Grille2,long,larg,bombmax,t1,Grille3))
         Grille3[i][j].grid(row=i, column=j, sticky=N+S+E+W)

#Les 4 procédures suivantes permettent de commencer une nouvelle partie, avec des difficultés différentes
#Débutant
def nouvellepartie():
    t1=time.time() # On prend le temps au démarrage de la partie
    #On définit les paramètres
    long=10
    larg=10
    bombmax=10
    # On fait appel à la procédure qui va générer les grilles
    generateur(long,larg,bombmax,t1)
#Intermédiaire 
def nouvellepartie2():
    t1=time.time()
    long=15
    larg=15
    bombmax=40
    generateur(long,larg,bombmax,t1)
# Expert 
def nouvellepartie3():
    t1=time.time()
    long=20
    larg=30
    bombmax=60
    generateur(long,larg,bombmax,t1) 
#Personnalise 
def nouvellepartie4():
    t1=time.time()
    #On initialise les paramètres
    long=0
    larg=0
    bombmax=0
    while long < 5 or long > 30 or type(long) != int : # On entre le paramètre, tant que la valeur n'est pas valide
        long = simpledialog.askinteger("Entrer", "Longueur de la grille(5 au minimum, 30 au maximum)")
        try: #on essaye de convertir la valeur entrer en entier
            long=int(long)
        except ValueError: # Si on n'y arrive pas, on indique une erreur et on recommence la boucle
            long=0
            print("erreur")
            
    while larg < 5 or larg > 30 or type(larg) != int :
        larg = simpledialog.askinteger("Entrer", "Largeur de la grille(5 au minimum, 30 au maximum)")
        try:
            larg=int(larg)
        except ValueError:
            larg=0
            print("erreur")
    while bombmax < 3 or  bombmax > (long*larg)/2 or type(bombmax) != int :
        bombmax = simpledialog.askinteger("Entrer", "Nombre de bombes(3 au minimum)")
        try:
            bombmax=int(bombmax)
        except ValueError:
            bombmax=0
            print("erreur")

    generateur(long,larg,bombmax,t1) 

def gestionscore(long,larg,bombmax,nom,t3): # Pour entrer un nouveau score
    score = open("score.txt", "a") #On écrit dans un fichier score, ou on le crée s'il n'existe pas
    score.write(" Longueur: ")
    score.write(long)
    score.write(" Largeur: ")
    score.write(larg)
    score.write(" Nombre de bombes: ")
    score.write(bombmax)
    score.write(" Nom du joueur: ")
    score.write(nom)
    score.write(" Score en secondes: ")
    score.write(t3)
    score.write(" Date de réalisation: ")
    date= str(datetime.now())
    score.write(date)
    score.write("\n")
    score.close() # On ferme le fichier
    return
    
def score(): # Pour afficher les scores
    score = open("score.txt", "a") 
    score = open("score.txt", "r")
    contenu = score.read()
    print(contenu)
    return
    
#Procédure permettant d'afficher les règles du jeu
def alert1():
    showinfo("Règle", "Le but du jeu est de déminer un terrain rempli de bombes")
#Procédure permettant d'afficher les instructions de jeu
def alert2():
    showinfo("Comment jouer", "Faites un clic gauche sur une case pour creuser, ou bien faites un clic droit pour y poser un drapeau et protéger la case")
        
#Début du programme
    
# Lancement de la fenêtre tkinter
fenetre = Tk() # on nomme la fenêtre tkinter "fenetre"
fenetre.title("Démineur") #titre de la fenêtre


#On met en place le menu
menubar = Menu(fenetre)
#Premier menu
menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Nouveau : Débutant",command=nouvellepartie) #1ère commande : Nouvelle partie Débutant
menu1.add_command(label="Nouveau : Intermédiaire",command=nouvellepartie2) #2ème commande : Nouvelle partie Intermediaire
menu1.add_command(label="Nouveau : Expert",command=nouvellepartie3) #3ème commande : Nouvelle partie Expert
menu1.add_command(label="Nouveau : Personnalisé",command=nouvellepartie4) #4ème commande : Nouvelle partie Personnalisé
menu1.add_command(label="Quitter", command=fenetre.destroy) #5ème commande : Quitter le jeu
menubar.add_cascade(label="Partie", menu=menu1) # Nom du menu 1, qui est de type "cascade"

#Deuxième menu
menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Règles", command=alert1) #1ère commande : Règles
menu2.add_command(label="Comment jouer", command=alert2) #2ème commande : Comment jouer
menu2.add_command(label="Scores", command=score) # On fait appel à la fonction score, qui va ouvrir et lire le fichier contenant les scores
menubar.add_cascade(label="Aide", menu=menu2) # Nom du menu, qui est de type "cascade"
fenetre.config(menu=menubar)

nouvellepartie() # On lance une nouvelle partie

fenetre.mainloop() # fin de la fenetre
fenetre.destroy # destruction de la fenetre
    




