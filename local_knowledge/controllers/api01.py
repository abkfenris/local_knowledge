""" Version 0.1 of api returning GeoJSON """
from flask import Blueprint, jsonify
from sqlalchemy import JSON

from local_knowledge.models import db, Way, Node

api = Blueprint('api', __name__)


@api.route('/nodes')
def nodes():
    """ Returns a GeoJSON Feature collection with all nodes """
    results = db.session.query(Node.id, Node.json, Node.geom.ST_AsGeoJSON().cast(JSON).label('geom')).all()
    
    features = {"type": "FeatureCollection",
                "features": [{'type': 'Feature',
                              'geometry': res.geom,
                              'properties': {'id': res.id,
                                             'osm_data': {k:res.json[k] for k in res.json if k != 'nd'}
                }} for res in results]}

    return jsonify(features)


@api.route('/ways')
def ways():
    """ Returns a GeoJSON Feature collection with all ways """
    results = db.session.query(Way.id, Way.name, Way.json, Way.geom.ST_AsGeoJSON().cast(JSON).label('geom')).all()
    fc = {
        'type': 'FeatureCollection',
        'features': [{'type': 'Feature',
                      'geometry': res.geom,
                      'properties' :{'id': res.id,
                                     'name': res.name,
                                      'osm_data': {k: res.json[k] for k in res.json
                                                   if k != 'linestring' and k != 'nd'} 
        }} for res in results]
    }
    return jsonify(fc)