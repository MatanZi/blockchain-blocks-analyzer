from blockchain_blocks_analyzer.Config import Config
from blockchain_blocks_analyzer.neo4j_handler import connect_db
config = Config()


def test_generate_graph():
    from blockchain_blocks_analyzer.neo4j_handler import generate_graph
    db = connect_db(credential=config.neo4j_credentials)
    generate_graph(graph=db, json_file="../out/12t9YDPgwueZ9NyMgw519p7AA8isjr6SMw.json")


def test_connect_db():
    from py2neo import Graph
    db = connect_db(credential=config.neo4j_credentials)
    assert isinstance(db, Graph)
    assert db.database
