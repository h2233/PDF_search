from datetime import datetime
from elasticsearch import Elasticsearch
import time
import os
from elasticsearch import helpers


def es_connect():
    """连接ES"""
    es = Elasticsearch(
        "http://localhost:9200",
        sniff_timeout=120,    # 设置超时时间
    )
    return es


def del_index(es):
    """清空pdf索引，仅在初始化中使用[销毁所有数据]"""
    if es.indices.exists(index="pdf"):
        es.indices.delete(index="pdf")["acknowledged"]
        return 0
    return -1


def es_init(es):
    """初始化"""
    es = es_connect()
    del_index(es)
    return 0