import json
from tqdm import tqdm
import click
import logging
from os import path, makedirs
from datetime import datetime, timedelta
from Config import conf_logger
from Config import Config
from blockchain_blocks_analyzer import to_millis
from blockchain_blocks_analyzer import generate_docs
from blockchain_blocks_analyzer import get_single_block
from blockchain_blocks_analyzer import get_blocks_by_date
from elastic_handler import add_index


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
    logger.info("calculating dates.")
    num_days = last_date - start_date
    dates = [start_date + timedelta(days=d) for d in tqdm(range(0, num_days.days))]

    # request all the blocks between the range date.
    logger.info("fetching all blocks hash by given date.")
    blocks_hash = []
    for date in tqdm(dates):
        try:
            blocks = get_blocks_by_date(time_mils=to_millis(date))
        except json.decoder.JSONDecodeError:
            logger.error('json decode for date: {} failed.'.format(date))
            continue

        blocks_hash.extend(list(map(lambda b: b['hash'], blocks['blocks'])))

    # parse transaction.
    logger.info("fetching all transaction by given block.")
    trxs = []
    for block_hash in blocks_hash:
        try:
            trxs.extend(generate_docs(get_single_block(block_hash=block_hash)))
        except json.decoder.JSONDecodeError:
            logger.error('json decode for hash: {} failed.'.format(block_hash))
            continue

        if len(trxs) >= 50:
            # upload date to elasticsearch
            logger.info("uploading transactions so far to elasticsearch.")
            add_index(es_url=conf.elasticsearch_url, body=trxs, index_name='btc_transactions', doc_type='btc_trx')
            trxs.clear()

    # upload date to elasticsearch
    logger.info("uploading all transaction to elasticsearch.")
    add_index(es_url=conf.elasticsearch_url, body=trxs, index_name='btc_transactions', doc_type='btc_trx')

    # track algorithm, after specific transaction.
    pass


if __name__ == '__main__':
    btc_analyzer_cli()
