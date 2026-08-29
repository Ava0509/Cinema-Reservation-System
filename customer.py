import database as db
import tkinter as tk
from tkinter import ttk, messagebox
import Seat_selection as SS
import hashlib

def hash_passkey(passkey):
    return hashlib.sha256(passkey.encode()).hexdigest()

con = db.con
cursor = db.con.cursor()
logged_in = False
logged_in_customer_id = None


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

def home():
    clear_content()

    tk.Label(content_frame, text = "WELCOME TO ALTAIR CINEMAS", font =("Georgia", 30, "bold"), bg= "#b4cdef").pack(pady=80)


def customer_login(on_success=None, parent=window):
    global logged_in
    global logged_in_customer_id

    if logged_in:
        if on_success is not None:
            on_success(logged_in_customer_id)
        else:
            messagebox.showinfo("LOGIN STATE","You are logged in.")
        return

    login_window = tk.Toplevel(parent)
    login_window.title("Customer Login")
    login_window.geometry("450x350")
    login_window.grab_set()

    tk.Label(login_window, text="CUSTOMER LOGIN", font=("Times New Roman", 22, "bold")).pack(pady=20)
    tk.Label(login_window, text="Phone or Email:", font=("Helvetica", 12)).pack(pady=5)
    login_identifier = tk.Entry(login_window, width=35, font=("Helvetica", 12))
    login_identifier.pack(pady=5)
    tk.Label(login_window, text = "Passkey", font=("Helvetica", 12)).pack(pady =5)
    login_passkey = tk.Entry(login_window, width=35, font=("Helvetica", 12), show="*")
    login_passkey.pack(pady=5)

    def login():
        global logged_in
        global logged_in_customer_id
        identifier = login_identifier.get().strip()
        entered_passkey = login_passkey.get()

        if identifier == "" or entered_passkey == "":
            messagebox.showwarning("Missing Information", "Please enter your phone/email and passkey.", parent = login_window)
            return

        try:
            cursor.execute("Select CustomerID, First_name, Last_name, Passkey_hash from Customers where Phone = %s or Email =%s", 
                           (identifier,identifier)) 
            customer = cursor.fetchone()

            if customer is None:
                messagebox.showerror("Customer Not Found", "No account was found with that phone/email.", parent=login_window)
                return
            customer_id = customer[0]
            first_name = customer[1]
            last_name = customer[2]
            stored_hash = customer[3]
            if hash_passkey(entered_passkey) != stored_hash:
                messagebox.showerror("Invalid Passkey", "The phone/email and passkey do not match",parent = login_window)
                return

            logged_in = True
            logged_in_customer_id = customer_id
            login_window.destroy()
            login_button.config(text = f"ID: {logged_in_customer_id}", state = "disabled")
            messagebox.showinfo("Login Successful", f"You have been logged in as {first_name} {last_name}.")

            if on_success is not None:
                on_success(customer_id)

        except Exception as e:
            messagebox.showerror("Login Error", f"Unable to log in. \n\n{e}", parent = login_window)

    tk.Button(login_window, text = "LOGIN", font =("Helvetica", 12, "bold"), bg= "#ffd153", width = 20, command = login).pack(pady=20)
    tk.Button(login_window, text = "CANCEL", font=("Helvetica", 11), bg="#fd8383", width=20, command=login_window.destroy).pack()

