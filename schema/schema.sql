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
    userQuiz VARCHAR(45) NOT NULL,
    question VARCHAR(45) NOT NULL,
    content VARCHAR(255),
    choice VARCHAR(45),
    PRIMARY KEY (userQuiz, question),
    FOREIGN KEY (userQuiz) REFERENCES UserQuiz(id),
    FOREIGN KEY (question) REFERENCES Question(id),
    FOREIGN KEY (choice) REFERENCES Choice(id)
);

INSERT INTO User (id, role, firstname, lastname, email, password)
VALUES
('ad341a5c-84f0-4617-abf2-5b7482a0e457', 'Administrator', 'John', 'Doe', 'jdoe@email.com', 'pbkdf2:sha256:260000$ZnX1SpCHcYEewgS5$35022d1d0b6490c07b3a6672cf86edb6291d35868115b10eeb3a795d31f3e0e6'),
('ba0a424e-8dc7-47e8-97e0-4824d812f4bf', 'Bruker', 'Kari', 'Olsen', 'kari@email.com', 'pbkdf2:sha256:260000$EciEAeMChVWpqVOC$740a34a2a271c7f93cc1ac3c0fc7584ab6458bde256648fd9b36746caace365f');


-- SELECT
--     Q.title,
--     QT.category,
--     QT.content AS question,
--     QT.is_multiple_choice,
--     A.content AS choice,
--     A.is_correct
-- FROM Quiz AS Q
-- INNER JOIN QuizQuestion AS QQ ON Q.id = QQ.quiz
-- INNER JOIN Question AS QT ON QQ.question = QT.id
-- INNER JOIN Choice AS A ON QT.id = A.question;