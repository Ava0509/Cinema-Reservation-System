import database as db
import tkinter as tk
from tkinter import ttk

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

    tk.Label(content_frame, text = "BOOK TICKETS", font = ("Helvetica",30,"bold"),bg = "#b4cdef").pack(pady=20)
    tk.Label(content_frame, text = "Select a movie:", font = ("Georgia", 16), bg="#b4cdef").pack(pady=5)
    movie_combobox = ttk.Combobox(content_frame, state = "readonly", font = ("Helvetica", 14), width = 35)
    movie_combobox.pack(pady = 5)
    tk.Label(content_frame, text = "Select a date:", font=("Helvetica",14), bg = "#ffffff").pack(pady =(20,5))
    date_combobox = ttk.Combobox(content_frame, state = "readonly", font = ("Helvetica", 14), width = 35)
    date_combobox.pack(pady= 5)
    tk.Label(content_frame, text = "Select a showtime:", font=("Helvetica",14), bg = "#ffffff").pack(pady =(20,5))
    time_combobox = ttk.Combobox(content_frame, state = "readonly", font = ("Helvetica", 14), width = 35)
    time_combobox.pack(pady= 5)
    
    cursor.execute("Select MovieID, Title from Movies where Is_active = true order by title")
    movies = cursor.fetchall()
    movie_dict = {}
    for movie in movies:
        movie_dict[movie[1]] = movie[0]
    movie_combobox["values"] = list(movie_dict.keys())

    def movie_selected(event):
        movie_title = movie_combobox.get()
        movie_id = movie_dict[movie_title]

        cursor.execute("Select distinct Show_date from Shows where MovieID = %s AND Is_active = true and " \
        "Is_booked_out = false order by show_date", (movie_id,))
        dates = cursor.fetchall()
        date_combobox["values"] = [date[0] for date in dates]
        date_combobox.set("")
    movie_combobox.bind("<<ComboboxSelected>>", movie_selected)

    def date_selected(event):
        movie_title = movie_combobox.get()
        movie_id = movie_dict[movie_title]
        selected_date = date_combobox.get()
        cursor.execute("Select Show_time from Shows where MovieID= %s and Show_date = %s and Is_active = true and " \
        "Is_booked_out = false order by show_time", (movie_id, selected_date))
        times = cursor.fetchall()
        time_combobox["values"] = [time[0] for time in times]
        time_combobox.set("")
    date_combobox.bind("<<ComboboxSelected>>", date_selected)

    def select_seats(show_id):
        movie_title = movie_combobox.get()
        selected_date = date_combobox.get()
        selected_time = time_combobox.get()

        if movie_title=="" or selected_date == "" or selected_time =="":
            tk.Label(content_frame, text = "Please select a movie, date and showtime.", font = ("Helvetica", 12, "bold"), bg = "#b4cdef").pack(pady= 10)
            return
        movie_id = movie_dict[movie_title]

        cursor.execute("Select ShowID from Shows where MovieID = %s and Show_date = %s and Show_time = %s and Is_active = true and " \
        "Is_booked_out = false",(movie_id, selected_date, selected_time))
        show = cursor.fetchone()
        if show is None:
            tk.Label(content_frame, text="Sorry, this show is no longer available", font = ("Helvetica", 12, "bold"), bg= "#b4cdef").pack(pady= 10)
            return

        show_id = show[0]

        print("Movie ID: ", movie_id)
        print("Show ID: ", show_id)
        print("Date: ", selected_date)
        print("Time: ", selected_time)


    select_seats_button = tk.Button(content_frame, text = "SELECT SEATS", font = ("Helvetica",14, "bold"), bg = "#ffd153", command = select_seats)
    select_seats_button.pack(pady=20)



    





