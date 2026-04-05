from flask import render_template, request, jsonify
from datetime import datetime, timedelta
import uuid
from database import commandes, assistances, abonnes, livres, sauvegarder_donnees

def register_routes(app):
    @app.route("/")
    def accueil():
        return render_template("index.html")

    # --- 📦 VOLET LIVRAISON (Complet avec détails) ---
    @app.route("/commande", methods=["POST"])
    def ajouter_commande():
        data = request.json
        frais_fixe = 5000
        transport = int(data.get("transport", 0))
        nouvelle = {
            "id_commande": f"CMD-{datetime.now().strftime('%y%m%d')}-{str(uuid.uuid4())[:4].upper()}",
            "client": data.get("client"),
            "lieu": data.get("lieu"),
            "besoin": data.get("besoin"),
            "frais_service": frais_fixe,
            "frais_transport": transport,
            "total_a_payer": frais_fixe + transport,
            "statut": "En attente",
            "date": datetime.now().strftime('%d/%m/%Y à %H:%M')
        }
        commandes.append(nouvelle)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify(nouvelle)

    # --- 💻 VOLET MAINTENANCE (PC & ANDROID) ---
    @app.route("/assistance", methods=["POST"])
    def demander_assistance():
        data = request.json
        nouvelle_panne = {
            "ticket_id": str(uuid.uuid4())[:8].upper(),
            "client_nom": data.get("nom"),
            "telephone": data.get("telephone"),
            "appareil": data.get("type"), # PC ou Android
            "probleme": data.get("probleme"),
            "date_depot": datetime.now().strftime('%d/%m/%Y'),
            "etat": "Diagnostic en cours"
        }
        assistances.append(nouvelle_panne)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify({"success": True, "ticket": nouvelle_panne["ticket_id"]})

    # --- 📚 VOLET CDI (Identité complète) ---
    @app.route("/inscription_cdi", methods=["POST"])
    def inscription_cdi():
        data = request.json
        # Abonnement 90 jours
        expiration = (datetime.now() + timedelta(days=90)).strftime('%d/%m/%Y')
        
        profil = data.get("profil")
        # Distinction Éleve vs Autres
        if profil == "Élève":
            niveau_complet = f"{data.get('classe')} - Option: {data.get('option')}"
        else:
            niveau_complet = f"Lecteur {profil}"

        abonne = {
            "id_lecteur": str(uuid.uuid4())[:6].upper(),
            "nom": data.get("nom").upper(), # Format Majuscule demandé
            "telephone": data.get("telephone"),
            "adresse": data.get("adresse"),
            "profil": profil,
            "niveau": niveau_complet,
            "date_fin": expiration,
            "statut_paiement": "Validé (5000 GNF)"
        }
        abonnes.append(abonne)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify(abonne)

    # --- 📖 GESTION DU STOCK LIVRES ---
    @app.route("/get_livres")
    def get_livres():
        return jsonify(livres)

    @app.route("/ajouter_livre", methods=["POST"])
    def ajouter_livre():
        data = request.json
        nouveau = {"id": str(uuid.uuid4())[:6], "titre": data.get("titre"), "qte": data.get("qte"), "categorie": data.get("cat", "Général")}
        livres.append(nouveau)
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify(nouveau)

    @app.route("/supprimer_livre/<id_l>", methods=["DELETE"])
    def supprimer_livre(id_l):
        global livres
        livres[:] = [l for l in livres if str(l.get('id')) != str(id_l)]
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances, "abonnes": abonnes, "livres": livres})
        return jsonify({"success": True})