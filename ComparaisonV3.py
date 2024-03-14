#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:28:46 2024

@author: Charles
"""

import matplotlib.pyplot as plt
import numpy as np



"""""""""""""""""""""
Extraction des data
"""""""""""""""""""""

def lire_derniere_colonne(nom_fichier):
    # Ouvrir le fichier en mode lecture
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()

    # Initialiser une liste vide pour stocker les valeurs de la dernière colonne
    derniere_colonne = []

    # Parcourir les lignes du fichier à partir de l'index après 'endheader'
    for ligne in lignes[lignes.index('endheader\n')+1:]:
        # Fractionner la ligne en fonction des tabulations
        valeurs = ligne.strip().split()
        # Vérifier si la dernière valeur de la ligne est numérique
        if valeurs[-1].replace('.', '', 1).replace('-', '', 1).isdigit():
            # Si c'est le cas, convertir la dernière valeur en float et l'ajouter à la liste
            derniere_colonne.append(float(valeurs[-1]))

    return derniere_colonne


"""""""""""
Filtre
"""""""""""

def moving_average(data, window_size):
    filtered_data = []
    for i in range(len(data)):
        if i < window_size - 1:
            filtered_data.append(sum(data[:i+1]) / (i + 1))
        else:
            filtered_data.append(sum(data[i-window_size+1:i+1]) / window_size)
    return filtered_data


"""""""""""""""""
Mise en forme
"""""""""""""""""


def aligner_remplir(tableau1, tableau2, valeur_par_defaut=None):
    len1 = len(tableau1)
    len2 = len(tableau2)
    
    if len1 > len2:
        tableau2 += [valeur_par_defaut] * (len1 - len2)
    elif len2 > len1:
        tableau1 += [valeur_par_defaut] * (len2 - len1)
    
    return tableau1, tableau2


"""""""""""""""
Comparaison
"""""""""""""""

# Fonction pour tracer les courbes maximale, minimale et tester
def plot_max_min_tester(max_curve, min_curve, test_curve, not_between_indices):
    plt.plot(max_curve,linestyle='--', color='gray')
    plt.plot(min_curve, linestyle='--', color='gray')
    plt.fill_between(range(len(max_curve)), max_curve, min_curve, color='green', alpha=0.5)
    plt.plot(test_curve, color='blue', label='Mouvement')
    #for index in not_between_indices:
     #   plt.scatter(index, test_curve[index], color='black', label='Point hors de la zone')
    plt.fill_between(range(len(max_curve)), max_curve, min_curve, color='white', alpha=0.5)
    plt.legend()
    plt.xlabel('Index')
    plt.ylabel('Angles °')
    plt.title('Acceptability Area')
    plt.show()

# Fonction pour vérifier quels points de la troisième courbe ne sont pas entre la courbe maximale et minimale
def points_not_between(curve, max_curve, min_curve):
    not_between_indices = []
    for i in range(len(curve)):
        if curve[i] > max_curve[i] or curve[i] < min_curve[i]:
            not_between_indices.append(i)
    return not_between_indices


# Fonction pour aligner les courbes à leur minimum commun
def align_curves_to_common_min(max_curve, min_curve):
    # Trouver les indices des valeurs minimales dans les courbes
    min_index_max_curve = np.argmin(max_curve)
    min_index_min_curve = np.argmin(min_curve)
    
    # Calculer l'écart entre les indices des valeurs minimales
    shift_amount = min_index_max_curve - min_index_min_curve
    
    # Décaler la courbe avec la valeur minimale la plus éloignée vers la gauche (vers les indices inférieurs)
    if shift_amount > 0:
        min_curve = np.roll(min_curve, shift_amount)
    elif shift_amount < 0:
        max_curve = np.roll(max_curve, -shift_amount)
    
    return max_curve, min_curve



"""""
Main
"""""

def Comp_min(Nom_test,Nom_Lent,Nom_Rapide):
    #lire les fichier
    test_curve = lire_derniere_colonne(Nom_test)
    min_curve = lire_derniere_colonne(Nom_Lent)
    max_curve = lire_derniere_colonne(Nom_Rapide)

    #filtre
    window_size = 7
    test_curve = moving_average(test_curve, window_size)
    min_curve = moving_average(min_curve, window_size)
    max_curve = moving_average(max_curve, window_size)

    #S'assurer que les courbes ont la même taille
    
    
    max_curve_clean, min_curve_clean = aligner_remplir(max_curve, min_curve, valeur_par_defaut=0)
    min_curve_clean, test_curve_clean = aligner_remplir(min_curve, test_curve, valeur_par_defaut=0)
    max_curve_clean, test_curve_clean = aligner_remplir(max_curve, test_curve, valeur_par_defaut=0)
    
    

    # Aligner les courbes à leur minimum commun
    max_curve, min_curve = align_curves_to_common_min(max_curve_clean, min_curve_clean)
    test_curve, min_curve = align_curves_to_common_min(test_curve_clean, min_curve_clean)


    # Vérifier quels points de la troisième courbe ne sont pas entre la courbe maximale et minimale
    not_between_indices = points_not_between(test_curve, max_curve, min_curve)

    # Tracer les courbes maximale, minimale et testée avec les points qui ne sont pas entre la courbe maximale et minimale
    plot_max_min_tester(max_curve, min_curve, test_curve, not_between_indices)

    





Comp_min('Lucile4','GenouxLent','GenouxRap')











