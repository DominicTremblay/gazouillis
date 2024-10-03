from app.api import bp
from app.modeles import Publication
from flask import jsonify
from flask import request

@bp.route('/publications2', methods=['GET'])
def publications2():
  return "publications2"

@bp.route('/publications/<int:id>', methods=['GET'])
def get_publication(id):
  return jsonify(Publication.query.get_or_404(id).to_dict())

@bp.route('/publications', methods=['GET'])
def get_publications():
  page = request.args.get('page', 1, type=int)
  par_page = min(request.args.get('par_page', 10, type=int), 100)
  data = Publication.to_collection_dict(Publication.query, page, par_page, 'api.get_publications')

  return jsonify(data)