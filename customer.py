import database as db
import tkinter as tk

con = db.con
cursor = db.con.cursor()

window = tk.Tk()
window.title("Cinema Reservation System")
window.state('zoomed')
window.configure(bg = "white")

top_frame = tk.Frame(window, bg="#ffffff")
top_frame.pack(fill = "x", padx=15, pady=10)

content_frame = tk.Frame(window, bg = "#b4cdef")
content_frame.pack(fill = "both", expand =True)

def clear_content():
    for widget in content_frame.winfo_children():
        widget.destroy()

def customer_menu():
    clear_content()
    heading = tk.Label(content_frame, text = " WELCOME TO xyz CINEMAS",  font = ("Georgia", 20, "bold"), bg = "white")
    heading.pack(pady=30)
    
def book_tickets():
    clear_content()

    tk.Label(content_frame,text="BOOK TICKETS", font=("Century Gothic", 22, "bold"),bg="white").pack(pady=20)
    
def browse_movies():
    clear_content()
    tk.Label(content_frame, text = "NOW SHOWING", font =("Century Gothic", 22, "bold"), bg = "#ffffff").pack(pady=20)

    cursor = db.con.cursor()
    cursor.execute("Select MovieID, Title, Genre, Language_, " \
                   "Duration, Rating, Release_date, Description_ " \
                   "from Movies where Is_active = true")

    
    movies = cursor.fetchall()

    canvas = tk.Canvas(content_frame, bg = "#b4cdef", highlightthickness=0) #Canvas makes it scrollable
    canvas.pack(side ="left", fill= "both", expand = True)
    scrollbar = tk.Scrollbar(content_frame, orient= "vertical", command = canvas.yview) #vertical scrollbar
    scrollbar.pack(side = "right", fill = "y")
    canvas.configure(yscrollcommand = scrollbar.set)

    movie_frame = tk.Frame(canvas, bg = "#1D0555")
    canvas_window = canvas.create_window((0,0), window = movie_frame, anchor = "nw")
    def update_scroll_region(event):
        canvas.configure(scrollregion = canvas.bbox("all"))
    movie_frame.bind("<Configure>", update_scroll_region)

    for column in range(5):
        movie_frame.grid_columnconfigure(column, minsize=250)

    for index, movie in enumerate(movies):
        card = tk.Frame(movie_frame, bg = "#c8a8d4",width= 250, height = 250, relief ="raised", borderwidth = 1 )
        card.grid(row = index//5, column= index%5, padx=10, pady = 10, sticky="n")
        card.grid_propagate(False) #to prevent auto-resizing
        tk.Label(card, text = movie[1], fg="#000000", font = ("Helvetica", 13, "bold"), bg = "#ffd153", wraplength = 220).pack(pady=15)
        tk.Label(card, text = movie[2], fg="#000000", font = ("Courier", 10), bg = "#c8a8d4").pack(pady=5)
        tk.Label(card, text = f"{movie[3]} | {movie[4]}", fg="#000000", font = ("Courier", 10), bg = "#c8a8d4").pack(pady=5)
        tk.Label(card, text = f"Rating: {movie[5]}", fg="#000000", font = ("Arial", 10, "bold"), bg = "#c8a8d4").pack(pady=5)
        tk.Label(card, text = f"Relased: {movie[6]}", fg = "#000000", font = ("Helvetica", 9), bg = "#c8a8d4").pack(pady=5)
        
        
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


book_ticket_button=tk.Button(top_frame, text="Book Tickets", bg="white", command=book_tickets)
view_shows_button=tk.Button(top_frame, text="View Shows", bg="white", command=view_shows)
search_booking_button=tk.Button(top_frame, text="My Booking", bg="white", command=search_booking)
cancel_booking_button=tk.Button(top_frame, text="Cancel Booking", bg="white", command=cancel_booking)
view_movies_button = tk.Button(top_frame, text = "Movies", bg = "white", command = browse_movies)
exit_button = tk.Button(top_frame, text = "Exit", bg = "white", command= window.destroy)


view_movies_button.pack(side="left", padx=5)
view_shows_button.pack(side="left", padx=5)
search_booking_button.pack(side="left", padx=5)
book_ticket_button.pack(side="left", padx=5)
cancel_booking_button.pack(side="left", padx=5)
exit_button.pack(side= "left", padx = 5)

window.mainloop()