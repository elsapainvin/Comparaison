import numpy as np
import matplotlib.pyplot as plt
from fastdtw import fastdtw

def load_data(file_name):
    return np.genfromtxt(file_name, delimiter="\t", skip_header=7)

def calculate_dtw(seq1, seq2):
    distance, path = fastdtw(seq1, seq2, 200)
    if isinstance(path, tuple):
        path = path[1]
    return distance, path

def plot_trajectories(data1, data2, path):
    indices_seq1, indices_seq2 = zip(*path)
    
    plt.figure(figsize=(8, 6))
    plt.plot(data1[:, 1], data1[:, 2], label='Trajectoire 1', marker='o')
    plt.plot(data2[:, 1], data2[:, 2], label='Trajectoire 2', marker='o')
    plt.plot([data1[indices_seq1, 1], data2[indices_seq2, 1]],
             [data1[indices_seq1, 2], data2[indices_seq2, 2]], 'k--')
    plt.xlabel('Temps (s)')
    plt.ylabel('Angle du genou (l)')
    plt.title('Comparaison des trajectoires')
    plt.legend()
    plt.show()
    
def plot_dtw_results(data1, data2, path):
    """
    Modifie les données en fonction du chemin d'alignement DTW et renvoie les valeurs des courbes.
    
    Args:
    - data1 : np.array, les données de la première séquence.
    - data2 : np.array, les données de la deuxième séquence.
    - path : list, le chemin d'alignement obtenu par DTW.
    
    Returns:
    - dict: Dictionnaire contenant les listes des valeurs x et y pour chaque courbe.
    """
    # Extraire les indices des chemins d'alignement
    indices_seq1, indices_seq2 = zip(*path)
    
    # Réalignement des séquences en utilisant le chemin d'alignement
    aligned_data1 = np.array([data1[i] for i in indices_seq1])
    
    # Préparer les données pour les courbes
    curve_data = {
        'original_user_movement_x': data1[:, 1].tolist(),
        'original_user_movement_y': data1[:, 2].tolist(),
        'reference_movement_x': data2[:, 1].tolist(),
        'reference_movement_y': data2[:, 2].tolist(),
        'aligned_user_movement_x': data2[indices_seq2, 1].tolist(),
        'aligned_user_movement_y': aligned_data1[:, 2].tolist(),
    }
    
    # Optionnel : afficher le graphique ici ou dans un autre contexte
    plt.figure(figsize=(10, 6))
    plt.plot(curve_data['original_user_movement_x'], curve_data['original_user_movement_y'], label='Mouvement de l’utilisateur', linestyle='-')
    plt.plot(curve_data['reference_movement_x'], curve_data['reference_movement_y'], label='Mouvement de référence', linestyle='-')
    plt.plot(curve_data['aligned_user_movement_x'], curve_data['aligned_user_movement_y'], label='Mouvement de l’utilisateur après DTW', linestyle='--')
    plt.xlabel('Temps (s)')
    plt.ylabel('Angle du genou (l)')
    plt.title('Résultat du DTW')
    plt.legend(loc='lower right', fontsize='small')
    plt.show()
    
    return curve_data


def create_alignment_matrix(path, len_seq1, len_seq2):
    """
    Crée une matrice d'alignement à partir du chemin d'alignement fourni par DTW.

    Args:
    - path : list, le chemin d'alignement obtenu par DTW.
    - len_seq1 : int, la longueur de la première séquence.
    - len_seq2 : int, la longueur de la deuxième séquence.

    Returns:
    - alignment_matrix : np.array, une matrice indiquant les points d'alignement.
    """
    alignment_matrix = np.zeros((len_seq1, len_seq2))
    for i, j in path:
        alignment_matrix[i, j] = 1
    return alignment_matrix

def plot_alignment_matrix_with_acceptance_zone(data_em, data_lu, alignment_matrix):
    """
    Trace la matrice de chemin d'alignement avec une zone d'acceptabilité.

    Args:
    - data_em : np.array, les données de la première séquence.
    - data_lu : np.array, les données de la deuxième séquence.
    - alignment_matrix : np.array, une matrice indiquant les points d'alignement entre les séquences.
    """
    # Calculer la droite x = y
    x_values = np.arange(max(len(data_em), len(data_lu)))

    # Définir une marge constante pour la zone d'acceptabilité
    marge = max(len(data_em), len(data_lu)) * 0.05  # 5% de la longueur maximale

    # Calculer les limites de la zone d'acceptabilité parallèles à x = y
    lower_bound = x_values - marge
    upper_bound = x_values + marge

    plt.figure(figsize=(10, 6))
    # Afficher la droite x=y en bleu
    plt.plot(x_values, x_values, color='blue', linewidth=2)

    # Remplir la zone d'acceptabilité en vert quasi opaque
    plt.fill_between(x_values, lower_bound, upper_bound, color='green', alpha=0.5)

    # Tracer les points d'alignement en dehors de la zone d'acceptabilité en rouge
    for i in range(len(data_em)):
        for j in range(len(data_lu)):
            if alignment_matrix[i, j] == 1:
                if not (i - marge <= j <= i + marge):
                    plt.scatter(j, i, color='red', s=6)

    plt.xlabel('Indices de data_lu')
    plt.ylabel('Indices de data_em')
    plt.title('Matrice de chemin d\'alignement')
    plt.show()

