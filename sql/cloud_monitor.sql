/*
Navicat MySQL Data Transfer

Source Server         : 173.26.100.209
Source Server Version : 50546
Source Host           : 173.26.100.209:3306
Source Database       : cloud_monitor

Target Server Type    : MYSQL
Target Server Version : 50546
File Encoding         : 65001

Date: 2015-11-14 18:02:04
*/

SET FOREIGN_KEY_CHECKS=0;

--
-- Current Database: `cloud_monitor`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `cloud_monitor` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `cloud_monitor`;
-- ----------------------------
-- Table structure for cloud_config
-- ----------------------------
DROP TABLE IF EXISTS `cloud_config`;
CREATE TABLE `cloud_config` (
  `id` int(64) NOT NULL AUTO_INCREMENT,
  `key` varchar(64) NOT NULL,
  `value` varchar(64) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of cloud_config
-- ----------------------------
INSERT INTO `cloud_config` VALUES ('1', 'interval_check', '200');
INSERT INTO `cloud_config` VALUES ('2', 'interval_travelsal', '200');
INSERT INTO `host` VALUES ('3', 'host', '');

-- ----------------------------
-- Table structure for cloud_host
-- ----------------------------
DROP TABLE IF EXISTS `cloud_vhost`;
CREATE TABLE `cloud_host` (
  `id` int(64) NOT NULL AUTO_INCREMENT,
  `host` varchar(64) NOT NULL,
  `uuid` varchar(256) NOT NULL,
  `enable` int(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for cloud_result
-- ----------------------------
DROP TABLE IF EXISTS `cloud_result`;
CREATE TABLE `cloud_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(128) NOT NULL,
  `time` varchar(50) NOT NULL,
  `result` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=131409 DEFAULT CHARSET=utf8;
