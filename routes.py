from flask import render_template, request, jsonify
from models import Commande, Assistance
from database import commandes, assistances, sauvegarder_donnees

def register_routes(app):

    # 1. PAGE D'ACCUEIL
    @app.route("/")
    def accueil():
        return render_template("index.html")

    # 2. PAGE FORMULAIRE COMMANDE
    @app.route("/passer-commande")
    def afficher_formulaire_commande():
        return render_template("commande.html")

    # 3. PAGE FORMULAIRE ASSISTANCE
    @app.route("/demander-aide")
    def afficher_formulaire_assistance():
        return render_template("assistance.html")

    # 4. ACTION : ENREGISTRER UNE COMMANDE
    @app.route("/commande", methods=["POST"])
    def ajouter_commande():
        data = request.json
        cmd = Commande(data["client"], data["adresse"], data["produit"])
        
        # On ajoute à la liste locale
        commandes.append(cmd.__dict__)
        
        # ON SAUVEGARDE DANS LE FICHIER data.json
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances})
        
        return jsonify({"message": "Commande enregistrée sur le disque !"})

    # 5. ACTION : ENVOYER UNE DEMANDE D'AIDE
    @app.route("/assistance", methods=["POST"])
    def demander_assistance():
        data = request.json
        assist = Assistance(data["client"], data["probleme"])
        
        # On ajoute à la liste locale
        assistances.append(assist.__dict__)
        
        # ON SAUVEGARDE DANS LE FICHIER data.json
        sauvegarder_donnees({"commandes": commandes, "assistances": assistances})
        
        return jsonify({"message": "Demande d'assistance sauvegardée !"})