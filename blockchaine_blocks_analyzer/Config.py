class Config:
    def __init__(self):
        self.blockchain_url = "https://blockchain.info"
        self.blocks = "/blocks/{time_in_milliseconds}"
        self.unconfirmed_tx = "/unconfirmed-transactions"
        self.latest_block = "/latestblock"
        self.block_height = "/block-height/{block_height}"
        self.single_tx = "/rawtx/{tx_hash}"
        self.single_block = "/rawblock/{block_hash}"
