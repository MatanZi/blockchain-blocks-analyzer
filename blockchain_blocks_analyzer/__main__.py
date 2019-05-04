import time
import click
import logging
from os import path, makedirs
from Config import conf_logger
from Config import Config
from datetime import datetime, timedelta
from blockchain_blocks_analyzer import to_millis
from blockchain_blocks_analyzer import generate_docs
from blockchain_blocks_analyzer import get_single_block
from blockchain_blocks_analyzer import get_blocks_by_date
from blockchain_blocks_analyzer import add_index


def validate(ctx, param, value):
    try:
        if not value:
            return
        return datetime.strptime(str(value), '%d-%m-%Y')
    except ValueError as ve:
        click.echo("Incorrect data format {}, should be DD-MM-YYYY".format(str(value)))
        ctx.exit()


@click.command()
@click.option('-sd', '--start_date', help='a date of the first transaction.', callback=validate)
@click.option('-ld', '--last_date', help='a date of the last transaction.', callback=validate)
def btc_analyzer_cli(start_date, last_date):
    """

    Blockchain analyzer is a tool for parse a Bitcoin blocks and track a specific transaction.

    """
    conf = Config()
    # root folder path.
    root_folder = path.dirname(path.dirname(__file__))
    # path to log file
    log_path = "{}/log".format(root_folder)
    # create log folder if not exists.
    if not path.exists(log_path):
        makedirs(log_path)

    # cofigure logger
    conf_logger(log_path=log_path, file_name="blockchain_blocks_analyzer")
    logger = logging.getLogger("blockchain_blocks_analyzer")

    if not(start_date and last_date):
        click.echo("start date and last date must be specify.")
        return

    logger.info("starting btc-analyzer.")

    # swap dates if start date is bigger.
    if start_date > last_date:
        start_date, last_date = last_date, start_date

    # get all date range in a list
    num_days = last_date - start_date
    dates = [start_date + timedelta(days=d) for d in range(0, num_days.days)]
    # request all the blocks between the range date.
    blocks_hash = []
    for date in dates:
        blocks = get_blocks_by_date(time_mils=to_millis(date))
        blocks_hash.extend(list(map(lambda b: b['hash'], blocks)))
        time.sleep(5)

    # parse transaction.
    trxs = []
    for block_hash in blocks_hash:
        trxs.extend(list(map(generate_docs, get_single_block(block_hash=block_hash))))

    # upload date to elasticsearch
    for doc in trxs:
        add_index(es_url=conf.elasticsearch_url, body=doc, index_name='btc_transactions', doc_type='btc_trx')
    # track algorithm, after specific transaction.
    pass


if __name__ == '__main__':
    btc_analyzer_cli()
