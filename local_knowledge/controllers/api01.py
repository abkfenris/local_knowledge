from flask import Blueprint, jsonify
from sqlalchemy import JSON

from local_knowledge.models import db, Way, Node

api = Blueprint('api', __name__)

@api.route('/')
def index():
    return "Hello World"


@api.route('/nodes')
def nodes():
    """ Returns a GeoJSON Feature collection with all nodes """
    results = db.session.query(Node.id, Node.json, Node.geom.ST_AsGeoJSON().cast(JSON).label('geom')).all()
    fc = {"type": "FeatureCollection",
          "features": [dict(res.geom, 
                            properties={'id': res.id, 
                                        'osm_data': {k:res.json[k] for k in res.json if k!='nd'}
                                        }) for res in results]}
    return jsonify(fc)


@api.route('/ways')
def ways():
    """ Returns a GeoJSON Feature collection with all ways """
    results = db.session.query(Way.id, Way.name, Way.json, Way.geom.ST_AsGeoJSON().cast(JSON).label('geom')).all()
    fc = {
        'type': 'FeatureCollection',
        'features': [dict(res.geom, 
                          properties={'id': res.id, 
                                      'name': res.name, 
                                      'osm_data': {k:res.json[k] for k in res.json if k!='linestring' and k!='nd'} 
                                      }) for res in results]
    }
    return jsonify(fc)