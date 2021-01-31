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
-- Table structure for table `posti`
--

DROP TABLE IF EXISTS `posti`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `posti` (
  `CodClassi` varchar(15) DEFAULT NULL,
  `CodPosti` varchar(4) NOT NULL,
  `CodPrenotazioni` int NOT NULL,
  PRIMARY KEY (`CodPosti`,`CodPrenotazioni`),
  KEY `CodClassi` (`CodClassi`),
  KEY `posti_ibfk_2_idx` (`CodPrenotazioni`),
  CONSTRAINT `posti_ibfk_1` FOREIGN KEY (`CodClassi`) REFERENCES `classi` (`CodClassi`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `posti_ibfk_2` FOREIGN KEY (`CodPrenotazioni`) REFERENCES `prenotazioni` (`CodPrenotazioni`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `posti`
--

LOCK TABLES `posti` WRITE;
/*!40000 ALTER TABLE `posti` DISABLE KEYS */;
INSERT INTO `posti` VALUES ('Business','10A',144),('Business','10B',132),('Business','10B',144),('Business','10C',132),('Business','10D',132),('Business','10D',136),('Business','10E',132),('Business','10E',136),('Business','11B',132),('Business','11C',132),('Business','11D',132),('Business','11E',132),('Business','12A',162),('Business','12B',162),('Business','12C',162),('Business','12E',155),('Business','12E',162),('Business','12F',155),('Business','12F',162),('Business','13C',162),('Business','13D',155),('Business','13D',162),('Business','13E',155),('Business','13E',162),('Business','13F',162),('Business','14A',132),('Business','14B',132),('Business','4A',148),('Business','4B',148),('Business','4C',148),('Business','4D',134),('Business','4D',148),('Business','4E',134),('Business','4E',148),('Business','4F',134),('Business','4F',169),('Business','5A',136),('Business','5A',143),('Business','5A',148),('Business','5B',136),('Business','5B',143),('Business','5B',148),('Business','5C',136),('Business','5C',143),('Business','5D',143),('Business','5D',169),('Business','5E',143),('Business','5E',154),('Business','5E',169),('Business','5F',143),('Business','5F',154),('Business','5F',169),('Business','6A',143),('Business','6A',166),('Business','6A',170),('Business','6B',143),('Business','6B',166),('Business','6B',170),('Business','6C',143),('Business','6C',166),('Business','6C',170),('Business','6D',131),('Business','6D',138),('Business','6D',143),('Business','6D',166),('Business','6E',129),('Business','6E',131),('Business','6E',138),('Business','6E',143),('Business','6E',158),('Business','6E',166),('Business','6E',169),('Business','6E',170),('Business','6F',129),('Business','6F',131),('Business','6F',143),('Business','6F',154),('Business','6F',157),('Business','6F',158),('Business','6F',169),('Business','6F',170),('Business','7A',149),('Business','7A',158),('Business','7A',170),('Business','7B',149),('Business','7B',158),('Business','7B',166),('Business','7B',170),('Business','7C',149),('Business','7C',158),('Business','7C',166),('Business','7D',130),('Business','7D',134),('Business','7D',158),('Business','7D',166),('Business','7E',129),('Business','7E',130),('Business','7E',134),('Business','7E',143),('Business','7E',158),('Business','7E',166),('Business','7F',129),('Business','7F',134),('Business','7F',143),('Business','7F',158),('Business','8A',128),('Business','8A',147),('Business','8A',149),('Business','8A',158),('Business','8B',128),('Business','8B',138),('Business','8B',147),('Business','8B',149),('Business','8B',158),('Business','8B',166),('Business','8C',138),('Business','8C',149),('Business','8C',158),('Business','8C',166),('Business','8D',130),('Business','8E',128),('Business','8E',130),('Business','8E',132),('Business','8F',128),('Business','8F',132),('Business','9A',142),('Business','9A',144),('Business','9A',147),('Business','9B',142),('Business','9B',144),('Business','9B',147),('Business','9C',144),('Business','9C',147),('Business','9D',130),('Business','9E',130),('Business','9E',142),('Business','9E',149),('Business','9F',142),('Business','9F',149),('Economy','11C',145),('Economy','11D',145),('Economy','11E',145),('Economy','11F',145),('Economy','12C',145),('Economy','12D',145),('Economy','12E',145),('Economy','12F',145),('Economy','13E',145),('Economy','13F',145),('Economy','14D',139),('Economy','14E',139),('Economy','14E',145),('Economy','14F',139),('Economy','14F',145),('Economy','15A',171),('Economy','15B',171),('Economy','15C',171),('Economy','15D',171),('Economy','15E',139),('Economy','15E',171),('Economy','15F',139),('Economy','15F',171),('Economy','16A',153),('Economy','16A',171),('Economy','16B',153),('Economy','16B',171),('Economy','16C',171),('Economy','16D',171),('Economy','16E',171),('Economy','17A',153),('Economy','17A',164),('Economy','17B',153),('Economy','17B',159),('Economy','17B',164),('Economy','17C',153),('Economy','17C',159),('Economy','17D',153),('Economy','17D',159),('Economy','17E',153),('Economy','17E',159),('Economy','17E',164),('Economy','17F',153),('Economy','17F',159),('Economy','17F',164),('Economy','18A',164),('Economy','18A',167),('Economy','18B',159),('Economy','18B',164),('Economy','18C',159),('Economy','18D',159),('Economy','18E',159),('Economy','18E',164),('Economy','18F',159),('Economy','18F',164),('Economy','19A',164),('Economy','19A',167),('Economy','19B',164),('Economy','19B',167),('Economy','19C',164),('Economy','19D',159),('Economy','19E',159),('Economy','19E',173),('Economy','19F',173),('Economy','20A',175),('Economy','20B',175),('Economy','20D',173),('Economy','20E',163),('Economy','20E',173),('Economy','20E',175),('Economy','20F',163),('Economy','20F',173),('Economy','20F',175),('Economy','21B',173),('Economy','21C',173),('Economy','21D',173),('Economy','21D',175),('Economy','21E',163),('Economy','21E',173),('Economy','21E',175),('Economy','21F',163),('Economy','21F',173),('Economy','21F',175),('Economy','22A',163),('Economy','22A',165),('Economy','22A',173),('Economy','22B',163),('Economy','22B',165),('Economy','22B',173),('Economy','22C',173),('Economy','22D',163),('Economy','22D',173),('Economy','22E',163),('Economy','22E',173),('Economy','22F',163),('Economy','22F',173),('Economy','23A',163),('Economy','23A',165),('Economy','23A',173),('Economy','23B',163),('Economy','23B',165),('Economy','23B',173),('Economy','23C',163),('Economy','23C',165),('Economy','23D',163),('Economy','23E',163),('Economy','23F',163),('Economy','24A',163),('Economy','24A',165),('Economy','24B',163),('Economy','24B',165),('Economy','26D',140),('Economy','28A',140),('Economy','28B',140),('Economy','28C',140),('Economy','29B',140),('Economy','29C',140),('Economy','30F',140),('Economy','39C',137),('Economy','43D',137),('Economy','43E',137),('Economy','43F',137),('Economy','46E',137),('Economy','46F',137),('Economy','47A',137),('Economy','47B',137),('Economy','48D',137),('Economy','48E',137),('Economy','48F',137),('First','1B',101),('First','1B',124),('First','1B',125),('First','1B',135),('First','1B',150),('First','1B',151),('First','1B',172),('First','1C',101),('First','1C',124),('First','1C',125),('First','1C',135),('First','1C',150),('First','1C',151),('First','1C',172),('First','1D',101),('First','1D',114),('First','1D',124),('First','1D',125),('First','1D',146),('First','1D',150),('First','1D',151),('First','1E',101),('First','1E',114),('First','1E',124),('First','1E',125),('First','1E',146),('First','1E',150),('First','2A',101),('First','2A',123),('First','2A',172),('First','2A',181),('First','2B',101),('First','2B',123),('First','2B',172),('First','2C',101),('First','2C',123),('First','2C',150),('First','2D',124),('First','2D',127),('First','2D',150),('First','2E',124),('First','2E',150),('First','2E',152),('First','2F',124),('First','2F',125),('First','2F',141),('First','2F',150),('First','2F',152),('First','3A',123),('First','3A',133),('First','3A',160),('First','3A',161),('First','3B',123),('First','3B',133),('First','3B',160),('First','3B',161),('First','3C',123),('First','3D',152),('First','3D',160),('First','3E',141),('First','3E',152),('First','3E',160),('First','3F',141),('First','3F',152),('First','3F',160),('First','4D',152),('First','4E',126),('First','4E',152),('First','4F',126),('First','5A',126),('First','5B',126),('First','5E',156),('First','5F',156);
/*!40000 ALTER TABLE `posti` ENABLE KEYS */;
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
