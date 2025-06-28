from tkinter import *
from tkinter import ttk
import mysql.connector

cn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='mv_managment'
)

cr = cn.cursor()

win = Tk()
win.geometry('600x350')
win.title("M o v i e")
win.resizable(0, 0)

global data
data = []

def save_booking():
    selected_movie = cb.get()
    room = v1.get()
    time = vr.get()

    if selected_movie == "Select Movie" or not room or not time:
        print("Please complete all booking information.")
        return

    try:
        cr.execute("SELECT mv_id FROM movie WHERE name = %s", (selected_movie,))
        movie_data = cr.fetchone()
        if not movie_data:
            print("Movie not found.")
            return

        mv_id = movie_data[0]

        for index, status in enumerate(ch):
            if status == 1 and bt[index].cget("bg") == "lightgreen":
                seat_num = index + 1
                sql = "INSERT INTO booking (b_mvid, b_theater, b_time, seat) VALUES (%s, %s, %s, %s)"
                cr.execute(sql, (mv_id, room, time, seat_num))

        cn.commit()
        print("Booking saved successfully.")
        load_seats(cb.get())

    except mysql.connector.Error as err:
        print("MySQL Error:", err)

def toggle_or_unbook(index):
    if bt[index].cget("bg") == "red":
        unbook_seat(index)
    else:
        toggle_seat(index)

def toggle_seat(index):
    if ch[index] == 0:
        ch[index] = 1
        bt[index].config(bg="lightgreen")
    else:
        ch[index] = 0
        bt[index].config(bg="SystemButtonFace")

def unbook_seat(index):
    selected_movie = cb.get()
    time = vr.get()

    if selected_movie == "Select Movie" or time == 0:
        print("Please select a movie and time before unbooking.")
        return

    try:
        cr.execute("SELECT mv_id FROM movie WHERE name = %s", (selected_movie,))
        movie_data = cr.fetchone()
        if not movie_data:
            print("Movie not found.")
            return

        mv_id = movie_data[0]
        seat_num = index + 1

        cr.execute("DELETE FROM booking WHERE b_mvid = %s AND b_time = %s AND seat = %s", (mv_id, time, seat_num))
        cn.commit()

        ch[index] = 0
        bt[index].config(bg="SystemButtonFace", state='normal')
        print(f"Seat {seat_num} unbooked.")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)

def unlock_booked_seats():
    for index in range(len(bt)):
        if bt[index].cget("bg") == "red":
            bt[index].config(state='normal')  # Enable click
    print("Booked seats are now clickable for unbooking.")

def showseat():
    for i in range(nbr_row):
        for j in range(nbr_col):
            index = i * nbr_col + j

            def create_command(idx=index):
                return lambda: toggle_or_unbook(idx)

            btn = Button(win, text=str(index + 1), width=4, height=1, command=create_command())
            x = start_x + j * (btn_width + spacing_x)
            y = start_y + i * (btn_height + spacing_y)
            btn.place(x=x, y=y)
            bt.append(btn)

def load_seats(selected_movie):
    global ch, bt

    for i in range(len(ch)):
        ch[i] = 0
        bt[i].config(bg="SystemButtonFace", state='normal')

    try:
        sql = "SELECT * FROM movie WHERE name = %s"
        cr.execute(sql, (selected_movie,))
        ids = cr.fetchone()

        if ids is not None:
            mv_id = ids[0]
            v1.set(ids[3])  

            selected_time = vr.get()
            if selected_time == 0:
                return 

            sql = "SELECT seat FROM booking WHERE b_mvid = %s AND b_time = %s"
            cr.execute(sql, (mv_id, selected_time))
            rows = cr.fetchall()

            for row in rows:
                seat_num = row[0] - 1
                if 0 <= seat_num < len(ch):
                    ch[seat_num] = 1
                    bt[seat_num].config(bg="red", state='disabled')  # Disabled until UnBook is clicked

        else:
            print("Movie not found.")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)
        for i in range(len(ch)):
            ch[i] = 0
            bt[i].config(bg="SystemButtonFace", state='normal')

def on_time_change():
    selected = cb.get()
    if selected != "Select Movie":
        load_seats(selected)

def on_selection(event):
    selected = cb.get()
    load_seats(selected)

def datas():
    global data
    data = [] 
    sql = "SELECT * FROM movie WHERE activ = '1'"
    try:
        cr.execute(sql)
        rows = cr.fetchall()
        for rd in rows:
            data.append(rd[1])
    except Exception as e:
        print("Error fetching data:", e)

def reset_all_seats():
    selected_movie = cb.get()
    time = vr.get()

    if selected_movie == "Select Movie" or time == 0:
        print("Please select both movie and time.")
        return

    try:
        cr.execute("SELECT mv_id FROM movie WHERE name = %s", (selected_movie,))
        movie_data = cr.fetchone()
        if not movie_data:
            print("Movie not found.")
            return

        mv_id = movie_data[0]

        cr.execute("DELETE FROM booking WHERE b_mvid = %s AND b_time = %s", (mv_id, time))
        cn.commit()

        for index in range(len(bt)):
            ch[index] = 0
            bt[index].config(bg="SystemButtonFace", state='normal')

        print("All seats have been reset.")

    except mysql.connector.Error as err:
        print("MySQL Error:", err)

def exit():
    win.destroy()

nbr_col = 5
nbr_row = 6

start_x = 310
start_y = 60
btn_width = 30
btn_height = 35
spacing_x = 20
spacing_y = 5

bt = []
ch = []

for i in range(nbr_row * nbr_col):
    ch.append(0)

lb1 = Label(win, text="Booking Managment System", font=('Arial', 16))

lb2 = Label(win, text="Choose a Movie", font=('Arial', 10))
datas()
cb = ttk.Combobox(win, width=18, state='readonly', values=data)
cb.set("Select Movie")
cb.bind("<<ComboboxSelected>>", on_selection)

v1 = StringVar()
lb3 = Label(win, text="Room", font=('Arial', 10))
e1 = Entry(win, textvariable=v1)

vr = IntVar()
f1 = LabelFrame(win, text="Select Time")
r1 = Radiobutton(f1, text="6:00 --> 7:30", variable=vr, value=6, command=on_time_change)
r2 = Radiobutton(f1, text="8:00 --> 9:30", variable=vr, value=8, command=on_time_change)
r3 = Radiobutton(f1, text="10:00 --> 11:30", variable=vr, value=10, command=on_time_change)

showseat()

bt1 = Button(win, text="New", width=8, command=reset_all_seats)
bt2 = Button(win, text="Save", width=8, command=save_booking)
bt3 = Button(win, text="UnBook", width=8, command=unlock_booked_seats)
bt4 = Button(win, text="Exit", width=8, command=exit)

lb1.place(x=180, y=10)
lb2.place(x=20, y=60)
cb.place(x=140, y=60)
lb3.place(x=20, y=100)
e1.place(x=140, y=100)
f1.place(x=140, y=140)
r1.pack(anchor=W)
r2.pack(anchor=W)
r3.pack(anchor=W)
bt1.place(x=20, y=300)
bt2.place(x=100, y=300)
bt3.place(x=180, y=300)
bt4.place(x=260, y=300)

win.mainloop()
