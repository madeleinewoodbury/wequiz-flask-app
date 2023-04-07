USE quizApp;
DROP TABLE IF EXISTS Answer;
DROP TABLE IF EXISTS UserQuiz;
DROP TABLE IF EXISTS Choice;
DROP TABLE IF EXISTS QuizQuestion;
DROP TABLE IF EXISTS Question;
DROP TABLE IF EXISTS Quiz;
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Category;
DROP TABLE IF EXISTS UserRole;

CREATE TABLE UserRole (
    name VARCHAR(45) PRIMARY KEY
);

CREATE TABLE Category (
    name VARCHAR(45) PRIMARY KEY
);

INSERT INTO UserRole (name) 
VALUES ('Bruker'), ('Administrator');

INSERT INTO Category (name) 
VALUES ('Databaser'), ('Programmering'), ('Fysikk'), ('Historie'), ('Geografi');

CREATE TABLE User (
    id VARCHAR(45) PRIMARY KEY,
    role VARCHAR(45) NOT NULL DEFAULT 'Bruker',
    firstname VARCHAR(50),
    lastname VARCHAR(50),
    email VARCHAR(50) UNIQUE,
    password VARCHAR(255),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role) REFERENCES UserRole(name)
);

CREATE TABLE Quiz (
    id VARCHAR(45) PRIMARY KEY,
    title VARCHAR(45) NOT NULL,
    is_active TINYINT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE Question (
    id VARCHAR(45) PRIMARY KEY,
    category VARCHAR(45),
    content VARCHAR(255),
    is_multiple_choice TINYINT DEFAULT 0,
    FOREIGN KEY (category) REFERENCES Category(name)
);

CREATE TABLE QuizQuestion (
    quiz VARCHAR(45) NOT NULL,
    question VARCHAR(45) NOT NULL,
    PRIMARY KEY (quiz, question),
    FOREIGN KEY (quiz) REFERENCES Quiz(id) ON DELETE CASCADE,
    FOREIGN KEY (question) REFERENCES Question(id) ON DELETE CASCADE
);

CREATE TABLE Choice (
    id VARCHAR(45) PRIMARY KEY,
    question VARCHAR(45) NOT NULL,
    content VARCHAR(255),
    is_correct TINYINT,
    FOREIGN KEY (question) REFERENCES Question(id) ON DELETE CASCADE
);

CREATE TABLE UserQuiz (
    id VARCHAR(45) PRIMARY KEY,
    quiz VARCHAR(45) NOT NULL,
    user VARCHAR(45) NOT NULL,
    date_taken DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz) REFERENCES Quiz(id),
    FOREIGN KEY (user) REFERENCES User(id)
);

CREATE TABLE Answer (
    user_quiz VARCHAR(45) NOT NULL,
    question VARCHAR(45) NOT NULL,
    content VARCHAR(255),
    PRIMARY KEY (user_quiz, question),
    FOREIGN KEY (user_quiz) REFERENCES UserQuiz(id) ON DELETE CASCADE,
    FOREIGN KEY (question) REFERENCES Question(id) ON DELETE CASCADE
);

INSERT INTO User (id, role, firstname, lastname, email, password)
VALUES
('ad341a5c-84f0-4617-abf2-5b7482a0e457', 'Administrator', 'John', 'Doe', 'jdoe@email.com', 'pbkdf2:sha256:260000$ZnX1SpCHcYEewgS5$35022d1d0b6490c07b3a6672cf86edb6291d35868115b10eeb3a795d31f3e0e6'),
('ba0a424e-8dc7-47e8-97e0-4824d812f4bf', 'Bruker', 'Kari', 'Olsen', 'kari@email.com', 'pbkdf2:sha256:260000$EciEAeMChVWpqVOC$740a34a2a271c7f93cc1ac3c0fc7584ab6458bde256648fd9b36746caace365f');

--
-- Dumping data for table `Quiz`
--

INSERT INTO `Quiz` (`id`, `title`, `is_active`, `created_at`) VALUES
('4e68a8a5-ef11-426b-bdc3-2d0c12c0c338', 'Eurovision 2023', 0, '2023-04-06 14:47:04'),
('89dc5b23-09dc-4d33-af33-b2e340483d4d', 'Bare et spørsmål', 0, '2023-04-06 17:06:49');

--
-- Dumping data for table `Question`
--

INSERT INTO `Question` (`id`, `category`, `content`, `is_multiple_choice`) VALUES
('1148f0bb-e0bf-4799-9b05-15ca2aa7ab48', 'Geografi', 'Hvem skal representere Sverige i 2023?', 1),
('73a8294c-afbc-4c61-99a3-3288b0c987ac', 'Geografi', 'Hvor mange land er med i ESC 2023?', 1),
('afd94689-4672-4051-86d2-5260cd198b1f', 'Geografi', 'Hvor mange land er med i ESC 2023?', 1),
('e2b43992-c2fc-4fec-b378-1fc39a9fbc82', 'Programmering', 'Hvem oppfant Linux?', 0),
('f1e887e9-15dd-4f97-a698-a8cf9b888a49', 'Geografi', 'Hva heter vinnerlåta fra 2022?', 0),
('f6bdc785-5ae1-4184-b93f-88df2e73a501', 'Geografi', 'Hva heter vinnerlåta fra 2022?', 0);


