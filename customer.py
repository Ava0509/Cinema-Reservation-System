import database as db
import tkinter as tk
from tkinter import ttk, messagebox
import Seat_selection as SS
import hashlib

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

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

    def select_seats():
        movie_title = movie_combobox.get()
        selected_date = date_combobox.get()
        selected_time = time_combobox.get()

        if movie_title=="" or selected_date == "" or selected_time =="":
            messagebox.showwarning("Incomplete selection",
                                   "Please select a movie, date and showtime.")
            return
        movie_id = movie_dict[movie_title]

        cursor.execute("Select ShowID from Shows where MovieID = %s and Show_date = %s and Show_time = %s and Is_active = true and " \
        "Is_booked_out = false",(movie_id, selected_date, selected_time))
        show = cursor.fetchone()
        if show is None:
            tk.Label(content_frame, text="Sorry, this show is no longer available", font = ("Helvetica", 12, "bold"), bg= "#b4cdef").pack(pady= 10)
            return

        show_id = show[0]
        def show_booking_summary(selected_seats, show_id):
            summary_window = tk.Toplevel(window)
            summary_window.title("Booking Summary")
            summary_window.geometry("500x600")
            summary_window.grab_set()

            tk.Label(summary_window, text= "BOOKING SUMMARY", font = ("Times New Roman", 24, "bold")).pack(pady = 20)
            tk.Label(summary_window, text = f"Movie: {movie_title}", font = ("Georgia", 13)).pack(pady =5)
            tk.Label(summary_window, text = f"Date: {selected_date}", font = ("Georgia", 13)).pack(pady =5)
            tk.Label(summary_window, text = f"Time: {selected_time}", font = ("Georgia", 13)).pack(pady =5)
            tk.Label(summary_window, text = f"Seats: {", ".join(selected_seats)}", font = ("Georgia", 13)).pack(pady =5)

            tk.Label(summary_window, text = "CUSTOMER DETAILS", font = ("Helvetica", 18, "bold")).pack(pady=(25, 10))
            tk.Label(summary_window, text="Already have an account? Log in.\nNew customer? Register below.", font=("Courier", 11, "bold")).pack(pady=5)

            def customer_login()
                login_window = tk.Toplevel(summary_window)
                login_window.title("Customer Login")
                login_window.geometry("450x350")
                login_window.grab_set()

                tk.Label(login_window, text = "CUSTOMER LOGIN", font= ("Times New Roman", 22, "bold")).pack(pady=20)
                tk.Label(login_window, text = "Phone or Email:",  font=("Helvetica", 12)).pack(pady=5)
                login_identifier = tk.Entry(login_window, width=35,font=("Helvetica", 12))
                login_identifier.pack(pady=5)
                tk.Label(login_window, text = "Passkey: ", font=("Helvetica", 12)).pack(pady=5)
                login_passkey = tk.Entry(login_window, width=35, font = ("Helvetica", 12), show"*")
                login_passkey.pack(pady=5)

                def login():
                    identifier = login_identifier.get().strip()
                    entered_passkey = login_passkey.get()
                    if identifier == "" or entered_passkey == "":
                        messagebox.showwarning("Missing Information", "Please enter your phone/email and passkey.",parent=login_window)
                        return

                    try:
                        cursor.execute("SELECT CustomerID, Passkey_hash FROM Customers WHERE Phone = %s OR Email = %s", (identifier, identifier))
                        customer = cursor.fetchone()
                        if customer is None:
                            messagebox.showerror("Customer Not Found","No account was found with that phone/email.",parent = login_window)
                            return
                        customer_id = customer[0]
                        stored_hash = customer[1]

                        if hash_passkey(entered_passkey) != stored_hash:
                            messagebox.showerror("Invalid Passkey","The phone/email and passkey do not match.",parent=login_window)
                            return
                        login_window.destroy()
                        create_booking(customer_id)

                    except:
                        messagebox.showerror("Login Error",f"Unable to log in.\n\n{e}", parent=login_window)

                tk.Button(login_window,text="LOGIN", font=("Helvetica", 12, "bold"),  bg="#ffd153",, width = 15, command=login).pack(pady=20)
                tk.Button(login_window,text="I'M NEW", font=("Helvetica", 12, "bold"),  bg="#ffd153",, width = 15, command=lambda: [login_window.destroy(), customer_registration()]).pack(pady=20)

             def customer_registration():
                register_window = tk.Toplevel(summary_window)
                register_window.title("Customer Registration")
                register_window.geometry("500x600")
                register_window.grab_set()

                tk.Label(register_window, text = "CUSTOMER REGISTRATION", font=("Times New Roman", 22, "bold")).pack(pady=20)
                tk.Label(register_window, text="First Name:").pack()
                first_name = tk.Entry(register_window, width=35)
                first_name.pack(pady=5)
                tk.Label(register_window, text="Last Name:").pack()
                last_name = tk.Entry(register_window, width=35)
                last_name.pack(pady=5)

                tk.Label(register_window, text="Phone or Email:", font=("Helvetica", 11, "bold")).pack(pady=(10, 3))

            tk.Label(summary_window, text = "Please enter your details:", font=("Courier", 13, "bold")).pack(pady = 5)

            tk.Label(summary_window, text = "First Name: ").pack()
            first_name = tk.Entry(summary_window,width = 35)
            first_name.pack(pady=5)

            tk.Label(summary_window, text = "Last Name: ").pack()
            last_name = tk.Entry(summary_window,width = 35)
            last_name.pack(pady=5)

            tk.Label(summary_window, text = "Phone: ").pack()
            phone = tk.Entry(summary_window,width = 35)
            phone.pack(pady=5)

            tk.Label(summary_window, text = "Email: ").pack()
            email = tk.Entry(summary_window,width = 35)
            email.pack(pady=5)

            tk.Label(summary_window, text="Passkey: ").pack()
            passkey = tk.Entry(summary_window, width=35, show="*")
            passkey.pack(pady=5)

            tk.Label(summary_window, text="Confirm Passkey: ").pack()
            confirm_passkey = tk.Entry(summary_window, width=35, show="*")
            confirm_passkey.pack(pady=5)

            total_amount= 0
            for seat in selected_seats:
                row=seat[0]
                if row in ["A","B", "C", "D"]:
                    total_amount +=50
                elif row in ["E", "F", "G", "H"]:
                    total_amount+=80
                else:
                    total_amount +=150
            tk.Label(summary_window, text = f"Total Amount: AED {total_amount:.2f}", font = ("Georgia", 16, "bold")).pack(pady = 15)

            def confirm_booking():
                first = first_name.get().strip()
                last = last_name.get().strip()
                phone_number = phone.get().strip()
                email_address = email.get().strip()
                customer_passkey = passkey.get()
                confirmed_passkey = confirm_passkey.get()

                if first == "" or last == "" or phone_number == "" or email_address == "" or customer_passkey == "" or confirmed_passkey == "":
                    messagebox.showwarning("Missing Details",
                                           "Please enter all details.")
                    return

                if customer_passkey != confirmed_passkey:
                    messagebox.showwarning("Passkey Mismatch", "Please make sure both passkey fields are identical.")
                    return

                try:
                    cursor.execute("Select CustomerID, Passkey_hash from Customers where Phone = %s", (phone_number,))
                    customer = cursor.fetchone()

                    if customer is not None:
                        customer_id = customer[0]
                        stored_hash = customer[1]

                        if hash_passkey(customer_passkey) != stored_hash:
                            messagebox.showerror("Invalid Passkey", "The phone number and passkey do not match.")
                            return
                        
                    else:
                        passkey_hash = hash_passkey(customer_passkey)
                        cursor.execute("Insert into Customers (First_name, Last_name, Phone, Email, Passkey_hash) values(%s, %s, %s, %s,%s)", (first, last, phone_number,email_address, passkey_hash))
                        customer_id = cursor.lastrowid

                    cursor.execute("Insert into Bookings (CustomerID, ShowID, Booking_date, Total_amount, Booking_status)" \
                    "value(%s, %s, now(),%s,%s)", (customer_id, show_id, total_amount,"Confirmed"))
                    booking_id = cursor.lastrowid

                    for seat in selected_seats:
                        cursor.execute("Select SeatID from Seats where ScreenID = (Select ScreenID from Shows where ShowID = %s) and seat_number = %s",
                                    (show_id, seat))
                        seat_result = cursor.fetchone()

                        if seat_result is not None:
                            seat_id = seat_result[0]
                            cursor.execute("Insert into BookingSeats (BookingID, SeatID) values (%s,%s)", (booking_id, seat_id))

                    cursor.execute("Select count(*) from Seats where ScreenID = (Select ScreenID from Shows where ShowID = %s)", (show_id,))
                    total_seats = cursor.fetchone()[0]
                    cursor.execute("Select count(*) from BookingSeats bs join Bookings b on bs.BookingID = b.BookingID where b.ShowID = %s and b.Booking_status = 'Confirmed'", (show_id,))
                    booked_seats = cursor.fetchone()[0]
                    if booked_seats == total_seats:
                        cursor.execute("Update Shows set Is_booked_out = True where ShowID = %s", (show_id,))

                    con.commit()

                    messagebox.showinfo(
                        "Booking Confirmed",
                        f"Your booking has been confirmed!\n\n"
                        f"Booking ID: {booking_id}\n"
                        f"Total Amount: AED {total_amount:.2f}")
                    summary_window.destroy()

                except Exception as e:
                    con.rollback()
                    messagebox.showerror("Booking Error", f"Unable to complete the booking.\n\n{e}")

            button_frame = tk.Frame(summary_window)
            button_frame. pack(pady =25)
            tk.Button(button_frame, text ="CANCEL", font = ("Helvetica", 12, "bold"), bg = "#fD8383", width = 12, command= summary_window.destroy).pack(side= "left", padx = 10)
            tk.Button(button_frame, text = "CONFIRM", font = ("Helvetica", 12, "bold"), bg = "#ffd153", width =12, command = confirm_booking ).pack(side = "left", padx=10)
        SS.select_seats(show_id, show_booking_summary)
        
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
        show_frame = tk.Frame(content_frame, bg = "#ffffff", relief = "raised", borderwidth=1)
        show_frame.pack(padx=10,pady=10)
        tk.Label(show_frame, text = f"Screen {show[1]}", font=("Helvetica",12,"bold"), bg = "#ffffff").pack(side = "left", padx=20, pady= 20)
        tk.Label(show_frame, text = f"{show[2]} | {show[3]}", font = ("Helvetica",11), bg= "#ffffff").pack(side="left", padx= 20)

