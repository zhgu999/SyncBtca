#!/usr/bin/python3
# -*- coding: UTF-8 -*-

from TokenDistribution import TokenDistribution
import time
import os
import logging
import threading
import queue
import math
import random

td = TokenDistribution()

logger = logging.getLogger()
logger.setLevel(logging.INFO)
rq = time.strftime('%Y%m%d%H%M', time.localtime(time.time()))
log_path = os.getcwd() + '/logs/'
log_name = log_path + rq + '.log'
fh = logging.FileHandler(log_name, mode='w')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

def getm(v2):
    if v2 > 129600:
        m = 1153 * 43200 + 1043 * 43200  + 933 * 43200 + 823 * (v2 - 129600)
    elif v2 > 86400:
        m = 1153 * 43200 + 1043 * 43200  + 933 * (v2 - 86400)
    elif v2 > 43200:
        m = 1153 * 43200 + 1043 * (v2 - 43200)
    else:
        m = 1153 * v2
    return m

if __name__ == '__main__':
    err = 0
    for i in range(129800):
        v1 = getm(i)
        v2 = td.GetTotal(i)
        if v1 != v2:
            err = err + 1
    logger.info("err=%d" % err)