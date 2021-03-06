DROP TABLE IF EXISTS Income;
DROP TABLE IF EXISTS Event_Committee;
DROP TABLE IF EXISTS Clearance;
DROP TABLE IF EXISTS Guests;
DROP TABLE IF EXISTS Expenses;
DROP TABLE IF EXISTS Feedback;
DROP TABLE IF EXISTS Inventory;
DROP TABLE IF EXISTS Sponsor;
DROP TABLE IF EXISTS Login_cred;
DROP TABLE IF EXISTS Members;
DROP TABLE IF EXISTS Events;

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
    Clearance_Level ENUM("1", "2", "3") NOT NULL,
    Event_Id SMALLINT NOT NULL,
    FOREIGN KEY (Member_id) REFERENCES Members(Id),
    FOREIGN KEY (Event_id) REFERENCES Events(Id)
);

CREATE TABLE Event_Committee(
    Event_Id SMALLINT NOT NULL,
    Member_Id SMALLINT NOT NULL,
    Member_Role VARCHAR(50) NOT NULL,
    IsVolunteer BOOLEAN NOT NULL,
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
    Email VARCHAR(50),
    Phone_Number VARCHAR(30),
    Category VARCHAR(50),
    Event_Id SMALLINT NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Expenses(
    Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Expense_Type ENUM("Venue", "Marketing", "Food and Beverage", "Art Supplies", "Equipment", "Other") NOT NULL,
    Item_Name VARCHAR(50),
    Amount BIGINT NOT NULL,
    Event_Id SMALLINT NOT NULL,
    Expense_Date DATE NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Sponsor(
    Id SMALLINT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Sponsor_Name VARCHAR(50) NOT NULL,
    Contact_Name VARCHAR(50) NOT NULL,
    Sponsor_Address VARCHAR(50) NOT NULL,
    Phone_Number VARCHAR(50) NOT NULL,
    Sponsor_Type ENUM("Money", "Equipment", "Money and Equipment") NOT NULL
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
    Item_Name VARCHAR(50),
    Amount BIGINT NOT NULL,
    Sponsor_Id SMALLINT,
    Event_Id SMALLINT NOT NULL,
    Income_Date DATE NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id),
    FOREIGN KEY (Sponsor_Id) REFERENCES Sponsor(Id)
);

CREATE TABLE Login_Cred(
    Id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Pass VARCHAR(200) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Username VARCHAR(50) NOT NULL,
    IsAdmin BOOLEAN NOT NULL,
    Member_Id SMALLINT NOT NULL,
    FOREIGN KEY (Member_Id) REFERENCES Members(Id)
);