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
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `ID` varchar(20) NOT NULL,
  `Nome` varchar(50) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `Password` varchar(20) NOT NULL,
  `Ruolo` enum('Cliente','Operatore','Anonimo') NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES ('anonimo','anonimo','anonimo@anonimo.it','anonimo','Anonimo'),('BRTIRS35O8991','Iris','iris.iris@mail.en','iris678','Operatore'),('cliente','cliente','cliente@cliente.it','cliente','Cliente'),('CLVKVN89Y7471','Kevin','kkkevin@mail.es','kevin007','Cliente'),('COCLUS17R289W','Luisa','luisa@far.it','luisa000','Cliente'),('GHLDNL34R57AE','Daniela','dani@hotmail.it','daniela111','Cliente'),('LDRALC78T098B','Alice','alice@hotmail.it','alice558','Operatore'),('LYTCRL23J563L','Carlo','carlol@gmail.com','carlo000','Cliente'),('MRREMM89Q345L','Emma','emma@gmail.com','emma333','Operatore'),('MTTUGO94D598U','Ugo','ugo@gmail.com','ugo997','Operatore'),('operatore','operatore','operatore@operatore.it','operatore','Operatore'),('PMPMRC99M200R','Marco','marco.p@gmail.com','marco345','Cliente'),('QPTJSN38T077R','Jason','json@gmail.com','jason337','Cliente'),('RRNGRG78S10E','Giorgia','giorgia@fast.it','giorgia77','Cliente'),('SCHFRN23F452M','Francesca','franci.sc@mail.fr','francesca123','Cliente'),('SZCHMR91E578E','Homer','homoh@live.it','homer86','Cliente'),('TNTBOB83Y24DP','Bob','bob@mail.it','bob010','Cliente'),('TWSLVR18L50R','Oliver','oliver@mail.en','oliver006','Operatore'),('VRLNOA12D345G','Noa','noa@mail.en','noa554','Cliente');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
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
