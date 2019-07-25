from blockchain_blocks_analyzer.Config import Config
config = Config()


def test_generate_graph():
    from blockchain_blocks_analyzer.neo4j_handler import generate_graph


def test_connect_db():
    from blockchain_blocks_analyzer.neo4j_handler import connect_db
    from py2neo import Graph
    assert isinstance(connect_db(credential=config.neo4j_credentials), Graph)