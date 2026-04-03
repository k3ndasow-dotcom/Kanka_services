class Commande:
    def __init__(self, client, adresse, produit):
        self.client = client
        self.adresse = adresse
        self.produit = produit

class Assistance:
    def __init__(self, client, probleme):
        self.client = client
        self.probleme = probleme