'''
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
            tk.Label(content_frame, text="Sorry, this show is no longer available", font = ("Helvetica", 12, "bold"), bg= "#b4cdef"
                     ).pack(pady= 10)
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
            seat_list = ", ".join(selected_seats)
            tk.Label(summary_window, text = f"Seats: {seat_list}", font = ("Georgia", 13)).pack(pady =5)

            total_amount = 0
            for seat in selected_seats:
                row = seat[0]

                if row in ["A", "B", "C", "D"]:
                    total_amount += 50
                elif row in ["E", "F", "G", "H"]:
                    total_amount += 80
                elif row in ["I", "J", "K", "L"]:
                    total_amount += 150
            tk.Label(summary_window, text = f"Total: AED {total_amount:.2f}", font=("Georgia", 13, "bold")).pack(pady = 10)
            tk.Label(summary_window, text = "CUSTOMER DETAILS", font = ("Helvetica", 18, "bold")).pack(pady=(25, 10))
            tk.Label(summary_window, text="Already have an account? Press continue.\nNew customer? Register below (Press \"I'M NEW\").", font=("Courier", 11, "bold")
                     ).pack(pady=5)

            button_frame_2 = tk.Frame(summary_window)
            button_frame_2.pack(pady = 25)
            tk.Button(button_frame_2, text="CONTINUE",font=("Helvetica", 12, "bold"),bg="#ffd153",width=12,command=lambda: customer_login(on_success=lambda customer_id: create_booking(customer_id),parent=summary_window)).pack(side="left", padx=10)
            tk.Button(button_frame_2,text="I'M NEW", font=("Helvetica", 12, "bold"),  bg="#ffd153", width = 15, command=lambda: customer_registration()).pack(pady=20)

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
                tk.Label(register_window, text="Enter at least one. You may provide both.").pack()
                phone = tk.Entry(register_window, width=35)
                phone.pack(pady=5)

                email = tk.Entry(register_window, width=35)
                email.pack(pady=5)

                tk.Label(register_window, text="Passkey:").pack(pady=(10, 3))
                new_passkey = tk.Entry(register_window, width = 35, show="*")
                new_passkey.pack(pady=5)
                tk.Label(register_window, text="Confirm Passkey:").pack()
                confirm_passkey = tk.Entry(register_window, width = 35, show="*")
                confirm_passkey.pack(pady=5)

                def register():
                    first = first_name.get().strip()
                    last = last_name.get().strip()
                    phone_number = phone.get().strip()
                    email_address = email.get().strip()
                    password = new_passkey.get()
                    confirmed_password = confirm_passkey.get()

                    if first == "" or last == "":
                        messagebox.showwarning("Missing Details","Please enter your first and last name.",parent=register_window)
                        return
                    if phone_number == "" and email_address == "":
                        messagebox.showwarning("Missing Contact Details","Please enter either a phone number or an email.",parent=register_window)
                        return
                    if password == "" or confirmed_password == "":
                        messagebox.showwarning("Missing Passkey","Please enter and confirm your passkey.",parent=register_window)
                        return
                    if password != confirmed_password:
                        messagebox.showwarning("Passkey Mismatch","Both passkey fields must be identical.",parent=register_window)
                        return

                    try:
                        cursor.execute("Select CustomerID from Customers where Phone =%s or Email = %s",
                                       (phone_number if phone_number != "" else None, email_address if email_address != "" else None)) 
                        existing_customer = cursor.fetchone()
                        if existing_customer is not None:
                            messagebox.showerror("Account Already Exists", "An account already exists with this phone/email.\nPlease use the " \
                            "login option instead.", parent = register_window)
                            return
                        passkey_hash = hash_passkey(password)
                        cursor.execute("Insert into Customers (First_name, Last_name, Phone, Email, Passkey_hash) values (%s, %s, %s, %s, %s)", 
                                       (first, last, phone_number if phone_number!="" else None, email_address if email_address != "" else None, 
                                        passkey_hash))
                        customer_id = cursor.lastrowid
                        con.commit()
                        register_window.destroy()

                        messagebox.showinfo("Registration Successful", "Your account has been created successfully!", parent= summary_window)
                        create_booking(customer_id)

                    except Exception as e:
                        con.rollback()
                        messagebox.showerror("Registration Error", f"Unable to create your account.\n\n{e}", parent = summary_window)

                tk.Button(register_window, text="REGISTER", font=("Helvetica", 12, "bold"), bg="#ffd153", width =15, command = register
                          ).pack(pady=20)
                tk.Button(register_window, text = "Cancel", font=("Helvetica", 11), bg= "#fd8383", width= 15, command=register_window.destroy
                          ).pack()

            def create_booking(customer_id):

                try:
                    cursor.execute("Insert into Bookings (CustomerID, ShowID, Booking_date, Total_amount, Booking_status) " \
                    "values (%s, %s, now(), %s,%s)", (customer_id, show_id, total_amount, "Confirmed"))
                    booking_id = cursor.lastrowid

                    for seat in selected_seats:
                        cursor.execute("Select SeatID from Seats where ScreenID = (Select ScreenID from Shows where ShowID = %s) " \
                        "and Seat_number = %s", (show_id, seat))
                        seat_result =cursor.fetchone()
                        if seat_result is not None:
                            seat_id = seat_result[0]
                            cursor.execute("Insert into BookingSeats (BookingID, SeatID) values (%s, %s)", (booking_id, seat_id))

                    cursor.execute("Select count(*) from BookingSeats bs join Bookings b on bs.BookingID = b.BookingID where b.ShowID = %s " \
                    "and b.Booking_status = 'Confirmed'", (show_id,))
                    booked_seats = cursor.fetchone()[0]
                    if booked_seats >= 120:
                        cursor.execute("Update Shows set Is_booked_out = True where ShowID = %s", (show_id,))
                    con.commit()

                    messagebox.showinfo("Booking Confirmed", f"Your booking has been confirmed!\n\n"
                                        f"Booking ID: {booking_id}\nTotal Amount: AED {total_amount:.2f}", parent = summary_window)
                    summary_window.destroy()

                except Exception as e:
                    con.rollback()
                    messagebox.showerror("Booking Error", f"Unable to complete booking.\n\n{e}", parent = summary_window)

            
            tk.Button(button_frame_2, text = "CANCEL", font =("Helvetica", 12, "bold"), bg= "#fd8383", width =12, 
                      command = summary_window.destroy).pack(side='left', padx = 10)
            tk.Button(button_frame_2, text = "CONTINUE", font =("Helvetica", 12, "bold"), bg= "#ffd153", width =12, 
                      command = customer_login).pack(side='left', padx = 10)
        
    select_seats_button = tk.Button(content_frame, text = "SELECT SEATS", font = ("Helvetica",14, "bold"), bg = "#ffd153", 
                                    command = select_seats)
    select_seats_button.pack(pady=20)
'''

