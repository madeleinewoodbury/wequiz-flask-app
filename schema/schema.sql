-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: db
-- Generation Time: Apr 09, 2023 at 11:29 PM
-- Server version: 10.11.2-MariaDB-1:10.11.2+maria~ubu2204
-- PHP Version: 8.1.15

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `webquiz`
--
DROP TABLE IF EXISTS Answer;
DROP TABLE IF EXISTS UserQuiz;
DROP TABLE IF EXISTS Choice;
DROP TABLE IF EXISTS QuizQuestion;
DROP TABLE IF EXISTS Question;
DROP TABLE IF EXISTS Quiz;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS UserRole;

--
-- Table structure for table `Answer`
--

CREATE TABLE `Answer` (
  `user_quiz` varchar(45) NOT NULL,
  `question` varchar(45) NOT NULL,
  `content` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Answer`
--

INSERT INTO `Answer` (`user_quiz`, `question`, `content`) VALUES
('4137d821-0b59-477f-9ce4-a4bd92434315', '113b1337-a368-40cd-9720-521de805808d', 'Prepared statements'),
('4137d821-0b59-477f-9ce4-a4bd92434315', '559cde55-ba34-487d-a8c7-0a0229778ee7', 'Det beregnes en hash av alle hidden input verdier i skjemaet og disse\r\nverifiseres ved innsending av skjema'),
('4137d821-0b59-477f-9ce4-a4bd92434315', 'ccdb2ab9-6117-4de1-8879-f97cd526ac5a', 'SQL injection');

-- --------------------------------------------------------

--
-- Table structure for table `Category`
--

CREATE TABLE `Category` (
  `name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Category`
--

INSERT INTO `Category` (`name`) VALUES
('Databaser'),
('Diverse'),
('Fysikk'),
('Geografi'),
('Historie'),
('Kjemi'),
('Kultur'),
('Programmering');

-- --------------------------------------------------------

--
-- Table structure for table `Choice`
--

CREATE TABLE `Choice` (
  `id` varchar(45) NOT NULL,
  `question` varchar(45) NOT NULL,
  `content` varchar(255) DEFAULT NULL,
  `is_correct` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Choice`
--

INSERT INTO `Choice` (`id`, `question`, `content`, `is_correct`) VALUES
('0c98a12c-c52d-4832-b9ee-9bfb240a9ace', '2bb5bd14-cdc8-4440-a7d6-5e9b6d1e8bae', 'HyperText Markup Language', 1),
('18667516-5c64-4be2-8b29-39f0eb80bfa3', '6ae19e92-0023-457a-a064-45d72f7d0d20', '70 år', 1),
('1b1a6487-16b6-4c22-93f6-075e57b39d46', 'f3be0bbc-1be9-400d-9030-26cac9572ffd', 'Månelandingen', 0),
('1c3f5fae-61b1-45e4-b484-f37a6005f06e', 'f3be0bbc-1be9-400d-9030-26cac9572ffd', 'Prins Harry ble født', 0),
('1cba5b46-4e48-42f2-abcb-703f70389f16', '7de91ceb-6595-4dda-9dbd-b002ae1990ae', 'etter vann', 1),
('1e6237e9-80ff-4dd8-aba2-d36c53be924b', '559cde55-ba34-487d-a8c7-0a0229778ee7', 'Det kan settes en token som et hidden input felt i skjema og denne vil\r\nverifisere ved innsending av skjema', 1),
('1f553cea-4d4f-4187-b015-d218b756cc7e', 'ba6a732d-1759-4299-b25f-2b164a9e1d35', 'Nitrogen', 1),
('20676ed4-0829-46ed-a963-53931030e197', 'ba6a732d-1759-4299-b25f-2b164a9e1d35', 'Argon', 0),
('239fbf61-5d32-455b-9ed0-5356a60aa3f7', 'b6f1d743-435a-48a0-abd6-8786ca8d6888', 'Verona', 1),
('27c8b340-9919-4f7c-b13c-5c86e9923a8f', 'ccdb2ab9-6117-4de1-8879-f97cd526ac5a', 'XSS', 1),
('3262bde7-c167-4e05-87e8-763d6495b6c8', 'b6f1d743-435a-48a0-abd6-8786ca8d6888', 'Napoli', 0),
('35f593fb-232c-4eb7-93ef-40d74c90fc6a', 'ba6a732d-1759-4299-b25f-2b164a9e1d35', 'Vanndamp', 0),
('3cc52925-cf70-4fd1-be78-11a46f2d1d26', '59836f43-8e05-419a-b698-edc6b4e2cd25', 'Italia', 1),
('3cd9789b-4855-41e8-ac19-00d4b22338f0', '559cde55-ba34-487d-a8c7-0a0229778ee7', 'All input vaskes ved hjelp av Flask.escape()', 0),
('41698259-41b2-4947-97c5-32b1a6b42296', 'b6f1d743-435a-48a0-abd6-8786ca8d6888', 'Roma', 0),
('4ef25f29-6b2a-4fd6-822a-5d1148d02a1f', '2bb5bd14-cdc8-4440-a7d6-5e9b6d1e8bae', 'HyperTransfer Media Language', 0),
('53f11b1d-5a06-4bd6-bee1-a643789d6530', '362c2876-01e2-407f-8114-c323b6ed132a', 'Amman', 0),
('5731dbdc-7efe-4ab8-a730-1b5502eb4051', 'ccdb2ab9-6117-4de1-8879-f97cd526ac5a', 'XSRF', 0),
('6247fe7c-4409-4ed7-ae4f-4363c3b80322', '59836f43-8e05-419a-b698-edc6b4e2cd25', 'Polen', 0),
('710aed76-47d3-46ec-bd4c-b59e4146a1fb', 'f3be0bbc-1be9-400d-9030-26cac9572ffd', 'Berlinmuren falt', 1),
('7678237f-0953-4ff7-92a7-8abf74111b05', '59836f43-8e05-419a-b698-edc6b4e2cd25', 'Belgia', 0),
('76f0e533-1964-48fb-b3fd-26775c57fcf1', '2bb5bd14-cdc8-4440-a7d6-5e9b6d1e8bae', 'Human Text Markup Language', 0),
('794f5b86-5d09-49fa-a42e-02de2b847f61', 'ccdb2ab9-6117-4de1-8879-f97cd526ac5a', 'SQL injection', 0),
('854f6114-98b7-4476-b866-5350fcdd6bbb', '250e1ddc-3bc0-4286-91a3-9cc40b530013', 'Månelandingen', 0),
('96c84a3c-c3fb-4b65-93a2-6e35f532ad5a', '250e1ddc-3bc0-4286-91a3-9cc40b530013', 'Attentatet på John F. Kennedy', 0),
('9aa96d94-888d-4861-a49e-f2d5e0b16c16', '250e1ddc-3bc0-4286-91a3-9cc40b530013', 'Bombingen av Hiroshima', 0),
('a3731935-d42a-40de-9d68-043730e4070f', 'ccdb2ab9-6117-4de1-8879-f97cd526ac5a', 'Phishing', 0),
('a71033f4-8778-4083-9e55-254002f13c69', '559cde55-ba34-487d-a8c7-0a0229778ee7', 'Det beregnes en hash av alle hidden input verdier i skjemaet og disse\r\nverifiseres ved innsending av skjema', 0),
('ab0d5152-2179-4baa-a170-d2fefb62afed', '2bb5bd14-cdc8-4440-a7d6-5e9b6d1e8bae', 'High Transfer Modifying Language', 0),
('abd2d853-70f7-470b-a080-7ba63b429f8c', '6ae19e92-0023-457a-a064-45d72f7d0d20', '65 år', 0),
('b025f77f-bdec-467e-892e-f97d6f5a8f86', '113b1337-a368-40cd-9720-521de805808d', 'Prepared statements', 1),
('b83be58e-6055-493b-ac32-df867f303971', '362c2876-01e2-407f-8114-c323b6ed132a', 'Jerevan', 1),
('bdcae997-7c17-4c45-8276-3a4eb94b61eb', '6ae19e92-0023-457a-a064-45d72f7d0d20', '80 år', 0),
('be2bae20-8931-4bff-90ca-69c92dc2cf2f', 'b6f1d743-435a-48a0-abd6-8786ca8d6888', 'Venzia', 0),
('c09bdb67-4430-4ca9-8234-86f8daff4549', '362c2876-01e2-407f-8114-c323b6ed132a', 'Tbilisi', 0),
('c11f7b1c-10cb-4c70-bb20-e67d231b4ff8', '6ae19e92-0023-457a-a064-45d72f7d0d20', '60 år', 0),
('c514a43f-9fe3-46ac-9a1a-622d20165732', 'f3be0bbc-1be9-400d-9030-26cac9572ffd', 'Watergate skandalen', 0),
('cb5a804f-7978-481a-9eb9-0a0c878d5732', '59836f43-8e05-419a-b698-edc6b4e2cd25', 'Østerrike', 0),
('cd3f6531-92c8-4300-9951-329fb5c7b4bd', '6ae19e92-0023-457a-a064-45d72f7d0d20', '75 år', 0),
('cfeb3da5-f23b-4656-a6c9-dfc8c8d8fb22', '250e1ddc-3bc0-4286-91a3-9cc40b530013', 'Angrepet på Pearl Harbor', 1),
('d10a89ab-0bd6-4b1c-be38-b573f057112b', '362c2876-01e2-407f-8114-c323b6ed132a', 'Baku', 0),
('d8178fc8-4256-4950-8e1d-94b1840e314d', 'ba6a732d-1759-4299-b25f-2b164a9e1d35', 'Oksygen', 0),
('de7273d3-956f-482e-a7a3-5d3910dbed68', '559cde55-ba34-487d-a8c7-0a0229778ee7', 'All output vaskes ved hjelp av Jinja2 template systemet', 0),
('ebc68217-570a-4c8a-b118-68af836469ed', '59836f43-8e05-419a-b698-edc6b4e2cd25', 'Frankrike', 0),
('ed3458c8-91fb-45c5-a98e-1e0e87d5d8b5', 'b6f1d743-435a-48a0-abd6-8786ca8d6888', 'Firenze', 0);

-- --------------------------------------------------------

--
-- Table structure for table `Question`
--

CREATE TABLE `Question` (
  `id` varchar(45) NOT NULL,
  `category` varchar(45) DEFAULT NULL,
  `content` varchar(255) DEFAULT NULL,
  `is_multiple_choice` tinyint(4) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Question`
--

INSERT INTO `Question` (`id`, `category`, `content`, `is_multiple_choice`) VALUES
('113b1337-a368-40cd-9720-521de805808d', 'Databaser', 'Hvilke metoder kan benyttes for beskyttelse mot SQL injection?', 0),
('250e1ddc-3bc0-4286-91a3-9cc40b530013', 'Historie', 'Hva skjedde den 7. desember 1941?', 1),
('2bb5bd14-cdc8-4440-a7d6-5e9b6d1e8bae', 'Programmering', 'Hva står HTML for?', 1),
('362c2876-01e2-407f-8114-c323b6ed132a', 'Geografi', 'Hva heter hovedstaden i Armenia?', 1),
('559cde55-ba34-487d-a8c7-0a0229778ee7', 'Databaser', 'Flask Python har god støtte for XSRF beskyttelse, hva innebærer dette?', 1),
('59836f43-8e05-419a-b698-edc6b4e2cd25', 'Geografi', 'Hvilke land grenser IKKE til Tyskland?', 1),
('6ae19e92-0023-457a-a064-45d72f7d0d20', 'Historie', 'Hvor mange år satt dronning Elizabeth II av Storbritannia på tronen?', 1),
('7de91ceb-6595-4dda-9dbd-b002ae1990ae', 'Diverse', 'Hvordan fortsetter dette ordtaket:\r\n\"Over bekken...\"', 0),
('b6f1d743-435a-48a0-abd6-8786ca8d6888', 'Kultur', 'I hvilken italiensk by utspiller Shakespeares tragedie \"Romeo og Julie\" seg?', 1),
('ba6a732d-1759-4299-b25f-2b164a9e1d35', 'Kjemi', 'Hvilken gass finnes det mest av i jordens atmosfære?', 1),
('ccdb2ab9-6117-4de1-8879-f97cd526ac5a', 'Programmering', 'Hvilken type angrep kan få kjørt skript i brukerens nettleser, stjele brukerens sesjon og sende brukeren til falske nettsider?', 1),
('f3be0bbc-1be9-400d-9030-26cac9572ffd', 'Historie', 'Hva skjedde natten mellom torsdag 9. november og 10. november 1989?', 1);

-- --------------------------------------------------------

--
-- Table structure for table `Quiz`
--

CREATE TABLE `Quiz` (
  `id` varchar(45) NOT NULL,
  `title` varchar(45) NOT NULL,
  `is_active` tinyint(4) DEFAULT 0,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `Quiz`
--

INSERT INTO `Quiz` (`id`, `title`, `is_active`, `created_at`) VALUES
('ba3c02cc-03f9-46b2-b6fc-7f8fe2768b90', 'Hva skjedde når...?', 0, '2023-04-09 23:25:21'),
('d5a78d5b-c59a-4401-a182-83377535e430', 'Websikkerhet', 1, '2023-04-09 23:18:06'),
('fb3f8735-8a31-4ee9-a4eb-428d46622282', 'Påskequiz', 1, '2023-04-09 23:07:39');

-- --------------------------------------------------------

--
-- Table structure for table `QuizQuestion`
--

CREATE TABLE `QuizQuestion` (
  `quiz` varchar(45) NOT NULL,
  `question` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `QuizQuestion`
--

INSERT INTO `QuizQuestion` (`quiz`, `question`) VALUES
('ba3c02cc-03f9-46b2-b6fc-7f8fe2768b90', '250e1ddc-3bc0-4286-91a3-9cc40b530013'),
('ba3c02cc-03f9-46b2-b6fc-7f8fe2768b90', 'f3be0bbc-1be9-400d-9030-26cac9572ffd'),
('d5a78d5b-c59a-4401-a182-83377535e430', '113b1337-a368-40cd-9720-521de805808d'),
('d5a78d5b-c59a-4401-a182-83377535e430', '559cde55-ba34-487d-a8c7-0a0229778ee7'),
('d5a78d5b-c59a-4401-a182-83377535e430', 'ccdb2ab9-6117-4de1-8879-f97cd526ac5a'),
('fb3f8735-8a31-4ee9-a4eb-428d46622282', '362c2876-01e2-407f-8114-c323b6ed132a'),
('fb3f8735-8a31-4ee9-a4eb-428d46622282', '6ae19e92-0023-457a-a064-45d72f7d0d20'),
('fb3f8735-8a31-4ee9-a4eb-428d46622282', '7de91ceb-6595-4dda-9dbd-b002ae1990ae'),
('fb3f8735-8a31-4ee9-a4eb-428d46622282', 'b6f1d743-435a-48a0-abd6-8786ca8d6888'),
('fb3f8735-8a31-4ee9-a4eb-428d46622282', 'ba6a732d-1759-4299-b25f-2b164a9e1d35');

-- --------------------------------------------------------

--
-- Table structure for table `User`
--

CREATE TABLE `User` (
  `id` varchar(45) NOT NULL,
  `role` varchar(45) NOT NULL DEFAULT 'Bruker',
  `firstname` varchar(50) DEFAULT NULL,
  `lastname` varchar(50) DEFAULT NULL,
  `email` varchar(50) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `User`
--

INSERT INTO `User` (`id`, `role`, `firstname`, `lastname`, `email`, `password`, `created_at`) VALUES
('33ce1c93-6fa7-44a9-b658-320dc7641dc6', 'Bruker', 'Kari', 'Olsen', 'k.olsen@epost.com', 'pbkdf2:sha256:260000$piOrCL27PwpASt0A$aa2e77ef3c498b75853fc416c0aff5234cc36eb47edf5264819eb67caf00f562', '2023-04-10 03:32:24'),
('b14236cd-9423-4f67-aa5a-0ba99e02b99e', 'Administrator', 'Teodor', 'Nilsen', 't.nilsen@epost.no', 'pbkdf2:sha256:260000$dUWB8dZ0szqipij8$13e9480aa94710440090e6bfec5157eaaac8284b03c429b2189f6a9ab91a978a', '2023-04-09 23:05:12');

-- --------------------------------------------------------

--
-- Table structure for table `UserQuiz`
--

CREATE TABLE `UserQuiz` (
  `id` varchar(45) NOT NULL,
  `quiz` varchar(45) NOT NULL,
  `user` varchar(45) NOT NULL,
  `date_taken` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `UserQuiz`
--

INSERT INTO `UserQuiz` (`id`, `quiz`, `user`, `date_taken`) VALUES
('4137d821-0b59-477f-9ce4-a4bd92434315', 'd5a78d5b-c59a-4401-a182-83377535e430', '33ce1c93-6fa7-44a9-b658-320dc7641dc6', '2023-04-10 03:51:15');

-- --------------------------------------------------------

--
-- Table structure for table `UserRole`
--

CREATE TABLE `UserRole` (
  `name` varchar(45) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `UserRole`
--

INSERT INTO `UserRole` (`name`) VALUES
('Administrator'),
('Bruker');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Answer`
--
ALTER TABLE `Answer`
  ADD PRIMARY KEY (`user_quiz`,`question`),
  ADD KEY `question` (`question`);

--
-- Indexes for table `Category`
--
ALTER TABLE `Category`
  ADD PRIMARY KEY (`name`);

--
-- Indexes for table `Choice`
--
ALTER TABLE `Choice`
  ADD PRIMARY KEY (`id`),
  ADD KEY `question` (`question`);

--
-- Indexes for table `Question`
--
ALTER TABLE `Question`
  ADD PRIMARY KEY (`id`),
  ADD KEY `category` (`category`);

--
-- Indexes for table `Quiz`
--
ALTER TABLE `Quiz`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `QuizQuestion`
--
ALTER TABLE `QuizQuestion`
  ADD PRIMARY KEY (`quiz`,`question`),
  ADD KEY `question` (`question`);

--
-- Indexes for table `User`
--
ALTER TABLE `User`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `role` (`role`);

--
-- Indexes for table `UserQuiz`
--
ALTER TABLE `UserQuiz`
  ADD PRIMARY KEY (`id`),
  ADD KEY `quiz` (`quiz`),
  ADD KEY `user` (`user`);

--
-- Indexes for table `UserRole`
--
ALTER TABLE `UserRole`
  ADD PRIMARY KEY (`name`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Answer`
--
ALTER TABLE `Answer`
  ADD CONSTRAINT `Answer_ibfk_1` FOREIGN KEY (`user_quiz`) REFERENCES `UserQuiz` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `Answer_ibfk_2` FOREIGN KEY (`question`) REFERENCES `Question` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `Choice`
--
ALTER TABLE `Choice`
  ADD CONSTRAINT `Choice_ibfk_1` FOREIGN KEY (`question`) REFERENCES `Question` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `Question`
--
ALTER TABLE `Question`
  ADD CONSTRAINT `Question_ibfk_1` FOREIGN KEY (`category`) REFERENCES `Category` (`name`);

--
-- Constraints for table `QuizQuestion`
--
ALTER TABLE `QuizQuestion`
  ADD CONSTRAINT `QuizQuestion_ibfk_1` FOREIGN KEY (`quiz`) REFERENCES `Quiz` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `QuizQuestion_ibfk_2` FOREIGN KEY (`question`) REFERENCES `Question` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `User`
--
ALTER TABLE `User`
  ADD CONSTRAINT `User_ibfk_1` FOREIGN KEY (`role`) REFERENCES `UserRole` (`name`);

--
-- Constraints for table `UserQuiz`
--
ALTER TABLE `UserQuiz`
  ADD CONSTRAINT `UserQuiz_ibfk_1` FOREIGN KEY (`quiz`) REFERENCES `Quiz` (`id`),
  ADD CONSTRAINT `UserQuiz_ibfk_2` FOREIGN KEY (`user`) REFERENCES `User` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
