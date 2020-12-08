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
    id INT(255) PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Event_name VARCHAR(40) NOT NULL,
    Venue VARCHAR(40) NOT NULL,
    Budget INT(255) NOT NULL
);

CREATE TABLE Members(
    Id INT(30) PRIMARY KEY NOT NULL,
    Full_Name VARCHAR(50) NOT NULL,
    Position VARCHAR(50) NOT NULL
);

CREATE TABLE Clearance(
    Member_id INT(30) NOT NULL,
    Clearance_level ENUM("1", "2", "3", "4", "5") NOT NULL,
    Event_id INT(255) NOT NULL,
    FOREIGN KEY (Member_id) REFERENCES Members(id),
    FOREIGN KEY (Event_id) REFERENCES Events(id)
);



CREATE TABLE Event_Committee(
    Event_id INT(255) NOT NULL,
    Member_id INT(255) NOT NULL,
    Member_Role VARCHAR(50) NOT NULL,
    FOREIGN KEY (Member_id) REFERENCES Members(id),
    FOREIGN KEY (Event_id) REFERENCES Events(id)
);

CREATE TABLE Feedback(
    Rating INT(10) NOT NULL,
    Comments VARCHAR(255) NOT NULL,
    Event_id INT(255) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id)
);

CREATE TABLE Guests(
    Full_Name VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Phone_Number INT(25) NOT NULL,
    Category VARCHAR(50) NOT NULL,
    Event_id INT(255) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id)
);

CREATE TABLE Expenses(
    Expense_Type ENUM("Venue", "Marketing", "Food and Beverage", "Art Supplies", "Equipment", "Other") NOT NULL,
    Other_expense VARCHAR(50),
    Amount INT(255) NOT NULL,
    Event_id INT(255) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id)
);

CREATE TABLE Sponsor(
    Id INT(50) PRIMARY KEY NOT NULL,
    Full_Name VARCHAR(50) NOT NULL,
    Sponsor_Address VARCHAR(50) NOT NULL,
    Phone_Number VARCHAR(50) NOT NULL,
    Sponsor_Type VARCHAR(10) NOT NULL,
    Event_id INT(255) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id)
);

CREATE TABLE Inventory(
    Inventory_id INT(50) PRIMARY KEY NOT NULL,
    Item_Name VARCHAR(255) NOT NULL,
    Item_Quantity INT(50) NOT NULL,
    Sponsor_id INT(50),
    Event_id INT(255) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id),
    FOREIGN KEY (Sponsor_id) REFERENCES Sponsor(id)
);

CREATE TABLE Income(
    Income_Type ENUM("Sponsor", "Ticket Sales", "Merchandise", "Other") NOT NULL,
    Other_income VARCHAR(50),
    Amount INT(100) NOT NULL,
    Sponsor_id INT(50),
    Event_id INT(50) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id),
    FOREIGN KEY (Sponsor_id) REFERENCES Sponsor(id)
);

CREATE TABLE Login_cred(
    Id VARCHAR(50) NOT NULL,
    pass VARCHAR(50) NOT NULL,
    Email VARCHAR(50) NOT NULL
);