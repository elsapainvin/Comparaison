
import numpy as np
import matplotlib.pyplot as plt
from fastdtw import fastdtw

data_em = np.genfromtxt("jG_emma.sto", delimiter="\t", skip_header=7)
data_lu = np.genfromtxt("jG_lucile.sto", delimiter="\t", skip_header=7)


# Fonction pour calculer le DTW et obtenir les indices du chemin d'alignement
def calculate_dtw(seq1, seq2):
  distance, path = fastdtw(seq1, seq2, 200)
  return distance, path


# Calculer le DTW
distance, path = calculate_dtw(data_em, data_lu)

# Gérer les différentes versions de la sortie de fastdtw
if isinstance(path, tuple):
  path = path[1]

# Extraire les indices du chemin d'alignement
indices_seq1, indices_seq2 = zip(*path)

plt.plot(data_em[:, 1], data_em[:, 2], label='data_1', marker='o')
plt.plot(data_lu[:, 1], data_lu[:, 2], label='data_2', marker='o')

plt.plot([data_em[indices_seq1, 1], data_lu[indices_seq2, 1]],
         [data_em[indices_seq1, 2], data_lu[indices_seq2, 2]], 'k--')
plt.xlabel('time (s)')
plt.ylabel('knee_angle_l')
plt.title('Changes in left knee angle during acquisition')
plt.legend()

plt.figure(2)
# Réalignement des séquences en utilisant le chemin d'alignement
aligned_data_em = np.array([data_em[i] for i, _ in path])

# Tracer les séquences originales
plt.plot(data_em[:, 1], data_em[:, 2], label='Mouvement de l utilisateur')
plt.plot(data_lu[:, 1], data_lu[:, 2], label='Mouvement de référence')
# recalage data_em sur time data_lu
plt.plot(data_lu[indices_seq2, 1],
         aligned_data_em[:, 2],
         label='Mouvement de l utilisateur après DTW', linestyle='--')

# légende
plt.legend(loc='lower right', fontsize='small')
plt.xlabel('time')
plt.ylabel('knee_angle_l')
plt.title('Résultat du DTW')

# Créer une nouvelle figure pour la courbe bleue
plt.figure(figsize=(8, 6))
plt.plot(data_em[:, 1], data_em[:, 2], label='Votre mouvement', linestyle='-')
plt.xlabel('temps (s)')
plt.ylabel('knee_angle_l')
plt.title('Analyse de la vitesse du mouvement')
plt.legend()

# Créer une nouvelle figure pour la courbe orange et verte
plt.figure(figsize=(8, 6))
plt.plot(data_lu[:, 1], data_lu[:, 2], label='Mouvement de référnce', linestyle='-', color="orange")
plt.plot(data_lu[indices_seq2, 1], data_em[indices_seq1, 2], label='Votre mouvement', linestyle='--', color='blue')
plt.xlabel('time (s)')
plt.ylabel('knee_angle_l')
plt.title('Analyse de l amplitude du mouvement')
plt.legend()

# Créer une matrice de chemin d'alignement avec des zéros
alignment_matrix = np.zeros((len(data_em), len(data_lu)))

# Mettre à jour la matrice avec les valeurs de chemin d'alignement
for i, j in path:
    alignment_matrix[i, j] = 1  # Mettre à 1 pour indiquer un point d'alignement

# Afficher la matrice de chemin (s fct de t ou qqch comme ca)
plt.figure(figsize=(10, 6), facecolor='white')
plt.imshow(alignment_matrix, cmap='gray_r', aspect='auto', vmin=0, vmax=1)

# Afficher la droite x=y en bleu
plt.plot(np.arange(len(data_lu)), np.arange(len(data_lu)), color='blue', linewidth=2)

# Trouver les points qui dépassent de la droite x=y et les tracer en rouge
for i in range(len(data_em)):
    for j in range(len(data_lu)):
        if alignment_matrix[i, j] == 1 and i != j:
            plt.scatter(j, i, color='red', s=6)
            
# Liste pour stocker les indices des points d'intersection
indices_intersection = []

# Parcourir les points rouges pour trouver les indices correspondants
for i in range(len(data_em)):
    for j in range(len(data_lu)):
        if alignment_matrix[i, j] == 1 and i == j:  # Vérifiez si le point d'alignement est sur la diagonale x=y
            indice_data_em = i  # Indice dans data_em
            indice_data_lu = j  # Indice dans data_lu
            indices_intersection.append((indice_data_em, indice_data_lu))  # Ajoutez l'indice à la liste

# Afficher les indices des points d'intersection
print("Indices des points d'intersection :", indices_intersection)

