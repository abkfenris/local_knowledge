""" Tests for version 0.1 of the api """
import geojson
import pytest

from local_knowledge.helpers import osm
from .fixtures.helper_osm import map_data as mock_map_data

create_user = False


@pytest.mark.usefixtures('testapp')
class TestApi01:
    def test_nodes(self, testapp):
        """ Tests that after OSM data is imported a GeoJSON can be returned """
        nodes, ways = osm.map_data_to_nodes_ways(mock_map_data)
        osm.update_db_nodes(nodes)

        rv = testapp.get('/api/0.1/nodes')
        rv_str = rv.data.decode('utf-8')

        assert rv.status_code == 200
        assert 'FeatureCollection' in rv_str
        assert 'Feature' in rv_str
        assert 'Point' in rv_str

        node_geo = geojson.loads(rv_str)

        assert node_geo['type'] == 'FeatureCollection'
        assert node_geo['features'][0]['type'] == 'Feature'
        assert node_geo['features'][0]['geometry']['type'] == 'Point'
        assert 'id' in node_geo['features'][0]['properties']['osm_data']
        assert 'yes' == geojson.is_valid(node_geo)['valid']
        

    def test_ways(self, testapp):
        """ Tests that after OSM data is imported, valid GeoJSON can be returned """
        nodes, ways = osm.map_data_to_nodes_ways(mock_map_data)
        osm.update_db_ways(ways)

        rv = testapp.get('/api/0.1/ways')
        rv_str = rv.data.decode('utf-8')

        assert rv.status_code == 200
        assert 'FeatureCollection' in rv_str
        assert 'Feature' in rv_str
        assert 'LineString' in rv_str

        way_geo = geojson.loads(rv_str)

        assert way_geo['type'] == 'FeatureCollection'
        assert way_geo['features'][0]['type'] == 'Feature'
        assert way_geo['features'][0]['geometry']['type'] == 'LineString'
        assert 'id' in way_geo['features'][0]['properties']['osm_data']
        assert 'yes' == geojson.is_valid(way_geo)['valid']