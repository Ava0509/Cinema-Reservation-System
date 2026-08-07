import tkinter as tk
root=tk.Tk()
root.geometry("800x600")
root.title("Admin Page")

frame=tk.Frame(root)
frame.place(relx=0.5, rely=0.5, anchor="center")

Heading_label=tk.Label(frame, text="Login Page", font=("Bahnschrift", 36))
Heading_label.grid(row=2, columnspan=2)

admin_number_label=tk.Label(frame, text="Username ")
admin_number_label.grid(row=4, column=0)
admin_number_entry=tk.Entry(frame, font=("Helvetica", 22))
admin_number_entry.grid(row=4, column=1)

password_label=tk.Label(frame, text="Password ")
password_label.grid(row=5, column=0)
password_entry=tk.Entry(frame, font=("Helvetica", 22))
password_entry.grid(row=5, column=1)

def login():
    global admin_number
    global password
    admin_number=admin_number_entry.get()
    password=password_entry.get()
    admin_number_entry.delete(0,tk.END)
    password_entry.delete(0,tk.END)
       
Login_Button=tk.Button(frame, text="Login", command=login)
Login_Button.grid(row=6,column=1)

def Add_movie():
    cursor=con.cursor()
    Fields=["Title" ,"Genre","Language","Duration","Is_active","Rating" ,"Release_date","Description"]
    values=[]
    temporary_values=[]

    for field_no in range(len(Fields)):
        text=tk.Label(root, text=Fields[field_no], font=("Helvetica", 18))
        text.grid(row=field_no+4)
        entry=tk.Entry(root, font=("Helvetica", 18))
        entry.grid(row=field_no+4, column=1)
        temporary_values.append(entry)
    def submit():
        for entry in temporary_values:
            values.append(entry.get())
            entry.delete(0,tk.END)
    submit_button=tk.Button(root, text="submit", command=submit)
    submit_button.grid(row=14, column=1)

    query="insert into table(title,genre,language,duration,is_active,rating,release_date,description) values(%s)"
    cursor.execute(query(values))

Add_movies_Button=tk.button(root, text="Add Movie", font=("Arial", 15), command=Add_movie)
Add_movies_Button.pack()

def Update_movies():
    pass

def Update_showtimes():
    pass

def Show_bookings():
    pass

root.mainloop()


                



                
    