"""
    heading_label=tk.Label(content_frame, text="Book Tickets", font=("Georgia", 34))
    heading_label.pack(pady=10)

    date_label=tk.Label(content_frame,text="Date:", font=("Arial", 23))
    date_label.pack(pady=10)

    timings_label=tk.Label(content_frame, text="Timings:", font=("Arial", 23))
    timings_label.pack(pady=10)

    movie_entry=tk.Entry(content_frame, font=("Arial", 23))
    movie_entry.pack(pady=10)
    movie_label=tk.Label(content_frame, text="Enter Movie Name:", font=("Arial", 23))
    movie_label.pack(pady=10)

    error_message_check=False
    Invalid_Movie_Label=""

    def timing(a):
        global user_timing
        user_timing=str(a[0])
    
    
    def selection_changed(event):
        selected_label.config(content_frame,text=f"You have selected {event.widget.get()}")

        #making language stuff
        cursor=con.cursor()
        query="select language from movies where movieID=%s"
        cursor.execute(query, tuple(movieID))
        languages=cursor.fetchall()
        for i in range(len(languages)):
            button=tk.Button(content_frame, text=languages[i], font=("Arial", 19), command= lambda l=languages[i]: language(l))
            button.pack(pady=10)
        
    
    
    def submit():
        movie=movie_entry.get()
        #movie_entry.delete(0,tk.END)

        nonlocal Invalid_Movie_Label

        cursor=con.cursor()
        movieID_query="select movieID from movies where title=%s"
        cursor.execute(movieID_query, (movie, ))
        global movieID
        movieID=cursor.fetchone()
        if movieID!=None:
            show_date_query="select show_date from shows where movieID=%s"
            cursor.execute(show_date_query, tuple(movieID))
            global show_dates
            show_dates=cursor.fetchall()
        else:
            show_dates=[]

        if show_dates!=[]:
            nonlocal error_message_check
            if error_message_check==True:
                Invalid_Movie_Label.destroy()
            date_combobox=ttk.Combobox(content_frame, values=show_dates, font=("Helvetica", 23))
            date_combobox.set(show_dates[0])
            date_combobox.bind("<<ComboboxSelected>>", selection_changed)
            date_combobox.pack(pady=10)

            global selected_label
            selected_label = tk.Label(content_frame, text=f"You have selected ---")
            selected_label.pack(pady=10)
        else:
            Invalid_Movie_Label=tk.Label(content_frame, text="Sorry, The movie you have entered does not exist, \nPlease try again", font=("Helvetica", 17))
            Invalid_Movie_Label.pack(pady=10)

            error_message_check=True

    submit_button=tk.Button(text="submit", command=submit)
    submit_button.pack(pady=10)

"""
       
def view_shows(movie_id):
    clear_content()
    
    cursor.execute("Select title, Genre, Language_, Duration, Rating, Release_date, Description_ from Movies where movieid = %s",(movie_id,))
    details = cursor.fetchone()

    tk.Label(content_frame,
             text = f"SHOW TIMINGS", font = ("Century Gothic", 22,"bold"), bg = "#eeeeee").pack(pady=20)
    tk.Label(content_frame, text = details[0],font = ("Century Gothic", 24,"bold"), bg = "#e3bb8e").pack(pady = 15)
    tk.Label(content_frame, text=f"{details[1]} | {details[2]} | {details[3]} minutes", font=("Helvetica",11), bg="#ffffff").pack(pady=5)
    tk.Label(content_frame, text = f"Rating: {details[4]}", font = ("Helvetica", 11, "bold"), bg ="#ffffff").pack(pady=5)
    tk.Label(content_frame, text= f"Release Date: {details[5]}", font = ("Helvetica", 10), bg = "#ffffff").pack(pady=5)
    tk.Label(content_frame, text = details[6], font = ("Helvetica", 10), bg= "#ffffff" , wraplength=650, justify = "center").pack(padx=20, pady=15)


    cursor.execute("Select ShowID, ScreenID, show_date, show_time from Shows " \
        "where MovieID = %s and Is_active = true and Is_booked_out = false order by Show_date, show_time",(movie_id,))
    shows = cursor.fetchall()
    for show in shows:
        show_frame = tk.Frame(content_frame, bg = "#caedcb", relief = "raised", borderwidth=1)
        show_frame.pack(padx=10,pady=10)
        tk.Label(show_frame, text = f"Screen {show[1]}", font=("Helvetica",12,"bold"), bg = "#caedcb").pack(side = "left", padx=20, pady= 20)
        tk.Label(show_frame, text = f"{show[2]} | {show[3]}", font = ("Helvetica",11), bg= "#caedcb").pack(side="left", padx= 20)

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
        tk.Label(card, text = f"{movie[3]} | {movie[4]} minutes", fg="#000000", font = ("Courier", 10), bg = "#c8a8d4").pack(pady=5)
        tk.Label(card, text = f"Rating: {movie[5]}", fg="#000000", font = ("Arial", 10, "bold"), bg = "#c8a8d4").pack(pady=5)
        tk.Label(card, text = f"Relased: {movie[6]}", fg = "#000000", font = ("Helvetica", 9), bg = "#c8a8d4").pack(pady=5)

        tk.Button(card, text = "VIEW Shows", bg = "#ffd153", command = lambda movie_id = movie[0]: view_shows(movie_id)).pack(pady=10)
        
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