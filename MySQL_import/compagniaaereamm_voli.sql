-- MySQL dump 10.13  Distrib 8.0.21, for Win64 (x86_64)
--
-- Host: localhost    Database: compagniaaereamm
-- ------------------------------------------------------
-- Server version	8.0.21

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `voli`
--

DROP TABLE IF EXISTS `voli`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `voli` (
  `CodVoli` int NOT NULL AUTO_INCREMENT,
  `Partenza` datetime DEFAULT NULL,
  `Arrivo` datetime DEFAULT NULL,
  `Durata` varchar(10) DEFAULT NULL,
  `CodAerei` int NOT NULL,
  `Da` int NOT NULL,
  `Verso` int NOT NULL,
  `NumScali` int unsigned DEFAULT '0',
  `PrezzoFirst` double NOT NULL,
  `PrezzoBusiness` double NOT NULL,
  `PrezzoEconomy` double NOT NULL,
  `Sconto` int unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`CodVoli`),
  KEY `voli_ibfk_2_idx` (`CodAerei`),
  KEY `voli_ibfk_3_idx` (`Da`),
  KEY `voli_ibfk_4_idx` (`Verso`),
  CONSTRAINT `voli_ibfk_1` FOREIGN KEY (`Verso`) REFERENCES `localita` (`CodLocalita`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `voli_ibfk_2` FOREIGN KEY (`CodAerei`) REFERENCES `aerei` (`CodAerei`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `voli_ibfk_3` FOREIGN KEY (`Da`) REFERENCES `localita` (`CodLocalita`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=124 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `voli`
--

LOCK TABLES `voli` WRITE;
/*!40000 ALTER TABLE `voli` DISABLE KEYS */;
INSERT INTO `voli` VALUES (101,'2020-09-15 20:23:00','2020-09-16 14:08:00','17h 45m',115,111,102,1,1875,1125,375,20),(102,'2020-10-13 17:23:00','2020-10-14 10:33:00','17h 10m',102,127,103,1,1500,900,300,0),(103,'2020-09-26 03:01:00','2020-09-26 18:06:00','13h 5m',110,129,104,1,2000,1200,400,25),(104,'2020-09-08 08:56:00','2020-09-08 13:11:00','4h 15m',105,105,125,0,350,210,70,0),(105,'2020-09-30 12:10:00','2020-09-30 14:35:00','2h 25m',112,101,106,0,250,150,50,0),(106,'2020-10-04 22:30:00','2020-10-05 13:55:00','15h 25m',114,107,117,1,2875,1725,575,15),(107,'2020-09-17 13:47:00','2020-09-18 02:47:00','13h 0m',109,110,108,0,1375,825,275,0),(108,'2020-10-02 23:32:00','2020-10-03 01:27:00','1h 55m',108,109,122,0,425,255,85,5),(110,'2020-10-05 11:00:00','2020-10-06 04:20:00','17h 20m',113,131,128,1,5000,3000,1000,30),(111,'2020-11-10 12:45:00','2020-11-10 16:25:00','3h 35m',123,112,124,0,750,450,150,0),(112,'2020-09-10 18:05:00','2020-09-10 20:00:00','1h 55m',103,120,123,0,300,180,60,0),(113,'2020-10-14 06:30:00','2020-10-14 09:10:00','2h 40m',105,126,121,0,350,280,70,5),(114,'2020-11-03 19:20:00','2020-11-04 15:50:00','20h 30m',134,118,114,1,1250,750,250,10),(115,'2020-09-23 14:28:00','2020-09-24 13:18:00','22h 50m',125,130,116,2,4000,2400,800,0),(116,'2020-09-25 03:42:00','2020-09-26 00:02:00','20h 20m',125,115,119,2,2300,1380,460,0),(117,'2020-09-27 21:20:00','2020-09-28 13:00:00','15h 40m',136,113,114,1,10000,6000,2000,25),(118,'2020-09-07 14:38:00','2020-09-07 16:43:00','2h 5m',121,112,108,0,150,90,30,0),(119,'2020-10-19 00:57:00','2020-10-20 01:37:00','24h 30m',109,130,106,2,4500,2700,900,0),(120,'2020-09-21 07:40:00','2020-09-21 08:45:00','1h 5m',105,111,101,0,350,210,70,10);
/*!40000 ALTER TABLE `voli` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-30  9:46:46
