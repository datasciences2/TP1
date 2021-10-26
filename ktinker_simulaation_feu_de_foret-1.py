# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 13:33:00 2020

@author: NEM'S
"""

from random import sample, randrange
from tkinter import Tk, Canvas, Scale, Button, Label, N, ALL
import math
import random

COLORS=["ivory","ivory", "lime green","red", "gray75"]
etat={'vide':1,'arbre':2,'feu':3,'cendre':4}

def random_forest(p, n):
    units=[(line,col) for col in range(n) for line in range(n)]
    nbr_arbres=int(n**2*p)
    arbres_complet=sample(units,nbr_arbres)# on tire au hasard l’échantillon de ntrees arbres parmi les n*n emplacements possibles.
    states=[[0]*n for _ in range(n)]
    for (i,j) in arbres_complet:
        states[i][j]=etat["arbre"]
    return states


def init_vegetation():
    veg_matrix = [[0 for col in range(taille)] for row in range(taille)]
    for i in range(taille):
        for j in range(taille):
            veg_matrix[i][j] = etat["vide"]
    return veg_matrix


def init_density():
    den_matrix = [[0 for col in range(taille)] for row in range(taille)]
    for i in range(taille):
        for j in range(taille):
            den_matrix[i][j] = etat["vide"]
    return den_matrix


def init_altitude():
    alt_matrix = [[0 for col in range(taille)] for row in range(taille)]
    for i in range(taille):
        for j in range(taille):
            alt_matrix[i][j] = etat["vide"]
    return alt_matrix



def Creat_case(states, line, col):
        A=(unit*col, unit*line)
        B=(unit*(col+1), unit*(line+1))
        state=states[line][col]
        color=COLORS[state]
        cnv.create_rectangle(A, B, fill=color, outline='')

def Afficher(states):
    n=len(states)
    for line in range(n):
        for col in range(n):
            Creat_case(states, line, col)


def tg(x):
    return math.degrees(math.atan(x))


def get_pente(altitude_matrix):
    matrice_pente = [[0 for col in range(taille)] for row in range(taille)]
    for ligne in range(taille):
        for col in range(taille):
            sous_matrice_de_pente = [[0,0,0],[0,0,0],[0,0,0]]
            if ligne == 0 or ligne == taille-1 or col == 0 or col == taille-1:  # marge de debourdement
                matrice_pente[ligne][col] = sous_matrice_de_pente
                continue
            altitude_actuelle = altitude_matrix[ligne][col]
            sous_matrice_de_pente[0][0] = tg((altitude_actuelle - altitude_matrix[ligne-1][col-1])/1.414)
            sous_matrice_de_pente[0][1] = tg(altitude_actuelle - altitude_matrix[ligne-1][col])
            sous_matrice_de_pente[0][2] = tg((altitude_actuelle - altitude_matrix[ligne-1][col+1])/1.414)
            sous_matrice_de_pente[1][0] = tg(altitude_actuelle - altitude_matrix[ligne][col-1])
            sous_matrice_de_pente[1][1] = 0
            sous_matrice_de_pente[1][2] = tg(altitude_actuelle - altitude_matrix[ligne][col+1])
            sous_matrice_de_pente[2][0] = tg((altitude_actuelle - altitude_matrix[ligne+1][col-1])/1.414)
            sous_matrice_de_pente[2][1] = tg(altitude_actuelle - altitude_matrix[ligne+1][col])
            sous_matrice_de_pente[2][2] = tg((altitude_actuelle - altitude_matrix[ligne+1][col+1])/1.414)
            matrice_pente[ligne][col] = sous_matrice_de_pente
    return matrice_pente


def calc_pw(angles):
    c_1 = 0.04#0.045  -----0.5 juste la partie droite---12 nord au sud
    c_2 = 0.111#0.131-----0.31juste la partie droite---12 nord au sud
    V = 10 # 12juste la partie droite ---12 nord au sud
    t = math.radians(angles)
    ft = math.exp(V*c_2*(math.cos(t)-1))
    return math.exp(c_1*V)*ft

def get_direction_vitesse_vent():

    matrice_vent = [[0 for col in [0,1,2]] for row in [0,1,2]]
    angles = [[45,0,45],
              #[30,0,30],
              [90,0,90],
              [135,180,135]]
    for ligne in [0,1,2]:
        for col in [0,1,2]:
            matrice_vent[ligne][col] = calc_pw(angles[ligne][col])
    matrice_vent[1][1] = 0
    return matrice_vent


def burn_or_not_burn(ligne_abs,col_abs,matrice_voisinage):
    global p#proba de densité
    p_veg = {1:-0.3,2:0,3:0.4}[matrice_vegetation[ligne_abs][col_abs]]
    # p_den = {1:-0.4,2:0,3:0.3}[matrice_density[ligne_abs][col_abs]]
    p_h = 0.58#0.58  ----0.058 juste la partie droite
    a = 0.058#0.078  ----0.0078juste la partie droite

    for ligne in [0,1,2]:
        for col in [0,1,2]:
            if matrice_voisinage[ligne][col] == etat["feu"]: # voisinage en feu
                # print(row,col)
                pente = matrice_pente[ligne_abs][col_abs][ligne][col]
                p_pente = math.exp(a * pente)
                p_vent = matrice_vent[ligne][col]
                p_feu = p_h * (1 + p_veg) * (1 + p) * p_vent * p_pente
                if p_feu > random.random():
                    
                    return etat["feu"]  #feu 

    return etat["arbre"] # arbre  qui reste intacte


def Actualisation_foret(ancien_foret):
    # global states
    resultat_foret = [[1 for i in range(taille)] for j in range(taille)]
    for ligne in range(1, taille-1):
        for col in range(1, taille-1):

            if ancien_foret[ligne][col] == 1 or ancien_foret[ligne][col] == 4:
                resultat_foret[ligne][col] = ancien_foret[ligne][col]  # c'est vide=1 ou c'est du cendre=4
            if ancien_foret[ligne][col] == 3:
                if random.random() < 0.4:
                    resultat_foret[ligne][col] = 3  # feu
                else:
                    resultat_foret[ligne][col] = 4#cendre
            if ancien_foret[ligne][col] == 2:
                voisinages = [[row_vec[col_vec] for col_vec in range(col-1, col+2)]
                              for row_vec in ancien_foret[ligne-1:ligne+2]]
                # print(voisinagesrs)
                resultat_foret[ligne][col] = burn_or_not_burn(ligne, col, voisinages)
    return resultat_foret



def init():
    global density, p,states, cpt, nb_total_abres, running,matrice_vegetation,matrice_density,matrice_vent,matrice_pente

    p=int(curseur.get())/100
    running=False
    cpt=0
    lbl["text"]="Étandue brulée %3s %%" %0
    lbl2["text"]="nombre arbres brulés %3s "%0
    curseur["state"]='normal'
    matrice_vegetation = init_vegetation()
    matrice_density = init_density()
    matrice_altitude = init_altitude()
    matrice_vent = get_direction_vitesse_vent()
    matrice_pente = get_pente(matrice_altitude)
    states=random_forest(p, n)
    nb_total_abres=int(n*n*p)
    cnv.delete(ALL)
    Afficher(states)
    print(p)
def set_density(states, p):
    global density
    n=len(states)
    arbres= [(i,j) for i in range(n) for j in range(n) if states[i][j]==etat["arbre"]]
    non_abrres=[(i,j) for i in range(n) for j in range(n) if states[i][j]!=etat["arbre"]]
    density=len(arbres)/n**2
    new_arbres=int(n*n*p)
    before=len(arbres) #nombre d'arbre qui existait deja 
    print(density,"proba ",p)
    now=len(non_abrres)
    delta=abs(new_arbres-before)
    if new_arbres>=before:
        for (i, j) in sample(non_abrres, delta):
            states[i][j]=etat["arbre"]
    else:
        for (i, j) in sample(arbres, delta):
            states[i][j]=etat["vide"]

def foret_refrabrique(percent):
    global nb_total_abres

    cnv.delete("all")
    p=float(percent)/100
    nb_total_abres=int(n*n*p)
    set_density(states,p)
    Afficher(states)


def propagate():
    global cpt, running,states

    states=Actualisation_foret(states)
    nfires=sum(states[i][j]==etat["feu"] for i in range(n) for j in range(n))
    cpt+=nfires
    percent = int(cpt/nb_total_abres*65)
    cnv.delete("all")
    Afficher(states)
    lbl["text"]="Étandue brulée %3s %%" %percent
    lbl2["text"]="nombre arbres brulés %3s " %cpt
    if nfires==0:
        running=False
        return
    cnv.after(100, propagate)

def mise_à_feu(event):
    global running, cpt

    i, j=event.y//unit, event.x//unit
    if states[i][j]==etat["arbre"]:
        states[i][j]=etat["feu"]
        Creat_case(states, i, j)

        cpt+=1
        if not running:
            running=True
            curseur["state"]='disabled'
            propagate()
CONSTANT=70
taille=CONSTANT
n=CONSTANT
unit=10

# Fenêtre et canevass
Mafenetre = Tk()
blanc_space =" "# epace blanche
Mafenetre.winfo_toplevel().title(80*blanc_space+'Propagation de feu de foret'.ljust(15).upper())
cnv = Canvas(Mafenetre, width=unit*n, height=unit*n, background="ivory")
# cnv.grid
cnv.grid(row=0, column=0 ,rowspan=1)

BoutonQuitter = Button(Mafenetre, text ='Quitter',font='Arial 15 bold', command = Mafenetre.destroy,width=18)
BoutonQuitter.grid(row=0, column=1)#, sticky=N)
btn=Button(Mafenetre,text="Nouvelle foret",  font='Arial 15 bold', command=init, width=18)
btn.grid(row=0, column=1, sticky=N)

lbl=Label(Mafenetre,text="Étandue brulée %3s %%" %0,  font='Arial 13 bold', bg='silver', width=18)
lbl.grid(row=2, column=1, sticky=N)

lbl2=Label(Mafenetre,text="Nombre d'arbres brulés %3s " %0,  font='Arial 13 bold',fg='blue', bg='white', width=25)
lbl2.grid(row=3, column=0, sticky=N)
# Clic qui met le feu
cnv.bind("<Button-1>", mise_à_feu)

curseur = Scale(Mafenetre, orient = "horizontal", command=foret_refrabrique, from_=100,
                to=0, length=200)
curseur.set(50)
curseur.grid(row=1, column=0,sticky=N)

init()

Mafenetre.mainloop()