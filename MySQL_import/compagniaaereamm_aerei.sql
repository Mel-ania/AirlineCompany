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
-- Table structure for table `aerei`
--

DROP TABLE IF EXISTS `aerei`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aerei` (
  `CodAerei` int NOT NULL AUTO_INCREMENT,
  `Tipo` varchar(30) NOT NULL,
  `NumFile` int unsigned DEFAULT '10',
  `PesoStiva` double DEFAULT '180',
  PRIMARY KEY (`CodAerei`)
) ENGINE=InnoDB AUTO_INCREMENT=139 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aerei`
--

LOCK TABLES `aerei` WRITE;
/*!40000 ALTER TABLE `aerei` DISABLE KEYS */;
INSERT INTO `aerei` VALUES (101,'Airbus A220',24,2160),(102,'Airbus A221',24,2160),(103,'Airbus A222',26,2280),(104,'Airbus A223',26,2280),(105,'Boeing 757',33,2970),(106,'Boeing 751',30,2700),(107,'Boeing 753',30,2700),(108,'Boeing 755',33,2970),(109,'Airbus A321',39,3510),(110,'Airbus A320',39,3510),(111,'Airbus A340',50,4500),(112,'Airbus A341',50,4500),(113,'Airbus A344',51,4590),(114,'Ilyushin 96',53,4770),(115,'Ilyushin 97',53,4770),(116,'Boeing 756',37,3330),(117,'Boeing 752',35,3150),(118,'Boeing 755',37,3330),(119,'Airbus A224',21,1890),(120,'Airbus A225',21,1890),(121,'Airbus A226',25,2250),(122,'Airbus A323',37,3330),(123,'Airbus A325',35,3150),(124,'Airbus A227',25,2250),(125,'Airbus A346',52,4680),(126,'Airbus A347',52,4680),(127,'Airbus A342',54,4860),(128,'Airbus A343',54,4860),(129,'Airbus A345',51,4590),(130,'Airbus A321',36,3240),(131,'Airbus A321',36,3240),(132,'Airbus A321',35,3150),(133,'Airbus A321',37,3330),(134,'Ilyushin 98',59,5310),(135,'Ilyushin 98',59,5310),(136,'Ilyushin 99',58,5220),(137,'Ilyushin 94',58,5220);
/*!40000 ALTER TABLE `aerei` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-08-30  9:46:45
