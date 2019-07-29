from blockchain_track import generate_record, get_single_address
from neo4j_handler import exist_in_graph, connect_db
from Config import Config, print_json_to_file
import queue


def create_node(from_address, graph):
    result = []
    json_file = get_single_address(from_address)
    node_info = generate_record(json_file)
    suspicious = node_info['suspicious']
    final_balance = json_file['final_balance']
    print_json_to_file(filename=json_file['address'], content=node_info)
    #print(final_balance)
    if final_balance == 0:
        for address in suspicious:
            if not (exist_in_graph(address, graph)):
                result.append(address)

    #print(result)
    return result


def nodes_builder(from_address, credential):
    graph = connect_db(credential=credential)
    from_address_queue = queue.Queue()
    suspicious = create_node(from_address, graph)
    #print(type(suspicious))
    from_address_queue.put(suspicious)
    #print(suspicious)
    while not from_address_queue.empty():
        suspicious = create_node(from_address_queue.get(), graph)
        for address in suspicious:
            from_address_queue.put(address)


#conf = Config()
#nodes_builder("1HctxwLwjEFCacTPi83me927UBs7aTJ7LF", conf.neo4j_credentials)
