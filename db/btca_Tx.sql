-- MySQL dump 10.13  Distrib 5.7.37, for Linux (x86_64)
--
-- Host: localhost    Database: btca
-- ------------------------------------------------------
-- Server version	5.7.37-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `Tx`
--

DROP TABLE IF EXISTS `Tx`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Tx` (
  `id` bigint(20) NOT NULL AUTO_INCREMENT,
  `block_hash` varchar(64) DEFAULT NULL COMMENT '交易所在区块的hash',
  `txid` varchar(64) DEFAULT NULL COMMENT '交易的hash',
  `form` varchar(64) DEFAULT NULL COMMENT 'from 地址',
  `to` varchar(64) DEFAULT NULL COMMENT 'to 地址',
  `amount` decimal(20,10) DEFAULT NULL COMMENT '转账金额',
  `free` decimal(20,10) DEFAULT NULL COMMENT '手续费',
  `type` varchar(16) DEFAULT NULL COMMENT '交易类型',
  `lock_until` int(11) DEFAULT NULL COMMENT '锁定的块高',
  `n` tinyint(6) DEFAULT NULL COMMENT '是否找零',
  `spend_txid` varchar(64) DEFAULT NULL COMMENT '本交易被那个交易花费掉',
  `data` varchar(4096) DEFAULT NULL COMMENT '数据附加的信息',
  `dpos_in` varchar(64) DEFAULT NULL COMMENT '投票的dpos地址',
  `client_in` varchar(64) DEFAULT NULL COMMENT '投票的客户地址',
  `dpos_out` varchar(64) DEFAULT NULL COMMENT '赎回的dpos地址',
  `client_out` varchar(64) DEFAULT NULL COMMENT '赎回的客户地址',
  `transtime` bigint(20) DEFAULT NULL COMMENT '交易时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE KEY `id` (`id`) USING BTREE,
  KEY `block_id` (`block_hash`) USING BTREE,
  KEY `txid` (`txid`) USING BTREE,
  KEY `spend_txid` (`spend_txid`) USING BTREE,
  KEY `to` (`to`) USING BTREE,
  KEY `type` (`type`),
  KEY `form` (`form`) USING BTREE,
  KEY `n` (`n`) USING BTREE,
  KEY `dpos_in` (`dpos_in`) USING BTREE,
  KEY `client_in` (`client_in`) USING BTREE,
  KEY `dpos_out` (`dpos_out`) USING BTREE,
  KEY `client_out` (`client_out`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
/*!40101 SET character_set_client = @saved_cs_client */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-03-17 11:29:49
