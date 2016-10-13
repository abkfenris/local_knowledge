""" Celery tasks """
from celery import Celery
from osmapi import ApiError


from local_knowledge.settings import Config
from local_knowledge.helpers import osm

celery = Celery(__name__, broker=Config.CELERY_BROKER_URL)


def update_nodes_and_ways(min_lat, max_lon, max_lat, min_lon):
    """ Update local nodes and ways from osm for bounding_box"""
    print('Trying to update nodes and ways for {} {} {} {}'.format(min_lat, max_lon, max_lat, min_lon))
    try:
        map_data = osm.retrieve_map_data(min_lat, max_lon, max_lat, min_lon)
    except ApiError:
        # OSM throws a 400 error when 
        mid_lat = (min_lat + max_lat) / 2
        mid_lon = (min_lon + max_lon) / 2

        for lons in ((min_lon, mid_lon), (mid_lon, max_lon)):
            lower_lon, upper_lon = lons
            for lats in ((min_lat, mid_lat), (mid_lat, max_lat)):
                lower_lat, upper_lat = lats
                
                update_nodes_and_ways(lower_lat, upper_lon, upper_lat, lower_lon)
    else:
        nodes, ways = osm.map_data_to_nodes_ways(map_data)

        osm.update_db_nodes(nodes)
        osm.update_db_ways(ways)