def start_booking(show_id):
    cursor.execute("Select m.Title, s.Show_date, s.Show_time, s.ScreenID from Shows s join Movies m ON s.MovieID = m.MovieID where s.ShowID = %s AND s.Is_active = true AND s.Is_booked_out = false", (show_id,))
    show= cursor.fetchone()

    if show is None:
        messagebox.showerror("Show Unavailable","Sorry, this show is no longer available.")
        return

    movie_title = show[0]
    show_date = show[1]
    show_time = show[2]
    screen_id = show[3]

    def show_booking_summary(selected_seats, show_id):
        summary_window = tk.Toplevel(window)
        summary_window.title("Booking Summary")
        summary_window.geometry("500x600")
        summary_window.grab_set()

        tk.Label(summary_window, text= "BOOKING SUMMARY", font = ("Times New Roman", 24, "bold")).pack(pady = 20)
        tk.Label(summary_window, text = f"Movie: {movie_title}", font = ("Georgia", 13)).pack(pady =5)
        tk.Label(summary_window, text=f"Date: {show_date}", font=("Georgia", 13)).pack(pady=5)
        tk.Label(summary_window, text=f"Time: {show_time}", font=("Georgia", 13)).pack(pady=5)
        seat_list = ", ".join(selected_seats)
        tk.Label(summary_window, text = f"Seats: {seat_list}", font = ("Georgia", 13)).pack(pady =5)
        tk.Label(summary_window, text = "CUSTOMER DETAILS", font = ("Helvetica", 18, "bold")).pack(pady=(25, 10))

        tk.Label(summary_window, text="Already have an account? Press continue.\nNew customer? Register below (Press \"I'M NEW\").", font=("Courier", 11, "bold")
                    ).pack(pady=5)

        button_frame = tk.Frame(summary_window)
        button_frame.pack(pady=25)
        tk.Button(button_frame, text="CONTINUE",font=("Helvetica", 12, "bold"),bg="#ffd153",width=12,command=lambda: customer_login(on_success=lambda customer_id: create_booking(customer_id),parent=summary_window)).pack(side="left", padx=10)
        tk.Button(button_frame,text="I'M NEW", font=("Helvetica", 12, "bold"),  bg="#ffd153", width = 15, command=lambda: customer_registration()).pack(pady=20)
        total_amount = 0

        for seat in selected_seats:
            row = seat[0]
            if row in ["A", "B", "C", "D"]:
                total_amount += 50
            elif row in ["E", "F", "G", "H"]:
                total_amount += 80
            elif row in ["I", "J", "K", "L"]:
                total_amount += 150

        tk.Label(summary_window, text=f"Total: AED {total_amount:.2f}", font=("Georgia", 13, "bold")).pack(pady= 10)

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

            tk.Label(register_window, text="Phone number:", font=("Helvetica", 11, "bold")).pack(pady=(10, 3))
            tk.Label(register_window, text="Enter at least one. You may provide both.").pack()
            phone = tk.Entry(register_window, width=35)
            phone.pack(pady=5)

            tk.Label(register_window, text="Email:", font=("Helvetica", 11, "bold")).pack(pady=(5, 3))
            email = tk.Entry(register_window, width=35)
            email.pack(pady=5)

            tk.Label(register_window, text="Passkey:").pack(pady=(10, 3))
            new_passkey = tk.Entry(register_window, width = 35, show="*")
            new_passkey.pack(pady=5)
            tk.Label(register_window, text="Confirm Passkey:").pack()
            confirm_passkey = tk.Entry(register_window, width = 35, show="*")
            confirm_passkey.pack(pady=5)

            def register():
                first = first_name.get().strip()
                last = last_name.get().strip()
                phone_number = phone.get().strip()
                email_address = email.get().strip()
                password = new_passkey.get()
                confirmed_password = confirm_passkey.get()

                if first == "" or last == "":
                    messagebox.showwarning("Missing Details","Please enter your first and last name.",parent=register_window)
                    return
                if phone_number == "" and email_address == "":
                    messagebox.showwarning("Missing Contact Details","Please enter either a phone number or an email.",parent=register_window)
                    return
                if password == "" or confirmed_password == "":
                    messagebox.showwarning("Missing Passkey","Please enter and confirm your passkey.",parent=register_window)
                    return
                if password != confirmed_password:
                    messagebox.showwarning("Passkey Mismatch","Both passkey fields must be identical.",parent=register_window)
                    return

                try:
                    cursor.execute("Select CustomerID from Customers where Phone =%s or Email = %s",
                                    (phone_number if phone_number != "" else None, email_address if email_address != "" else None)) 
                    existing_customer = cursor.fetchone()
                    if existing_customer is not None:
                        messagebox.showerror("Account Already Exists", "An account already exists with this phone/email.\nPlease use the " \
                        "login option instead.", parent = register_window)
                        return
                    passkey_hash = hash_passkey(password)
                    cursor.execute("Insert into Customers (First_name, Last_name, Phone, Email, Passkey_hash) values (%s, %s, %s, %s, %s)", 
                                    (first, last, phone_number if phone_number!="" else None, email_address if email_address != "" else None, 
                                    passkey_hash))
                    customer_id = cursor.lastrowid
                    con.commit()
                    register_window.destroy()

                    messagebox.showinfo("Registration Successful", "Your account has been created successfully!", parent= summary_window)
                    create_booking(customer_id)

                except Exception as e:
                    con.rollback()
                    messagebox.showerror("Registration Error", f"Unable to create your account.\n\n{e}", parent = summary_window)

            tk.Button(register_window, text="REGISTER", font=("Helvetica", 12, "bold"), bg="#ffd153", width =15, command = register
                        ).pack(pady=20)
            tk.Button(register_window, text = "Cancel", font=("Helvetica", 11), bg= "#fd8383", width= 15, command=register_window.destroy
                        ).pack()

        def create_booking(customer_id):

            try:
                for seat in selected_seats:
                    cursor.execute(
                        "Select bs.BookingSeatID from BookingSeats bs join Bookings b on bs.BookingID = b.BookingID join Seats s on bs.SeatID = s.SeatID " \
                        "where b.ShowID = %s and b.Booking_status = 'Confirmed' and s.Seat_number = %s",(show_id, seat))

                    if cursor.fetchone() is not None:
                        raise Exception(f"Seat {seat} has just been booked by another customer.")

                cursor.execute("Insert into Bookings (CustomerID, ShowID, Booking_date, Total_amount, Booking_status) " \
                "values (%s, %s, now(), %s,%s)", (customer_id, show_id, total_amount, "Confirmed"))
                booking_id = cursor.lastrowid

                for seat in selected_seats:
                    cursor.execute("Select SeatID from Seats where ScreenID = (Select ScreenID from Shows where ShowID = %s) " \
                    "and Seat_number = %s", (show_id, seat))
                    seat_result =cursor.fetchone()
                    if seat_result is not None:
                        seat_id = seat_result[0]
                        cursor.execute("Insert into BookingSeats (BookingID, SeatID) values (%s, %s)", (booking_id, seat_id))
                    else:
                        raise Exception(f"Seat {seat} could not be found.")

                cursor.execute("Select count(*) from BookingSeats bs join Bookings b on bs.BookingID = b.BookingID where b.ShowID = %s " \
                "and b.Booking_status = 'Confirmed'", (show_id,))
                booked_seats = cursor.fetchone()[0]
                if booked_seats >= 120:
                    cursor.execute("Update Shows set Is_booked_out = True where ShowID = %s", (show_id,))
                con.commit()

                messagebox.showinfo("Booking Confirmed", f"Your booking has been confirmed!\n\n"
                                    f"Booking ID: {booking_id}\nTotal Amount: AED {total_amount:.2f}", parent = summary_window)
                summary_window.destroy()

            except Exception as e:
                con.rollback()
                messagebox.showerror("Booking Error", f"Unable to complete booking.\n\n{e}", parent = summary_window)

    SS.select_seats(show_id, show_booking_summary)

       
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
    tk.Label(content_frame, text = details[6], font = ("Helvetica", 10), bg= "#ffffff" , wraplength=650, justify = "center"
             ).pack(padx=20, pady=15)


    cursor.execute("Select ShowID, ScreenID, show_date, show_time from Shows " \
        "where MovieID = %s and Is_active = true and Is_booked_out = false order by Show_date, show_time",(movie_id,))
    shows = cursor.fetchall()
    for show in shows:
        show_frame = tk.Frame(content_frame, bg = "#ffffff", relief = "raised", borderwidth=1)
        show_frame.pack(padx=10,pady=10)
        tk.Label(show_frame, text = f"Screen {show[1]}", font=("Helvetica",12,"bold"), bg = "#ffffff").pack(side = "left", padx=20, pady= 20)
        tk.Label(show_frame, text = f"{show[2]} | {show[3]}", font = ("Helvetica",11), bg= "#ffffff").pack(side="left", padx= 20)
        tk.Button(show_frame, text= "BOOK NOW", font = ("Helvetica",11, "bold"), bg = "#ffd153", command = lambda showID=show[0]: start_booking(showID)).pack(side="left", padx = 20)

