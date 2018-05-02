# -*-coding:utf-8-*-

import sys
reload(sys)
sys.path.append('../../')
from global_utils import es_flow_text as es

def main():
    uid_list = []
    with open("group.txt", "rb") as f:
        for line in f:
            uid_list.append(line.strip())

    query_body = {
        "query":{
            "bool":{
                "must":[
                    {"terms":""





