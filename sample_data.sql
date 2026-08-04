use Cinema_DB;

insert into Movies
(Title, Genre, Language_, Duration, Is_active, Rating, Release_date, Description_)

values
('Superman', 'Action, Sci-Fi', 'English', 129, true, 'PG-13', '2025-07-11',
 'Clark Kent embraces his destiny as Superman while confronting a powerful new threat.'),

('Jurassic World: Rebirth', 'Action, Adventure', 'English', 134, true, 'PG-13', '2025-07-02',
 'A new expedition enters dinosaur territory where survival is far from guaranteed.'),

('F1', 'Sports, Drama', 'English', 156, true, 'PG-13', '2025-06-27',
 'A veteran Formula One driver returns to mentor a promising young racer.'),

('Mission: Impossible – The Final Reckoning', 'Action, Thriller', 'English', 170, true, 'PG-13', '2025-05-23',
 'Ethan Hunt faces his most dangerous mission yet to stop a global catastrophe.'),

('Thunderbolts*', 'Action, Superhero', 'English', 127, true, 'PG-13', '2025-05-02',
 'A team of unlikely antiheroes undertakes a dangerous government mission.'),

('The Fantastic Four: First Steps', 'Superhero, Sci-Fi', 'English', 130, true, 'PG-13', '2025-07-25',
 'Marvel''s first family begins a new adventure against cosmic threats.'),

('How to Train Your Dragon', 'Fantasy, Adventure', 'English', 125, true, 'PG', '2025-06-13',
 'A live-action retelling of the friendship between Hiccup and Toothless.'),

('M3GAN 2.0', 'Horror, Sci-Fi', 'English', 119, true, 'PG-13', '2025-06-27',
 'The AI doll returns with even greater intelligence and deadlier intentions.'),

('28 Years Later', 'Horror, Thriller', 'English', 126, true, 'R', '2025-06-20',
 'Survivors continue to battle the aftermath of the devastating rage virus.'),

('The Naked Gun', 'Comedy', 'English', 108, true, 'PG-13', '2025-08-01',
 'A modern reboot of the classic slapstick police comedy.'),

('Avatar: The Way of Water', 'Sci-Fi, Adventure', 'English', 192, true, 'PG-13', '2022-12-16',
 'Jake Sully and his family seek refuge among Pandora''s ocean clans.'),

('Oppenheimer', 'Biography, Drama', 'English', 180, true, 'R', '2023-07-21',
 'The story of physicist J. Robert Oppenheimer and the Manhattan Project.'),

('Barbie', 'Comedy, Fantasy', 'English', 114, true, 'PG-13', '2023-07-21',
 'Barbie leaves Barbieland to discover the real world.'),

('Dune: Part Two', 'Sci-Fi, Adventure', 'English', 166, true, 'PG-13', '2024-03-01',
 'Paul Atreides joins the Fremen in a battle for the future of Arrakis.'),

('Inside Out 2', 'Animation, Family', 'English', 96, true, 'PG', '2024-06-14',
 'Riley faces new emotions as she enters her teenage years.'),

('Deadpool & Wolverine', 'Action, Comedy', 'English', 128, true, 'R', '2024-07-26',
 'Deadpool teams up with Wolverine for a multiverse adventure.'),

('The Batman', 'Action, Crime', 'English', 176, true, 'PG-13', '2022-03-04',
 'Batman investigates a series of murders committed by the Riddler.'),

('No Time to Die', 'Action, Spy', 'English', 163, true, 'PG-13', '2021-09-30',
 'James Bond comes out of retirement for one final mission.'),

('Wonka', 'Fantasy, Musical', 'English', 116, true, 'PG', '2023-12-15',
 'The origin story of the world''s most imaginative chocolatier.'),

('Top Gun: Maverick', 'Action, Drama', 'English', 131, true, 'PG-13', '2022-05-27',
 'Pete Maverick Mitchell returns to train the next generation of elite fighter pilots.');

insert into Screens
(ScreenID, Screen_name, Total_Seats) 
values
(1, 'Screen 1', 120),
(2, 'Screen 2', 120),
(3, 'Screen 3', 120),
(4, 'Screen 4', 120),
(5, 'Screen 5', 120),
(6, 'Screen 6', 120),
(7, 'Screen 7', 120),
(8, 'Screen 8', 120),
(9, 'Screen 9', 120),
(10, 'Screen 10', 120);

insert into Seat_categories
(Category_name, Ticket_price)
values
('Standard', 250.00),
('Premium', 400.00),
('VIP', 650.00);

insert into Shows
(MovieID, ScreenID, Show_date, Show_time, Is_booked_out, Is_active)

values
(1,1,'2026-08-05','10:00:00',false,true),
(1,1,'2026-08-05','14:00:00',false,true),
(1,1,'2026-08-05','18:00:00',false,true),

(2,2,'2026-08-05','11:00:00',false,true),
(2,2,'2026-08-05','15:00:00',false,true),

(3,3,'2026-08-05','12:00:00',false,true),
(3,3,'2026-08-05','19:00:00',false,true),

(4,4,'2026-08-05','13:00:00',false,true),

(5,5,'2026-08-05','16:00:00',false,true),

(6,6,'2026-08-05','18:30:00',false,true),

(7,7,'2026-08-05','09:30:00',false,true),

(8,8,'2026-08-05','20:00:00',false,true),

(9,9,'2026-08-05','17:30:00',false,true),

(10,10,'2026-08-05','21:00:00',false,true),

(14,2,'2026-08-06','18:30:00',false,true),

(16,5,'2026-08-06','20:30:00',false,true);

