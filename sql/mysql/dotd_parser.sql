-- MySQL dump 10.13  Distrib 5.6.23, for osx10.8 (x86_64)
--
-- Host: localhost    Database: dotd_parser
-- ------------------------------------------------------
-- Server version	5.6.23

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
-- Table structure for table `auth_cas`
--

DROP TABLE IF EXISTS `auth_cas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_cas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `created_on` datetime DEFAULT NULL,
  `service` varchar(512) DEFAULT NULL,
  `ticket` varchar(512) DEFAULT NULL,
  `renew` char(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_cas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_cas`
--

LOCK TABLES `auth_cas` WRITE;
/*!40000 ALTER TABLE `auth_cas` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_cas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_event`
--

DROP TABLE IF EXISTS `auth_event`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time_stamp` datetime DEFAULT NULL,
  `client_ip` varchar(512) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `origin` varchar(512) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  CONSTRAINT `auth_event_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_event`
--

LOCK TABLES `auth_event` WRITE;
/*!40000 ALTER TABLE `auth_event` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_event` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `role` varchar(512) DEFAULT NULL,
  `description` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_membership`
--

DROP TABLE IF EXISTS `auth_membership`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_membership` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `group_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id__idx` (`user_id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_membership_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`) ON DELETE CASCADE,
  CONSTRAINT `auth_membership_ibfk_2` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_membership`
--

LOCK TABLES `auth_membership` WRITE;
/*!40000 ALTER TABLE `auth_membership` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_membership` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) DEFAULT NULL,
  `name` varchar(512) DEFAULT NULL,
  `table_name` varchar(512) DEFAULT NULL,
  `record_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `group_id__idx` (`group_id`),
  CONSTRAINT `auth_permission_ibfk_1` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(128) DEFAULT NULL,
  `last_name` varchar(128) DEFAULT NULL,
  `email` varchar(512) DEFAULT NULL,
  `password` varchar(512) DEFAULT NULL,
  `registration_key` varchar(512) DEFAULT NULL,
  `reset_password_key` varchar(512) DEFAULT NULL,
  `registration_id` varchar(512) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dawn_enchantments`
--

DROP TABLE IF EXISTS `dawn_enchantments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dawn_enchantments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dawn_enchantments`
--

LOCK TABLES `dawn_enchantments` WRITE;
/*!40000 ALTER TABLE `dawn_enchantments` DISABLE KEYS */;
/*!40000 ALTER TABLE `dawn_enchantments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dawn_equipment`
--

DROP TABLE IF EXISTS `dawn_equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dawn_equipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `perception` int(11) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `value_gtoken` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `isUnique` int(11) DEFAULT NULL,
  `canEnchant` int(11) DEFAULT NULL,
  `equipType` int(11) DEFAULT NULL,
  `hlt` int(11) DEFAULT NULL,
  `eng` int(11) DEFAULT NULL,
  `sta` int(11) DEFAULT NULL,
  `hnr` int(11) DEFAULT NULL,
  `atk` int(11) DEFAULT NULL,
  `defn` int(11) DEFAULT NULL,
  `power` int(11) DEFAULT NULL,
  `dmg` int(11) DEFAULT NULL,
  `deflect` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dawn_equipment`
--

LOCK TABLES `dawn_equipment` WRITE;
/*!40000 ALTER TABLE `dawn_equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `dawn_equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dawn_generals`
--

DROP TABLE IF EXISTS `dawn_generals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dawn_generals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `race` int(11) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `buffType` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dawn_generals`
--

LOCK TABLES `dawn_generals` WRITE;
/*!40000 ALTER TABLE `dawn_generals` DISABLE KEYS */;
/*!40000 ALTER TABLE `dawn_generals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dawn_legions`
--

DROP TABLE IF EXISTS `dawn_legions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dawn_legions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `num_gen` int(11) DEFAULT NULL,
  `num_trp` int(11) DEFAULT NULL,
  `bonus` int(11) DEFAULT NULL,
  `bonusSpecial` int(11) DEFAULT NULL,
  `bonusText` varchar(512) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `canPurchase` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  `specification` varchar(512) DEFAULT NULL,
  `general_format` longtext,
  `troop_format` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dawn_legions`
--

LOCK TABLES `dawn_legions` WRITE;
/*!40000 ALTER TABLE `dawn_legions` DISABLE KEYS */;
/*!40000 ALTER TABLE `dawn_legions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dawn_mounts`
--

DROP TABLE IF EXISTS `dawn_mounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dawn_mounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `perception` int(11) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `isUnique` int(11) DEFAULT NULL,
  `hlt` int(11) DEFAULT NULL,
  `eng` int(11) DEFAULT NULL,
  `sta` int(11) DEFAULT NULL,
  `hnr` int(11) DEFAULT NULL,
  `atk` int(11) DEFAULT NULL,
  `defn` int(11) DEFAULT NULL,
  `power` int(11) DEFAULT NULL,
  `dmg` int(11) DEFAULT NULL,
  `deflect` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dawn_mounts`
--

LOCK TABLES `dawn_mounts` WRITE;
/*!40000 ALTER TABLE `dawn_mounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `dawn_mounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `dawn_troops`
--

DROP TABLE IF EXISTS `dawn_troops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `dawn_troops` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `race` int(11) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `canPurchase` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `buffType` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `dawn_troops`
--

LOCK TABLES `dawn_troops` WRITE;
/*!40000 ALTER TABLE `dawn_troops` DISABLE KEYS */;
/*!40000 ALTER TABLE `dawn_troops` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs`
--

DROP TABLE IF EXISTS `logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `logs` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(48) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `data` longtext,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uuid` (`uuid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs`
--

LOCK TABLES `logs` WRITE;
/*!40000 ALTER TABLE `logs` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suns_enchantments`
--

DROP TABLE IF EXISTS `suns_enchantments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suns_enchantments` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suns_enchantments`
--

LOCK TABLES `suns_enchantments` WRITE;
/*!40000 ALTER TABLE `suns_enchantments` DISABLE KEYS */;
/*!40000 ALTER TABLE `suns_enchantments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suns_equipment`
--

DROP TABLE IF EXISTS `suns_equipment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suns_equipment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `perception` int(11) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `value_gtoken` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `isUnique` int(11) DEFAULT NULL,
  `canEnchant` int(11) DEFAULT NULL,
  `equipType` int(11) DEFAULT NULL,
  `hlt` int(11) DEFAULT NULL,
  `eng` int(11) DEFAULT NULL,
  `sta` int(11) DEFAULT NULL,
  `hnr` int(11) DEFAULT NULL,
  `atk` int(11) DEFAULT NULL,
  `defn` int(11) DEFAULT NULL,
  `power` int(11) DEFAULT NULL,
  `dmg` int(11) DEFAULT NULL,
  `deflect` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suns_equipment`
--

LOCK TABLES `suns_equipment` WRITE;
/*!40000 ALTER TABLE `suns_equipment` DISABLE KEYS */;
/*!40000 ALTER TABLE `suns_equipment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suns_generals`
--

DROP TABLE IF EXISTS `suns_generals`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suns_generals` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `race` int(11) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `buffType` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suns_generals`
--

LOCK TABLES `suns_generals` WRITE;
/*!40000 ALTER TABLE `suns_generals` DISABLE KEYS */;
/*!40000 ALTER TABLE `suns_generals` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suns_legions`
--

DROP TABLE IF EXISTS `suns_legions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suns_legions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `num_gen` int(11) DEFAULT NULL,
  `num_trp` int(11) DEFAULT NULL,
  `bonus` int(11) DEFAULT NULL,
  `bonusSpecial` int(11) DEFAULT NULL,
  `bonusText` varchar(512) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `canPurchase` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  `specification` varchar(512) DEFAULT NULL,
  `general_format` longtext,
  `troop_format` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suns_legions`
--

LOCK TABLES `suns_legions` WRITE;
/*!40000 ALTER TABLE `suns_legions` DISABLE KEYS */;
/*!40000 ALTER TABLE `suns_legions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suns_mounts`
--

DROP TABLE IF EXISTS `suns_mounts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suns_mounts` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `perception` int(11) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `isUnique` int(11) DEFAULT NULL,
  `hlt` int(11) DEFAULT NULL,
  `eng` int(11) DEFAULT NULL,
  `sta` int(11) DEFAULT NULL,
  `hnr` int(11) DEFAULT NULL,
  `atk` int(11) DEFAULT NULL,
  `defn` int(11) DEFAULT NULL,
  `power` int(11) DEFAULT NULL,
  `dmg` int(11) DEFAULT NULL,
  `deflect` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suns_mounts`
--

LOCK TABLES `suns_mounts` WRITE;
/*!40000 ALTER TABLE `suns_mounts` DISABLE KEYS */;
/*!40000 ALTER TABLE `suns_mounts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `suns_troops`
--

DROP TABLE IF EXISTS `suns_troops`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `suns_troops` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(512) DEFAULT NULL,
  `attack` int(11) DEFAULT NULL,
  `defense` int(11) DEFAULT NULL,
  `race` int(11) DEFAULT NULL,
  `role` int(11) DEFAULT NULL,
  `rarity` int(11) DEFAULT NULL,
  `value_gold` int(11) DEFAULT NULL,
  `value_credits` int(11) DEFAULT NULL,
  `canPurchase` int(11) DEFAULT NULL,
  `questReq` int(11) DEFAULT NULL,
  `source` int(11) DEFAULT NULL,
  `buffType` int(11) DEFAULT NULL,
  `lore` longtext,
  `proc_name` varchar(512) DEFAULT NULL,
  `proc_desc` longtext,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `suns_troops`
--

LOCK TABLES `suns_troops` WRITE;
/*!40000 ALTER TABLE `suns_troops` DISABLE KEYS */;
/*!40000 ALTER TABLE `suns_troops` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-03-01 18:13:48
