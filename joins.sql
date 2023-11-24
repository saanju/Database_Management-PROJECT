select event_id, GROUP_CONCAT(CONCAT(users.user_id, " | ", users.first_name)) from registration join users on users.user_id=registration.user_id group by event_id;

select event_id, GROUP_CONCAT(CONCAT(clubs.club_id, '|', clubs.name)) from club_event join clubs on clubs.club_id=club_event.club_id group by event_id;

