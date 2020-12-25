DROP TABLE IF EXISTS Income;
DROP TABLE IF EXISTS Event_Committee;
DROP TABLE IF EXISTS Clearance;
DROP TABLE IF EXISTS Guests;
DROP TABLE IF EXISTS Expenses;
DROP TABLE IF EXISTS Feedback;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Sponsor;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Events;
DROP TABLE IF EXISTS Login_cred;


CREATE TABLE Events(
    Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Event_Name VARCHAR(40) NOT NULL,
    Venue VARCHAR(40) NOT NULL,
    Budget INT NOT NULL,
    Event_Desc TEXT NOT NULL
);

CREATE TABLE Members(
    Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Full_Name VARCHAR(50) NOT NULL,
    Position VARCHAR(50) NOT NULL
);

CREATE TABLE Clearance(
    Member_Id SMALLINT NOT NULL,
    Clearance_Level ENUM("1", "2", "3", "4", "5") NOT NULL,
    Event_Id SMALLINT NOT NULL,
    FOREIGN KEY (Member_id) REFERENCES Members(Id),
    FOREIGN KEY (Event_id) REFERENCES Events(Id)
);

CREATE TABLE Event_Committee(
    Event_Id SMALLINT NOT NULL,
    Member_Id SMALLINT NOT NULL,
    Member_Role VARCHAR(50) NOT NULL,
    FOREIGN KEY (Member_Id) REFERENCES Members(Id),
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Feedback(
    Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Rating TINYINT NOT NULL,
    Comments TEXT NOT NULL,
    Event_Id SMALLINT NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Guests(
    Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Full_Name VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Phone_Number VARCHAR(30) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Event_Id SMALLINT NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Expenses(
    Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Expense_Type ENUM("Venue", "Marketing", "Food and Beverage", "Art Supplies", "Equipment", "Other") NOT NULL,
    Other_Expense VARCHAR(50),
    Amount INT NOT NULL,
    Event_Id SMALLINT NOT NULL,
    Expense_Date DATE NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Sponsor(
    Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Full_Name VARCHAR(50) NOT NULL,
    Sponsor_Address VARCHAR(50) NOT NULL,
    Phone_Number VARCHAR(50) NOT NULL,
    Sponsor_Type ENUM("Money", "Equipment") NOT NULL,
    Event_Id SMALLINT NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Inventory(
    Inventory_Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Item_Name VARCHAR(255) NOT NULL,
    Item_Quantity SMALLINT NOT NULL,
    Sponsor_Id SMALLINT,
    Event_Id SMALLINT NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id),
    FOREIGN KEY (Sponsor_Id) REFERENCES Sponsor(Id)
);

CREATE TABLE Income(
    Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Income_Type ENUM("Sponsor", "Ticket Sales", "Merchandise", "Other") NOT NULL,
    Other_Income VARCHAR(50),
    Amount INT NOT NULL,
    Sponsor_Id SMALLINT,
    Event_Id SMALLINT NOT NULL,
    Income_Date DATE NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id),
    FOREIGN KEY (Sponsor_Id) REFERENCES Sponsor(Id)
);

CREATE TABLE Login_Cred(
    Id VARCHAR(50) NOT NULL,
    Pass VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Username VARCHAR(50) NOT NULL
);

INSERT INTO Events(Event_Name, Venue, Budget, Event_Desc)  
    VALUES("Bruh Event", "Chad, Africa", 69420, "HEH FUNI NUMBER"), 
    ("Only Talk About Anime Event", "Nihon", 1437, "Weebs RISE UP"), 
    ("OKRUDDYBETARD APPRECIATION EVENT", "Le Reddit", 0, "COD zombi");

INSERT INTO Members(Full_Name, Position)
    VALUES("JC", "Head of Everything"),
    ("Eric Hernando", "Leader of the Weebs"),
    ("Bently Edyson", "A car");

INSERT INTO Clearance(Member_Id, Clearance_Level, Event_id)
    VALUES(1, "5", 1),
    (2, "3", 2),
    (3, "1", 2);

INSERT INTO Event_Committee(Event_id,  Member_Id, Member_Role)
    VALUES(1, 1, "Bruh"),
    (2, 2, "Hololiver"),
    (2, 3, "Genshiin Player");

INSERT INTO Feedback(Rating, Comments, Event_id)
    VALUES(5, "yeah dude im :(", 1),
    (4, "yeah idk what to put here", 2),
    (0, "yeah this one too", 3);

INSERT INTO Guests(Full_Name, Email, Phone_Number, Category, Event_id)
    VALUES("Gardyan Potato Akbar", "Potato@gmail.com", "+629371287323", "Speaker", 1),
    ("Yowen Yowen Yowen", "Yowen@yowen.com", "+696969696969", "Moderator", 2),
    ("Reximus Maximus", "Rex@ganteng.com", "+273187362", "Speaker", 3);

INSERT INTO Expenses(Expense_Type, Other_Expense, Amount, Event_id, Expense_Date)
    VALUES("Venue", NULL, 23012838, 1, "2019-05-19"),
    ("Marketing", NULL, 24612983, 1, "2019-06-01"),
    ("Other", "Something idk", 2734724726, "2019-05-29");

INSERT INTO Sponsor(Full_Name, Sponsor_Address, Phone_Number, Sponsor_Type, Event_Id)
    VALUES("NordVPN", "Nord@VPN.com", "0812373737349", "Money", 1),
    ("Raid Shadow Legends", "Shadow@man.com", "+65482947523", "Money", 2),
    ("Ring Doorbell", "Ring@door.com", "+64278361232", "Equipment", 3);

INSERT INTO Inventory(Item_Name, Item_Quantity, Sponsor_Id, Event_Id)
    VALUES("Bruh Mat", 20, NULL, 1),
    ("IOT Doorbell", 5, 3, 2),
    ("Playstation 6", 69, NULL, 3);

INSERT INTO Income(Income_Type, Other_Income, Amount, Sponsor_Id, Event_id, Income_Date)
    VALUES("Ticket Sales", NULL, 234500000, NULL, 1, "2020-05-09"),
    ("Merchandise", NULL, 2381723899, NULL, 2, "2077-12-10"),
    ("Other", "Robbery", 23818900000, NULL, 2, "2019-12-25");