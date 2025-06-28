from tkinter import *
import mysql.connector
from tkinter.messagebox import *

cn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='mv_managment'
)

cr = cn.cursor()

global activation
activation = "no"

def checking_box(activated):
    return 1 if activated == 1 else 0

def clear():
    s1.set("")
    s2.set("")
    v1.set(1)
    vr.set("theater 1")

def save():
    movie_id = e1.get()
    name = e2.get()
    activated = v1.get()
    activation = checking_box(activated) 
    theatre = vr.get()

    sq = '''INSERT INTO movie (mv_id, name, activ, m_theater) VALUES (%s, %s, %s, %s)'''

    try:
        cr.execute(sq, (movie_id, name, activation, theatre))
        cn.commit()
        clear()
    except mysql.connector.Error as err:
        showerror("Database Error:", err)
    

def update():
    movie_id = e1.get()
    name = e2.get()
    activated = v1.get()
    activation = checking_box(activated)
    theatre = vr.get()

    sq = '''update movie set name = %s, activ = %s, m_theater = %s where mv_id = %s'''

    try:
        cr.execute(sq, (name, activation, theatre, movie_id))
        cn.commit()
        clear()
    except mysql.connector.Error as err:
        showerror("Database Error:", err)

def v_one():
    movie_id = e1.get()
    sq = '''select * from movie where mv_id = %s'''

    try:
        cr.execute(sq, (movie_id,))
        rd = cr.fetchone()
        s1.set(rd[0])
        s2.set(rd[1])
        v1.set(rd[2])
        vr.set(rd[3])

    except mysql.connector.Error as err:
        showerror("Database Error:", err)

def v_all():
    win2 = Tk()
    win2.geometry('400x400')
    win2.title('M O V I E')
    win2.resizable(0,0)

    text_area = Text(win2, wrap="none", font=("Courier New", 10), width=60, height=10)
    text_area.pack(side="left", fill="both", expand=True)


    scrollbar = Scrollbar(win2, command=text_area.yview)
    scrollbar.pack(side="right", fill="y")
    text_area.config(yscrollcommand=scrollbar.set)

    headers = ["movie_id", "Name", "activated", "Theater"]

    sq = '''select * from movie'''

    try:
        cr.execute(sq,)
        rd = cr.fetchall()

        def format_row(row):
            return f"{row[0]:<10}{row[1]:<12}{row[2]:<15}{row[3]:<10}\n"

        text_area.insert("end", format_row(headers))
        text_area.insert("end", "-" * 48 + "\n")

        for row in rd:
            text_area.insert("end", format_row(row))

        text_area.config(state="disabled")
   

    except mysql.connector.Error as err:
        showerror("Database Error:", err)

    win2.mainloop()

def delete():
    movie_id = e1.get()

    sq = '''delete from movie where mv_id = %s'''

    try:
        cr.execute(sq, (movie_id,))
        cn.commit()
        clear()
    except mysql.connector.Error as err:
        showerror("Database Error:", err)


win = Tk()
win.title('M O V I E')
win.geometry('550x400')
win.resizable(0,0)

lb1 = Label(win, text="M O V I E", font=('Arial', 16))

s1 = StringVar()

lb2 = Label(win, text="Movie Id", font=('Arial', 11))
e1 = Entry(win, textvariable=s1)

s2 = StringVar()

lb3 = Label(win, text="Name", font=('Arial', 11))
e2 = Entry(win, textvariable=s2)

v1 = IntVar()

lb4 = Label(win, text="Activated", font=('Arial', 11))
c1 = Checkbutton(win, text="Yes", variable = v1)
v1.set(1)

vr = StringVar()
lf = LabelFrame(win, text="Room")
r1 = Radiobutton(lf, text="theater 1", variable=vr, value="theater 1")
r2 = Radiobutton(lf, text="theater 2", variable=vr, value="theater 2")
r3 = Radiobutton(lf, text="theater 3", variable=vr, value="theater 3")

vr.set('theater 1')

bt1 = Button(win, text="New", width=8, command=clear)
bt2 = Button(win, text="Save", width=8, command=save)
bt3 = Button(win, text="UpDate", width=8, command=update)
bt4 = Button(win, text="View One", width=8, command=v_one)
bt5 = Button(win, text="View All", width=8, command=v_all)
bt6 = Button(win, text="Delete", width=8, command=delete)


lb1.place(x=240,y=20)

lb2.place(x=40, y=80)
e1.place(x=120, y=80)

lb3.place(x=40, y=120)
e2.place(x=120, y=120)

lb4.place(x=40, y=160)
c1.place(x=120, y=160)

lf.place(x=120, y=200)
r1.pack(anchor=W)
r2.pack(anchor=W)
r3.pack(anchor=W)

bt1.place(x=40, y=320)
bt2.place(x=120, y=320)
bt3.place(x=200, y=320)
bt4.place(x=280, y=320)
bt5.place(x=360, y=320)
bt6.place(x=440, y=320)

win.mainloop()