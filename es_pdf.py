from datetime import datetime
from elasticsearch import Elasticsearch
import time
from elasticsearch import helpers


def pdfsearch_all(es):
    """查询所有pdf"""
    query = {
        "query": {
            "match_all": {}
        },
        "from": 0,
        "size": 10
    }
    # 有空看一下search的query与body的结构
    res = es.search(index="pdf", body=query)
    content = res["hits"]["hits"]
    return content


def pdfsearch_keyword(es, keyword):
    """查询关键字的pdf"""
    # should实现了or查询
    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "match": {
                            "title": keyword
                        }
                    },
                    {
                        "match": {
                            "author": keyword
                        }
                    },
                    {
                        "match": {
                            "key_word": keyword
                        }
                    },
                    {
                        "match": {
                            "abstract": keyword
                        }
                    },
                    {
                        "match": {
                            "conten_text": keyword
                        }
                    },
                    {
                        "match": {
                            "images_text": keyword
                        }
                    }
                ]
            }
        },
        "from": 0,
        "size": 10
    }
    # 有空看一下search的query与body的结构
    res = es.search(index="pdf", body=query)
    content = res["hits"]["hits"]
    return content


def add_pdf_date(es, doc):
    """提交数据给ES，也就是上传pdf用的"""
    es.index(index="pdf", document=doc)
    return 0

