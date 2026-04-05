from flask import render_template, request, jsonify
from datetime import datetime, timedelta
import uuid

# Importation des listes et de la fonction de sauvegarde depuis database.py
from database import commandes, assistances, abonnes, livres, sauvegarder_donnees

def register_routes(app):

    @app.route("/")
    def accueil():
        """Affiche la page principale avec tous les onglets."""
        return render_template("index.html")

    # --- 1. ONGLET LIVRAISON (Calcul 5000 GNF + Transport) ---
    @app.route("/commande", methods=["POST"])
    def ajouter_commande():
        data = request.json
        
        # Récupération et calcul des frais selon tes règles
        frais_prestation_fixe = 5000
        frais_transport_manuel = int(data.get("transport", 0))
        montant_total = frais_prestation_fixe + frais_transport_manuel
        
        nouvelle_livraison = {
            "id_commande": str(uuid.uuid4())[:8],
            "client_nom": data.get("client"),
            "lieu_livraison": data.get("lieu"),
            "description_besoin": data.get("besoin"),
            "frais_transport": frais_transport_manuel,
            "frais_prestation": frais_prestation_fixe,
            "total_a_payer": montant_total,
            "date_enregistrement": datetime.now().strftime('%d/%m/%Y à %H:%M'),
            "statut_livraison": "En attente"
        }
        
        commandes.append(nouvelle_livraison)
        # Sauvegarde globale pour ne rien perdre des autres onglets
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        
        print(f"INFO: Nouvelle commande de {nouvelle_livraison['client_nom']} enregistrée.")
        return jsonify(nouvelle_livraison)

    # --- 2. ONGLET MAINTENANCE (PC et ANDROID) ---
    @app.route("/assistance", methods=["POST"])
    def demander_assistance():
        data = request.json
        
        nouvelle_demande = {
            "id_ticket": datetime.now().strftime('%Y%m%d-%H%M'),
            "nom_client": data.get("nom"),
            "type_appareil": data.get("type"), # 'PC' ou 'Android'
            "description_panne": data.get("probleme"),
            "date_depot": datetime.now().strftime('%d/%m/%Y'),
            "etat_reparation": "Reçu"
        }
        
        assistances.append(nouvelle_demande)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        
        return jsonify({"status": "success", "message": "Demande de maintenance bien reçue."})

    # --- 3. ONGLET CDI : INSCRIPTION (Frais 5000 GNF) ---
    @app.route("/inscription_cdi", methods=["POST"])
    def inscription_cdi():
        data = request.json
        
        date_debut = datetime.now()
        # Validité de 3 mois (90 jours) pour l'abonnement
        date_fin = date_debut + timedelta(days=90)
        
        nouvel_abonne = {
            "nom_eleve": data.get("nom"),
            "classe_eleve": data.get("classe"),
            "quartier_eleve": data.get("adresse"),
            "date_adhesion": date_debut.strftime('%d/%m/%Y'),
            "date_expiration": date_fin.strftime('%d/%m/%Y'),
            "frais_inscription": "5 000 GNF",
            "statut_paiement": "Payé"
        }
        
        abonnes.append(nouvel_abonne)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        
        return jsonify(nouvel_abonne)

    # --- 4. ONGLET CDI : GESTION DU STOCK (Livres) ---
    @app.route("/get_livres", methods=["GET"])
    def recuperer_stock_livres():
        """Renvoie la liste complète des livres pour la recherche."""
        return jsonify(livres)

    @app.route("/ajouter_livre", methods=["POST"])
    def ajouter_livre_bibliotheque():
        data = request.json
        
        nouveau_livre = {
            "id_livre": datetime.now().strftime('%S%M%H'), # ID basé sur le temps
            "titre_ouvrage": data.get("titre"),
            "quantite_disponible": int(data.get("qte", 1)),
            "date_ajout": datetime.now().strftime('%d/%m/%Y')
        }
        
        livres.append(nouveau_livre)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        
        return jsonify(nouveau_livre)

    @app.route("/supprimer_livre/<id_livre>", methods=["DELETE"])
    def supprimer_livre_du_stock(id_livre):
        """Supprime définitivement un livre par son ID."""
        global livres
        # Filtrage pour garder tous les livres SAUF celui à supprimer
        livres[:] = [livre for livre in livres if str(livre.get('id_livre')) != str(id_livre)]
        
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify({"resultat": "Livre supprimé avec succès."})