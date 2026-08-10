import database as db
import tabulate as tb
import tkinter as tk

con = db.con
cursor = db.con.cursor()

window = tk.Tk()
window.title("Cinema Reservation System")
window.geometry("600X500")
window.configure(bg = "white")



def clear_window():
    for widget in window.winfo_children():
        widget.destroy()

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
    pass
def view_movies():
    pass

def browse_movies():
    clear_window()
    tk.Label(window, text = "NOW SHOWING", 
             font =("Century Gothic", 22, "bold"), bg = "white").pack(pady=20)

    cursor = db.con.cursor()
    cursor.execute("Select MovieID, Genre, Language_, " \
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
