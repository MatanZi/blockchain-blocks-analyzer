from Config import Config
from requests import get


class ErrorAddressInfo(Exception):
    pass


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
    :raise ErrorAddressInfo: in case of api didn't received info about an address.
    """
    try:
        info = _get_info(query=query, params=params)
        if not info:
            info = _retry_query(query=query, params=params)
        n_tx = info["n_tx"] - 50
        while n_tx > 0:
            params['offset'] += 50
            more_info = _get_info(query=query, params=params)
            if not more_info:
                more_info = _retry_query(query=query, params=params)
            info["txs"].extend(more_info["txs"])
            n_tx -= 50
        return info
    except KeyError:
        raise ErrorAddressInfo("can't fetch info from the api.")


def _retry_query(query, params):
    """retry get query 3 times.

    :param query: a url.
    :type query: str
    :param params: an additional parameters.
    :type params: dict
    :return: a data about an address.
    :rtype: dict
    """
    for _ in range(3):
        info = _get_info(query=query, params=params)
        if info:
            return info


def _get_info(query, params):
    """get information about an address.

    :param query: a url.
    :type query: str
    :param params: an additional parameters.
    :type params: dict
    :return: a data about an address.
    :rtype: dict
    """
    with get(query, params=params) as r:
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


def is_outcome(out, wallet):
    """check if transaction is a outcome.

    :param out: a outcome report.
    :type out: list
    :param wallet: a wallet address.
    :type wallet: str
    :return: a transaction is an outcome True, otherwise False.
    :rtype: bool
    """
    for o in out:
        if wallet == o['addr']:
            return False
    return True


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
        is_out = is_outcome(out=tx['out'], wallet=json_file['address'])
        transactions = initial_transaction()
        value = 0
        if not is_out:
            for trans in tx['inputs']:
                trans = trans['prev_out']
                trans_format = generate_transaction(trans)
                value += trans_format['value']
                if trans['addr'] != json_file['address']:
                    template['node'].update(generate_default_node_fields(address=trans['addr']))
                if not is_exist_update(txs=transactions['from'], tx=trans_format):
                    transactions['from'].append(trans_format)
            transactions['to'].append(generate_transaction({'addr': json_file['address'], 'value': value}))
        else:
            for trans in tx['out']:
                trans_format = generate_transaction(trans)
                value += trans_format['value']
                if trans['addr'] != json_file['address']:
                    template['node'].update(generate_default_node_fields(address=trans['addr']))
                if not is_exist_update(txs=transactions['to'], tx=trans_format):
                    transactions['to'].append(trans_format)
                if is_out and trans_format['addr'] not in template['suspicious']:
                    template['suspicious'].append(trans_format['addr'])
            transactions['from'].append(generate_transaction({'addr': json_file['address'], 'value': value}))
        template['txs'].append(transactions.copy())
    return template
