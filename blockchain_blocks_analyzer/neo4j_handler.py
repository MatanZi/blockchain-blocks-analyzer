from py2neo import Graph, GraphError, Node, Relationship


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


def generate_graph(credential, json_file):
    """generate graph database from address info file.

    :param credential: a user name and password and uri.
    :type credential: dict
    :param json_file: an address info file.
    :type json_file: dict
    :return:
    """
    db = connect_db(credential=credential)

