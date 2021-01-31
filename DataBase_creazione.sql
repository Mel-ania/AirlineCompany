/* Tabelle */

CREATE TABLE aerei (
	CodAerei int PRIMARY KEY,
    Tipo varchar(30),
    NumPosti int UNSIGNED DEFAULT(0),
    PesoStiva double DEFAULT (0)
);

CREATE TABLE classi (
	CodClassi varchar(15) PRIMARY KEY,
    Wifi boolean DEFAULT(false),
    Schermo boolean DEFAULT(false),
    PastoGratis boolean DEFAULT(false),
    Corrente boolean DEFAULT(false)
);

CREATE TABLE localita (
	CodLocalita int PRIMARY KEY,
    Citta varchar(60) NOT NULL,
    Nazione varchar(50) NOT NULL,
    NomeAeroporto varchar(50)
);

CREATE TABLE voli (
	CodVoli int PRIMARY KEY,
    Partenza datetime,
    Arrivo datetime,
    Durata varchar(10),
    CodViaggi int NOT NULL,
    CodAerei int NOT NULL,
    Da int NOT NULL,
    Verso int NOT NULL,
    NumScali int UNSIGNED,
    Sconto int,
    FOREIGN KEY (CodViaggi) REFERENCES viaggi (CodViaggi)
		ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (CodAerei) REFERENCES aerei (CodAerei)
		ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Da) REFERENCES localita (CodLocalita)
		ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (Verso) REFERENCES localita (CodLocalita)
		ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE posti (
    CodClassi varchar(15),
    CodPosti varchar(4) PRIMARY KEY,
    CodPrenotazioni int NOT NULL,
    Libero boolean DEFAULT(true),
	FOREIGN KEY (CodClassi) REFERENCES classi (CodClassi)
		ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (CodPrenotazioni) REFERENCES prenotazioni (CodPrenotazioni)
		ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE prenotazioni (
	CodPrenotazioni int PRIMARY KEY,
	CodVoli int NOT NULL,
    CF varchar(20) NOT NULL,
    CodAgenzie int NOT NULL,
    DataPrenotazione date NOT NULL,
    Bagagli int,
    FOREIGN KEY (CodVoli) REFERENCES voli (CodVoli)
		ON UPDATE CASCADE ON DELETE CASCADE,
	FOREIGN KEY (CF) REFERENCES clienti (CF)
		ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE users (
	ID varchar(15) PRIMARY KEY,
    Nome varchar(50),
    Email varchar(50),
    Password varchar(20),
    Ruolo enum ('Cliente', 'Operatore', 'Anonimo')
);

/* Ruoli */

CREATE ROLE Anonimo;
GRANT INSERT ON users TO Anonimo;

CREATE ROLE Cliente;
GRANT INSERT ON prenotazioni TO Cliente;
GRANT INSERT ON bagagli TO Cliente;
GRANT INSERT ON posti TO Cliente;
GRANT SELECT ON users TO Cliente;
GRANT SELECT ON aerei TO Cliente;
GRANT SELECT ON prenotazioni TO Cliente;
GRANT SELECT ON voli TO Cliente;
GRANT SELECT ON localita TO Cliente;
GRANT SELECT ON posti TO Cliente;
GRANT SELECT ON sconti TO Cliente;
GRANT SELECT ON bagagli TO Cliente;
GRANT SELECT ON classi TO Cliente;
GRANT DELETE ON prenotazioni TO Cliente;
GRANT DELETE ON bagagli TO Cliente;
GRANT DELETE ON users TO Cliente;
GRANT UPDATE ON prenotazioni TO Cliente;
GRANT UPDATE ON bagagli TO Cliente;
GRANT UPDATE ON users TO Cliente;

CREATE ROLE Operatore;
GRANT SELECT ON * TO Operatore;
GRANT SELECT ON voli TO Operatore;
GRANT SELECT ON aerei TO Operatore;
GRANT SELECT ON localita TO Operatore;
GRANT INSERT ON users TO Operatore;
GRANT INSERT ON aerei TO Operatore;
GRANT INSERT ON localita TO Operatore;
GRANT INSERT ON voli TO Operatore;
GRANT DELETE ON aerei TO Operatore;
GRANT DELETE ON localita TO Operatore;
GRANT DELETE ON voli TO Operatore;
GRANT UPDATE ON aerei TO Operatore;
GRANT UPDATE ON localita TO Operatore;
GRANT UPDATE ON voli TO Operatore;

/* Trigger */

delimiter |
CREATE TRIGGER PesoStivaInsert BEFORE INSERT ON prenotazioni
	FOR EACH ROW
    BEGIN
		DECLARE NumBagagli int;
        DECLARE NumBagagliMax int;
        
        SELECT SUM(p.Bagagli) 
        INTO NumBagagli
        FROM prenotazioni p
        WHERE p.CodVoli = NEW.CodVoli;
        
        SELECT a.PesoStiva
        INTO NumBagagliMax
        FROM aerei a NATURAL JOIN voli v
        WHERE v.CodVoli = NEW.CodVoli;
        
		IF NEW.Bagagli > ((NumBagagliMax / 30) - NumBagagli) THEN
			SET NEW.Bagagli = ((NumBagagliMax / 30) - NumBagagli);
		END IF;
    END;
|
delimiter ;
delimiter |
CREATE TRIGGER PesoStivaUpdate BEFORE UPDATE ON prenotazioni
	FOR EACH ROW
    BEGIN
		DECLARE NumBagagli int;
        DECLARE NumBagagliMax int;
        
        SELECT SUM(p.Bagagli) 
        INTO NumBagagli
        FROM prenotazioni p
        WHERE p.CodVoli = NEW.CodVoli;
        
        SELECT a.PesoStiva
        INTO NumBagagliMax
        FROM aerei a NATURAL JOIN voli v
        WHERE v.CodVoli = NEW.CodVoli;
        
		IF NEW.Bagagli > ((NumBagagliMax / 30) - NumBagagli) THEN
			SET NEW.Bagagli = ((NumBagagliMax / 30) - NumBagagli + OLD.Bagagli);
		END IF;
    END;
|
delimiter ;
delimiter |
CREATE TRIGGER ProfiloUpdate BEFORE UPDATE ON users
	FOR EACH ROW
    BEGIN
		IF NEW.Nome = null OR NEW.Nome = '' THEN
			SET NEW.Nome = OLD.Nome;
		END IF;
		IF NEW.Email = null OR NEW.Email = '' THEN
			SET NEW.Email = OLD.Email;
		END IF;
    END;
|
delimiter ;

