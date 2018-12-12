-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: December 09, 2018 at 02:02 PM
-- Server version: 5.7.14
-- PHP Version: 5.6.25

-- Airline Staff:
-- 1. username: AirlineStaff password: abcd1234

-- Booking Agent:
-- 1. email: Booking@agent.com password: abcd1234

-- Customer:
-- 1. email: Customer@nyu.edu password: abcd1234
-- 2. email: one@nyu.edu password: test
-- 3. email: two@nyu.edu password: test

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `_databases_427`
--

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Emirates');

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`) VALUES
('AirlineStaff', '$pbkdf2-sha256$29000$7B0DYGyttRYiJCRkjJEyBg$TI8Gpk1vuUgiwEhVfP8YhgiNm5mtrVP92qoK27CfwIQ', 'Joe', 'Bland', '1980-02-05', 'Emirates');

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_id`, `seats`) VALUES
('Emirates', 1, 100),
('Emirates', 2, 50),
('Emirates', 3, 75);

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_name`, `airport_city`) VALUES
('JFK', 'New York City'),
('La Guardia', 'New York City'),
('Louisville SDF', 'Louisville'),
('O\'Hare', 'Chicago'),
('SFO', 'San Francisco');

--
-- Dumping data for table `booking_agent`
--

INSERT INTO `booking_agent` (`email`, `password`, `booking_agent_id`) VALUES
('Booking@agent.com', '$pbkdf2-sha256$29000$7B0DYGyttRYiJCRkjJEyBg$TI8Gpk1vuUgiwEhVfP8YhgiNm5mtrVP92qoK27CfwIQ', 1),
('Professional@booking.com', '$pbkdf2-sha256$29000$7B0DYGyttRYiJCRkjJEyBg$TI8Gpk1vuUgiwEhVfP8YhgiNm5mtrVP92qoK27CfwIQ', 2);

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('Customer@nyu.edu', 'Customer', '$pbkdf2-sha256$29000$7B0DYGyttRYiJCRkjJEyBg$TI8Gpk1vuUgiwEhVfP8YhgiNm5mtrVP92qoK27CfwIQ', '2', 'Metrotech', 'New York', 'New York', 51234, 'P123456', '2020-10-24', 'USA', '1990-04-01'),
('one@nyu.edu', 'One', '$pbkdf2-sha256$29000$glDK.f//PyfE2NubU8p5rw$hN9rDv2WOzWnjDwOpdL5wb.i0QScSQvvUq2rdFd8iJM', '6', 'Metrotech', 'New York', 'New York', 59873, 'P53412', '2021-04-05', 'USA', '1990-04-04'),
('two@nyu.edu', 'Two', '$pbkdf2-sha256$29000$glDK.f//PyfE2NubU8p5rw$hN9rDv2WOzWnjDwOpdL5wb.i0QScSQvvUq2rdFd8iJM', '5', 'Metrotech', 'New York', 'New York', 58123, 'P436246', '2027-04-20', 'USA', '1992-04-18');

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES
('Emirates', 139, 'SFO', '2018-12-20 23:50:00', 'JFK', '2018-12-21 08:50:00', '200', 'On Time', 1),
('Emirates', 296, 'O\'Hare', '2019-01-01 12:00:00', 'SFO', '2019-01-01 14:00:00', '420', 'On Time', 1),
('Emirates', 307, 'La Guardia', '2018-12-19 22:00:00', 'SFO', '2018-12-20 02:00:00', '600', 'On Time', 1),
('Emirates', 455, 'JFK', '2018-12-25 05:00:00', 'Louisville SDF', '2018-12-25 07:00:00', '97', 'On Time', 3),
('Emirates', 915, 'O\'Hare', '2018-09-01 00:00:00', 'SFO', '2018-09-01 04:00:00', '500', 'Delayed', 2);

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES
(1, 'Emirates', 139),
(2, 'Emirates', 307),
(3, 'Emirates', 915),
(4, 'Emirates', 915),
(5, 'Emirates', 915),
(6, 'Emirates', 455),
(7, 'Emirates', 455),
(8, 'Emirates', 307),
(9, 'Emirates', 455);


--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES
(1, 'Customer@nyu.edu', NULL, '2018-11-01'),
(2, 'Customer@nyu.edu', 1, '2018-11-17'),
(3, 'one@nyu.edu', 2, '2018-10-10'),
(4, 'two@nyu.edu', 2, '2018-10-11'),
(5, 'Customer@nyu.edu', 1, '2018-09-12'),
(6, 'one@nyu.edu', null, '2018-08-19'),
(7, 'two@nyu.edu', null, '2018-08-23'),
(8, 'one@nyu.edu', 1, '2018-11-15'),
(9, 'Customer@nyu.edu', 1, '2018-06-19');


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
