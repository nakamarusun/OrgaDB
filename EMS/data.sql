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