from app.api import bp
from app.modeles import Utilisateur
from flask import jsonify
from flask import request

@bp.route('/jeton2', methods=['GET'])
def jeton2():
  return "jeton2"