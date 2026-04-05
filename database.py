import json
import os

# Configuration du fichier de stockage
DATA_FILE = "data.json"

def charger_donnees():
    """
    Charge les données depuis le fichier JSON.
    Si le fichier n'existe pas ou est corrompu, crée une structure vide.
    """
    # Structure complète pour ne perdre aucun onglet
    structure_initiale = {
        "commandes": [],    # Pour l'onglet Livraison
        "assistances": [],  # Pour l'onglet Maintenance
        "abonnes": [],      # Pour l'onglet CDI (Membres)
        "livres": []        # Pour l'onglet CDI (Stock)
    }

    if not os.path.exists(DATA_FILE):
        print("INFO: Fichier de données inexistant. Création d'une nouvelle base.")
        return structure_initiale

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            contenu = f.read()
            if not contenu:
                return structure_initiale
            
            data = json.loads(contenu)
            
            # Vérification de la présence de chaque clé pour éviter les bugs
            for cle in structure_initiale.keys():
                if cle not in data:
                    data[cle] = []
                    print(f"ALERTE: Clé manquante '{cle}' ajoutée à la base.")
            
            return data
            
    except json.JSONDecodeError:
        print("ERREUR: Le fichier data.json est corrompu. Réinitialisation...")
        return structure_initiale
    except Exception as e:
        print(f"ERREUR INCONNUE: {str(e)}")
        return structure_initiale

def sauvegarder_donnees(donnees_a_sauver):
    """
    Enregistre l'intégralité des données dans le fichier JSON avec indentation.
    """
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(donnees_a_sauver, f, indent=4, ensure_ascii=False)
            return True
    except Exception as e:
        print(f"ERREUR SAUVEGARDE: {str(e)}")
        return False

# --- INITIALISATION DES VARIABLES GLOBALES ---
# Ces variables permettent de manipuler les données dans routes.py
base_complete = charger_donnees()

commandes = base_complete["commandes"]
assistances = base_complete["assistances"]
abonnes = base_complete["abonnes"]
livres = base_complete["livres"]

print("--- BASE DE DONNÉES KANKA SERVICES PRÊTE ---")