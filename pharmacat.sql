-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 13, 2022 at 05:53 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 7.4.27

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pharmacat`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `ID` int(11) NOT NULL,
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Full_Name` varchar(255) DEFAULT NULL,
  `Registration_Number` varchar(255) DEFAULT NULL,
  `Contact_Number` bigint(13) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`ID`, `Username`, `Password`, `Email`, `Full_Name`, `Registration_Number`, `Contact_Number`, `Address`) VALUES
(1, 'cha', '$2b$12$cw7m4Oe8mxyqUqqGHjLw/edPuV1E.xy.QEsPCw7PmYbmosuy7aAqi', 'chalie@gmail.com', 'Chalie Lijalem', '1234568', 930564881, 'Adama');

-- --------------------------------------------------------

--
-- Table structure for table `booking`
--

CREATE TABLE `booking` (
  `Record_ID` int(11) NOT NULL,
  `Doctor_ID` int(11) DEFAULT NULL,
  `Patient_ID` int(11) DEFAULT NULL,
  `Date` date DEFAULT NULL,
  `Appointment_Time` time DEFAULT NULL,
  `Status` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `booking`
--

INSERT INTO `booking` (`Record_ID`, `Doctor_ID`, `Patient_ID`, `Date`, `Appointment_Time`, `Status`) VALUES
(33, 2, 1, '2022-06-30', '05:27:00', 1),
(34, 1, 1, '2022-07-04', '06:05:00', 0),
(35, 3, 1, '2022-07-03', '04:28:00', 0),
(36, 2, 1, '2022-07-02', '08:28:00', 0),
(38, 1, 3, '2022-06-30', '02:34:00', 0),
(39, 2, 3, '2022-06-29', '03:20:00', 0),
(40, 4, 3, '2022-06-26', '04:21:00', 0),
(41, 2, 3, '2022-06-29', '07:26:00', 1),
(43, 2, 3, '2022-06-21', '09:35:00', 1);

-- --------------------------------------------------------

--
-- Table structure for table `contactus`
--

CREATE TABLE `contactus` (
  `ID` int(40) NOT NULL,
  `name` varchar(40) NOT NULL,
  `email` varchar(30) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `message` varchar(1000) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `contactus`
--

INSERT INTO `contactus` (`ID`, `name`, `email`, `phone`, `message`) VALUES
(2, 'jhjhkk', 'kljlkl@gmail.com', '15454', 'klkjlkjlm'),
(3, 'dsda', 'ccdhsj@gmail.com', '0930564881', 'sdfasdfxcvzxc dsdfa sfasd xcvzxcv'),
(4, 'fdssf', 'hgfhgf@gmail.com', '0930564881', 'fgsdfgsdfg');

-- --------------------------------------------------------

--
-- Table structure for table `doctors`
--

CREATE TABLE `doctors` (
  `ID` int(11) NOT NULL,
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Full_Name` varchar(255) DEFAULT NULL,
  `Registration_Number` varchar(255) DEFAULT NULL,
  `Contact_Number` bigint(13) DEFAULT NULL,
  `Hospital_Name` varchar(255) DEFAULT NULL,
  `Specialization` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `online` int(11) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `doctors`
--

INSERT INTO `doctors` (`ID`, `Username`, `Password`, `Email`, `Full_Name`, `Registration_Number`, `Contact_Number`, `Hospital_Name`, `Specialization`, `Address`, `online`) VALUES
(1, 'decha', '$2b$12$4bduKke2Y1gC3/FbzY06Re5rOf4.zUp8JWgP/6G.uU7mVwMwmYAzO', 'decha@gmail.com', 'Dr. DECHASA SHIMELIS', '235468', 930564881, '', 'General Physician\r\n', 'Dire Dawa', 0),
(2, 'cha', '$2b$12$N.ZCD8wKGovix3xKrmId1eWzHNO3aCExymQcAwskeN92bSxHDzmPK', 'chalie@gmail.com', 'Dr. CHALIE LIJALEM', '123456', 930564881, '', 'Dermatologist', 'Addis Ababa', 0),
(3, 'ela', '$2b$12$7rnWnIqE6qY/xifjB3VFH.daNxLNSOo6B0vf3Qjl5dTv3tOA65WSG', 'elias@gmail.com', 'Dr. ELIAS MEKUANINT', '1234568', 918309819, '', 'Dermatologist', 'Gonder', 0),
(4, 'madan', '$2b$12$y5c/wmxbX5KIXcYf8sv7uOkSwJPikqRFu1D0AXPUupNGrCWkkVhbu', 'madan@gmail.com', 'Dr. MADAN BESHIR', '1223654', 968073824, '', 'Microbiologist', 'ADAMA', 0),
(5, 'daniss', '$2b$12$moAWnbn44ejraTxNi2ylFOoxPVD2sNGViDi5ueH.c6JK.AwpMB1va', 'dani@gmail.com', 'Dr. DANIEL YENIEW', '123698', 942032794, '', 'Dermatologist', 'BDR', 0);

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `id` int(11) NOT NULL,
  `body` text NOT NULL,
  `msg_by` text NOT NULL,
  `msg_to` text NOT NULL,
  `msg_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`id`, `body`, `msg_by`, `msg_to`, `msg_time`) VALUES
(182, 'Hi Dr Dechasa', 'Chalie Lijalem', 'Dr. DECHASA SHIMELIS', '2022-03-21 21:01:21'),
(183, 'Hi Dr Chalie', 'Chalie Lijalem', 'Dr. CHALIE LIJALEM', '2022-03-21 21:01:58'),
(184, 'Hi Dr Elias', 'Chalie Lijalem', 'Dr. ELIAS MEKUANINT', '2022-03-21 21:02:07'),
(185, 'Hi Dr Madan', 'Chalie Lijalem', 'Dr. MADAN BESHIR', '2022-03-21 21:02:18'),
(186, 'Hi Dr Daniel', 'Chalie Lijalem', 'Dr. DANIEL YENIEW', '2022-03-21 21:02:32'),
(187, 'Hi chacha', 'Dr. CHALIE LIJALEM', 'Chalie Lijalem', '2022-03-22 18:01:45'),
(188, 'How are you dr?', 'Chalie Lijalem', 'Dr. CHALIE LIJALEM', '2022-03-22 18:02:10'),
(189, 'I\'m fine. Is there any thing can I help you', 'Dr. CHALIE LIJALEM', 'Chalie Lijalem', '2022-03-22 18:02:41'),
(214, 'tttt', 'Dr. CHALIE LIJALEM', 'Elias Mekuanint', '2022-05-23 07:55:55'),
(213, 'hhh', 'Dr. CHALIE LIJALEM', 'Dechassa Shimels', '2022-05-23 07:55:49'),
(212, 'hi', 'Dr. CHALIE LIJALEM', 'Chalie Lijalem', '2022-05-23 07:41:13'),
(209, 'hi', 'Chalie Lijalem', 'Dr. DECHASA SHIMELIS', '2022-04-19 10:14:00'),
(194, 'how are', 'Dr. DECHASA SHIMELIS', 'Chalie Lijalem', '2022-03-24 18:21:00'),
(210, 'frvgtvg', 'Chalie Lijalem', 'Dr. DECHASA SHIMELIS', '2022-04-19 11:09:42'),
(196, 'ghdjhqsgjh', 'Chalie Lijalem', 'Dr. ELIAS MEKUANINT', '2022-03-24 18:21:26'),
(197, 'gfsgashd', 'Chalie Lijalem', 'Dr. MADAN BESHIR', '2022-03-24 18:21:31'),
(219, 'dasdhajs', 'Elias Mekuanint', 'Dr. MADAN BESHIR', '2022-06-11 20:58:49'),
(216, 'dadaa', 'Elias Mekuanint', 'Dr. CHALIE LIJALEM', '2022-05-25 21:15:06'),
(217, 'mdkajsdkaj', 'Elias Mekuanint', 'Dr. CHALIE LIJALEM', '2022-06-11 20:58:40'),
(218, 'sdahskdj', 'Elias Mekuanint', 'Dr. ELIAS MEKUANINT', '2022-06-11 20:58:45'),
(211, 'gggg', 'Dr. DECHASA SHIMELIS', 'Chalie Lijalem', '2022-04-19 11:09:58'),
(204, 'hjdfgsdjh', 'Dr. CHALIE LIJALEM', 'Dr. ELIAS MEKUANINT', '2022-04-19 06:52:09'),
(205, 'hwegjhwe', 'Dr. CHALIE LIJALEM', 'Dr. MADAN BESHIR', '2022-04-19 06:52:17'),
(220, 'dsjdhgasj', 'Elias Mekuanint', 'Dr. DANIEL YENIEW', '2022-06-11 20:58:54'),
(221, 'hi decha negn', 'Elias Mekuanint', 'Dr. CHALIE LIJALEM', '2022-06-11 20:59:08'),
(222, 'dfsdfs', 'Chalie Lijalem', 'Dr. CHALIE LIJALEM', '2022-06-13 00:15:36'),
(223, 'gfsdfg', 'Chalie Lijalem', 'Dr. DANIEL YENIEW', '2022-06-13 00:15:45');

-- --------------------------------------------------------

--
-- Table structure for table `recommendations`
--

CREATE TABLE `recommendations` (
  `id` int(11) NOT NULL,
  `body` text NOT NULL,
  `recommend_by` text NOT NULL,
  `recommend_to` text NOT NULL,
  `recommend_time` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=MyISAM DEFAULT CHARSET=latin1;

--
-- Dumping data for table `recommendations`
--

INSERT INTO `recommendations` (`id`, `body`, `recommend_by`, `recommend_to`, `recommend_time`) VALUES
(14, 'rrrrrrrrr', 'Dr. CHALIE LIJALEM', 'Chalie Lijalem', '2022-05-23 07:48:44'),
(13, 'dhfdjhaf', 'Dr. CHALIE LIJALEM', 'Chalie Lijalem', '2022-05-20 06:56:29'),
(3, 'sahjkdashd', 'Dr. CHALIE LIJALEM', 'Elias Mekuanint', '2022-05-15 19:21:43'),
(2, 'decha', 'Dr. CHALIE LIJALEM', 'Dechassa Shimels', '2022-05-15 19:21:36'),
(1, 'cha', 'Dr. CHALIE LIJALEM', 'Chalie Lijalem', '2022-05-15 19:20:08'),
(15, 'dsfd', 'Dr. CHALIE LIJALEM', 'Chalie Lijalem', '2022-06-13 06:01:34'),
(16, 'fsdfsd', 'Dr. CHALIE LIJALEM', 'Elias Mekuanint', '2022-06-13 06:01:38'),
(17, 'f08794ad-6708-4507-ab7d-0de16f79a002', 'Dr. CHALIE LIJALEM', 'Elias Mekuanint', '2022-06-13 12:37:46'),
(18, 'd9d834a3-1af0-45d4-9720-fc9eff9b3b5c', 'Dr. CHALIE LIJALEM', 'Elias Mekuanint', '2022-06-13 12:45:55'),
(19, 'da474d80-be89-45c4-86f8-0c850918a5cb', 'Dr. CHALIE LIJALEM', 'Elias Mekuanint', '2022-06-13 12:47:54');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `ID` int(11) NOT NULL,
  `Username` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `token` varchar(255) DEFAULT NULL,
  `Full_Name` varchar(255) NOT NULL,
  `Address` varchar(255) DEFAULT NULL,
  `Blood_Group` varchar(255) DEFAULT NULL,
  `Age` date DEFAULT NULL,
  `API_Token` varchar(255) DEFAULT NULL,
  `online` int(11) NOT NULL DEFAULT 0,
  `channel` int(15) DEFAULT NULL,
  `temp` int(20) DEFAULT NULL,
  `humi` int(20) DEFAULT NULL,
  `pulse` int(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`ID`, `Username`, `Password`, `Email`, `token`, `Full_Name`, `Address`, `Blood_Group`, `Age`, `API_Token`, `online`, `channel`, `temp`, `humi`, `pulse`) VALUES
(1, 'cha', '$2b$12$PGdIQAMnWnXkYjVn2U5SDu0/.wgMYk8bfjPirRIEVuPGSQNwazNBi', 'chalielijalemnn@gmail.com', '085de30a-a58f-49a6-a691-7473be426811', 'Chalie Lijalem', 'Adama', 'A+', '1999-04-10', 'Y2hhY2hhKH4pY2hh', 0, 1726721, 465135, 465136, 465137),
(2, 'decha', '$2b$12$rF87y4DOEfMcyDmz8M5oWeP9bH.qL6e4yd5WQWdz2/p3W.qw/5.sG', 'dechasashimels95@gmail.com', '848268ff-964b-4c3b-bb34-10490e5eb94a', 'Dechassa Shimels', 'Dire', 'O+', '0000-00-00', 'c2hpbih+KTEyMzQ1', 0, 1725215, 465124, 465125, 465126),
(3, 'ela', '$2b$12$I5W0lb3kUXERC/MqMe3uYuWqcZ4VYoWMIR18DyKQg/irbQ3HR2F5G', 'elias@gmail.com', '', 'Elias Mekuanint', 'Gonder', 'A+', '0000-00-00', 'ZWxpYXMofikxMjM0', 0, 1720545, 465578, 465580, 465581),
(9, 'fdfsdf', '$2b$12$/aC8YzEEXucTz8/sIlo0sOvGIlYKKEfalqxywYUKTkHrmzir5g/Ya', 'dfsd@gmail.com', NULL, 'ffff', 'weqw', 'A+', '2022-05-31', 'ZmRmc2RmKH4pMTIzNA==', 0, 3423, 4666, 999, 9800),
(15, 'dfd', '$2b$12$yob0pdAGc7PoVeD04ONX.enP1Cf8Sh5NHgSuJcjrQep1mpQHLOl2a', 'sdf@gmail.com', NULL, 'derf gt', 'adana', 'A+', '1999-05-10', 'ZGZkKH4pMzIx', 0, 1720545, 465578, 465129, 465130);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `booking`
--
ALTER TABLE `booking`
  ADD PRIMARY KEY (`Record_ID`);

--
-- Indexes for table `contactus`
--
ALTER TABLE `contactus`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `recommendations`
--
ALTER TABLE `recommendations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `booking`
--
ALTER TABLE `booking`
  MODIFY `Record_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=44;

--
-- AUTO_INCREMENT for table `contactus`
--
ALTER TABLE `contactus`
  MODIFY `ID` int(40) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=224;

--
-- AUTO_INCREMENT for table `recommendations`
--
ALTER TABLE `recommendations`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=20;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
