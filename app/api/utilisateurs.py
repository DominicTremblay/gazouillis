from app.api import bp
from app.modeles import Utilisateur
from flask import jsonify
from flask import request


@bp.route('/utilisateurs2', methods=['GET'])
def get_utilisateurs():
    return "utilisateurs2"

# Operation CRUD

# Obetnir 1 utilisateur

@bp.route('/utilisateurs/<int:id>')
def get_utilisateur(id):
    return jsonify(Utilisateur.query.get_or_404(id).to_dict())


 # Creer un utilisateur
@bp.route('/utilisateurs', methods=['POST'])
def creer_utilisateur():
    return 'creer utilisateur'
 
 # Modifer un utilisateur
@bp.route('/utilisateurs/<int:id>', methods=['PUT'])
def modifier_utilisateur(id):
    return "modifier utilisateur"

# Supprimer un utilisateur
@bp.route('/utilisateurs/<int:id>', methods=['DELETE'])
def supprimer_utilisateur(id):
    return "Supprimer utilisateur"