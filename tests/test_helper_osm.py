""" Test OpenStreetMap helper functions """
import pytest

from local_knowledge.helpers import osm
from local_knowledge.models import Node, Way
from .fixtures.helper_osm import map_data as mock_map_data

bounding_box = [44.5963, -70.8620, 44.6111, -70.9626]

SRID_VALUE = '4326'


@pytest.mark.usefixtures("testapp")
class TestOsmHelper:
    def test_retrieve_map_data(self, testapp):
        """ Test if a list of nodes, ways, and relations can be
        retrieved from OpenStreetMap """
        map_data = osm.retrieve_map_data(*bounding_box)

        assert isinstance(map_data, list), 'retrieve_map_data did not return a list'
        
        kinds = {item['type'] for item in map_data}

        assert 'node' in kinds, 'node not found in output of retrieve_map_data'
        assert 'relation' in kinds, 'relation not found in output of retrieve_map_data'
        assert 'way' in kinds, 'way not found in output of retrieve_map_data'

    def test_map_data_to_nodes_ways(self, testapp):
        """ Test if dictionaries of nodes and ways are returned
        from map_data_to_nodes_ways """
        nodes, ways = osm.map_data_to_nodes_ways(mock_map_data)
        
        assert isinstance(nodes, dict)
        assert isinstance(ways, dict)
    
    def test_node_wkt(self):
        """ Tests if WKT can be formed from a node """
        nodes, ways = osm.map_data_to_nodes_ways(mock_map_data)

        node = nodes[list(nodes.keys())[0]]

        wkt = osm.node_to_wkt(node)

        assert 'SRID' in wkt
        assert SRID_VALUE in wkt
        assert 'POINT' in wkt
    
    def test_way_wkt(self, testapp):
        """ Tests if WKT can be formed from a way """
        nodes, ways = osm.map_data_to_nodes_ways(mock_map_data)

        way = ways[list(ways.keys())[0]]

        wkt = osm.way_to_wkt(way)

        assert 'SRID' in wkt
        assert SRID_VALUE in wkt
        assert 'LINESTRING' in wkt
    
    def test_update_nodes(self, testapp):
        """ Tests if nodes can be stored in the database """
        nodes, ways = osm.map_data_to_nodes_ways(mock_map_data)

        osm.update_db_nodes(nodes)

        for node_id in nodes:
            assert node_id == Node.query.filter_by(osm_id=node_id).first().osm_id
    

    def test_update_ways(self, testapp):
        """ Test if ways can be stored in the database """
        nodes, ways = osm.map_data_to_nodes_ways(mock_map_data)

        osm.update_db_ways(ways)

        for way_id in ways:
            assert way_id == Way.query.filter_by(osm_id=way_id).first().osm_id
