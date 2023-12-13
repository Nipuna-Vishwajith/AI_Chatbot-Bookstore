-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 13, 2023 at 07:17 PM
-- Server version: 10.4.24-MariaDB
-- PHP Version: 8.1.6

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `book_orders`
--

-- --------------------------------------------------------

--
-- Table structure for table `complete_orders`
--

CREATE TABLE `complete_orders` (
  `id` int(11) NOT NULL,
  `book_id` int(11) DEFAULT NULL,
  `telephone_number` varchar(255) DEFAULT NULL,
  `username` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `complete_orders`
--

INSERT INTO `complete_orders` (`id`, `book_id`, `telephone_number`, `username`) VALUES
(1, 3, '105', 'all'),
(2, 10, '104', '0744444444'),
(3, 107, '0777777777', 'dfdf'),
(8, 113, '0777777777', '1234'),
(9, 111, '0777777777', 'now'),
(10, 105, '0775505502', 'Hai'),
(11, 110, '0754404401', 'Nipuna'),
(12, 105, '0744444444', 'nipuna'),
(13, 108, '0774444444', 'hjhjhjh'),
(14, 110, '0755555555', 'kavindu'),
(15, 110, '0711111111', 'Nipuna'),
(16, 102, '0744444444', '1234'),
(17, 102, '0745555555', '145'),
(18, 108, '0788989899', 'Nipuna'),
(19, 108, '0744545456', 'Nipuna'),
(20, 102, '0784545654', 'Nipuna'),
(21, 101, '0714455456', 'Nipuna');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `book_id` int(11) DEFAULT NULL,
  `telephone_number` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `book_id`, `telephone_number`) VALUES
(2, 106, '0775505503'),
(25, 102, '0784545788');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `complete_orders`
--
ALTER TABLE `complete_orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `complete_orders`
--
ALTER TABLE `complete_orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=27;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
