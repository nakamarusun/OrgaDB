CREATE TABLE Events(
    id INT(255) PRIMARY KEY AUTO_INCREMENT NOT NULL,
    Event_name VARCHAR(40) NOT NULL,
    Venue VARCHAR(40) NOT NULL,
    Budget INT(255) NOT NULL
);

CREATE TABLE Members(
    Full_Name VARCHAR(50) NOT NULL,
    Position VARCHAR(50) NOT NULL,
    Id INT(30) PRIMARY KEY NOT NULL
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
    Full_Name VARCHAR(50) NOT NULL,
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
    Expense_Type VARCHAR(50) NOT NULL,
    Amount INT(255) NOT NULL,
    Event_id INT(255) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id)
);

CREATE TABLE Sponsor(
    Full_Name VARCHAR(50) NOT NULL,
    Sponsor_Type VARCHAR(10) NOT NULL,
    Id INT(50) PRIMARY KEY NOT NULL,
    Event_id INT(255) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id)
);

CREATE TABLE Inventory(
    Item_Name VARCHAR(255) NOT NULL,
    Item_Amount INT(50) NOT NULL,
    Sponsor_id INT(50),
    Event_id INT(255) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id),
    FOREIGN KEY (Sponsor_id) REFERENCES Sponsor(id)
);

CREATE TABLE Income(
    Income_Type VARCHAR(50) NOT NULL,
    Amount INT(100) NOT NULL,
    Sponsor_id INT(50),
    Event_id INT(50) NOT NULL,
    FOREIGN KEY (Event_id) REFERENCES Events(id),
    FOREIGN KEY (Sponsor_id) REFERENCES Sponsor(id)
);