INSERT INTO `QuizQuestion` (`quiz`, `question`) VALUES
('4e68a8a5-ef11-426b-bdc3-2d0c12c0c338', '1148f0bb-e0bf-4799-9b05-15ca2aa7ab48'),
('4e68a8a5-ef11-426b-bdc3-2d0c12c0c338', '73a8294c-afbc-4c61-99a3-3288b0c987ac'),
('4e68a8a5-ef11-426b-bdc3-2d0c12c0c338', 'f1e887e9-15dd-4f97-a698-a8cf9b888a49'),
('89dc5b23-09dc-4d33-af33-b2e340483d4d', 'e2b43992-c2fc-4fec-b378-1fc39a9fbc82');

--
-- Dumping data for table `Choice`
--

INSERT INTO `Choice` (`id`, `question`, `content`, `is_correct`) VALUES
('07e68aaf-e135-4d48-b794-d8c14011573f', '1148f0bb-e0bf-4799-9b05-15ca2aa7ab48', 'Marcus & Martinus', 0),
('1a907407-0875-42ec-ac84-ed3525981aba', 'afd94689-4672-4051-86d2-5260cd198b1f', '40', 0),
('2237fcb8-5434-45c5-954e-3fb4bb895e66', '1148f0bb-e0bf-4799-9b05-15ca2aa7ab48', 'Loreen', 1),
('7b943157-6c77-4c55-a505-92af1d1ee2de', '73a8294c-afbc-4c61-99a3-3288b0c987ac', '38', 0),
('7cea9d5f-d73e-45d6-9d04-e4542fdef773', '73a8294c-afbc-4c61-99a3-3288b0c987ac', '37', 1),
('84c7253b-ba85-4263-9651-ecf90da21ffd', 'f6bdc785-5ae1-4184-b93f-88df2e73a501', 'Stefania', 1),
('85aba95e-3c95-4949-b84a-71a40aecad16', 'e2b43992-c2fc-4fec-b378-1fc39a9fbc82', 'Linus Torvald', 1),
('8855f8be-fc18-478f-9b5c-53f881c4bb92', '73a8294c-afbc-4c61-99a3-3288b0c987ac', '35', 0),
('9ae33c36-bfb3-4460-ab82-f75c6c869f9f', '1148f0bb-e0bf-4799-9b05-15ca2aa7ab48', 'Tone Sekelius', 0),
('a509dd52-87af-44f2-ad9e-3799175c0d4e', '1148f0bb-e0bf-4799-9b05-15ca2aa7ab48', 'Danny Saudedo', 0),
('a7bc3e58-0508-4edc-bebb-b06ffecbd3d5', 'f1e887e9-15dd-4f97-a698-a8cf9b888a49', 'Stefania', 1),
('b85c5cac-bc3b-4ae3-8df9-ed29eb149322', 'afd94689-4672-4051-86d2-5260cd198b1f', '35', 0),
('ed5b816e-1469-45f9-96d4-70ae8f606de5', 'afd94689-4672-4051-86d2-5260cd198b1f', '38', 0),
('f13883ad-7005-4ffe-a374-500f6d3f68f8', 'afd94689-4672-4051-86d2-5260cd198b1f', '37', 1),
('f3226330-8d39-4a89-b6d6-218b68c5bedc', '1148f0bb-e0bf-4799-9b05-15ca2aa7ab48', 'Carola', 0),
('f72db514-acdc-45ab-87d3-7c3dd7b12b65', 'afd94689-4672-4051-86d2-5260cd198b1f', '41', 0),
('ffcefc50-bd14-4e5a-8885-e11954a509ac', '73a8294c-afbc-4c61-99a3-3288b0c987ac', '41', 0);


-- SELECT content, date_taken 
-- FROM Answer
-- INNER JOIN UserQuiz 
-- ON UserQuiz.id = Answer.user_quiz 
-- WHERE question = "1148f0bb-e0bf-4799-9b05-15ca2aa7ab48";


-- SELECT 
--     Q.id, 
--     Q.category, 
--     Q.content, 
--     Q.is_multiple_choice
-- FROM Question AS Q
-- INNER JOIN QuizQuestion AS QQ 
--     ON QQ.question = Q.id 
-- WHERE QQ.quiz="4e68a8a5-ef11-426b-bdc3-2d0c12c0c338";

-- SELECT 
--     COUNT(*) 
-- FROM UserQuiz 
-- WHERE
--     quiz="4e68a8a5-ef11-426b-bdc3-2d0c12c0c338" AND
--     user="ba0a424e-8dc7-47e8-97e0-4824d812f4bf";