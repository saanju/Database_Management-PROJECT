DELIMITER $$

CREATE PROCEDURE get_events_in_date_range(
    IN s DATE,
    IN e DATE
)
BEGIN
    SELECT *
    FROM add_events
    WHERE start_date >= s AND end_date <= e;
END$$

DELIMITER ;
