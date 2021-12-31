#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# 参考地址 https://github.com/FissionAndFusion/FnFnCoreWallet/wiki/Socket%E6%8E%A5%E5%8F%A3%E5%8D%8F%E8%AE%AE

from socket import *
import dbp_pb2
import lws_pb2
import sys
import struct
import config
import task
import time
import requests
import pymysql
import json
import traceback
import os
import threading
from ctypes import *
from binascii import a2b_hex,hexlify, unhexlify

bbc = cdll.LoadLibrary('./libcrypto.so')
bbc.GetAddr.argtypes = [c_char_p]
bbc.GetAddr.restype = c_char_p

url = config.url
connection = pymysql.connect(host=config.host, port=config.port, user=config.user, password=config.password, db=config.db)


def GetVote(hex_str):
    dpos_addr = bbc.GetAddr(a2b_hex(hex_str[0:66]))
    client_addr = bbc.GetAddr(a2b_hex(hex_str[66:]))
    return dpos_addr,client_addr

def InsertPoolTx(txid):
    rpc_cmd = { "id":1,
                "method":"gettransaction",
                "jsonrpc":"2.0",
                "params":{"txid": txid}
            }
    response = requests.post(url, json=rpc_cmd)
    obj = json.loads(response.text)
    tx = obj["result"]["transaction"]
    dpos_in = None
    client_in = None
    dpos_out = None
    client_out = None
    if tx["sendto"][:4] == "20w0":
        dpos_in,client_in = GetVote(tx["sig"][0:132])
    if tx["sendfrom"][:4] == "20w0":
        if tx["sendto"][:4] == "20w0":
            dpos_out,client_out = GetVote(tx["sig"][132:264])
        else:
            dpos_out,client_out = GetVote(tx["sig"][0:132])

    data = None
    if len(tx["data"]) > 0:
        data = tx["data"]
        if tx["type"] == 'certification':
            data = 'certification'
        elif len(data) >= 4096:
            data = data[:4096]
    with connection.cursor() as cursor:
        sql = "delete from PoolTx where (transtime + 600) < %s" % int(time.time())
        cursor.execute(sql)
        sql = "insert PoolTx(txid,form,`to`,amount,free,type,lock_until,n,data,dpos_in,client_in,dpos_out,client_out,transtime)values(%s,%s,%s,%s,%s,%s,%s,0,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,[tx["txid"], tx["sendfrom"],tx["sendto"],tx["amount"],tx["txfee"],tx["type"],tx["lockuntil"],data,dpos_in,client_in,dpos_out,client_out,tx["time"]])
    connection.commit()


event_block = threading.Event()
is_exit = False
class block_run(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        while is_exit == False:
            event_block.wait()
            event_block.clear()
            task.Run()


if __name__ == '__main__':
    try:
        br = block_run()
        br.start()
        ADDR = ("127.0.0.1",9905)
        s = socket(AF_INET,SOCK_STREAM)
        s.connect(ADDR)
        conn = dbp_pb2.Connect()
        conn.session = ""
        conn.version = 1
        conn.client = "lws"
        obj = lws_pb2.ForkID()
        obj.ids.append(config.forkid)
        conn.udata["forkid"].Pack(obj)
        b = dbp_pb2.Base()
        b.msg = dbp_pb2.CONNECT
        b.object.Pack(conn)
        msg = b.SerializeToString()
        l = struct.pack(">I", len(msg))
        s.send(l + msg)
        ret = s.recv(1024)
        base = dbp_pb2.Base()
        base.ParseFromString(ret[4:])
        if base.msg == dbp_pb2.FAILED:
            failed = dbp_pb2.Failed()
            base.object.Unpack(failed)
            print("failed:",failed)
            s.close()
            sys.exit()    
        if base.msg == dbp_pb2.CONNECTED:
            Connected = dbp_pb2.Connected()
            base.object.Unpack(Connected)
            print("Connected:",Connected)

        b.msg = dbp_pb2.SUB
        sub = dbp_pb2.Sub()
        sub.id = "tx"
        sub.name = "all-tx"
        b.object.Pack(sub)
        msg = b.SerializeToString()
        l = struct.pack(">I", len(msg))
        s.send(l + msg)

        ret = s.recv(1024)
        base = dbp_pb2.Base()
        base.ParseFromString(ret[4:])
        if base.msg == dbp_pb2.READY:
            ready = dbp_pb2.Ready()
            base.object.Unpack(ready)
            print("ready:",ready)
        if base.msg == dbp_pb2.NOSUB:
            nosub = dbp_pb2.Nosub()
            base.object.Unpack(nosub)
            print("nosub:",nosub)

        b.msg = dbp_pb2.SUB
        sub = dbp_pb2.Sub()
        sub.id = "block"
        sub.name = "all-block"
        b.object.Pack(sub)
        msg = b.SerializeToString()
        l = struct.pack(">I", len(msg))
        s.send(l + msg)

        ret = s.recv(1024)
        base = dbp_pb2.Base()
        base.ParseFromString(ret[4:])
        if base.msg == dbp_pb2.READY:
            ready = dbp_pb2.Ready()
            base.object.Unpack(ready)
            print("ready:",ready)
        if base.msg == dbp_pb2.NOSUB:
            nosub = dbp_pb2.Nosub()
            base.object.Unpack(nosub)
            print("nosub:",nosub)

        while True:
            ret = s.recv(4)
            head_len = struct.unpack(">I",ret)[0]
            ret = b""
            while len(ret) < head_len:
                ret = ret + s.recv(head_len - len(ret))
            #print(len(ret),head_len)
            base = dbp_pb2.Base()
            base.ParseFromString(ret)
            if base.msg == dbp_pb2.ADDED:
                add = dbp_pb2.Added()
                base.object.Unpack(add)
                if add.id == "tx":
                    tx = lws_pb2.Transaction()
                    add.object.Unpack(tx)
                    txid = hexlify(tx.hash[::-1]).decode()
                    InsertPoolTx(txid)
                    print("tx id:", txid)
                if add.id == "block":
                    block = lws_pb2.Block()
                    add.object.Unpack(block)
                    print("block nHeight:",block.nHeight)
                    event_block.set()
        
            elif base.msg == dbp_pb2.PING:
                p = dbp_pb2.Pong()
                p.id = "1"
                b.object.Pack(p)
                msg = b.SerializeToString()
                l = struct.pack(">I", len(msg))
                s.send(l + msg)
                print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),"PING PONG ...")
        s.close()
    except KeyboardInterrupt:
        is_exit = True
        event_block.set()
        time.sleep(2)
        sys.exit()
    except:
        is_exit = True
        event_block.set()
        traceback.print_exc()
        print("restart.....",time.time())
        time.sleep(3)
        python = sys.executable
        os.execl(python, python, *sys.argv)