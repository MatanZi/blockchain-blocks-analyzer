from blockchain_track import generate_record,get_single_address
from neo4j_handler import generate_graph, exist_in_graph


def create_node(from_address):
    json_file = get_single_address(from_address)
    node_info = generate_record(json_file)
    from blockchain_blocks_analyzer import Config
    node_graph = generate_graph(Config.neo4j_credentials, node_info)

    return node_graph

def nodes_builder(from_address , final_balance , graph):
    while(not(exist_in_graph(from_address, graph)) or final_balance == 0):
        create_node(from_address)




