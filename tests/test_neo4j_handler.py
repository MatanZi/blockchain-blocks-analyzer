from blockchain_blocks_analyzer.Config import Config
config = Config()


def test_generate_graph():
    from blockchain_blocks_analyzer.neo4j_handler import generate_graph
    generate_graph(credential=config.neo4j_credentials, json_file_path="../out/sample_out.json")


def test_connect_db():
    from blockchain_blocks_analyzer.neo4j_handler import connect_db
    from py2neo import Graph
    assert isinstance(connect_db(credential=config.neo4j_credentials), Graph)

