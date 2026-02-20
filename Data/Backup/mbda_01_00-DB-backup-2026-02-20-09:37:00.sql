/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19  Distrib 10.11.14-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: 127.0.0.1    Database: mbda_01_00
-- ------------------------------------------------------
-- Server version	10.11.14-MariaDB-0ubuntu0.24.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `area`
--

DROP TABLE IF EXISTS `area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `area` (
  `area_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `areaID` varchar(25) NOT NULL,
  `area` varchar(25) NOT NULL,
  PRIMARY KEY (`area_id`),
  UNIQUE KEY `unique_area` (`areaID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `area`
--

LOCK TABLES `area` WRITE;
/*!40000 ALTER TABLE `area` DISABLE KEYS */;
INSERT INTO `area` VALUES
(1,'AREA_02','Assembly'),
(2,'AREA_03','Material Handling'),
(3,'AREA_01','Machining'),
(4,'AREA_04','Quality Control');
/*!40000 ALTER TABLE `area` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `component`
--

DROP TABLE IF EXISTS `component`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `component` (
  `component_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `machine_id` smallint(5) unsigned NOT NULL,
  `componentClass` varchar(25) NOT NULL,
  `componentID` varchar(25) NOT NULL,
  `measure_id` smallint(5) unsigned NOT NULL,
  `component_mttf` double DEFAULT NULL,
  `component_mtbf` double DEFAULT NULL,
  `component_mttr` double DEFAULT NULL,
  `activationTime` datetime NOT NULL,
  `deactivationTime` datetime DEFAULT NULL,
  PRIMARY KEY (`component_id`),
  UNIQUE KEY `unique_componentID` (`componentID`),
  KEY `fk_machine_id` (`machine_id`),
  KEY `fk_component_measure_id` (`measure_id`),
  CONSTRAINT `fk_component_measure_id` FOREIGN KEY (`measure_id`) REFERENCES `measure` (`measure_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_machine_id` FOREIGN KEY (`machine_id`) REFERENCES `machine` (`machine_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `component`
--

LOCK TABLES `component` WRITE;
/*!40000 ALTER TABLE `component` DISABLE KEYS */;
INSERT INTO `component` VALUES
(1,4,'Servo Motor','R001',11,2000,2500,60,'2024-01-01 08:00:00',NULL),
(2,4,'Gripper','R002',11,1800,2200,55,'2024-01-01 08:00:00',NULL),
(3,3,'Drive Motor','B001',11,1500,1800,40,'2024-01-01 08:00:00',NULL),
(4,1,'Laser Sensor','Q002',11,3000,3500,20,'2024-01-01 08:00:00',NULL),
(5,1,'Camera System','Q001',11,3000,3500,20,'2024-01-01 08:00:00',NULL),
(6,2,'Tool Changer','C003',11,900,1100,35,'2024-01-01 08:00:00',NULL),
(7,2,'Spindle Motor','C001',11,1200.5,1500,45,'2024-01-01 08:00:00',NULL),
(8,2,'Cooling System','C002',11,800,1000,30,'2024-01-01 08:00:00',NULL);
/*!40000 ALTER TABLE `component` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item`
--

DROP TABLE IF EXISTS `item`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `item` (
  `item_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `itemID` varchar(25) NOT NULL,
  `measure_id` smallint(5) unsigned NOT NULL,
  `cycleTime` double NOT NULL,
  PRIMARY KEY (`item_id`),
  UNIQUE KEY `unique_itemID` (`itemID`),
  KEY `fk_item_measure_id` (`measure_id`),
  CONSTRAINT `fk_item_measure_id` FOREIGN KEY (`measure_id`) REFERENCES `measure` (`measure_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item`
--

LOCK TABLES `item` WRITE;
/*!40000 ALTER TABLE `item` DISABLE KEYS */;
INSERT INTO `item` VALUES
(1,'Landing Gear Component',7,200),
(2,'Control Surface Actuator',5,175),
(3,'Fuel Pump Assembly',2,150),
(4,'Hydraulic Valve V2',2,100),
(5,'Hydraulic Valve V1',2,95),
(6,'Aerospace Bracket B',1,115),
(7,'Aerospace Bracket A',1,120.5),
(8,'Navigation Housing',6,130),
(9,'Engine Mount M2',3,90),
(10,'Engine Mount M1',3,85);
/*!40000 ALTER TABLE `item` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `item_measure_component`
--

DROP TABLE IF EXISTS `item_measure_component`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `item_measure_component` (
  `item_measure_component_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `measure_component_id` smallint(5) unsigned NOT NULL,
  `item_id` smallint(5) unsigned NOT NULL,
  `min_value` double NOT NULL,
  `avg_value` double NOT NULL,
  `max_value` double NOT NULL,
  PRIMARY KEY (`item_measure_component_id`),
  UNIQUE KEY `unique_item_measure_component` (`measure_component_id`,`item_id`),
  KEY `fk_item_measure_component_item_id` (`item_id`),
  CONSTRAINT `fk_item_measure_component_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`item_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_item_measure_component_measure_component_id` FOREIGN KEY (`measure_component_id`) REFERENCES `measure_component` (`measure_component_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `item_measure_component`
--

LOCK TABLES `item_measure_component` WRITE;
/*!40000 ALTER TABLE `item_measure_component` DISABLE KEYS */;
/*!40000 ALTER TABLE `item_measure_component` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `machine`
--

DROP TABLE IF EXISTS `machine`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `machine` (
  `machine_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `area_id` smallint(5) unsigned NOT NULL,
  `machineClass` varchar(25) NOT NULL,
  `machineID` varchar(25) NOT NULL,
  `measure_id` smallint(5) unsigned NOT NULL,
  `machine_mttf` double DEFAULT NULL,
  `machine_mtbf` double DEFAULT NULL,
  `machine_mttr` double DEFAULT NULL,
  `activationTime` datetime NOT NULL,
  `deactivationTime` datetime DEFAULT NULL,
  PRIMARY KEY (`machine_id`),
  UNIQUE KEY `unique_machineID` (`machineID`),
  KEY `fk_area_id` (`area_id`),
  KEY `fk_machine_measure_id` (`measure_id`),
  CONSTRAINT `fk_area_id` FOREIGN KEY (`area_id`) REFERENCES `area` (`area_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_machine_measure_id` FOREIGN KEY (`measure_id`) REFERENCES `measure` (`measure_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `machine`
--

LOCK TABLES `machine` WRITE;
/*!40000 ALTER TABLE `machine` DISABLE KEYS */;
INSERT INTO `machine` VALUES
(1,4,'Quality Scanner','M004',11,3000,3500,20,'2024-01-01 08:00:00',NULL),
(2,3,'CNC Milling','M001',11,1200.5,1500,45,'2024-01-01 08:00:00',NULL),
(3,2,'Conveyor Belt','M003',11,1500,1800,40,'2024-01-01 08:00:00',NULL),
(4,1,'Robotic Arm','M002',11,2000,2500,60,'2024-01-01 08:00:00',NULL);
/*!40000 ALTER TABLE `machine` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measure`
--

DROP TABLE IF EXISTS `measure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `measure` (
  `measure_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `unitID` varchar(25) NOT NULL,
  `unit` varchar(50) NOT NULL,
  `measure` varchar(50) NOT NULL,
  PRIMARY KEY (`measure_id`),
  UNIQUE KEY `unique_measue_measure` (`measure`),
  UNIQUE KEY `unique_measure_unit` (`unitID`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measure`
--

LOCK TABLES `measure` WRITE;
/*!40000 ALTER TABLE `measure` DISABLE KEYS */;
INSERT INTO `measure` VALUES
(1,'TEMP_C','°C','Temperature'),
(2,'PRES_BAR','bar','Pressure'),
(3,'VIB_MM_S','mm/s','Vibration'),
(4,'RPM_VAL','rpm','RPM'),
(5,'FORCE_N','N','Force'),
(6,'TORQUE_NM','Nm','Torque'),
(7,'DIM_MM','mm','Dimension'),
(8,'ROUGH_MU','μm','Surface Roughness'),
(9,'CURR_A','A','Current'),
(10,'VOLT_V','V','Voltage'),
(11,'HOUR','H','hour');
/*!40000 ALTER TABLE `measure` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `measure_component`
--

DROP TABLE IF EXISTS `measure_component`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `measure_component` (
  `measure_component_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `component_id` smallint(5) unsigned NOT NULL,
  `measure_id` smallint(5) unsigned NOT NULL,
  PRIMARY KEY (`measure_component_id`),
  UNIQUE KEY `unique_measure_component` (`component_id`,`measure_id`),
  KEY `fk_measure_component_measure_id` (`measure_id`),
  CONSTRAINT `fk_measure_component_component_id` FOREIGN KEY (`component_id`) REFERENCES `component` (`component_id`) ON DELETE CASCADE,
  CONSTRAINT `fk_measure_component_measure_id` FOREIGN KEY (`measure_id`) REFERENCES `measure` (`measure_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `measure_component`
--

LOCK TABLES `measure_component` WRITE;
/*!40000 ALTER TABLE `measure_component` DISABLE KEYS */;
INSERT INTO `measure_component` VALUES
(8,1,5),
(7,2,5),
(4,3,4),
(1,4,7),
(2,5,7),
(3,6,6),
(6,7,1),
(5,8,1);
/*!40000 ALTER TABLE `measure_component` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `prodPlan`
--

DROP TABLE IF EXISTS `prodPlan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `prodPlan` (
  `prodPlan_id` smallint(5) unsigned NOT NULL AUTO_INCREMENT,
  `batchID` varchar(25) NOT NULL,
  `item_id` smallint(5) unsigned NOT NULL,
  `startTime` datetime DEFAULT NULL,
  `endTime` datetime DEFAULT NULL,
  `itemQuantity` double DEFAULT NULL,
  `event_time` datetime(6) NOT NULL,
  `recording_time` datetime(6) NOT NULL,
  PRIMARY KEY (`prodPlan_id`),
  UNIQUE KEY `unique_prodPlan` (`batchID`),
  KEY `fk_prodPlan_item_id` (`item_id`),
  CONSTRAINT `fk_prodPlan_item_id` FOREIGN KEY (`item_id`) REFERENCES `item` (`item_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `prodPlan`
--

LOCK TABLES `prodPlan` WRITE;
/*!40000 ALTER TABLE `prodPlan` DISABLE KEYS */;
/*!40000 ALTER TABLE `prodPlan` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-20  9:37:02
