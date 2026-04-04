from flask import render_template, request, jsonify
from datetime import datetime, timedelta
from database import commandes, assistances, abonnes, livres, sauvegarder_donnees

def register_routes(app):

    @app.route("/")
    def accueil():
        return render_template("index.html")

    # --- 1. ONGLET LIVRAISON (Logique de paiement incluse) ---
    @app.route("/commande", methods=["POST"])
    def ajouter_commande():
        data = request.json
        frais_fixe = 5000 # Prestation Kanka Services
        transport = int(data.get("transport", 0))
        
        nouvelle_commande = {
            "id": datetime.now().strftime('%Y%m%d%H%M%S'),
            "nom_client": data.get("client"),
            "lieu_livraison": data.get("lieu"),
            "details_besoin": data.get("besoin"),
            "frais_transport": transport,
            "frais_prestation": frais_fixe,
            "total_a_payer": frais_fixe + transport,
            "date": datetime.now().strftime('%d/%m/%Y à %H:%M')
        }
        commandes.append(nouvelle_commande)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify(nouvelle_commande)

    # --- 2. ONGLET MAINTENANCE & ASSISTANCE ---
    @app.route("/assistance", methods=["POST"])
    def demander_assistance():
        data = request.json
        nouvelle_aide = {
            "id": datetime.now().strftime('%Y%m%d%H%M%S'),
            "nom": data.get("nom"),
            "type_appareil": data.get("appareil", "Non précisé"),
            "description_probleme": data.get("probleme"),
            "date": datetime.now().strftime('%d/%m/%Y')
        }
        assistances.append(nouvelle_aide)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify({"status": "success", "message": "Demande enregistrée"})

    # --- 3. ONGLET CDI (Inscription, Frais 5000, Dates) ---
    @app.route("/inscription_cdi", methods=["POST"])
    def inscription_cdi():
        data = request.json
        maintenant = datetime.now()
        fin_validite = maintenant + timedelta(days=90) # Trimestre
        
        nouvel_abonne = {
            "nom": data.get("nom"),
            "classe": data.get("classe"),
            "quartier": data.get("adresse"),
            "date_inscription": maintenant.strftime('%d/%m/%Y'),
            "date_expiration": fin_validite.strftime('%d/%m/%Y'),
            "frais_trimestre": "5 000 GNF"
        }
        abonnes.append(nouvel_abonne)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify(nouvel_abonne)

    # --- 4. GESTION DU STOCK (Ajout, Recherche, Suppression) ---
    @app.route("/ajouter_livre", methods=["POST"])
    def ajouter_livre_stock():
        data = request.json
        livre = {
            "id": datetime.now().strftime('%H%M%S'), # ID unique basé sur l'heure
            "titre": data.get("titre"),
            "auteur": data.get("auteur", "Inconnu"),
            "quantite": int(data.get("qte", 1))
        }
        livres.append(livre)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify(livre)

    @app.route("/supprimer_livre/<id_livre>", methods=["DELETE"])
    def supprimer_livre(id_livre):
        global livres
        livres[:] = [l for l in livres if str(l.get('id')) != str(id_livre)]
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify({"success": True})

    @app.route("/get_livres")
    def get_livres():
        return jsonify(livres)