# -*- coding: utf-8 -*-
'''
use to save function---about deal database
'''
import sys
from xnr.global_utils import es_xnr


def create_qq_xnr(xnr_info):
# xnr_info = [qq_number,qq_groups,nickname,active_time]
    qq_number = xnr[0]
    qq_groups = xnr[1]
    nickname = xnr[2]
    active_time = xnr[3]
    es.index(index="qq_xnr", doc_type='text', id=qq_number, \
        body={'qq_number':qq_number,'nickname':nickname,'qq_groups':qq_groups,'active_time':active_time})
    return xnr_info


def show_qq_xnr():
    result = True
    return result

def delete_qq_xnr():
    result = True
    return result