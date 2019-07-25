from Config import Config
from requests import get


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


def generate_default_node_fields(address):
    """generate a default template.

    :param address: an bitcoin wallet address.
    :type address: str
    :return: a default template.
    :rtype: dict
    """
    return {
        address: {
            "address": address,
            "n_tx": None,
            "total_received": None,
            "total_sent": None,
            "final_balance": None
        }}


def extract_main_address_fields(json_file):
    """extract a proper fields from json file of the main address.

    :param json_file: an address info. (transaction, and wallet info)
    :type json_file: dict
    :return: a required fields, address info.
    :rtype: dict
    """
    return {
        json_file['address']: {
            "address": json_file['address'],
            "n_tx": json_file['n_tx'],
            "total_received": json_file['total_received'],
            "total_sent": json_file['total_sent'],
            "final_balance": json_file['final_balance']
        }}


def generate_transaction(txs):
    """generate transaction record file.

    :param txs: a transaction info, of a wallet.
    :type txs: dict
    :return: a required fields, address transaction info.
    :rtype: dict
    """
    return {
        'addr': txs['addr'],
        'value': txs['value']
    }


def is_exist_update(txs, tx):
    """check is address exist in our list, if does update value.

    :param txs: our transaction records.
    :rtype txs: set
    :param tx: a transaction record.
    :rtype tx: dict
    :return:
    """
    for tr in txs:
        if tr['addr'] == tx['addr']:
            tr['value'] += tx['value']
            return True
    return False


def initial_transaction():
    """initial transaction format.

    :return: a transaction format.
    :rtype: dict
    """
    return{
            'from': [],
            'to': []
        }


def generate_record(json_file):
    """generate record of address info.

    :param json_file: an address info. (transaction, and wallet info)
    :type json_file: dict
    :return: a final report of transaction.
    :type: dict
    """
    # a default template.
    template = {
        'suspicious': [],
        'node': extract_main_address_fields(json_file=json_file),
        'txs': []
    }

    for tx in json_file['txs']:
        transactions = initial_transaction()
        for trans in tx['inputs']:
            trans = trans['prev_out']
            trans_format = generate_transaction(trans)
            if trans['addr'] != json_file['address']:
                template['node'].update(generate_default_node_fields(address=trans['addr']))
            if not is_exist_update(txs=transactions['from'], tx=trans_format):
                transactions['from'].append(trans_format)

        for trans in tx['out']:
            trans_format = generate_transaction(trans)
            if trans['addr'] != json_file['address']:
                template['node'].update(generate_default_node_fields(address=trans['addr']))
            if not is_exist_update(txs=transactions['to'], tx=trans_format):
                transactions['to'].append(trans_format)
            if trans_format['addr'] not in template and trans['addr'] != json_file['address']:
                template['suspicious'].append(trans_format['addr'])

        template['txs'].append(transactions.copy())
    return template
