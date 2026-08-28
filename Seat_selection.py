import database as db
import tkinter as tk
from tkinter import messagebox

def select_seats(show_id, on_seats_selected):
    window = tk.Toplevel()
    window.title("Seat Selection")
    window.geometry("800x700")
    selected_seats = []
    booked_seats = []
    seat_buttons = {}

    cursor = db.con.cursor()
    cursor.execute("Select s.Seat_number from Seats s " \
    "join BookingSeats bs on s.SeatID = bs.SeatID " \
    "join Bookings b on bs.BookingID = b.BookingID where b.ShowID = %s", (show_id,))

    booked_seats = [seat[0] for seat in cursor.fetchall()]

    layout = (['A',12], ['B',12], ['C',12], ['D',12], 
            ['E',10], ['F',10], ['G',10], ['H',10],
            ['I',8], ['J',8], ['K',8], ['L',8])

    def seat_clicked(seat):
        if seat in selected_seats:
            selected_seats.remove(seat)
            seat_buttons[seat].config(bg = "SystemButtonFace")
        else:
            selected_seats.append(seat)
            seat_buttons[seat].config(bg = "green")
    def confirm_seats():
        if selected_seats == []:
            messagebox.showwarning("No Seats Selected",
                                   "Please select at least one seat.")
            return
        on_seats_selected(selected_seats.copy(), show_id)
        window.destroy()

    tk.Label(window, 
            text = "|---------------------------------------- SCREEN ----------------------------------------|",
            font = ("Helvetica", 14, "bold")).grid(row = 0, column = 0, columnspan = 16, pady = 10)

    current_row = 2 #row A starts here

    for row, seats in layout:
        if row == "A": #Divider between zones
            tk.Label(window, text = "--------------------------- CLASSIC / AED 50 ---------------------------",
                    font = ("Georgia", 12, "bold")).grid(row = current_row, column = 0,columnspan = 16, pady = (10,5))
            current_row +=1
        if row == "E": #Divider between zones
            tk.Label(window, text = "--------------------------- PREMIUM / AED 80 ---------------------------",
                        font = ("Georgia", 12, "bold")).grid(row = current_row, column = 0,columnspan = 16, pady = (15,5))
            current_row +=1
        if row == "I": #Divider between zones
            tk.Label(window, text = "--------------------------- VIP / AED 150 ---------------------------",
                        font = ("Georgia", 12, "bold")).grid(row = current_row, column = 0,columnspan = 16, pady = (15,5))
            current_row +=1

        tk.Label(window, text = row, 
                font = ("Helvetica", 11, "normal"), bg = "#ffea00").grid(row = current_row, column = 0)

        for seat in range(1, seats+1):
            seat_name = f"{row}{seat}"

            #Generating the middle aisle
            if seats ==12:
                if seat<=6:
                    column = seat 
                else:
                    column = seat + 2

            elif seats == 10:
                if seat<=5:
                    column = seat + 1
                else:
                    column = seat + 3

            else:
                column = seat + 3

            if seat_name in booked_seats: #deactivating booked seats
                btn = tk.Button(window, text = seat_name, width = 5, bg="red", fg = "white", state = "disabled")
            else:
                btn = tk.Button(window, text = seat_name, width = 5, command = lambda s=seat_name: seat_clicked(s))
            btn.grid(row = current_row, column =column, padx = 3, pady = 2)
            seat_buttons[seat_name] = btn

        current_row+=1

    legend = tk.Frame(window)
    legend.grid(row = current_row + 1, column=0, columnspan = 16, pady = 20)
    tk.Label(legend, text = "AVAILABLE", font =("Georgia", 10),bg = "#ffffff").pack(side = "left", padx = 10)
    tk.Label(legend, text = "SELECTED", font =("Georgia", 10), bg = "#08e100").pack(side = "left", padx = 10)
    tk.Label(legend, text = "BOOKED", font =("Georgia", 10), bg = "#FD8383").pack(side = "left", padx = 10)

    select_button = tk.Button(window, text = "SELECT", font=("Helvetica", 14, "bold"), bg = "#ffd153", width = 15, command=confirm_seats)
    select_button.grid(row = current_row+2, column= 0, columnspan = 16, pady=3)

    cancel_button = tk.Button(window, text = "CANCEL", font=("Helvetica", 14, "bold"), bg = "#f58989", width = 15, command = window.destroy)
    cancel_button.grid(row = current_row+ 2, column =7, pady = 10)
