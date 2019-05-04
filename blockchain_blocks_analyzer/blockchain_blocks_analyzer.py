import requests
from Config import Config


def to_millis(dt):
    """date to milliseconds. (2018/5/17 -> 1526515200000)

    :param dt: datetime, a date.
    :return: a date as milliseconds.
    :rtype: int
    """
    import pandas
    return int(pandas.to_datetime(dt).value / 1000000)


def get_blocks_by_date(time_mils):
    """Get a blockchain blocks by date.

    :param time_mils: string, date in milliseconds.
    :return:
    """
    config = Config()
    payload = {'format': 'json'}
    r = requests.get(config.blockchain_url + config.blocks.format(time_in_milliseconds=time_mils), params=payload)
    return r.json()


def get_single_block(block_hash):
    """Get a single block full info (include transactions).

    :param block_hash: string (hex), a hexadecimal block hash.
    :return: a single blockchain block full info.
    :rtype: json.
    """
    config = Config()
    payload = {'format': 'json'}
    r = requests.get(config.blockchain_url + config.single_block.format(block_hash=block_hash), params=payload)
    return r.json()


def get_payer(out_list):
    """get payer name.

    :param out_list: list of dict, a list of out information from block transaction.
    :return: a name of the payer.
    :rtype: str.
    """
    for o in out_list:
        if 'addr' in o:
            return o['addr']


def get_spent(out_list):
    """get spent boolean value.

   :param out_list: list of dict, a list of out information from block transaction.
   :return: a spent status.
   :rtype: boolean.
   """
    for o in out_list:
        if 'spent' in o:
            return o['spent']


def get_value(out_list):
    """get value of transaction.

   :param out_list: list of dict, a list of out information from block transaction.
   :return: amount of Bitcoin.
   :rtype: long.
   """
    for o in out_list:
        if 'value' in o:
            return o['value']


def generate_fields(block_hash, prev_block, next_block, trans):
    """generate required fields from blocks transaction.

    :param trans: all transaction from block.
    :param next_block: a next block hash.
    :param prev_block: a previous block hash.
    :param block_hash: a block hash.
    :return: a json of required fields.
    :rtype: dictionary.
    """
    return {
        "block_hash":block_hash,
        "prev_block": prev_block,
        "next_block": next_block,
        "payer": get_payer(trans["out"]),
        "payee": trans["hash"],
        "time": trans["time"],
        "fee": trans["fee"],
        "relayed_by": trans["relayed_by"],
        "tx_index": trans["tx_index"],
        "block_index": trans["block_index"],
        "spent": get_spent(trans["out"]),
        "value": get_value(trans["out"])
    }


def generate_docs(block):
    """generate docs with required fields from bitcoin blocks.


    :return:a docs of information about all transaction.
    :rtype: list of dictionary.
    """
    return [generate_fields(block_hash=block["hash"],
                            prev_block=block["prev_block"],
                            next_block=block["next_block"],
                            trans=blk_tx) for blk_tx in block["tx"]]
