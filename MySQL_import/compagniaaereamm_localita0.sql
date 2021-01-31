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
-- Table structure for table `localita`
--

DROP TABLE IF EXISTS `localita`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `localita` (
  `CodLocalita` int NOT NULL AUTO_INCREMENT,
  `Citta` varchar(60) NOT NULL,
  `Nazione` varchar(50) NOT NULL,
  `NomeAeroporto` varchar(50) NOT NULL,
  PRIMARY KEY (`CodLocalita`)
) ENGINE=InnoDB AUTO_INCREMENT=135 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `localita`
--

LOCK TABLES `localita` WRITE;
/*!40000 ALTER TABLE `localita` DISABLE KEYS */;
INSERT INTO `localita` VALUES (101,'Venezia','Italia','Aeroporto di Venezia-Marco Polo'),(102,'Tokyo','Giappone','Aeroporto di Tokyo-Haneda'),(103,'Parigi','Francia','Aeroporto di Parigi Charles de Gaulle'),(104,'New York','USA','Aeroporto Internazionale John F. Kennedy'),(105,'Barcellona','Spagna','Aeroporto di Barcellona-El Prat'),(106,'Istanbul','Turchia','Aeroporto di Istanbul-Atatürk'),(107,'Bangkok','Thailandia','Aeroporto Internazionale di Bangkok-Suvarnabhumi'),(108,'Amsterdam','Olanda','Aeroporto di Amsterdam-Schiphol'),(109,'Londra','Regno Unito','Aeroporto di Londra-Heathrow'),(110,'Vancouver','Canada','Aeroporto Internazionale di Vancouver'),(111,'Roma','Italia','Aeroporto internazionale Leonardo da Vinci'),(112,'Milano','Italia','Aeroporto di Milano-Malpensa'),(113,'Napoli','Italia','Aeroporto Internazionale di Napoli'),(114,'San Francisco','USA','Aeroporto Internazionale di San Francisco'),(115,'Las Vegas','USA','Aeroporto Internazionale McCarran'),(116,'Miami','USA','Aeroporto Internazionale di Miami'),(117,'Bruxelles','Belgio','Aeroporto di Bruxelles-National'),(118,'Madrid','Spagna','Aeroporto di Madrid-Barajas'),(119,'Valencia','Spagna','Aeroporto di Valencia'),(120,'Bordeaux','Francia','Aeroporto di Bordeaux-Mérignac'),(121,'Nizza','Francia','Aeroporto di Nizza Costa Azzurra'),(122,'Berlino','Germania','Aeroporto di Berlino-Brandeburgo'),(123,'Dublino','Irlanda','Aeroporto Internazionale di Dublino'),(124,'Mosca','Russia','Aeroporto di Mosca-Šeremet\'evo'),(125,'San Pietroburgo','Russia','Aeroporto di San Pietroburgo-Pulkovo'),(126,'Atene','Grecia','Aeroporto Internazionale di Atene'),(127,'Pechino','Cina','Aeroporto Internazionale di Pechino-Capital'),(128,'Shanghai','Cina','Aeroporto Internazionale di Shanghai-Pudong'),(129,'Vienna','Austria','Aeroporto di Vienna-Schwechat'),(130,'Sydney','Australia','Aeroporto Internazionale Kingsford Smith'),(131,'Nuova Delhi','India','Aeroporto Internazionale Indira Gandhi');
/*!40000 ALTER TABLE `localita` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-31 19:34:47
