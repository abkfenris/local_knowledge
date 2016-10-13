""" Test OpenStreetMap helper functions """
from local_knowledge.helpers import osm
from .fixtures.helper_osm import map_data as mock_map_data

bounding_box = [44.5963, -70.8620, 44.6111, -70.9626]



class TestOsmHelper:
    def test_retrieve_map_data(self):
        """ Test if a list of nodes, ways, and relations can be
        retrieved from OpenStreetMap """
        map_data = osm.retrieve_map_data(*bounding_box)

        assert isinstance(map_data, list), 'retrieve_map_data did not return a list'
        
        kinds = {item['type'] for item in map_data}

        assert 'node' in kinds, 'node not found in output of retrieve_map_data'
        assert 'relation' in kinds, 'relation not found in output of retrieve_map_data'
        assert 'way' in kinds, 'way not found in output of retrieve_map_data'

    def test_map_data_to_nodes_ways(self):
        """ Test if dictionaries of nodes and ways are returned
        from map_data_to_nodes_ways """
        nodes, ways = osm.map_data_to_nodes_ways(mock_map_data)
        
        assert isinstance(nodes, dict)
        assert isinstance(ways, dict)