def view_movies():
    clear_content()
    tk.Label(content_frame, text = "NOW SHOWING", font =("Century Gothic", 22, "bold"), bg = "#ffffff").pack(pady=20)

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
        tk.Label(card, text = f"Released: {movie[6]}", fg = "#000000", font = ("Helvetica", 9), bg = "#c8a8d4").pack(pady=5)

        tk.Button(card, text = "VIEW Shows", bg = "#ffd153", command = lambda movie_id = movie[0]: view_shows(movie_id)).pack(pady=10)
        
def search_booking():
    clear_content()

    tk.Label(content_frame, text = "MY BOOKINGS", font = ("Helvetica", 30, "bold"), bg = "#b4cdef").pack(pady = 25)
    tk.Label(content_frame, text = "Enter phone or email:", font= ("Georgia", 16),bg= "#b4cdef").pack(pady= 10)
    identifier_entry = tk.Entry(content_frame, font= ("Helvetica",14), width=30)
    identifier_entry.pack(pady= 5)

    tk.Label(content_frame, text="Booking ID (optional):", font=("Georgia", 16), bg="#b4cdef").pack(pady=(15, 10))
    booking_id_entry = tk.Entry(content_frame,font=("Helvetica", 14),width=30)
    booking_id_entry.pack(pady=5)
    results_frame = tk.Frame(content_frame,bg="#b4cdef")
    results_frame.pack(fill="both", expand=True, padx=30, pady=15)

    def search():
        identifier = identifier_entry.get().strip()
        booking_id = booking_id_entry.get().strip()

        if identifier == "":
            messagebox.showwarning("Missing Information", "Please enter your phone/email.")
            return

        try:
            for widget in results_frame.winfo_children():
                widget.destroy()
            cursor.execute("Select CustomerID, First_name, Last_name from Customers where Phone = %s OR Email = %s", (identifier, identifier))
            customer = cursor.fetchone()

            if customer is None:
                messagebox.showwarning("Customer Not Found", "No customer was found with that phone/email.")
                return

            customer_id = customer[0]
            customer_name = f"{customer[1]} {customer[2]}"

            if booking_id != "":
                cursor.execute("Select b.BookingID, m.Title, s.Show_date, s.Show_time, b.Total_amount, b.Booking_status from Bookings b " \
                "join Shows s on b.ShowID = s.ShowID join Movies m on s.MovieID = m.MovieID where b.BookingID = %s and b.CustomerID =%s",
                (booking_id, customer_id))

            else:
                cursor.execute("Select b.BookingID, m.Title, s.Show_date, s.Show_time, b.Total_amount, b.Booking_status from Bookings b " \
                                "join Shows s on b.ShowID = s.ShowID join Movies m on s.MovieID = m.MovieID where b.CustomerID =%s order by " \
                                "b.Booking_date desc",(customer_id,))
            bookings = cursor.fetchall()

            if not bookings:
                messagebox.showinfo("No Bookings", "You do not have any bookings.")
                return

            tk.Label(results_frame, text=f"Bookings for {customer_name}", font=("Helvetica", 18, "bold"), bg="#ffffff").pack(pady=15)

            for booking in bookings:
                booking_id_value = booking[0]
                cursor.execute("Select se.Seat_number from BookingSeats bs join Seats se ON bs.SeatID = se.SeatID where bs.BookingID = %s" \
                "order by se.Seat_number", (booking_id_value,))
                seats = cursor.fetchall()

                seat_list = ", ".join([seat[0] for seat in seats])
                booking_frame = tk.Frame(results_frame, bg="#ffffff", relief="raised", borderwidth=2)
                booking_frame.pack(padx=30,pady=10, fill="x")
                tk.Label(booking_frame, text=f"Booking ID: {booking_id_value}",font=("Helvetica", 14, "bold"),bg="#ffffff"
                            ).pack(anchor="w",padx=20,pady=5)
                tk.Label(booking_frame,text=f"Movie: {booking[1]}",font=("Georgia", 12),bg="#ffffff").pack( anchor="w", padx=20, pady=3)
                tk.Label(booking_frame, text=f"Date: {booking[2]}", font=("Georgia", 12), bg="#ffffff").pack(anchor="w", padx=20, pady=3)
                tk.Label(booking_frame, text=f"Time: {booking[3]}", font=("Georgia", 12), bg="#ffffff").pack(anchor="w", padx=20, pady=3)
                tk.Label(booking_frame, text=f"Seats: {seat_list}", font=("Georgia", 12), bg="#ffffff").pack(anchor="w", padx=20, pady=3)
                tk.Label(booking_frame, text=f"Amount: AED {booking[4]:.2f}", font=("Georgia", 12), bg="#ffffff"
                            ).pack(anchor="w", padx=20, pady=3)
                tk.Label(booking_frame, text=f"Status: {booking[5]}", font=("Georgia", 12), bg="#ffffff").pack(anchor="w", padx=20, pady=3)

        except Exception as e:
            messagebox.showerror("Search Error", f"Unable to search bookings.\n\n{e}")

    tk.Button(content_frame, text= "SEARCH", font= ("Helvetica", 14, "bold"), bg="#ffd153", width= 15, command =search).pack(pady= 15)


