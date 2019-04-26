import requests
from .Config import Config
import pandas


def to_millis(dt):
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
