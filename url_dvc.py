import pandas as pd
import dvc.api
import subprocess

# Définir le chemin d'accès et le dépôt
path = 'data/wine_original.csv'
repo = '.'

# Fonction pour obtenir les branches ou tags Git, en filtrant les éléments non pertinents
def get_git_versions():
    try:
        # Obtenir les tags Git
        result = subprocess.run(['git', 'tag'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        versions = result.stdout.splitlines()

        if not versions:
            # Si pas de tags, obtenir les branches distantes
            result = subprocess.run(['git', 'branch', '-r'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            versions = result.stdout.splitlines()
            versions = [version.strip().replace('origin/', '') for version in versions]

        # Filtrer les versions inutiles (par exemple 'status')
        versions = [v for v in versions if 'status' not in v.lower()]

        return versions
    except Exception as e:
        print(f"Erreur lors de l'obtention des versions Git : {e}")
        return []

# Obtenir toutes les versions disponibles via Git
versions = get_git_versions()

# Vérifier s'il y a des versions disponibles
if not versions:
    print("Aucune version disponible.")
else:
    # Afficher toutes les versions disponibles
    print("Versions disponibles :")
    for i, version in enumerate(versions):
        print(f"{i + 1}. {version}")

    # Demander à l'utilisateur de choisir une version
    while True:
        try:
            version_choice = int(input(f"Choisissez la version (1 à {len(versions)}): "))
            if version_choice < 1 or version_choice > len(versions):
                print("Choix invalide, veuillez entrer un nombre valide.")
            else:
                version = versions[version_choice - 1]
                break
        except ValueError:
            print("Veuillez entrer un numéro valide.")

    # Obtenir l'URL de la version choisie
    data_url = dvc.api.get_url(path=path, repo=repo, rev=version)

    # Charger les données
    data = pd.read_csv(data_url, sep=";")

    # Afficher les données
    print(data)