def find_intersection_points(alignment_matrix):
    indices_intersection = []
    for i in range(alignment_matrix.shape[0]):
        for j in range(alignment_matrix.shape[1]):
            if alignment_matrix[i, j] == 1 and i == j:
                indices_intersection.append((i, j))
    return indices_intersection

def read_second_column(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()
    index_endheader = lines.index('endheader\n')
    second_column = [float(line.split()[1]) for line in lines[index_endheader+2:] if len(line.split()) >= 2]
    return second_column

def find_intersection_times(indices_intersection, data_em, data_lu):
    temps_intersection = [(data_em[i], data_lu[j]) for i, j in indices_intersection]
    return temps_intersection

def find_overlaps(indices_intersection):
    overlaps = []
    for i, (indice_data_em, indice_data_lu) in enumerate(indices_intersection):
        # Logic to identify overlaps...
        # This is a placeholder for overlap logic.
        pass
    return overlaps

def identifier_segments_hors_zone(data_em, alignment_matrix, marge):
    segments = []
    segment_en_cours = []
    etat_precedent = None

    for i in range(alignment_matrix.shape[0]):
        for j in range(alignment_matrix.shape[1]):
            if alignment_matrix[i, j] == 1:
                # Point hors zone
                if not (i - marge <= j <= i + marge):
                    if i < j:
                        etat_actuel = "Trop rapide"
                    else:
                        etat_actuel = "Trop lent"
                    
                    if etat_actuel != etat_precedent and segment_en_cours:
                        # Fin du segment précédent
                        segments.append((etat_precedent, segment_en_cours))
                        segment_en_cours = []

                    segment_en_cours.append(data_em[i, 1])
                    etat_precedent = etat_actuel
                elif segment_en_cours:
                    # Fin du segment en cours
                    segments.append((etat_precedent, segment_en_cours))
                    segment_en_cours = []
                    etat_precedent = None

    # Ajouter le dernier segment s'il existe
    if segment_en_cours:
        segments.append((etat_precedent, segment_en_cours))

    return segments


def plot_movement_analysis(data_em, segments):
    plt.figure(figsize=(8, 6))
    plt.plot(data_em[:, 1], data_em[:, 2], label='Mouvement de l’utilisateur', linestyle='-')

    for etat, segment in segments:
        temps_debut = segment[0]
        temps_fin = segment[-1]
        plt.axvspan(temps_debut, temps_fin, color='lightpink', alpha=0.5)
        plt.text((temps_debut + temps_fin) / 2, np.mean(plt.ylim()), etat, color='red', ha='center', fontsize=9)

    plt.xlabel('Temps (s)')
    plt.ylabel('Angle du genou (l)')
    plt.title('Analyse de la vitesse du mouvement de l’utilisateur après DTW')
    plt.legend()
    plt.show()




def main():
    # Chargement des données
    data_em = load_data("test_lent.sto")
    data_lu = load_data("test_rapide.sto")
    
    # Calcul du DTW et obtention du chemin d'alignement
    distance, path = calculate_dtw(data_em, data_lu)
    
    # Appel de plot_trajectories pour afficher les trajectoires initiales
    plot_trajectories(data_em, data_lu, path)
    
    # Utilisation de plot_dtw_results modifié pour obtenir les données des courbes
    curve_data = plot_dtw_results(data_em, data_lu, path)
    print("Données des courbes renvoyées par plot_dtw_results :")
    for key, value in curve_data.items():
        print(f"{key} a {len(value)} points.")
    
    # Création et affichage de la matrice d'alignement
    alignment_matrix = create_alignment_matrix(path, len(data_em), len(data_lu))
    
    # Création et affichage de la matrice d'alignement avec zone d'acceptabilité
    plot_alignment_matrix_with_acceptance_zone(data_em, data_lu, alignment_matrix)
    
    # Analyse et affichage des intersections et des chevauchements (si implémenté)
    # analyze_and_display_intersections_and_overlaps(path)
    
    # Assuming `alignment_matrix` and other necessary data are already defined.
    indices_intersection = find_intersection_points(alignment_matrix)
    print("Indices des points d'intersection :", indices_intersection)

    temps_data_em = read_second_column("test_lent.sto")
    temps_data_lu = read_second_column("test_rapide.sto")
    temps_intersection = find_intersection_times(indices_intersection, temps_data_em, temps_data_lu)
    print("Temps correspondants aux indices des points d'intersection :", temps_intersection)
   
    # Chargement des données, calcul du DTW, etc...
    alignment_matrix = create_alignment_matrix(path, len(data_em), len(data_lu))
    marge_acceptabilite = int(max(len(data_em), len(data_lu)) * 0.05)
    segments = identifier_segments_hors_zone(data_em, alignment_matrix, marge_acceptabilite)
    plot_movement_analysis(data_em, segments)

if __name__ == "__main__":
    main()