def view_movies():
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
        
def search_booking():
    clear_content()

    tk.Label(content_frame, text = "MY BOOKINGS", font = ("Helvetica", 30, "bold"), bg = "#b4cdef").pack(pady = 25)
    tk.Label(content_frame, text = "Enter your phone number:", font= ("Georgia", 16),bg= "#b4cdef").pack(pady= 10)
    phone_entry = tk.Entry(content_frame, font= ("Helvetica",14), width=30)
    phone_entry.pack(pady= 5)

    def search():
        phone_number = phone_entry.get().strip()
        if phone_number == "":
            messagebox.showwarning("Missing Information", "Please enter your phone number.")
            return
        cursor.execute("Select CustomerID, First_name, Last_name from Customers where phone= %s ", (phone_number,))
        customer = cursor.fetchone()

        if customer is None:
            messagebox.showwarning("Booking not found", "No customer was found with this phone number.")
            return
        customer_id = customer[0]

        cursor.execute("Select b.BookingID, m.Title, s.Show_date, s.Show_time, b.Total_amount, b.Booking_status from Bookings b " \
        "join Shows s on b.ShowID = s.ShowID join Movies m on s.MovieID = m.MovieID where CustomerID = %s order by b.Booking_date desc",
        (customer_id,))
        bookings = cursor.fetchall()

        if not bookings:
            messagebox.showinfo("No Bookings", "You do not have any bookings")
            return

        results_frame = tk.Frame(content_frame, bg= "#b4cdef")
        results_frame.pack(fill="both", expand = True, padx=30, pady=10)
        
        for widget in results_frame.winfo_children():
            widget.destroy()

        tk.Label(results_frame, text= f"Booking for {customer[1]} {customer[2]}", font =("Helvetica", 18, "bold"), bg = "#ffffff").pack(pady= 15)

        for booking in bookings:
            booking_id= booking[0]
            cursor.execute("Select se.Seat_number from BookingSeats bs join Seats se on bs.SeatID= se.SeatID where bs.BookingID= %s " \
            "order by se.Seat_number", (booking_id,))
            seats= cursor.fetchall()
            seat_list= ", ".join([seat[0] for seat in seats])

            booking_frame = tk.Frame(results_frame, bg = "#ffffff", relief= "raised", borderwidth =2)
            booking_frame.pack(padx = 30, pady=10, fill="x")
            tk.Label(booking_frame, text = f"Booking ID: {booking_id}", font = ("Helvetica", 14, "bold"), bg ="#ffffff").pack(anchor="w", padx =20, pady=5)
            tk.Label(booking_frame, text=f"Movie: {booking[1]}", font=("Georgia", 12), bg="#ffffff").pack(anchor="w", padx=20, pady=3)
            tk.Label(booking_frame, text=f"Date: {booking[2]}", font=("Georgia", 12), bg="#ffffff").pack(anchor="w", padx=20, pady=3)
            tk.Label(booking_frame, text=f"Time: {booking[3]}", font=("Georgia", 12), bg="#ffffff").pack(anchor="w", padx=20, pady=3)
            tk.Label(booking_frame, text=f"Seats: {seat_list}", font=("Georgia", 12), bg="#ffffff").pack(anchor="w", padx=20, pady=3)
            tk.Label(booking_frame, text=f"Total Amount: AED {booking[4]:.2f}", font=("Georgia", 12), bg="#ffffff").pack(anchor="w", padx=20, pady=3)
            tk.Label(booking_frame, text=f"Status: {booking[5]}", font=("Helvetica", 12, "bold"), bg="#ffffff").pack(anchor="w", padx=20, pady=3)

    tk.Button(content_frame, text= "SEARCH", font= ("Helvetica", 14, "bold"), bg="#ffd153", width= 15, command =search).pack(pady= 15)