def lire_deuxieme_colonne(nom_fichier):
    # Ouvrir le fichier en mode lecture
    with open(nom_fichier, 'r') as fichier:
        lignes = fichier.readlines()

    # Initialiser une liste vide pour stocker les valeurs de la deuxième colonne
    deuxieme_colonne = []

    # Trouver l'index où se termine l'en-tête
    index_endheader = lignes.index('endheader\n')

    # Parcourir les lignes du fichier à partir de l'index après 'endheader'
    for ligne in lignes[index_endheader+2:]:  # Ignorer la première ligne après l'en-tête
        # Fractionner la ligne en fonction des tabulations
        valeurs = ligne.strip().split()
        # Vérifier si la liste de valeurs contient au moins 2 éléments
        if len(valeurs) >= 2:
            # Si c'est le cas, convertir la deuxième valeur en float et l'ajouter à la liste
            deuxieme_colonne.append(float(valeurs[1]))

    return deuxieme_colonne



# Utiliser la fonction pour extraire les données temporelles des deux fichiers
temps_data_em = lire_deuxieme_colonne("jG_emma.sto")
temps_data_lu = lire_deuxieme_colonne("jG_lucile.sto")

# Trouver les temps correspondants aux indices des points d'intersection
temps_intersection = []

for indice_data_em, indice_data_lu in indices_intersection:
    temps_intersection.append((temps_data_em[indice_data_em], temps_data_lu[indice_data_lu]))

# Afficher les temps correspondants aux indices des points d'intersection
print("Temps correspondants aux indices des points d'intersection :", temps_intersection)
                      
# Liste pour stocker les temps du premier et du dernier point d'intersection pour chaque dépassement
temps_premier_dernier_intersection = []

# Initialisation des variables pour stocker le premier indice de dépassement
premier_indice_depassement = None

# Parcourir les indices des points d'intersection
for i, (indice_data_em, indice_data_lu) in enumerate(indices_intersection):
    # Vérifier si c'est le début d'un nouveau dépassement
    if i == 0 or (indices_intersection[i - 1][0] != indice_data_em - 1 and indices_intersection[i - 1][1] != indice_data_lu - 1):
        premier_indice_depassement = i

    # Vérifier si c'est la fin du dépassement actuel ou la fin de la liste
    if i == len(indices_intersection) - 1 or (indices_intersection[i + 1][0] != indice_data_em + 1 and indices_intersection[i + 1][1] != indice_data_lu + 1):
        dernier_indice_depassement = i

        # Extraire les temps du premier et du dernier point d'intersection pour ce dépassement
        temps_premier_intersection = (temps_data_em[indices_intersection[premier_indice_depassement][0]], temps_data_lu[indices_intersection[premier_indice_depassement][1]])
        temps_dernier_intersection = (temps_data_em[indices_intersection[dernier_indice_depassement][0]], temps_data_lu[indices_intersection[dernier_indice_depassement][1]])

        # Ajouter les temps du premier et du dernier point d'intersection à la liste
        temps_premier_dernier_intersection.append((temps_premier_intersection, temps_dernier_intersection))

# Afficher les temps du premier et du dernier point d'intersection pour chaque dépassement
for i, (temps_premier, temps_dernier) in enumerate(temps_premier_dernier_intersection):
    print(f"Dépassement {i + 1}: Premier temps d'intersection = {temps_premier}, Dernier temps d'intersection = {temps_dernier}")


plt.xlabel('Indices de data_lu')
plt.ylabel('Indices de data_em')
plt.title('Matrice de chemin d\'alignement')

plt.figure(figsize=(8, 6))
plt.plot(data_em[:, 1], data_em[:, 2], label='Votre mouvement', linestyle='-')

# Calculer la durée totale de la séquence
duree_totale = data_em[-1, 1] - data_em[0, 1]

# Initialiser une variable pour suivre la position actuelle dans la séquence
position = data_em[0, 1]

# Parcourir les temps du premier et du dernier point d'intersection pour chaque dépassement
for temps_premier, temps_dernier in temps_premier_dernier_intersection:
    # Ajouter une bande semi-opaque blanche entre les temps actuel et du premier point d'intersection
    plt.axvspan(position, temps_premier[0], alpha=0.3, color='red')  
    # Ajouter le texte "trop rapide" dans la zone rose
    plt.text((position + temps_premier[0]) / 2, plt.ylim()[0] + (plt.ylim()[1] - plt.ylim()[0]) / 2, 'Trop rapide', color='red', ha='center', va='center')
    # Mettre à jour la position actuelle à la fin du dernier point d'intersection
    position = temps_dernier[0]

# Ajouter une bande semi-opaque blanche entre la dernière position et la fin de la séquence
plt.axvspan(position, data_em[-1, 1] + duree_totale * 0.1, alpha=0.3, color='white')

plt.xlabel('temps (s)')
plt.ylabel('knee_angle_l')
plt.title('Analyse de la vitesse du mouvement')
plt.legend()
plt.show()





plt.show()
