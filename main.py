#Ce programme permet de ranger les fichiers selon leur extension (dans leur nom (et non les extensions Windows))

# Importer les librairies
import os  # Importe le module os pour effectuer des opérations sur le système d'exploitation
import argparse  # Importe le module argparse pour analyser les arguments de ligne de commande

# Partie 1 : récupérer le nom du répertoire à nettoyer
parser = argparse.ArgumentParser(  # Crée un analyseur d'arguments
    description="Nettoyer le répertoire et mettre les fichiers dans les dossiers correspondants."  # Description de l'utilité du script
)

parser.add_argument(  # Ajoute un argument à l'analyseur d'arguments
    "--path",  # Spécifie le nom de l'argument
    type=str,  # Spécifie le type de l'argument (une chaîne de caractères)
    default=".",  # Spécifie la valeur par défaut si l'argument n'est pas fourni
    help="Chemin du répertoire à nettoyer"  # Description de l'argument
)

# Analyse les arguments fournis par l'utilisateur et extrait le chemin
args = parser.parse_args()  # Analyse les arguments de ligne de commande fournis par l'utilisateur
path = args.path  # Récupère le chemin du répertoire à nettoyer

print(f"Nettoyage du répertoire {path}")  # Affiche un message pour indiquer le début du nettoyage du répertoire

# Partie 2 : compter le nombre de fichiers
# Obtient tous les fichiers du répertoire spécifié
dir_content = os.listdir(path)  # Récupère la liste de tous les fichiers et dossiers dans le répertoire spécifié

# Crée un chemin relatif du répertoire au fichier et au nom du document
path_dir_content = [os.path.join(path, doc) for doc in dir_content]  # Crée le chemin complet de chaque fichier ou dossier

# Filtre le contenu du répertoire en une liste de documents et de dossiers
docs = [doc for doc in path_dir_content if os.path.isfile(doc)]  # Filtre les fichiers de la liste
folders = [folder for folder in path_dir_content if os.path.isdir(folder)]  # Filtre les dossiers de la liste

# Compteur pour suivre le nombre de fichiers déplacés
# et liste des dossiers déjà créés pour éviter les créations multiples
moved = 0  # Initialise un compteur pour suivre le nombre de fichiers déplacés
created_folders = {}  # Initialise un dictionnaire pour suivre les dossiers déjà créés afin d'éviter les créations multiples

print(f"Nettoyage de {len(docs)} éléments sur {len(dir_content)}.")  # Affiche le nombre total de fichiers à nettoyer

# Partie 3 : Préciser le type de fichier + nom
for doc in docs:  # Boucle à travers chaque fichier dans la liste de fichiers
    # Sépare le nom de l'extension du fichier
    full_doc_path, doc_extension = os.path.splitext(doc)
    doc_path = os.path.dirname(full_doc_path)  # Récupère le chemin du dossier contenant le fichier
    doc_name = os.path.basename(full_doc_path)  # Récupère le nom du fichier

    # Affiche les informations sur le fichier
    print("Extension du fichier :", doc_extension)  # Affiche l'extension du fichier
    print("Chemin complet du document :", full_doc_path)  # Affiche le chemin complet du fichier
    print("Chemin du document :", doc_path)  # Affiche le chemin du dossier contenant le fichier
    print("Nom du document :", doc_name)  # Affiche le nom du fichier

    # Génération du dossier correspondant au type de fichier
    subfolder_path = os.path.join(path, doc_extension[1:].lower())

    # Vérification et création du dossier si nécessaire
    if subfolder_path not in folders and subfolder_path not in created_folders:
        try:
            os.mkdir(subfolder_path)
            created_folders[subfolder_path] = True
            print(f"Dossier {subfolder_path} créé.")
        except FileExistsError as err:
            print(f"Le dossier existe déjà à {subfolder_path}... {err}")

    # Déplacement du fichier dans le dossier correspondant
    new_doc_path = os.path.join(subfolder_path, os.path.basename(doc))
    os.rename(doc, new_doc_path)
    moved += 1
    
    print(f"Fichier {doc} déplacé vers {new_doc_path}")  # Affiche un message indiquant le déplacement du fichier

# Affichage du nombre total de fichiers déplacés
print(f"Total de fichiers déplacés : {moved}")
