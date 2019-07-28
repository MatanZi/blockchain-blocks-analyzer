from blockchain_track import generate_record, get_single_address
from neo4j_handler import generate_graph, exist_in_graph, connect_db

from Config import print_json_to_file
import queue

from_address_queue = queue.Queue()


def nodes_builder(from_address, credential):
    graph = connect_db(credential=credential)
    json_file = get_single_address(from_address)
    node_info = generate_record(json_file)
    suspicious = node_info['suspicious']
    final_balance = node_info['final_balance']
    print_json_to_file(filename=json_file['address'], content=node_info)
    while not (exist_in_graph(from_address, graph)) or final_balance == 0:
        for val in suspicious:
            from_address_queue.put(val)

    nodes_builder(from_address=from_address_queue.get(), credential=credential)