def cancel_booking():
    clear_content()

    tk.Label(content_frame, text = "MY BOOKINGS", font = ("Helvetica", 30, "bold"), bg= "#b4cdef").pack(pady=25)
    tk.Label(content_frame,text="Enter your phone or email:", font=("Georgia", 16), bg="#b4cdef").pack(pady=10)
    identifier_entry = tk.Entry(content_frame, font=("Helvetica", 14), width=30)
    identifier_entry.pack(pady=5)
    tk.Label(content_frame, text="Enter your Booking ID (optional):", font=("Georgia", 16), bg="#b4cdef").pack(pady=10)
    booking_entry = tk.Entry(content_frame, font=("Helvetica", 14),width=30)
    booking_entry.pack(pady=5)

    results_frame = tk.Frame(content_frame,bg="#b4cdef")
    results_frame.pack(fill="both", expand=True, padx=30, pady=15)


    def find_booking():
        identifier = identifier_entry.get().strip()
        booking_id = booking_entry.get().strip()

        if identifier == "" or booking_id == "":
            messagebox.showwarning("Missing Information", "Please enter both you phone/email and Booking ID.")
            return
        try:
            cursor.execute("Select CustomerID, First_name, Last_name from Customers where Phone = %s OR Email = %s",(identifier, identifier))
            customer = cursor.fetchone()

            if customer is None:
                messagebox.showerror("Customer Not Found","No customer was found with this phone/email.")
                return

            customer_id = customer[0]
            cursor.execute("Select b.BookingID, m.Title, s.Show_date, s.Show_time, b.Total_amount, b.Booking_status,s.ShowID " \
                           "from Bookings b join Shows s ON b.ShowID = s.ShowID join  Movies m ON s.MovieID = m.MovieID " \
                           "where b.BookingID = %s and b.CustomerID = %s", (booking_id, customer_id) )
            booking = cursor.fetchone()

            if booking is None:
                messagebox.showerror("Booking Not Found", "No booking was found with these details.")
                return
            if booking[5] == "Cancelled":
                messagebox.showinfo( "Already Cancelled","This booking has already been cancelled." )
                return

            confirmation_window = tk.Toplevel(window)
            confirmation_window.title("Cancel Booking")
            confirmation_window.geometry("500x500")
            confirmation_window.grab_set()

            tk.Label(confirmation_window,text="BOOKING DETAILS",font=("Times New Roman", 22, "bold")).pack(pady=20)
            tk.Label(confirmation_window, text=f"Booking ID: {booking[0]}", font=("Georgia", 13)).pack(pady=5)
            tk.Label(confirmation_window, text=f"Movie: {booking[1]}", font=("Georgia", 13)).pack(pady=5)
            tk.Label(confirmation_window, text=f"Date: {booking[2]}", font=("Georgia", 13)).pack(pady=5)
            tk.Label(confirmation_window, text=f"Time: {booking[3]}", font=("Georgia", 13)).pack(pady=5)
            tk.Label(confirmation_window, text=f"Total Amount: AED {booking[4]:.2f}", font=("Georgia", 13)).pack(pady=5)

            cursor.execute("Select se.Seat_number from BookingSeats bs join Seats se on bs.SeatID = se.SeatID where bs.BookingID =%s " \
                           "order by se.Seat_number", (booking[0],))
            seats = cursor.fetchall()
            seat_list = ", ".join([seat[0] for seat in seats])
            tk.Label(confirmation_window, text=f"Seats: {seat_list}", font=("Georgia", 13)).pack(pady=5)

            tk.Label(confirmation_window, text = "Are you sure you want to cancel this booking?", font=("Helvetica", 13, "bold")).pack(pady=(25,15))

            def confirm_cancellation():
                try:
                    
                    cursor.execute("Update Bookings set Booking_status = 'Cancelled' where BookingID = %s and CustomerID = %s", (booking[0], customer_id))
                    cursor.execute("Select count(*) from BookingSeats bs join Bookings b on bs.BookingID = b.BookingID where b.ShowID = %s and b.Booking_status = 'Confirmed'", (booking[6],))
                    booked_seats = cursor.fetchone()[0]

                    if booked_seats >=120:
                        cursor.execute("Update Shows set Is_booked_out = true where ShowID = %s",(booking[6],))
                    else:
                        cursor.execute("Update Shows set Is_booked_out = false where ShowID = %s",(booking[6],))

                    con.commit()
                    confirmation_window.destroy()
                    messagebox.showinfo("Booking Cancelled", f"Booking {booking[0]} has been cancelled successfully")

                except Exception as e:
                    con.rollback()
                    messagebox.showerror("Cancellation Error", f"Unable to cancel the booking.\n\n{e}",parent=confirmation_window)

            button_frame = tk.Frame(confirmation_window)
            button_frame.pack(pady=25)
            tk.Button(button_frame,text="CANCEL BOOKING",font=("Helvetica", 12, "bold"),bg="#fd8383",width=18, command= confirm_cancellation).pack(side="left", padx = 10)
            tk.Button(button_frame,text="KEEP BOOKING",font=("Helvetica", 12, "bold"),bg="#ffd153",width=18, command= confirmation_window.destroy).pack(side="left", padx = 10)

        except Exception as e:
            messagebox.showerror("Cancellation Error", f"Unable to find booking. \n\n{e}")

    tk.Button(content_frame,text = "FIND BOOKING", font =("Helvetica", 14,"bold"), bg = "#ffd153", command = find_booking).pack(pady=20)


login_button = tk.Button(top_frame, text = "LOGIN", bg = "#ffd153", command = customer_login)
search_booking_button=tk.Button(top_frame, text="My Booking", bg="white", command=search_booking)
cancel_booking_button=tk.Button(top_frame, text="Cancel Booking", bg="white", command=cancel_booking)
view_movies_button = tk.Button(top_frame, text = "Movies", bg = "white", command = view_movies)
exit_button = tk.Button(top_frame, text = "Exit", bg = "white", command= window.destroy)

login_button.pack(side= "left", padx = 5)
view_movies_button.pack(side="left", padx=5)
search_booking_button.pack(side="left", padx=5)
cancel_booking_button.pack(side="left", padx=5)
exit_button.pack(side= "left", padx = 5)

home()
window.mainloop()