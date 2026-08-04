import tkinter as tk
import database as db
root=tk.Tk()
root.geometry("800x600")
root.title("Admin Page")
label=tk.Label(root, text="Login Page", font=("Bahnschrift, 15"))
label.pack(padx=10, pady=10)
#
def add_movie():
    cursor=con.cursor()
    movie_name=int