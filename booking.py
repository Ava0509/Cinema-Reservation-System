import database as db
import tabulate as tb

'''
def book_show():
    print("""
-------------- Select a Movie --------------
""")
    
    db.cursor.execute("Select MovieID, Title, Genre, Language_, Duration, Rating, Release_date, Description_ " \
    "from Movies where Is_active = true")
    movies = db.cursor.fetchall()

    if not movies:
        print("No movies available.")
    else:
        print(tb.tabulate(movies, 
                        headers = ("Movie ID", "Title", "Genre", "Language", "Duration", 
                                    "Rating", "Release Date","Description"), 
                        tablefmt = "rounded"))

        id_list = [id[0] for id in movies]
        while True:
            try:
                m_id = int(input("Enter Movie ID: "))
                if m_id not in id_list:
                    print("Invalid Movie ID. Try again.")
                else:
                    break
            except ValueError:
                print("Invalid input. Try again.")

        db.cursor.execute("Select ShowID, Show_date, Show_time from Shows " \
        "where MovieID = %s and Is_active = true and Is_booked_out = false",(m_id,))
        shows = db.cursor.fetchall()
        print(tb.tabulate(shows, 
                        headers = ("Show ID", "Show Date (YYYY-MM-DD)", "Show Time"), 
                        tablefmt = "rounded"))
'''

import tkinter as tk

window = tk.Tk()
window.title("Seat Selection")
window.geometry("1200x700")
selected = []
booked = ["A3", "F6"] #source from MySQL
seat_buttons = {}

layout = (['A',12], ['B',12], ['C',12], ['D',12], 
          ['E',10], ['F',10], ['G',10], ['H',10],
          ['I',8], ['J',8], ['K',8], ['L',8])

def seat_clicked(seat):
    if seat in selected:
        selected.remove(seat)
        seat_buttons[seat].config(bg = "SystemButtonFace")
    else:
        selected.append(seat)
        seat_buttons[seat].config(bg = "green")
    print(selected)

tk.Label(window, 
         text = "------------------------- SCREEN -------------------------",
         font = ("Helvetica", 14, "bold")).grid(row = 0, column = 0, columnspan = 16, pady = 10)

current_row = 2 #row A starts here

for row, seats in layout:
    if row in ('E','I'): #Divider between zones
        tk.Label(window, text = "").grid(row = current_row, column = 0)
        current_row +=1

    tk.Label(window, text = row, 
             font = ("Helvetica", 11, "normal")).grid(row = current_row, column = 0)

    for seat in range(1, seats+1):
        seat_name = f"{row}{seat}"

        #Generating the middle aisle
        if seats ==12:
            if seat<=6:
                column = seat
            else:
                column = seat+1

        elif seats == 10:
            if seat<=5:
                column = seat + 1
            else:
                column = seat + 2

        else:
            if seat<=4:
                column = seat + 2
            else:
                column = seat + 3

        if seat_name in booked: #deactivating booked seats
            btn = tk.Button(window, text = seat_name, 
                            width = 5, bg="red", fg = "white", state = "disabled")
        else:
            btn = tk.Button(window, text = seat_name, width = 5, 
                            command = lambda s=seat_name: seat_clicked(s))

        btn.grid(row = current_row, column =column, padx = 1, pady = 2)
        seat_buttons[seat_name] = btn

    current_row+=1
'''
confirm_btn = tk.Button(
    window,
    text="Confirm Booking",
    font=("Helvetica", 12, "bold"),
    command=confirm_booking
)

confirm_btn.grid(row=current_row + 1,
                 column=0,
                 columnspan=15,
                 pady=15)
def confirm_booking():

    print(selected)
'''
window.mainloop()
