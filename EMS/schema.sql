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
    Id INT(255) PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Event_Name VARCHAR(40) NOT NULL,
    Venue VARCHAR(40) NOT NULL,
    Budget INT(255) NOT NULL
);

CREATE TABLE Members(
    Id INT(30) PRIMARY KEY NOT NULL,
    Full_Name VARCHAR(50) NOT NULL,
    Position VARCHAR(50) NOT NULL
);

CREATE TABLE Clearance(
    Member_Id INT(30) NOT NULL,
    Clearance_Level ENUM("1", "2", "3", "4", "5") NOT NULL,
    Event_Id INT(255) NOT NULL,
    FOREIGN KEY (Member_id) REFERENCES Members(Id),
    FOREIGN KEY (Event_id) REFERENCES Events(Id)
);



CREATE TABLE Event_Committee(
    Event_Id INT(255) NOT NULL,
    Member_Id INT(255) NOT NULL,
    Member_Role VARCHAR(50) NOT NULL,
    FOREIGN KEY (Member_Id) REFERENCES Members(Id),
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Feedback(
    Rating INT(10) NOT NULL,
    Comments VARCHAR(255) NOT NULL,
    Event_Id INT(255) NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Guests(
    Full_Name VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Phone_Number INT(25) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Event_Id INT(255) NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Expenses(
    Expense_Type ENUM("Venue", "Marketing", "Food and Beverage", "Art Supplies", "Equipment", "Other") NOT NULL,
    Other_Expense VARCHAR(50),
    Amount INT(255) NOT NULL,
    Event_Id INT(255) NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Sponsor(
    Id INT(50) PRIMARY KEY NOT NULL,
    Full_Name VARCHAR(50) NOT NULL,
    Sponsor_Address VARCHAR(50) NOT NULL,
    Phone_Number VARCHAR(50) NOT NULL,
    Sponsor_Type VARCHAR(10) NOT NULL,
    Event_Id INT(255) NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id)
);

CREATE TABLE Inventory(
    Inventory_Id INT(50) PRIMARY KEY NOT NULL,
    Item_Name VARCHAR(255) NOT NULL,
    Item_Quantity INT(50) NOT NULL,
    Sponsor_Id INT(50),
    Event_Id INT(255) NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id),
    FOREIGN KEY (Sponsor_Id) REFERENCES Sponsor(Id)
);

CREATE TABLE Income(
    Income_Type ENUM("Sponsor", "Ticket Sales", "Merchandise", "Other") NOT NULL,
    Other_Income VARCHAR(50),
    Amount INT(100) NOT NULL,
    Sponsor_Id INT(50),
    Event_Id INT(50) NOT NULL,
    FOREIGN KEY (Event_Id) REFERENCES Events(Id),
    FOREIGN KEY (Sponsor_Id) REFERENCES Sponsor(Id)
);

CREATE TABLE Login_Cred(
    Id VARCHAR(50) NOT NULL,
    Pass VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL
);