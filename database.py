import json
import os

# Chemin vers la base de données
DATA_FILE = "data.json"

def charger_donnees():
    # Structure de base par défaut
    structure_vide = {
        "commandes": [],
        "assistances": [],
        "abonnes": [],
        "livres": []
    }
    
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # On s'assure que même si le fichier existe, toutes les clés sont là
                for cle in structure_vide.keys():
                    if cle not in data:
                        data[cle] = []
                return data
        except (json.JSONDecodeError, Exception):
            return structure_vide
    return structure_vide

def sauvegarder_donnees(donnees):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Erreur lors de la sauvegarde : {e}")

# Initialisation des variables globales pour le reste de l'application
base_de_donnees = charger_donnees()
commandes = base_de_donnees["commandes"]
assistances = base_de_donnees["assistances"]
abonnes = base_de_donnees["abonnes"]
livres = base_de_donnees["livres"]