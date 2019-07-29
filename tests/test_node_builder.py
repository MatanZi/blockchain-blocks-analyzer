from blockchain_blocks_analyzer.Config import Config
config = Config()


def test_nodes_builder():
    from blockchain_blocks_analyzer.node_builder import nodes_builder
    assert not nodes_builder(from_address='12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw', credential=config.neo4j_credentials)


def test_create_node():
    from blockchain_blocks_analyzer.node_builder import create_node
    from blockchain_blocks_analyzer.neo4j_handler import connect_db
    db = connect_db(credential=config.neo4j_credentials)
    assert not create_node(from_address='12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw', graph=db)
