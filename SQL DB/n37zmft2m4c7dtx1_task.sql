-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: cvktne7b4wbj4ks1.chr7pe7iynqr.eu-west-1.rds.amazonaws.com    Database: n37zmft2m4c7dtx1
-- ------------------------------------------------------
-- Server version	8.0.35

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
SET @MYSQLDUMP_TEMP_LOG_BIN = @@SESSION.SQL_LOG_BIN;
SET @@SESSION.SQL_LOG_BIN= 0;

--
-- GTID state at the beginning of the backup 
--

SET @@GLOBAL.GTID_PURGED=/*!80000 '+'*/ '';

--
-- Table structure for table `task`
--

DROP TABLE IF EXISTS `task`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `task` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `description` text NOT NULL,
  `date_created` datetime DEFAULT NULL,
  `hours_allocated` int NOT NULL,
  `status` varchar(20) NOT NULL,
  `hours_remaining` int NOT NULL,
  `assigned_to` int DEFAULT NULL,
  `created_by` int NOT NULL,
  `project_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `assigned_to` (`assigned_to`),
  KEY `created_by` (`created_by`),
  KEY `project_id` (`project_id`),
  CONSTRAINT `task_ibfk_1` FOREIGN KEY (`assigned_to`) REFERENCES `user` (`id`),
  CONSTRAINT `task_ibfk_2` FOREIGN KEY (`created_by`) REFERENCES `user` (`id`),
  CONSTRAINT `task_ibfk_3` FOREIGN KEY (`project_id`) REFERENCES `projects` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `task`
--

LOCK TABLES `task` WRITE;
/*!40000 ALTER TABLE `task` DISABLE KEYS */;
INSERT INTO `task` VALUES (4,'Create Python Project Folder','Include template and static folder.. Include forms.py, routes.py, models.py and run.py\r\nAs a user, admin I need ti be able to run the task management app locally','2024-12-19 11:12:04',2,'Completed',0,1,1,10),(6,'Create Routes Endpoints','As an admin I need to be able to CRUD tasks and projects. I also need to be able to manage user security roles.  Additionally, I need to be able to update my username and email\r\nAs a user I need to be able to CRU tasks and project. Additionally, I need to be able to update my username and email in my profile.','2024-12-19 11:28:46',10,'Completed',0,1,1,10),(7,'Create Routes Endpoint for Sprints','Removed as complications arose and prioritization was lowered','2024-12-19 11:29:56',3,'Removed',3,1,1,10),(8,'Create User, Task and Project table','Create tables in MySQL','2024-12-19 11:34:32',1,'Completed',0,4,1,10),(9,'Host Task Management App','Download Heroku\r\nCreate an account/ login\r\nCreate git repository\r\nAd a Procfile into your project folder root\r\nMake sure requirements.txt are included to download dependencies\r\nDeploy to heroku - (bash Windows)\r\ngit add .\r\ngit commit -m \"Title of migration\"\r\ngit push heroku master\r\n\r\nTo view logs - heroku --tail\r\n','2024-12-19 11:37:16',5,'Completed',0,1,1,10),(10,'Test Task Management App (user)','Test following features - \r\nFiltering tasks\r\nCreating tasks\r\nEditing tasks\r\nCreate Projects\r\nEdit Projects\r\nView Profile\r\nEdit Profile','2024-12-19 11:38:23',9,'In Progress',4,6,1,10),(11,'Test Task Management App (admin)','Test the following feature - \r\nFiltering tasks\r\nCreating tasks\r\nEditing tasks\r\nDelete Tasks\r\nCreate Projects\r\nEdit Projects\r\nDelete Projects\r\nView Profile\r\nEdit Profile\r\nManage user roles','2024-12-19 11:39:04',10,'In Progress',4,5,1,10),(12,'Create Sprint Table','Create Sprint Table in MySQL','2024-12-19 11:40:07',1,'Removed',1,1,1,10),(17,'Create Power Platform Model-Driven App','Create model driven app','2024-12-20 00:18:50',4,'New',4,4,1,14),(18,'Create Power BI Dashboard','Create dashboard to visualise companion/cleaners attendance individually and as a group','2024-12-20 00:20:03',2,'Completed',0,1,1,14);
/*!40000 ALTER TABLE `task` ENABLE KEYS */;
UNLOCK TABLES;
SET @@SESSION.SQL_LOG_BIN = @MYSQLDUMP_TEMP_LOG_BIN;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-12-20  0:38:12
