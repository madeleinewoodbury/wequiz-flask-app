CREATE TABLE Rolle (
    id TINYINT UNSIGNED PRIMARY KEY,
    navn VARCHAR(45)
);

CREATE TABLE Tema (
    id TINYINT UNSIGNED PRIMARY KEY,
    navn VARCHAR(45)
);

CREATE TABLE Status (
    id TINYINT UNSIGNED PRIMARY KEY,
    navn VARCHAR(45)
);

CREATE TABLE Bruker (
    id VARCHAR(45) PRIMARY KEY,
    rolle TINYINT UNSIGNED NOT NULL,
    fornavn VARCHAR(50),
    etternavn VARCHAR(50),
    epost VARCHAR(50) UNIQUE,
    passord VARCHAR(255),
    dato_opprettet DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (rolle) REFERENCES Rolle(id)
);

CREATE TABLE Quiz (
    id VARCHAR(45) PRIMARY KEY,
    admin VARCHAR(45) NOT NULL,
    tema TINYINT UNSIGNED NOT NULL,
    status TINYINT UNSIGNED NOT NULL,
    dato_opprettet DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (admin) REFERENCES Bruker(id),
    FOREIGN KEY (tema) REFERENCES Tema(id),
    FOREIGN KEY (status) REFERENCES Status(id)
);

CREATE TABLE Spørsmål (
    id VARCHAR(45) PRIMARY KEY,
    quiz VARCHAR(45) NOT NULL,
    tekst VARCHAR(255),
    har_alternativer TINYINT DEFAULT 0,
    FOREIGN KEY (quiz) REFERENCES Quiz(id)
);

CREATE TABLE SvarAlternativ (
    id VARCHAR(45) PRIMARY KEY,
    spørsmål VARCHAR(45) NOT NULL,
    tekst VARCHAR(255),
    korrekt TINYINT,
    FOREIGN KEY (spørsmål) REFERENCES Spørsmål(id)
);

CREATE TABLE Gjennomføring (
    id VARCHAR(45) PRIMARY KEY,
    quiz VARCHAR(45) NOT NULL,
    bruker VARCHAR(45) NOT NULL,
    dato_levert DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz) REFERENCES Quiz(id),
    FOREIGN KEY (bruker) REFERENCES Bruker(id)
);

CREATE TABLE Svar (
    gjennomføring VARCHAR(45) NOT NULL,
    spørsmål VARCHAR(45) NOT NULL,
    svar_tekst VARCHAR(255),
    svar_alternativ VARCHAR(45),
    FOREIGN KEY (gjennomføring) REFERENCES Gjennomføring(id),
    FOREIGN KEY (spørsmål) REFERENCES Spørsmål(id),
    FOREIGN KEY (svar_alternativ) REFERENCES SvarAlternativ(id)
);