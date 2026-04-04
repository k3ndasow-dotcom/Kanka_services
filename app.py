from flask import Flask
from routes import register_routes
from datetime import timedelta # On ajoute juste cette ligne pour le temps

app = Flask(__name__)

# On dit à Flask que la session (mémoire temporaire) dure 90 jours
app.permanent_session_lifetime = timedelta(days=90)

register_routes(app)

if __name__ == "__main__":
    app.run(debug=True)