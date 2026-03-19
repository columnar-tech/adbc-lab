CREATE TABLE IF NOT EXISTS trips (
  trip_id INTEGER PRIMARY KEY,
  user_type TEXT NOT NULL,
  start_station TEXT NOT NULL,
  end_station TEXT NOT NULL,
  duration_minutes INTEGER NOT NULL
);

INSERT INTO trips (trip_id, user_type, start_station, end_station, duration_minutes) VALUES
  (1, 'member', 'Waterloo', 'Bank', 14),
  (2, 'casual', 'Bank', 'London Bridge', 22),
  (3, 'member', 'Waterloo', 'Soho', 11),
  (4, 'member', 'Soho', 'Bank', 9),
  (5, 'casual', 'Waterloo', 'Bank', 18),
  (6, 'member', 'King''s Cross', 'Waterloo', 16),
  (7, 'casual', 'Soho', 'King''s Cross', 27),
  (8, 'member', 'Bank', 'Soho', 12),
  (9, 'member', 'London Bridge', 'Bank', 10),
  (10, 'casual', 'Waterloo', 'King''s Cross', 21),
  (11, 'member', 'Bank', 'Waterloo', 13),
  (12, 'casual', 'Soho', 'Waterloo', 19),
  (13, 'member', 'Waterloo', 'London Bridge', 17),
  (14, 'member', 'King''s Cross', 'Bank', 15),
  (15, 'casual', 'London Bridge', 'Soho', 24);
