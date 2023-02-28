import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from tkcalendar import *
#root definitiom
root = Tk()
root.title("Expense Analyzer")
root.geometry("800x500")
root.configure(bg="#70D6AA")
#background imgage
bg=PhotoImage(file="C:\\Users\\ajayb\\Desktop\\projectpics\\logo1.png")
bg_label=Label(root,image=bg)
bg_label.pack()

#pick date
def grab_date(date_entry,cal):
    date_entry.insert(0,cal.get_date())

#add record
def addrecord():
    top2 = Toplevel()
    top2.title("Add New Record")
    top2.geometry("800x500")
    top2.configure(bg="#70D6AA")
    Label1 = Label(top2, text="Product/Service Name :", bg="#70D6AA").place(x=20, y=20)
    Label2 = Label(top2, text="Category Of Product :", bg="#70D6AA").place(x=20, y=100)
    Label3 = Label(top2, text="Amount Paid : ", bg="#70D6AA").place(x=20, y=180)
    Label4 = Label(top2, text="Method Of Payment :", bg="#70D6AA").place(x=20, y=260)
    Label5 = Label(top2, text="Date Of Payment :", bg="#70D6AA").place(x=500, y=280)
    cal = Calendar(top2, selectmode='day',year=2022, month=11,day=20)
    cal.place(x=500,y=20)
    submitbutton=Button(top2,text="Add Record",command=lambda: submit(name_entry,category_entry,amount_entry,method_entry,date_entry,top2),height=3,width=20,bd=3)
    submitbutton.place(x=350,y=400)
    datebutton=Button(top2,text="Pick Date",command=lambda: grab_date(date_entry,cal),height=2,width=10,bd=3)
    datebutton.place(x=580, y=220)
    name_entry = Entry(top2, bd=3)
    name_entry.place(x=160, y=20)
    category_entry = Entry(top2, bd=3)
    category_entry.place(x=150, y=100)
    amount_entry = Entry(top2, bd=3)
    amount_entry.place(x=110, y=180)
    method_entry = Entry(top2, bd=3)
    method_entry.place(x=150, y=260)
    date_entry = Entry(top2, bd=3)
    date_entry.place(x=610, y=280)

#submit record into database
def submit(name_entry,category_entry,amount_entry,method_entry,date_entry,top2):
    pno_count=1
    conn = sqlite3.connect("expense.db")  # create/connect to database
    c = conn.cursor()  # create cursor
    c.execute("CREATE TABLE sample2(pid integer,name text,category text,date text,amount integer,method text)") #to create table
    c.execute("INSERT INTO sample1 VALUES (:pno, :name, :category, :date, :amount, :method)",
              {
                  "Product Number": pid_count,
                  "name": name_entry.get(),
                  "category": category_entry.get(),
                  "date": date_entry.get(),
                  "amount": amount_entry.get(),
                  "method": method_entry.get()
              })
    conn.commit() #commit changes to database
    conn.close() #close connection to database
    name_entry.delete(0,END)
    category_entry.delete(0, END)
    date_entry.delete(0, END)
    amount_entry.delete(0, END)
    method_entry.delete(0, END)
    top2.destroy()
    messagebox.showinfo("Message","Transaction Details Stored")

#delete selected record
def deleterecord(tree):
    x=tree.selection()[0]
    tree.delete(x)
    conn=sqlite3.connect("expense.db") #connect to database
    c=conn.cursor() #create cursor
    c.execute("DELETE from sample1 WHERE pid=" + pid_entry.get())

    conn.commit()  #commit changes made to database
    conn.close()  #close the database connection


#view record
def viewrecord():
    top3 = Toplevel()
    top3.title("View Records")
    top3.geometry("1000x500")
    top3.configure(bg="#70D6AA")
    conn = sqlite3.connect("expense.db")  # create/connect to database
    c = conn.cursor()  # create cursor
    Style=ttk.Style()
    Style.theme_use("clam")
    Style.configure("Treeview",background="silver",foreground="black",rowheight=35,fieldbackground="#70D6AA")
    Style.map("Treeview",background=[("selected", "red")])
    tree = ttk.Treeview(top3, column=("Product Name", "Product Category", "Date Of Payment", "Amount Paid", "Method Of Payment"), show='headings')
    tree.column("#1", anchor=tkinter.CENTER)
    tree.heading("#1", text="Product Name")
    tree.column("#2", anchor=tkinter.CENTER)
    tree.heading("#2", text="Product Category")
    tree.column("#3", anchor=tkinter.CENTER)
    tree.heading("#3", text="Date Of Payment")
    tree.column("#4", anchor=tkinter.CENTER)
    tree.heading("#4", text="Amount Paid")
    tree.column("#5", anchor=tkinter.CENTER)
    tree.heading("#5", text="Method Of Payment")
    c.execute("SELECT * FROM sample1")
    rows=c.fetchall()
    tree.tag_configure('oddrow',background="white")
    tree.tag_configure('evenrow', background="lightblue")
    global count
    count=0
    for row in rows:
        if count%2==0:
            tree.insert("",tkinter.END,values=row,tags=('evenrow',))
        else:
            tree.insert("", tkinter.END, values=row,tags=('oddrow',))
        count=count+1
    tree.pack()
    conn.close()  # close connection to database
    deletebutton = Button(top3, text="Delete Record", command=deleterecord(tree), height=3, width=20, bd=3)   # button to delete a selected record
    deletebutton.place(x=350, y=400)


#spending report
def report():
    slabel=Label(top1,text="Hey").place(x=10,y=10)

#main menu
def openmain():
    top1 = Toplevel()
    top1.title("Main Menu")
    top1.geometry("800x500")
    top1.configure(bg="#70D6AA")
    addbutton=Button(top1,text="Add New Records",command=addrecord,height=3,width=20,bd=3)
    addbutton.place(x=300,y=100)
    viewbutton = Button(top1, text="View Previous Records", command=viewrecord, height=3, width=20, bd=3)
    viewbutton.place(x=300, y=200)
    reportbutton = Button(top1, text="Spending Report", command=report, height=3, width=20, bd=3)
    reportbutton.place(x=300, y=300)


#login form
def login():
    username=entry1.get()
    password=entry2.get()
    if(username=="" and password==""):
        messagebox.showinfo("","Blank not allowed")
    elif(username=="ajay" and password=="admin"):
        root.iconify()
        openmain()
    else:
        messagebox.showinfo("", "Incorrect Username or Password")
global loginstatus
loginstatus=0
global entry1
global entry2
Label1=Label(root,text="Username",bg="#70D6AA").place(x=20,y=20)
Label2=Label(root,text="Password",bg="#70D6AA").place(x=20,y=90)
entry1=Entry(root,bd=3)
entry1.place(x=110,y=20)
entry2=Entry(root,bd=3)
entry2.place(x=110,y=90)
loginbutton=Button(root,text="Login",command=login,height=2,width=10,bd=3).place(x=80,y=140)


root.mainloop()