create database Cinema_DB;
use cinema_db;

create table Movies (
    MovieID int auto_increment primary key,
    Title varchar(100) not null,
    Genre varchar(50),
    Language_ varchar(30) not null,
    Duration int not null check (Duration > 0),
    Is_active boolean not null default true,
    Rating varchar(10),
    Release_date date,
    Description_ TEXT
);

create table Screens (
    ScreenID int primary key,
    Screen_name varchar(20) unique not null,
    Total_Seats int not null check (Total_Seats > 0)
);

create table Seat_categories (
    CategoryID int auto_increment primary key,
    Category_name varchar(20) not null unique,
    Ticket_price decimal(8,2) not null check (Ticket_price >= 0)
);

create table Seats (
    SeatID int auto_increment primary key,
    ScreenID int not null,
    Seat_number varchar(5) not null,
    CategoryID int not null,
    foreign key (ScreenID) references Screens(ScreenID) on delete cascade on update cascade,
    foreign key (CategoryID) references Seat_categories(CategoryID) on update cascade,
    unique(ScreenID, Seat_number)
);

create table Shows (
    ShowID int auto_increment primary key,
    MovieID int not null,
    ScreenID int not null,
    Show_date date not null,
    Show_time time not null,
    Is_booked_out boolean not null default false,
    Is_active boolean not null default true,
    foreign key (MovieID) references Movies(MovieID) on update cascade,
    foreign key (ScreenID) references Screens(ScreenID) on update cascade
);

create table Customers (
    CustomerID int auto_increment primary key,
    First_name varchar(50) not null,
    Last_name varchar(50) not null,
    Phone varchar(15) unique,
    Email varchar(100) unique,
    Passkey_hash varchar(255) not null
);

create table Bookings (
    BookingID int auto_increment primary key,
    CustomerID int not null,
    ShowID int not null,
    Booking_date datetime not null,
    Total_amount decimal(8,2) not null,
    Booking_status varchar(20) not null check(Booking_status in ('Confirmed', 'Cancelled')),
    foreign key (CustomerID) references Customers(CustomerID),
    foreign key (ShowID) references Shows(ShowID)
);

create table BookingSeats (
    BookingSeatID int auto_increment primary key,
    BookingID int not null,
    SeatID int not null,
    foreign key (BookingID) references Bookings(BookingID),
    foreign key (SeatID) references Seats(SeatID),
    unique (BookingID, SeatID) 
);
