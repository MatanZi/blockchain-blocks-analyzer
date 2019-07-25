from py2neo import Graph, GraphError, Node, Relationship, NodeMatcher
import json


def connect_db(credential):
    """connect to db.

    :param credential: a user name and password and uri.
    :type credential: dict
    :return: a reference to database.
    :rtype: Graph
    """
    try:
        return Graph(credential['uri'], user=credential['user'], password=credential['password'])
    except GraphError as ge:
        print(ge)


def generate_graph(credential, json_file_path):
    """generate graph database from address info file.

    :param credential: a user name and password and uri.
    :type credential: dict
    :param json_file_path: an address info file.
    :type json_file_path: str
    :return:
    """
    db = connect_db(credential=credential)
    j = json.load(open(json_file_path, 'r'))
    for node in generate_nodes(j):
        node_addr = node['address']
        node_from = exist_in_graph(node_addr, db)
        if node_from is None:
            db.create(node)
    for relation in (generate_relations(j, db)):
        db.create(relation)


def generate_nodes(json_file):
    node_list = []
    for addr, val in json_file['node'].items():
        node = Node("Block", **val)
        print(node['address'])
        node_list.append(node)
    return node_list


def generate_relations(json_file, graph):
    relations_list = []
    for val in json_file['txs']:
        for from_val in val['from']:
            address_from = from_val['addr']
            node_from = exist_in_graph(address_from, graph)
            for to_val in val['to']:
                address_to = to_val['addr']
                node_to = exist_in_graph(address_to, graph)
                unified = from_val
                unified.update(to_val)
                relations_list.append(Relationship(node_from, "tx", node_to, **unified))
    return relations_list


def exist_in_graph(node_address, graph):
    matcher = NodeMatcher(graph)
    return matcher.match("Block", address=node_address).first()