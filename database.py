import json
import os

# Nom du fichier où seront stockées les informations
DATA_FILE = "data.json"

def charger_donnees():
    # Si le fichier existe, on le lit. Sinon, on crée des listes vides.
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"commandes": [], "assistances": []}

def sauvegarder_donnees(donnees):
    # On écrit les listes dans le fichier data.json
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(donnees, f, indent=4, ensure_ascii=False)

# Au démarrage, on charge ce qui existe déjà
base_de_donnees = charger_donnees()
commandes = base_de_donnees["commandes"]
assistances = base_de_donnees["assistances"]