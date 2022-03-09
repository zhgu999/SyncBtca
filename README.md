## rpc and dbp sync data


### 安装数据库
```bash
sudo apt install mysql-server
sudo  mysql -u root
mysql> use mysql;
mysql> CREATE USER 'btca'@'localhost' IDENTIFIED BY '1234qwer';
mysql> GRANT ALL ON *.* TO 'btca'@'localhost';
mysql> FLUSH PRIVILEGES;
mysql> select User,plugin,host from user;
+------------------+-----------------------+-----------+
| User             | plugin                | host      |
+------------------+-----------------------+-----------+
| root             | auth_socket           | localhost |
| mysql.session    | mysql_native_password | localhost |
| mysql.sys        | mysql_native_password | localhost |
| debian-sys-maint | mysql_native_password | localhost |
| btca             | mysql_native_password | localhost |
+------------------+-----------------------+-----------+
5 rows in set (0.00 sec)
sudo apt install mysql-workbench
```

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
### 链上程序
[BigBang](https://github.com/BigBang-Foundation/BigBang)