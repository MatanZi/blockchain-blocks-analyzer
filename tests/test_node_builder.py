from blockchain_blocks_analyzer.Config import Config
from blockchain_blocks_analyzer.neo4j_handler import connect_db
config = Config()


def test_create_node():
    from blockchain_blocks_analyzer.node_builder import create_node

    graph = connect_db(credential=config.neo4j_credentials)
    assert not create_node(from_address='12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw', graph=graph)
