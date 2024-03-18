# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:29:47 2024

@author: emmad
"""

import tkinter as tk
from tkinter import ttk


def lire_colonne(nom_fichier,i):
    # Ouvrir le fichier en mode lecture
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()

    # Initialiser une liste vide pour stocker les valeurs de la colonne
    colonne = []

    # Trouver l'index où se termine l'en-tête
    index_endheader = lignes.index('endheader\n')

    # Parcourir les lignes du fichier à partir de l'index après 'endheader'
    for ligne in lignes[index_endheader+2:]:
        # Fractionner la ligne en fonction des tabulations
        valeurs = ligne.strip().split()
        # Vérifier si la liste de valeurs contient au moins 2 éléments
        if len(valeurs) >= 2:
            # Si c'est le cas, convertir la valeur souhaitée en float et l'ajouter à la liste
            colonne.append(float(valeurs[i]))   
            
    return colonne

def cut_file(nom_fichier, begin_entry, end_entry):
    
    #recup les instants de debut et de fin du mouvement
    val_b = float(begin_entry.get())
    val_e = float(end_entry.get())
   
    # recup les temps et valeurs
    time = lire_colonne(nom_fichier, 1)
    values = lire_colonne(nom_fichier, 2)
    
    #note les indices de dbut et fin du mvt
    for i in range(len(time)):
        if time[i]<=val_b:
            indx_b=i
    for i in range(len(time) - 1, -1, -1):
        if time[i] >= val_e:
            indx_e = i
            
    #on veut garder uniquement les lignes qui correspondent au mouvement
    time_cut=time[indx_b:indx_e+1]
    values_cut=values[indx_b:indx_e+1]
    #recuperer les listes des valeurs comprises entre les indoces de deb et de fin du mvt
    return(time_cut,values_cut)    
        
    
def close_window(root):
    root.destroy()
  
#regroupe les commandes du bouton entrer: couper le fichier et fermer la fenetre 
def bouton_entrer(nom_fichier, begin_entry, end_entry, root):
    cut_data = cut_file(nom_fichier, begin_entry, end_entry)
    close_window(root)
    return cut_data
   

def debut_fin_mvt(nom_fichier):
    # fenetre racine
    root = tk.Tk()
    root.geometry("280x100")
    root.title('Set up')
    root.resizable(1,1)
    
    # configurer la grille de la fenetre
    root.columnconfigure(0, weight=1)
    root.columnconfigure(1, weight=3)
    
    # Entrer le debut du mvt
    begin_label = ttk.Label(root, text="Debut du mouvement:")
    begin_label.grid(column=0, row=0, sticky=tk.W, padx=5, pady=5)
    
    begin_entry = ttk.Entry(root)
    begin_entry.grid(column=1, row=0, sticky=tk.E, padx=5, pady=5)
    
    # Entrer la fin
    end_label = ttk.Label(root, text="Fin du mouvement:")
    end_label.grid(column=0, row=1, sticky=tk.W, padx=5, pady=5)
    
    end_entry = ttk.Entry(root)
    end_entry.grid(column=1, row=1, sticky=tk.E, padx=5, pady=5)
    
    # Config bouton "entrer"
    enter_button = ttk.Button(root, text="Entrer",command=lambda: bouton_entrer(nom_fichier, begin_entry, end_entry, root))
    enter_button.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)
    
    root.mainloop()

#def variables
nom_fichier="C:/Users/emmad/Documents/2A/PI13/acqui/Lucile2"
debut_fin_mvt(nom_fichier)