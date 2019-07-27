from blockchain_track import generate_record, get_single_address
from neo4j_handler import generate_graph, exist_in_graph, connect_db


def create_node(from_address, graph):
    json_file = get_single_address(from_address)
    node_info = generate_record(json_file)
    node_graph = generate_graph(graph, node_info)
    return node_graph


def nodes_builder(from_address, final_balance, credentials):
    graph = connect_db(credential=credentials)
    while not (exist_in_graph(from_address, graph)) or final_balance == 0:
        create_node(from_address, graph)
