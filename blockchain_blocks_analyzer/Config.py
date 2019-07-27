def conf_logger(log_path, file_name, log_format="%(asctime)s  [%(levelname)s]  %(message)s"):
    import logging
    log_formatter = logging.Formatter(log_format)
    root_logger = logging.getLogger(name=file_name)

    # configure file handler
    file_handler = logging.FileHandler("{0}/{1}.log".format(log_path, file_name))
    file_handler.setFormatter(log_formatter)
    file_handler.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)

    # configure console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_formatter)
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    root_logger.setLevel(logging.DEBUG)


def print_json_to_file(filename, content):
    """

    :param filename:
    :param content:
    :return:
    """
    import json
    from os import path
    # If the file name exists, write a JSON string into the file.
    root_folder = path.dirname(path.dirname(__file__))
    if filename:
        # Writing JSON data
        with open(path.join(root_folder, 'out', '{}.json'.format(filename)), 'w') as f:
            json.dump(content, f, indent=4)


class Config:
    def __init__(self):
        self.blockchain_url = "https://blockchain.info"
        self.blocks = "/blocks/{time_in_milliseconds}"
        self.unconfirmed_tx = "/unconfirmed-transactions"
        self.latest_block = "/latestblock"
        self.block_height = "/block-height/{block_height}"
        self.single_tx = "/rawtx/{tx_hash}"
        self.single_block = "/rawblock/{block_hash}"
        self.elasticsearch_url = "http://localhost:9200/"
        self.single_addr = "/rawaddr/{bitcoin_address}"
        self.neo4j_credentials = {
            'uri': 'bolt://localhost:7687',
            'user': "blockchain",
            'password': "blockchain"
        }
