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

    window=tk.Tk()
    window.title("Book Ticket")
    window.geometry("800x500")
    heading_label=tk.Label(text="Booking Tickets", font=("Georgia", 34))
    heading_label.grid(row=1, column=0)

    date_label=tk.Label(text="Date:", font=("Arial", 23))
    date_label.grid(row=3, column=0)

    select_Language_label=tk.Label(window, text="Select Language:", font=("Arial", 23))
    select_Language_label.grid(row=5, column=0)

    timings_label=tk.Label(window, text="Timings:", font=("Arial", 23))
    timings_label.grid(row=8, column=0)

    movie_entry=tk.Entry(window, font=("Arial", 23))
    movie_entry.grid(row=2, column=1)
    movie_label=tk.Label(window, text="Enter Movie Name:", font=("Arial", 23))
    movie_label.grid(row=2, column=0)

    error_message_check=False
    Invalid_Movie_Label=""

    def timing(a):
        global user_timing
        user_timing=str(a[0])
    
    def language(a):
        global user_language
        user_language=a[0]
        
        cursor=con.cursor()
        query="select show_time from shows where movieID=%s"
        cursor.execute(query, tuple(movieID))
        timings=cursor.fetchall()
        for i in range(len(timings)):
            button=tk.Button(window, text=timings[i], font=("Arial", 19), command= lambda t=timings[i]: timing(t))
            button.grid(row=9, column=i)
    
    def selection_changed(event):
        selected_label.config(text=f"You have selected {event.widget.get()}")

        #making language stuff
        cursor=con.cursor()
        query="select language from movies where movieID=%s"
        cursor.execute(query, tuple(movieID))
        languages=cursor.fetchall()
        for i in range(len(languages)):
            button=tk.Button(window, text=languages[i], font=("Arial", 19), command= lambda l=languages[i]: language(l))
            button.grid(row=6, column=i)
        
    
    
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
            date_combobox=ttk.Combobox(window, values=show_dates, font=("Helvetica", 23))
            date_combobox.set(show_dates[0])
            date_combobox.bind("<<ComboboxSelected>>", selection_changed)
            date_combobox.grid(row=3, column=1)

            global selected_label
            selected_label = tk.Label(window, text=f"You have selected ---")
            selected_label.grid(row=4, column=1)
        else:
            Invalid_Movie_Label=tk.Label(window, text="Sorry, The movie you have entered does not exist, \nPlease try again", font=("Helvetica", 17))
            Invalid_Movie_Label.grid(row=6, column=0)

            error_message_check=True

    submit_button=tk.Button(text="submit", command=submit)
    submit_button.grid(row=2, column=2)


       
def view_shows(movie_id):
    clear_content()
    
    cursor.execute("Select title, Genre, Language_, Duration, Rating, Release_date, Description_ from Movies where movieid = %s",(movie_id,))
    details = cursor.fetchone()

    tk.Label(content_frame,
             text = f"SHOW TIMINGS", font = ("Century Gothic", 22,"bold"), bg = "white").pack(pady=20)
    tk.Label(content_frame, text = details[0],font = ("Century Gothic", 24,"bold"), bg = "#e3bb8e").pack(pady = 15)
    tk.Label(content_frame, text=f"{details[1]} | {details[2]} | {details[3]} minutes", font=("Helvetica",11), bg="#ffffff").pack(pady=5)
    tk.Label(content_frame, text = f"Rating: {details[4]}", font = ("Helvetica", 11, "bold"), bg ="#ffffff").pack(pady=5)
    tk.Label(content_frame, text= f"Release Date: {details[5]}", font = ("Helvetica", 10), bg = "#ffffff").pack(pady=5)
    tk.Label(content_frame, text = details[6], font = ("Helvetica", 10), bg= "#ffffff" , wraplength=650, justify = "center").pack(padx=20, pady=15)


    cursor.execute("Select ShowID, ScreenID, show_date, show_time from Shows " \
        "where MovieID = %s and Is_active = true and Is_booked_out = false order by Show_date, show_time",(movie_id,))
    shows = cursor.fetchall()
    for show in shows:
        show_frame = tk.Frame(content_frame, bg = "#ffffff", relief = "raised", borderwidth=1)
        show_frame.pack(padx=10,pady=10)
        tk.Label(show_frame, text = f"Screen {show[1]}", font=("Helvetica",12,"bold"), bg = "white").pack(side = "left", padx=20, pady= 20)
        tk.Label(show_frame, text = f"{show[2]} | {show[3]}", font = ("Helvetica",11), bg= "white").pack(side="left", padx= 20)

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