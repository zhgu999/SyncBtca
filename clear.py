#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import requests
import json
import pymysql
import time, datetime
from decimal import Decimal
import sys
import os
import config
import logging
import traceback 
import bbc_lib

connection = pymysql.connect(host=config.host, port=config.port, user=config.user, password=config.password, db=config.db)


def ExecSql(sql):
    try:
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        return 0
    
ExecSql("delete from Block")
ExecSql("delete from Tx")


