Begin;


CREATE TABLE users (
    User_id         INTEGER  PRIMARY KEY, 
    First_name      TEXT, 
    Last_name       TEXT, 
    Email           TEXT, 
    Created_Date    DATE 
);


CREATE TABLE projects (
    Project_id      INTEGER,   
    Project_Name    TEXT, 
    User_ID         INTEGER,
    City            TEXT, 
    State           TEXT,    
    Description     TEXT,
    Create_Date     DATE,  
    PRIMARY KEY     (Project_id),
    FOREIGN KEY     (User_id) REFERENCES users(User_id)
);

COMMIT;
