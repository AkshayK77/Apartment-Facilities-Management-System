CREATE DATABASE  IF NOT EXISTS `dbmsfinalpromise` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `dbmsfinalpromise`;
-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: dbmsfinalpromise
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `available_parking`
--

DROP TABLE IF EXISTS `available_parking`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `available_parking` (
  `car_park_no` int NOT NULL,
  `availability` enum('Available','Unavailable') DEFAULT 'Available',
  PRIMARY KEY (`car_park_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `available_parking`
--

LOCK TABLES `available_parking` WRITE;
/*!40000 ALTER TABLE `available_parking` DISABLE KEYS */;
INSERT INTO `available_parking` VALUES (1,'Available'),(2,'Available'),(3,'Available'),(4,'Available'),(5,'Available'),(6,'Available'),(7,'Available'),(8,'Unavailable'),(9,'Unavailable'),(10,'Unavailable'),(11,'Unavailable'),(12,'Unavailable'),(13,'Unavailable'),(14,'Unavailable'),(15,'Available'),(16,'Available'),(17,'Available'),(18,'Available'),(19,'Available'),(20,'Available');
/*!40000 ALTER TABLE `available_parking` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facilities_available`
--

DROP TABLE IF EXISTS `facilities_available`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facilities_available` (
  `facility_id` int NOT NULL AUTO_INCREMENT,
  `facility_name` varchar(50) NOT NULL,
  `availability_status` enum('Available','Unavailable') DEFAULT 'Available',
  `manager_id` int DEFAULT NULL,
  PRIMARY KEY (`facility_id`),
  KEY `manager_id` (`manager_id`),
  CONSTRAINT `facilities_available_ibfk_1` FOREIGN KEY (`manager_id`) REFERENCES `management_committee` (`manager_id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facilities_available`
--

LOCK TABLES `facilities_available` WRITE;
/*!40000 ALTER TABLE `facilities_available` DISABLE KEYS */;
INSERT INTO `facilities_available` VALUES (5,'Gardener','Available',NULL),(6,'Painter','Available',NULL),(7,'Painter','Available',NULL),(8,'Electrician','Available',53);
/*!40000 ALTER TABLE `facilities_available` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `facility_demand`
--

DROP TABLE IF EXISTS `facility_demand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `facility_demand` (
  `facility` varchar(50) NOT NULL,
  `flat_no` int NOT NULL,
  PRIMARY KEY (`flat_no`,`facility`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `facility_demand`
--

LOCK TABLES `facility_demand` WRITE;
/*!40000 ALTER TABLE `facility_demand` DISABLE KEYS */;
INSERT INTO `facility_demand` VALUES ('Plumber',1),('Electrician',8),('Plumber',56),('Electrician',100);
/*!40000 ALTER TABLE `facility_demand` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructor`
--

DROP TABLE IF EXISTS `instructor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructor` (
  `activity_id` int NOT NULL AUTO_INCREMENT,
  `manager_id` int DEFAULT NULL,
  `instructor_name` varchar(100) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `salary` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`activity_id`),
  KEY `fk_manager_id` (`manager_id`),
  CONSTRAINT `fk_manager_id` FOREIGN KEY (`manager_id`) REFERENCES `management_committee` (`manager_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructor`
--

LOCK TABLES `instructor` WRITE;
/*!40000 ALTER TABLE `instructor` DISABLE KEYS */;
INSERT INTO `instructor` VALUES (16,53,'akshay','Basketball Coach',75.00),(17,53,'anosh23','Guitar Tutor',75000.00),(18,53,'ay','Basketball Coach',50.00),(19,53,'dnidwnoodi','Kids Tuition',0.00);
/*!40000 ALTER TABLE `instructor` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `check_manager_role` BEFORE INSERT ON `instructor` FOR EACH ROW BEGIN
    DECLARE role_check VARCHAR(50);

    
    SELECT role INTO role_check
    FROM management_committee
    WHERE manager_id = NEW.manager_id;

    
    IF role_check != 'Activities' THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'manager_id must be a user with the Activities role in management_committee';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `check_manager_role_update` BEFORE UPDATE ON `instructor` FOR EACH ROW BEGIN
    DECLARE role_check VARCHAR(50);

    
    SELECT role INTO role_check
    FROM management_committee
    WHERE manager_id = NEW.manager_id;

    
    IF role_check != 'Activities' THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'manager_id must be a user with the Activities role in management_committee';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `management_committee`
--

DROP TABLE IF EXISTS `management_committee`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `management_committee` (
  `manager_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `role` enum('Supervisor','Activities','Facilities','Security','User') NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`manager_id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `management_committee`
--

LOCK TABLES `management_committee` WRITE;
/*!40000 ALTER TABLE `management_committee` DISABLE KEYS */;
INSERT INTO `management_committee` VALUES (5,'lol','Supervisor','ff3727276784ada3f6d609a19ed541d9e888759559d81a4045e3c790aa40f276'),(13,'eksay','Supervisor','07123e1f482356c415f684407a3b8723e10b2cbbc0b8fcd6282c49d37c9c1abc'),(15,'eksay1','Supervisor','07123e1f482356c415f684407a3b8723e10b2cbbc0b8fcd6282c49d37c9c1abc'),(47,'josh','Facilities','07123e1f482356c415f684407a3b8723e10b2cbbc0b8fcd6282c49d37c9c1abc'),(48,'machete','User','b791184e1d1274694794552e3ac4352249700bf2ec2b1a069ac64e9142d09173'),(51,'eksay3','Supervisor','07123e1f482356c415f684407a3b8723e10b2cbbc0b8fcd6282c49d37c9c1abc'),(52,'ruddy3','Security','cb593e374cd323a4d435c952c96e7a1e3127bf710a1b2c4d53cd63e6fa79daaf'),(53,'anosh','Activities','fe29ba93264a12414600624d41c6508ac1417ae3cd5a61dd94a96c0c7fb76125'),(54,'anoos','Activities','12e90b8e74f20fc0a7274cff9fcbae14592db12292757f1ea0d7503d30799fd2');
/*!40000 ALTER TABLE `management_committee` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notifications`
--

DROP TABLE IF EXISTS `notifications`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notifications` (
  `notification_id` int NOT NULL AUTO_INCREMENT,
  `message` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`notification_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notifications`
--

LOCK TABLES `notifications` WRITE;
/*!40000 ALTER TABLE `notifications` DISABLE KEYS */;
/*!40000 ALTER TABLE `notifications` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parking_demand`
--

DROP TABLE IF EXISTS `parking_demand`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parking_demand` (
  `flat_no` int NOT NULL,
  `num_vehicles` int NOT NULL,
  PRIMARY KEY (`flat_no`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parking_demand`
--

LOCK TABLES `parking_demand` WRITE;
/*!40000 ALTER TABLE `parking_demand` DISABLE KEYS */;
/*!40000 ALTER TABLE `parking_demand` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `check_parking_availability` AFTER INSERT ON `parking_demand` FOR EACH ROW BEGIN
    DECLARE latest_flat_no INT;
    DECLARE requested_vehicles INT;
    DECLARE available_spots INT;

    
    SELECT flat_no, num_vehicles INTO latest_flat_no, requested_vehicles
    FROM parking_demand
    ORDER BY flat_no DESC
    LIMIT 1;

    
    SELECT COUNT(*) INTO available_spots
    FROM available_parking
    WHERE availability = 'Available';

    
    IF available_spots >= requested_vehicles THEN
        
        UPDATE available_parking
        SET availability = 'Unavailable'
        WHERE availability = 'Available'
        LIMIT requested_vehicles;
    ELSE
        
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Not enough parking spots available for this request';
    END IF;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Dumping events for database 'dbmsfinalpromise'
--

--
-- Dumping routines for database 'dbmsfinalpromise'
--
/*!50003 DROP PROCEDURE IF EXISTS `add_facility_request` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `add_facility_request`(IN facility_name VARCHAR(255), IN flat_no INT, IN request_date DATE)
BEGIN
    DECLARE demand_count INT;

    
    INSERT INTO facility_demand (facility_name, flat_no, request_date)
    VALUES (facility_name, flat_no, request_date);

    
    SELECT COUNT(*) INTO demand_count
    FROM facility_demand
    WHERE facility_name = facility_name;

    
    IF demand_count > 5 THEN
        INSERT INTO notifications (message, recipient_role)
        VALUES (CONCAT('High demand for ', facility_name, ': ', demand_count, ' requests'), 'Supervisor');
    END IF;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `CalculateAverageSalaryByRole` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `CalculateAverageSalaryByRole`()
BEGIN
    SELECT 
        description,
        COUNT(*) as instructor_count,
        MIN(salary) as min_salary,
        MAX(salary) as max_salary,
        AVG(salary) as avg_salary,
        SUM(salary) as total_cost
    FROM instructor
    GROUP BY description
    ORDER BY avg_salary DESC;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `create_user` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = cp850 */ ;
/*!50003 SET character_set_results = cp850 */ ;
/*!50003 SET collation_connection  = cp850_general_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `create_user`(
    IN input_name VARCHAR(50),
    IN input_role ENUM('Supervisor', 'Activities'),
    IN input_password VARCHAR(50)
)
BEGIN
    DECLARE hashed_password VARCHAR(255);
    
    
    SET hashed_password = SHA2(input_password, 256);
    
    
    INSERT INTO management_committee (name, role, password_hash)
    VALUES (input_name, input_role, hashed_password);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-11-21 21:01:02
