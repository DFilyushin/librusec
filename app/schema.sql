/*
Library librusec database script
Database - books
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

/*Table structure for table `authors` */

CREATE TABLE `authors` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `first_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `middle_name` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `idxLastName` (`last_name`)
) ENGINE=MyISAM AUTO_INCREMENT=108526 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Table structure for table `books` */

CREATE TABLE `books` (
  `id` bigint(20) NOT NULL,
  `name` text COLLATE utf8_unicode_ci,
  `file_size` int(11) DEFAULT NULL,
  `file_type` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `lang` char(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `genre` text COLLATE utf8_unicode_ci,
  PRIMARY KEY (`id`),
  FULLTEXT KEY `idxBookName` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Table structure for table `genre` */

CREATE TABLE `genre` (
  `id_genre` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `ru_genre` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id_genre`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*Table structure for table `link_ab` */

CREATE TABLE `link_ab` (
  `id_book` bigint(20) NOT NULL,
  `id_author` bigint(20) NOT NULL,
  PRIMARY KEY (`id_author`,`id_book`),
  UNIQUE KEY `PRIMARY2` (`id_book`,`id_author`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
