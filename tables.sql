DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS Messages;
DROP TABLE IF EXISTS UserMessages;

PRAGMA foreign_keys = 1;

CREATE TABLE Users (id INTEGER Primary KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password TEXT NOT NULL, role INTEGER DEFAULT 2 NOT NULL);
INSERT INTO Users (name, email, password) VALUES 
    ('Jane', 'janedoe@test.com', '$2b$12$yQ7bf11kk6W/Kca1D3H2tuvfCyJ.YihiPOANNmQGCE3ZJ8WeJpgDG'),
    ('John', 'johndoe@test.com', '$2b$12$OHjqXpmqsYCSvVCJYmaTtejrggRYMUOx3kZfT7HJHSnDleQK.6olC'),
    ('Leon', 'leon@test.com', '$2b$12$Ipb9GJUZ8xpbcThGmqvL4ecM9673jKnBOs.hSkDADCD4UAZ8Foola');
UPDATE Users SET ROLE=1 WHERE id=3;

CREATE TABLE Messages (id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        body TEXT NOT NULL,
        created_at INTEGER NOT NULL,
        is_read INTEGER,
        owner INTEGER,
        FOREIGN KEY(owner) REFERENCES Users(id)
    );
INSERT INTO Messages (subject, body, created_at, is_read, owner) VALUES
    ('Hello', 'Ullamco laborum consequat qui adipisicing elit magna laboris. Id occaecat commodo reprehenderit aliqua Lorem nulla magna ea ipsum adipisicing.', strftime('%s', '2020-05-31 08:10:10'), 1, 1),
    ('Officia duis', 'Officia duis nostrud minim irure magna est cupidatat exercitation laboris mollit.', strftime('%s', '2020-05-31 12:10:10'), 1,2),
    ('Ullamco', 'Ullamco laborum consequat qui adipisicing elit magna laboris.', strftime('%s', '2020-06-01 11:00:00'), 1,2),
    ('Commodo reprehenderit', 'Id occaecat commodo reprehenderit aliqua Lorem nulla magna ea ipsum adipisicing.', strftime('%s', '2020-06-02 19:59:59'), 0, 3),
    ('Aliqua sit', 'Velit ex aliquip do proident laborum nisi aliqua sit quis eiusmod est enim.', strftime('%s', '2020-06-02 23:00:00'), 0, 3);

-- TODO: add another foreign key in order to delete for either user without deleteing 
-- message for both users. And owner can decide if to show to both users
CREATE TABLE UserMessages (
    m_id INTEGER,
    r_id INTEGER,
    FOREIGN KEY(m_id) REFERENCES Messages(id) ON DELETE CASCADE,
    FOREIGN KEY(r_id) REFERENCES Users(id) ON DELETE CASCADE,
    CONSTRAINT uc_mr_ids UNIQUE (m_id, r_id)
);
CREATE INDEX recepient_id on UserMessages (r_id);
INSERT INTO UserMessages VALUES (1, 2), (2, 1), (3, 3), (4, 2), (5, 1);
