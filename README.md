## rpc and dbp sync data

### 安装bbc_lib
```bash
cd bbc_lib
./setup.sh
```
### 同步区块数据和交易数据
```bash
sudo pip3 install requests
sudo pip3 install json
sudo pip3 install pymysql
./btca.py
```

### 同步排名数据
```bash
sudo pip3 install requests
sudo pip3 install json
sudo pip3 install pymysql
sudo pip3 install protobuf
protoc ./dbp/dbp.proto  --python_out=./
protoc ./dbp/lws.proto  --python_out=./
./task.py
```