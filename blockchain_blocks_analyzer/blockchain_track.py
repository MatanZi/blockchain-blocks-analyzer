from Config import Config
from requests import get
from py2neo import Graph, GraphError


def get_single_address(address):
    """Get a single address info.

    :param address: a hash address.
    :type: str
    :return: json
    """
    from time import sleep
    # As the API use require, 10 seconds between the requests.
    sleep(10)
    config = Config()
    payload = {'format': 'json', 'offset': 0}
    return fetch_info(query=config.blockchain_url + config.single_addr.format(bitcoin_address=address), params=payload)


def fetch_info(query, params):
    """fetch all the data about the address.

    :param query: a url.
    :type query: str
    :param params: an additional parameters.
    :type params: dict
    :return: a data about an address.
    :rtype: dict
    """
    info = _get_info(query=query, params=params)
    n_tx = info["n_tx"] - 50
    while n_tx:
        params['offset'] += 50
        more_info = _get_info(query=query, params=params)
        info["txs"].extend(more_info["txs"])
        n_tx -= 50
    return info


def _get_info(query, params):
    """get information about an address.

    :param query:
    :param params:
    :return:
    """
    r = get(query, params=params)
    return r.json()
