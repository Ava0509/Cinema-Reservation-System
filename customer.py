import database as db
import tkinter as tk

con = db.con
cursor = db.con.cursor()

window = tk.Tk()
window.title("Cinema Reservation System")
window.state('zoomed')
window.configure(bg = "white")

top_frame = tk.Frame(window, bg="#eeeee")
top_frame.pack(fill = "x", padx=15, pady=10)

book_ticket_button=tk.Button(top_frame, text="Book Tickets", bg="white", command=book_tickets)
view_shows_button=tk.Button(top_frame, text="View Shows", bg="white", command=view_shows)

search_booking_button=tk.Button(top_frame, text="Search booking", bg="white", command=search_booking)
cancel_booking_button=tk.Button(top_frame, text="Cancel Booking", bg="white", command=cancel_booking)

def customer_menu():
    heading = tk.Label(window, text = " WELCOME TO xyz CINEMAS",  #name needed!
                font = ("Georgia", 20, "bold"), bg = "white")
    heading.pack(pady=30)
    
"""
CINEMA TICKET BOOKING SYSTEM
1. View Movies [show movies]
2. View Show Timings [show timings for a movie - shows table]
3. Check Seat Availability [show screens and show timings and seats]
4. Book Tickets [choose movie, showtime, no of seats, for each seats pick seat type, once things have been updated, display bookingID]
5. Search Booking[bookingID, Name]
6. Cancel Booking [Booking ID, NAME]
7. Exit
-----

"""

def book_tickets():
    ticket_window=tk.Tk()
    ticket_window.geometry("800x800")
    

    
def view_movies():
    pass

def browse_movies():
    clear_window()
    tk.Label(window, text = "NOW SHOWING", 
             font =("Century Gothic", 22, "bold"), bg = "#ffffff").pack(pady=20)

    cursor = db.con.cursor()
    cursor.execute("Select MovieID, Title, Genre, Language_, " \
                   "Duration, Rating, Release_date, Description_ " \
                   "from Movies where Is_active = true")
    
    movies = cursor.fetchall()
def view_shows():
    pass
def check_availability():
    pass
def search_booking():
    pass
def cancel_booking():
    pass
def exit():
    pass
