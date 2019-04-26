from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


def generate_data(docs_list, index_name, doc_type):
    """Generate documents for bulk helpers.

    :param docs_list: list of dictionary, a list of documents for insertion.
    :param index_name: string, a name of an index.
    :param doc_type: string, documents type.
    :return:
    """
    for doc in docs_list:
        yield {
            "_index": index_name,
            "_type": doc_type,
            "doc": doc,
        }


def add_index(es_url, body, index_name, doc_type):
    """Add documents to an index in with bulk helpers.

    :param doc_type: string, documents type.
    :param index_name: string, a name of an index.
    :param body: list of dictionary, a list of documents for insertion.
    :param es_url: string, an elasticsearch url to connect.
    :return:
    """
    es = Elasticsearch([es_url])
    bulk(es, generate_data(docs_list=body, index_name=index_name, doc_type=doc_type))


def set_conf(es_url, index_name, doc_type, body):
    """Set index configuration for first time of creating a index.

    :param es_url: string, an elasticsearch url to connect.
    :param body: dict, a dictionary of configuration.
    :param doc_type: string, documents type.
    :param index_name: string, a name of an index.
    :return: status
    """
    es = Elasticsearch([es_url])
    res = es.index(index=index_name, doc_type=doc_type, body=body)
    return res['result']
