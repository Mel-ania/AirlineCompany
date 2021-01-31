/* Ruoli e permessi */

CREATE ROLE Anonimo;
GRANT INSERT ON users TO Anonimo;

CREATE ROLE Cliente;
GRANT INSERT ON prenotazioni TO Cliente;
GRANT INSERT ON posti TO Cliente;
GRANT SELECT ON users TO Cliente;
GRANT SELECT ON aerei TO Cliente;
GRANT SELECT ON prenotazioni TO Cliente;
GRANT SELECT ON voli TO Cliente;
GRANT SELECT ON localita TO Cliente;
GRANT SELECT ON posti TO Cliente;
GRANT SELECT ON classi TO Cliente;
GRANT DELETE ON prenotazioni TO Cliente;
GRANT DELETE ON users TO Cliente;
GRANT UPDATE ON prenotazioni TO Cliente;
GRANT UPDATE ON users TO Cliente;

CREATE ROLE Operatore;
GRANT SELECT ON * TO Operatore;
GRANT SELECT ON voli TO Operatore;
GRANT SELECT ON aerei TO Operatore;
GRANT SELECT ON localita TO Operatore;
GRANT SELECT ON users TO Operatore;
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
GRANT UPDATE ON users TO Operatore;

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