""" Celery tasks """
from celery import Celery


from local_knowledge.settings import Config
from local_knowledge.helpers import osm

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def update_nodes_and_ways(min_lat, max_lon, max_lat, min_lon):
    """ Update local nodes and ways from osm for bounding_box"""
    map_data = osm.retrieve_map_data(min_lat, max_lon, max_lat, min_lon)
    nodes, ways = osm.map_data_to_nodes_ways(map_data)

    osm.update_db_nodes(nodes)
    osm.update_db_ways(ways)
