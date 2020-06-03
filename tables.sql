CREATE TABLE User (id INTEGER Primary KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, password TEXT NOT NULL);
INSERT INTO User (name, email, password) VALUES 
    ('Jane', 'janedoe@test.com', '$2b$12$yQ7bf11kk6W/Kca1D3H2tuvfCyJ.YihiPOANNmQGCE3ZJ8WeJpgDG'),
    ('John', 'johndoe@test.com', '$2b$12$OHjqXpmqsYCSvVCJYmaTtejrggRYMUOx3kZfT7HJHSnDleQK.6olC'),
    ('Leon', 'leon@test.com', '$2b$12$Ipb9GJUZ8xpbcThGmqvL4ecM9673jKnBOs.hSkDADCD4UAZ8Foola');

CREATE TABLE Message (id INTEGER Primary KEY AUTOINCREMENT, subject TEXT NOT NULL, body TEXT NOT NULL, created_at INTEGER NOT NULL, is_read INTEGER, owner INTEGER);
INSERT INTO Message (subject, body, created_at, is_read, owner) VALUES
    ('Hello', 'Ullamco laborum consequat qui adipisicing elit magna laboris. Id occaecat commodo reprehenderit aliqua Lorem nulla magna ea ipsum adipisicing.', strftime('%s', '2020-05-31 08:10:10'), 1, 1),
    ('Officia duis', 'Officia duis nostrud minim irure magna est cupidatat exercitation laboris mollit.', strftime('%s', '2020-05-31 12:10:10'), 1,2),
    ('Ullamco', 'Ullamco laborum consequat qui adipisicing elit magna laboris.', strftime('%s', '2020-06-01 11:00:00'), 1,2),
    ('Commodo reprehenderit', 'Id occaecat commodo reprehenderit aliqua Lorem nulla magna ea ipsum adipisicing.', strftime('%s', '2020-06-02 19:59:59'), 0, 3),
    ('Aliqua sit', 'Velit ex aliquip do proident laborum nisi aliqua sit quis eiusmod est enim.', strftime('%s', '2020-06-02 23:00:00'), 0, 3);

CREATE TABLE UserMessage (m_id INTEGER, r_id INTEGER);
CREATE INDEX recepient_id on UserMessage (r_id);
INSERT INTO UserMessage VALUES (1, 2), (2, 1), (3, 3), (4, 2), (5, 1);