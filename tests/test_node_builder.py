from blockchain_blocks_analyzer.Config import Config
config = Config()


def test_nodes_builder():
    from blockchain_blocks_analyzer.node_builder import nodes_builder
    assert not nodes_builder(from_address='12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw', credentials=config.neo4j_credentials)
