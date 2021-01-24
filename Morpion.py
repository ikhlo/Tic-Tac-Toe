# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 14:02:11 2020

@author: ikhla
"""

from sys import maxsize
from math import sqrt
from random import *
from tkinter import *
from tkinter.messagebox import *

def Nouveau(n):
    grille = ["-" for i in range(n**2)]
    return grille

# Affiche la grille
def Affiche(grille):
    n = len(grille)
    for i in range(n):
        print(grille[i], end ='')
        if(i % sqrt(n) == sqrt(n)-1): print("")
        else : print(" ",end='')
       
# Indique quel joueur doit jouer        
def Tour(grille):
    countX = 0
    countO = 0
    for i in grille:
        if (i == "X") : countX += 1
        elif (i == "O") : countO += 1
    if countX == countO : return "X"
    else : return "O"
    
# Indique les différents coups à jouer    
def CoupPossible(grille):
    l = []
    for i in range(len(grille)) :
        if (grille[i] == "-") : l.append(i)
    return l
    
# Indique si'il y a une victoire  
def Victoire(grille, choix = "X"):
    rslt = ""
    n = int(sqrt(len(grille)))
    
    for i in range(n):
        testcolonne = []
        
        # Vérifie la victoire sur les colonnes
        for j in range(i,len(grille),n):
            testcolonne.append(grille[j])
        if ("-" not in testcolonne):
            if("X" not in testcolonne or "O" not in testcolonne):
                rslt = testcolonne[0]
        
        #Vérifie la victoire sur les lignes
        testligne = grille[i*n:(i*n)+n]
        if ("-" not in testligne):
            if("X" not in testligne or "O" not in testligne):
                rslt = testligne[0]
        
    #Verifie la victoire sur les diagonales
    diag1 = grille[0::(n+1)]
    diag2 = grille[n-1::n-1]
    del diag2[len(diag2)-1]
    
    if ("-" not in diag1):
        if("X" not in diag1 or "O" not in diag1):
            rslt = diag1[0]
    
    if ("-" not in diag2):
        if("X" not in diag2 or "O" not in diag2):
            rslt = diag2[0]          
                
    if (rslt == choix) : return 1
    elif (rslt == "") : return 0
    else : return -1
    
# Fonction qui va placer le symbole dans la grille    
def CoupJouer(grille,n):
    assert n in range(len(grille))
    cell = list(grille)
    cell[n] = Tour(grille)
    return cell
    
# Indique si la partie est terminée
def Terminal_Test(grille):
    if (Victoire(grille) != 0) : return True
    elif ("-" not in grille) : return True
    else : return False
    
  
def minimax(grille, choix):
    Actions = CoupPossible(grille)
    grille_actions = [minvalue(CoupJouer(grille,a),choix) for a in Actions]
    return Actions[grille_actions.index(max(grille_actions))]
    
def maxvalue(grille,choix):
    if (Terminal_Test(grille)): return Victoire(grille,choix)
    valeur = - maxsize
    for i in CoupPossible(grille):
        valeur = max(valeur,minvalue(CoupJouer(grille,i),choix))
    return valeur

def minvalue(grille,choix):
    if (Terminal_Test(grille)): return Victoire(grille,choix)
    valeur = maxsize
    for i in CoupPossible(grille):
        valeur = min(valeur,maxvalue(CoupJouer(grille,i),choix))
    return valeur
    


def Alpha_Beta(grille, profondeur, choix):
    resultat = 0
    best_profondeur = 0
    valeur = maxvalue2(grille,-maxsize,maxsize,profondeur,choix)
    Actions = CoupPossible(grille)
    grille_actions = [minvalue2(CoupJouer(grille,a),-maxsize,maxsize,profondeur-1,
                                choix) for a in Actions]
    # Partie qui va choisir l'action avec la bonne valeur et nécessitant le
    # moins de mouvement possible avec la profondeur
    for a in grille_actions :
        if (a[0] == valeur[0] and a[1] > best_profondeur): 
            resultat = grille_actions.index(a)
            best_profondeur = a[1]
    return Actions[resultat]
    
def maxvalue2(grille,alpha,beta,profondeur,choix):
    if (Terminal_Test(grille)) : return Victoire(grille,choix), profondeur
    v = -maxsize
    for a in CoupPossible(grille):
        f = minvalue2(CoupJouer(grille,a),alpha,beta,profondeur-1,choix)
        v = max(v,f[0])
        if (v >= beta) : return v, f[1]
        alpha = max(alpha,v)
    return v, f[1]

def minvalue2(grille,alpha,beta,profondeur,choix):
    if (Terminal_Test(grille)) : return Victoire(grille,choix), profondeur
    v = maxsize
    for a in CoupPossible(grille):
        f = maxvalue2(CoupJouer(grille,a),alpha,beta,profondeur-1,choix)
        v = min(v,f[0])
        if (v <= alpha) : return v, f[1]
        beta = min(beta,v)
    return v, f[1]

    
def TailleJeu():
    g = Nouveau(eval(input("Rentrez une dimension de jeu : ")))
    Affiche(g)
    print("")
    return g

def Mode():
    choix = input("Si vous souhaitez-commencer, tapez 'y' sinon tapez n : ")
    if choix == "y" : adv = "O"
    else : adv = "X"
    return adv

def Exo():
    ia = Mode()
    g = TailleJeu()
    N = len(g)
    while (not Terminal_Test(g)):
        if (Tour(g) == ia):
            g = CoupJouer(g, Alpha_Beta(g,9,ia))
            Affiche(g)
            print("")
        else :
            if(not Terminal_Test(g)):
                x = eval(
                    input(("Entrez un chiffre entre 1 et %i n'étant pas déjà pris : ")%N)) - 1
                while (g[x] != "-") :
                    x = eval(
                    input(("Entrez un chiffre entre 1 et %i n'étant pas déjà pris : ")%N)) - 1    
                g = CoupJouer(g, x)
                Affiche(g)
                print("")

def TEST():
    # Pour vérifier que le code choisit le meilleur chemin
    G = Nouveau(3)
    G[5],G[8] = "O","O"
    G[3],G[6] = "X","X"
    Affiche(G)
    print(minimax(G,"O"))
 
    
def Rond(x,y):
    Jeu.create_oval(x-72,y-72,x+72,y+72,outline="blue",width="4")
    
def Croix(x,y):
    Jeu.create_line(x-72,y-72,x+72,y+72,fill="red",width="4")
    Jeu.create_line(x+72,y-72,x-72,y+72,fill="red",width="4")
    
def ClickC(event):
    X = event.x
    Y = event.y
    
    X = int((X // 150)*150 + 75)
    Y = int((Y // 150)*150 + 75)
    index = (Y//150)*3 + X//150
    
    if (g[index] == "-") :

        if (ia == "X") : 
            Rond(X,Y)
            g[index] = "O"
        else : 
            Croix(X,Y)
            g[index] = "X"
            
        if (Terminal_Test(g)) : #Fin de partie
            if (Victoire(g,ia)== -1) :
                    showinfo(title="Morpion",message="La partie est finie, vous avez gagné.")
            else : showinfo(title="Morpion",message="La partie est finie, c'est un match nul.")
            Morpion.destroy()
            
        if (Terminal_Test(g) == False): #TOUR IA
            A = Alpha_Beta(g,9,ia)
            g[A] = ia
            X2 = (A % 3)*150 + 75
            Y2 = (A//3)*150 + 75
            if (ia == "X") : Croix(X2,Y2)
            else : Rond(X2,Y2)
            if (Terminal_Test(g)) : #Fin de partie apres l'ia
                if (Victoire(g,ia)==1) :
                    showinfo(title="Morpion",message="La partie est finie, vous avez perdu.")
                else : showinfo(title="Morpion",message="La partie est finie, c'est un match nul.")
                Morpion.destroy()
    else :
        showerror(message = "Vous ne pouvez pas jouer ici.")

ia = Mode()
g = Nouveau(3)
Morpion = Tk()
Morpion.title("Morpion")
Morpion.resizable(0,0)
Jeu = Canvas(Morpion,width=450,height=450, bg="white")
Jeu.pack()
Jeu.create_line(0,150,450,150,fill="gray", width="5")
Jeu.create_line(0,300,450,300,fill="gray", width="5")
Jeu.create_line(150,0,150,450,fill="gray", width="5")
Jeu.create_line(300,0,300,450,fill="gray", width="5")

QUIT = Button(Morpion,text="Quitter",fg="red",font="bold",
              command=Morpion.destroy).pack(side=BOTTOM)

Jeu.bind("<Button-1>",ClickC)

if(ia ==  "X") : 
     A = Alpha_Beta(g,9,ia)
     g[A] = ia
     X2 = (A % 3)*150 + 75
     Y2 = (A//3)*150 + 75
     Croix(X2,Y2)

Morpion.mainloop()

#Exo()
