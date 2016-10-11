from celery import Celery
import osmapi

from local_knowledge.settings import Config

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)

api = osmapi.OsmApi()

min_lat, max_lon, max_lat, min_lon = Config.BOUNDING_BOX


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

    # for each way make a linestring
    for way_id in ways:
        way = ways[way_id]
        linestring = []
        for node_id in way['nd']:
            node = nodes[node_id]
            linestring.append((node['lat'], node['lon']))

        ways[way_id]['linestring'] = linestring

    return nodes, ways
