import json
import os

DATA_FILE = "data.json"

def charger_donnees():
    """Initialisation avec structure complète pour éviter toute erreur de clé."""
    structure_initiale = {
        "commandes": [],
        "assistances": [],
        "abonnes": [],
        "livres": [],
        "journal_activites": []
    }
    if not os.path.exists(DATA_FILE):
        return structure_initiale
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            contenu = f.read()
            if not contenu: return structure_initiale
            data = json.loads(contenu)
            # Vérification de sécurité pour chaque section
            for cle in structure_initiale:
                if cle not in data: data[cle] = []
            return data
    except Exception as e:
        print(f"Erreur base de données : {e}")
        return structure_initiale

def sauvegarder_donnees(donnees):
    """Sauvegarde avec formatage propre pour lecture humaine dans le JSON."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(donnees, f, indent=4, ensure_ascii=False)
        return True
    except:
        return False

# Chargement global pour les routes
db = charger_donnees()
commandes = db["commandes"]
assistances = db["assistances"]
abonnes = db["abonnes"]
livres = db["livres"]