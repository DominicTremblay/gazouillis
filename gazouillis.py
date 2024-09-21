import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy import select
from app import app, db
from app.modeles import Utilisateur, Publication

# crée un contexte de shell qui ajoute l'instance de la base de données et les modèles à la session du shell
@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'Utilisateur': Utilisateur, 'Publication': Publication, 'select': select}