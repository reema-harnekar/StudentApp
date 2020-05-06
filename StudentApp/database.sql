-- MySQL dump 10.13  Distrib 5.7.30, for Linux (x86_64)
--
-- Host: localhost    Database: StudentApp
-- ------------------------------------------------------
-- Server version	5.7.30-0ubuntu0.18.04.1

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
-- Table structure for table `Grades`
--

DROP TABLE IF EXISTS `Grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Grades` (
  `ROLLNO` varchar(6) DEFAULT NULL,
  `STANDARD` int(11) NOT NULL,
  `GRADE` varchar(3) NOT NULL,
  `REMARK` varchar(10) NOT NULL,
  `PERCENTAGE` int(11) NOT NULL,
  KEY `ROLLNO` (`ROLLNO`),
  CONSTRAINT `Grades_ibfk_1` FOREIGN KEY (`ROLLNO`) REFERENCES `StudentApp` (`ROLL_NO`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Grades`
--

LOCK TABLES `Grades` WRITE;
/*!40000 ALTER TABLE `Grades` DISABLE KEYS */;
INSERT INTO `Grades` VALUES ('10@12',1,'O','Pass',98),('10@12',2,'O','Pass',90),('10@12',3,'O','Pass',89),('10@12',4,'O','Pass',76),('10@12',5,'O','Pass',85),('10@12',6,'O','Pass',91),('10@12',7,'O','Pass',94),('10@12',8,'O','Pass',89),('10@12',9,'O','Pass',90);
/*!40000 ALTER TABLE `Grades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `StudentApp`
--

DROP TABLE IF EXISTS `StudentApp`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `StudentApp` (
  `ROLL_NO` varchar(6) NOT NULL,
  `NAME` varchar(100) NOT NULL,
  `EMAIL` varchar(320) NOT NULL,
  `PASSWORD` varchar(100) NOT NULL,
  `STANDARD` int(11) NOT NULL,
  `REGISTER_DATE` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`ROLL_NO`),
  UNIQUE KEY `EMAIL` (`EMAIL`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `StudentApp`
--

LOCK TABLES `StudentApp` WRITE;
/*!40000 ALTER TABLE `StudentApp` DISABLE KEYS */;
INSERT INTO `StudentApp` VALUES ('10@12','Reema Harnekar','reema@gmail.com','$5$rounds=535000$hBKqlvxH4ENgDXPv$5OblFZ/Nmvq53fqSiUQw4TO.C4PLmAS7A9Czf4i3r91',10,'2020-05-06 08:38:46');
/*!40000 ALTER TABLE `StudentApp` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2020-05-06 14:12:08
