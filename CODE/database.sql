/*
SQLyog Enterprise - MySQL GUI v6.56
MySQL - 11.3.0-MariaDB : Database - epidemic
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`epidemic` /*!40100 DEFAULT CHARACTER SET latin1 COLLATE latin1_swedish_ci */;

USE `epidemic`;

/*Table structure for table `bookappointment` */

DROP TABLE IF EXISTS `bookappointment`;

CREATE TABLE `bookappointment` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `pname` varchar(200) DEFAULT NULL,
  `pcontact` varchar(200) DEFAULT NULL,
  `paddress` varchar(200) DEFAULT NULL,
  `profile` varchar(200) DEFAULT NULL,
  `pemail` varchar(200) DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `dfb` varchar(200) DEFAULT NULL,
  `age` varchar(200) DEFAULT NULL,
  `fever` varchar(200) DEFAULT NULL,
  `Cough` varchar(200) DEFAULT NULL,
  `breathing` varchar(200) DEFAULT NULL,
  `tiredness` varchar(200) DEFAULT NULL,
  `throat` varchar(200) DEFAULT NULL,
  `Runnynose` varchar(200) DEFAULT NULL,
  `bodypain` varchar(200) DEFAULT NULL,
  `Headache` varchar(200) DEFAULT NULL,
  `Vomiting` varchar(200) DEFAULT NULL,
  `EpidemicSpread` varchar(200) DEFAULT 'pending',
  `status` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `bookappointment` */

insert  into `bookappointment`(`id`,`pname`,`pcontact`,`paddress`,`profile`,`pemail`,`Time`,`Date`,`dfb`,`age`,`fever`,`Cough`,`breathing`,`tiredness`,`throat`,`Runnynose`,`bodypain`,`Headache`,`Vomiting`,`EpidemicSpread`,`status`) values (1,'kumar','9848251256','Nellore','static/profiles/comment_2.png','kumar@gmail.com','10:08:19','2023-12-12','2023-11-15','28','no','Yes','Yes','No','Yes','Yes','No','Yes','Yes','Present','Accepted'),(2,'malli','7896523658','bangalore','static/profiles/comment_1.png','malli@gmail.com','10:09:53','2023-12-12','2023-08-04','26','Yes','No','Yes','No','Yes','Yes','Yes','No','No','Present','Accepted');

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `name` varchar(200) DEFAULT NULL,
  `email` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `contact` varchar(200) DEFAULT NULL,
  `address` varchar(200) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `profile` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `doctor` */

insert  into `doctor`(`id`,`name`,`email`,`password`,`contact`,`address`,`Date`,`Time`,`profile`) values (1,'preeti','preeti@gmail.com','Preeti@123','6589745632','bangalore','2023-12-11','18:20:43','static/profiles/a2.jpg'),(2,'nakku','nakku@gmail.com','Nakku@123','6985748569','tirupati','2023-12-11','18:21:08','static/profiles/7.png');

/*Table structure for table `patient` */

DROP TABLE IF EXISTS `patient`;

CREATE TABLE `patient` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `pname` varchar(200) DEFAULT NULL,
  `pemail` varchar(200) DEFAULT NULL,
  `password` varchar(200) DEFAULT NULL,
  `pcontact` varchar(200) DEFAULT NULL,
  `paddress` varchar(200) DEFAULT NULL,
  `Date` varchar(200) DEFAULT NULL,
  `Time` varchar(200) DEFAULT NULL,
  `profile` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `patient` */

insert  into `patient`(`id`,`pname`,`pemail`,`password`,`pcontact`,`paddress`,`Date`,`Time`,`profile`) values (1,'malli','malli@gmail.com','Malli@123','7896523658','bangalore','2023-12-11','18:16:39','static/profiles/comment_1.png'),(2,'kumar','kumar@gmail.com','Kumar@123','9848251256','Nellore','2023-12-11','18:20:04','static/profiles/comment_2.png');

/*Table structure for table `recovery` */

DROP TABLE IF EXISTS `recovery`;

CREATE TABLE `recovery` (
  `id` int(20) NOT NULL AUTO_INCREMENT,
  `pname` varchar(200) DEFAULT NULL,
  `pcontact` varchar(200) DEFAULT NULL,
  `paddress` varchar(200) DEFAULT NULL,
  `profile` varchar(200) DEFAULT NULL,
  `pemail` varchar(200) DEFAULT NULL,
  `Time` time DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `dfb` varchar(200) DEFAULT NULL,
  `age` varbinary(200) DEFAULT NULL,
  `fever` varchar(200) DEFAULT NULL,
  `Cough` varchar(200) DEFAULT NULL,
  `breathing` varchar(200) DEFAULT NULL,
  `tiredness` varchar(200) DEFAULT NULL,
  `throat` varchar(200) DEFAULT NULL,
  `Runnynose` varchar(200) DEFAULT NULL,
  `bodypain` varchar(200) DEFAULT NULL,
  `Headache` varchar(200) DEFAULT NULL,
  `Vomiting` varchar(200) DEFAULT NULL,
  `EpidemicSpread` varchar(200) DEFAULT 'pending',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 COLLATE=latin1_swedish_ci;

/*Data for the table `recovery` */

insert  into `recovery`(`id`,`pname`,`pcontact`,`paddress`,`profile`,`pemail`,`Time`,`Date`,`dfb`,`age`,`fever`,`Cough`,`breathing`,`tiredness`,`throat`,`Runnynose`,`bodypain`,`Headache`,`Vomiting`,`EpidemicSpread`) values (1,'kumar','9848251256','Nellore','static/profiles/comment_2.png','kumar@gmail.com','10:46:56','2023-12-12','2023-11-15','28','no','Yes','Yes','No','Yes','Yes','No','Yes','Yes','Recovered');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
