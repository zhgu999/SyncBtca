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
import traceback 

connection = pymysql.connect(host=config.host, port=config.port, user=config.user, password=config.password, db=config.db)

def Init():
    try:
        sql = "delete from Rank"
        cursor = connection.cursor()
        cursor.execute(sql)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        return 0


def UpdateRank():
    with connection.cursor() as cursor :
        cursor.execute("SELECT sum(amount),`to` FROM Tx where spend_txid is null group by `to` having sum(amount) >= 100 order by sum(amount) asc")
        res = cursor.fetchall()
        ranking = 1
        old_balance = 0
        M = len(res) * (1 + len(res)) / 2
        for i in range(len(res)):
            balance = res[i][0]
            address = res[i][1]
            yield_ = Decimal(ranking) / Decimal(M)
            # 假设总收益为1个亿，为了防止数据过小
            yield_ =  (yield_ * Decimal(10**8)) / Decimal(balance)
            sql = "insert into Rank(address,ranking,balance,yield)values('%s',%d,%s,%s)" % (address,ranking,balance,yield_)
            cursor.execute(sql)
            if balance > old_balance:
                ranking = i + 2
            old_balance = balance
        connection.commit()

def UpdateInfo():
    with connection.cursor() as cursor :
        cursor.execute("SELECT sum(amount) as s FROM Tx where spend_txid is null")
        res = cursor.fetchone()
        current_coin_numner = res[0]
        cursor.execute("select count(A.`to`) as s from (SELECT `to` from Tx group by `to`) A")
        res = cursor.fetchone()
        wallet_number = res[0]
        cursor.execute("select balance from Rank order by yield desc limit 1")
        res = cursor.fetchone()
        max_coin_count = res[0]
        sql = "update Info set current_coin_numner = %f,wallet_number = %d,max_coin_count = %f where id = 1" \
            % (current_coin_numner,wallet_number,max_coin_count)
        cursor.execute(sql)
        connection.commit()

if __name__ == '__main__':
    while True:
        try:
            Init()
            UpdateRank()
            UpdateInfo()
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"wait task 3s ...")
            time.sleep(60*10)
        except KeyboardInterrupt:
            sys.exit()
        except:
            traceback.print_exc()
            print("restart.....")
            python = sys.executable
            os.execl(python, python, *sys.argv)