def cancel_booking():
    clear_content()

    tk.Label(content_frame, text = "CANCEL BOOKING", font = ("Helvetica", 30, "bold"), bg= "#b4cdef").pack(pady=25)
    tk.Label(content_frame, text ="Enter your phone number:" , font= ("Georgia", 16), bg = "#b4cdef").pack(pady=10)
    phone_entry= tk.Entry(content_frame, font = ("Helvetica", 14), width= 30)
    phone_entry.pack(pady=5)

    def find_booking():
        phone_number = phone_entry.get().strip()


        if booking_id == "" or phone_number == "":
            messagebox.showwarning("Missing Information", "Please enter both Booking ID and phone number.")
            return
    
def exit():
    pass


book_ticket_button=tk.Button(top_frame, text="Book Tickets", bg="white", command=book_tickets)
view_shows_button=tk.Button(top_frame, text="View Shows", bg="white", command=view_shows)
search_booking_button=tk.Button(top_frame, text="My Booking", bg="white", command=search_booking)
cancel_booking_button=tk.Button(top_frame, text="Cancel Booking", bg="white", command=cancel_booking)
view_movies_button = tk.Button(top_frame, text = "Movies", bg = "white", command = view_movies)
exit_button = tk.Button(top_frame, text = "Exit", bg = "white", command= window.destroy)


view_movies_button.pack(side="left", padx=5)
view_shows_button.pack(side="left", padx=5)
search_booking_button.pack(side="left", padx=5)
book_ticket_button.pack(side="left", padx=5)
cancel_booking_button.pack(side="left", padx=5)
exit_button.pack(side= "left", padx = 5)

window.mainloop()