""" Helper functions for OpenStreetMap"""
from datetime import datetime

import osmapi

from local_knowledge.models import Node, Way, db


api = osmapi.OsmApi()


def retrieve_map_data(min_lat, max_lon, max_lat, min_lon):
    """ Retrieves raw map data json from OpenStreetMap for bounding box """
    return api.Map(min_lon, min_lat, max_lon, max_lat)


def map_data_to_nodes_ways(map_data):
    """ Returns dicts of nodes and ways for given map data """
    nodes = {}
    ways = {}

    # make initial dictionaries
    for obj in map_data:
        if obj['type'] == 'node':
            nodes[obj['data']['id']] = obj['data']
        elif obj['type'] == 'way':
            ways[obj['data']['id']] = obj['data']

    # clean up nodes
    for node_id in nodes:
        node = nodes[node_id]
        nodes[node_id]['timestamp'] = node['timestamp'].isoformat()

    # for each way make a linestring
    for way_id in ways:
        way = ways[way_id]
        linestring = []
        for node_id in way['nd']:
            node = nodes[node_id]
            linestring.append((node['lon'], node['lat']))

        ways[way_id]['linestring'] = linestring
        ways[way_id]['timestamp'] = way['timestamp'].isoformat()

    return nodes, ways


def node_to_wkt(node):
    """ Returns a Well Known Text representation of given node """
    return "SRID=4326;POINT({x} {y})".format(x=node['lon'], y=node['lat'])


def way_to_wkt(way):
    """ Returns a Well Known Text representation of a given way """
    coords = ['{x} {y}'.format(x=point[0], y=point[1]) for point
              in way['linestring']]
    return 'SRID=4326;LINESTRING({})'.format(', '.join(coords))


def update_db_nodes(nodes):
    """ Updates node information in db """
    for node_id in nodes:
        node = nodes[node_id]

        db_node = Node.query.filter_by(osm_id=node['id']).first()

        # If node does not already exist, lets create it
        if not db_node:
            db_node = Node(osm_id=node['id'],
                           created=datetime.utcnow())
        
        db_node.updated = datetime.utcnow()
        db_node.geom = node_to_wkt(node)
        db_node.json = node
        db.session.add(db_node)
    db.session.commit()


def update_db_ways(ways):
    """ Updates or creates way information in db """
    for way_id in ways:
        way = ways[way_id]

        db_way = Way.query.filter_by(osm_id=way['id']).first()

        # If way does not already exist, lets create it
        if not db_way:
            db_way = Way(osm_id=way['id'],
                         created=datetime.utcnow())

        db_way.updated = datetime.utcnow()
        db_way.geom = way_to_wkt(way)
        db_way.json=way
        if way['tag'].get('name', False):
            db_way.name = way['tag']['name']

        db.session.add(db_way)
    db.session.commit()
