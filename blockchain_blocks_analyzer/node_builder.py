from blockchain_track import generate_record, get_single_address
from neo4j_handler import exist_in_graph, connect_db
from Config import print_json_to_file
import queue


def create_node(from_address, graph):
    json_file = get_single_address(from_address)
    node_info = generate_record(json_file)
    suspicious = node_info['suspicious']
    final_balance = json_file['final_balance']
    print_json_to_file(filename=json_file['address'], content=node_info)
    if final_balance == 0:
        result = [address for address in suspicious if not (exist_in_graph(address, graph))]
        return result


def nodes_builder(from_address, credential):
    try:
        from_address_queue = queue.Queue()
        graph = connect_db(credential=credential)
        json_file = get_single_address(from_address)
        node_info = generate_record(json_file)
        suspicious = node_info['suspicious']
        for address in suspicious:
            from_address_queue.put(address)
        while not from_address_queue.empty():
            try:
                suspicious = create_node(from_address_queue.get(), graph)
                for address in suspicious:
                    from_address_queue.put(address)
            except Exception as e:
                print(e)
                continue
    except Exception as e:
        print(e)
