import pytest
import vcr

from local_knowledge import tasks
from local_knowledge.models import Node, Way

create_user = False

BOUNDING_BOX = [44.5, -70.7, 45.1, -71.2]


@pytest.mark.usefixtures('testapp')
class TestTasks:

    @vcr.use_cassette()
    def test_update_nodes_and_ways(self, testapp):
        """ Test the update_nodes_and_ways task 
        with a large enough bounding box to cause it to recurse """
        tasks.update_nodes_and_ways(*BOUNDING_BOX)

        nodes = Node.query.all()

        assert len(nodes) > 0
        
        ways = Way.query.all()

        assert len(ways) > 0