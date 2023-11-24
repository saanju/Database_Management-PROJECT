DELIMITER //

CREATE TRIGGER check_seats_trigger
BEFORE INSERT ON registration
FOR EACH ROW
BEGIN
    DECLARE available_seats INT;

    SELECT slots_left INTO available_seats FROM add_events WHERE event_id = NEW.event_id;

    IF available_seats > 0 THEN
        SET available_seats = available_seats - 1;
        UPDATE add_events SET slots_left = available_seats WHERE event_id = NEW.event_id;
    ELSE
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'No available seats for the selected pack.';
    END IF;
END //

DELIMITER ;


DELIMITER //

CREATE TRIGGER check_phone_number_trigger
BEFORE INSERT ON users

FOR EACH ROW
BEGIN
    IF NEW.phone REGEXP '^(9|8|7|6)[0-9]{9}$' = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid phone number format.';
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER check_phone_number_trigger2

before insert on clubs

FOR EACH ROW
BEGIN
    IF NEW.contact REGEXP '^(9|8|7|6)[0-9]{9}$' = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid phone number format.';
    END IF;
END //

DELIMITER ;

DELIMITER //

CREATE TRIGGER check_phone_number_trigger3

before insert on sponsors
FOR EACH ROW
BEGIN
    IF NEW.contact REGEXP '^(9|8|7|6)[0-9]{9}$' = 0 THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid phone number format.';
    END IF;
END //

DELIMITER ;




DELIMITER //

CREATE TRIGGER check_email_format_trigger
BEFORE INSERT ON users
FOR EACH ROW
BEGIN
    DECLARE email_pattern VARCHAR(255);
    SET email_pattern = '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,4}$';
    
    IF NEW.email NOT REGEXP email_pattern THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'Invalid email format.';
    END IF;
END //

DELIMITER ;