from app.api import bp
from app.modeles import Utilisateur
from flask import jsonify
from flask import request


@bp.route('/utilisateurs2', methods=['GET'])
def get_utilisateurs():
    return "utilisateurs2"

# Operation CRUD