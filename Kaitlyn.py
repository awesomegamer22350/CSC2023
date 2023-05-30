#Kaitlyn Rohm
#This is my first internal for Computer science
#This program will help Julie's party hire keep track of purchases

#Seting up tkinter
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askyesno #Allows confirmation to happen
import datetime as dt
from tkcalendar import Calendar

#main window
root = Tk()

#setting up frames (creation and placement) and canvases
frame1 = Frame(root)
frame1.place(x= 10,y= 0)
for i in range(0, 7):
    frame1.columnconfigure(i, minsize=150)

frame2 = Frame(root, height=300, width=1100)
frame2.place(x=0, y=250)
for i in range(0, 8):
    frame2.columnconfigure(i, minsize=150)

#Canvas for scroll bar
can = Canvas(frame2, height=300, width=1200)
can.pack(side=LEFT, fill=BOTH, expand=True)

#Frame for scroll bar
frame3 = Frame(can)
can.create_window(10, 0, window=frame3, anchor=NW, width=1200)
#Will make the column length constant for the canvas
for i in range(0, 8):
    frame3.columnconfigure(i, minsize=150)

#Scroll bar for list and canvas it's stored in
scroll = Scrollbar(frame2, orient="vertical", command=can.yview)
scroll.pack(side=RIGHT, fill=Y)
#Connects scroll to canvas
can.config(yscrollcommand=scroll.set)


#Variables and lists (global)
#Items for hire (drop list)
droplist = ["Select an option", "Tables", "Chairs", "Plates", "String lights", "Cutlery", "Plates", "Bowls"]
clicked = StringVar()
clicked.set(droplist[0])
identify = -1    #For indentifying which group (-1 so that id = row)
info = []   #List for information
errors = []
hasup = 0   #Used for checking whether or not the update button needs to be removed
#Current date
date = dt.datetime.now()

#Functions
def updatescroll():
    #For updateing scroll region
    can.update_idletasks()
    can.config(scrollregion=frame3.bbox())

def confirm(button):
    #This double checks with the user whether or not they want to go through with an action
    global answer
    answer = askyesno(title="Confirmation", message=f"Are you sure you want to {button} this")

def validity():
    #Add max characters for inputs
    checking = [ name.get(), receipt.get(), clicked.get(), num.get()]   #Values inputed that need to be checked
    index = 0
    for i in checking:       
        if index == 0:
            if i == "":
                errors.append("You cannot leave the name blank.")
        elif index == 1:
            if i == "":
                errors.append("You cannot leave the receipt number blank.")
            else:
                try:
                    isint = int(i)
                except:
                    errors.append("The receipt number must be an integer.")
        elif index == 2:
            if i == "Select an option":
                errors.append("You must select an item being hired.")
        elif index == 3:
            if i == "":
                errors.append("You cannot leave the number of items hired blank.")
            else:
                try:
                    isint = int(i)
                    if isint < 1 or isint > 500:
                        errors.append("You cannot hire more than 500 or less then 1.")
                except:
                    errors.append("The number of items hired must be an integer.")
        else:
                errors.append("Something has gone wrong")
        index += 1

def error():
    #This is a pop up window that shows all of the errors
    top = Toplevel(root)
    #top.geometry("500x350")
    title = Label(top, text="Your entry has the following errors", font=(("Gorgia"),18), bg="Yellow")
    title.grid(row=0, column=0, sticky=W+E) #Griding a title
    global errors
    labels = [] #Allows me to easily grid all of the labels
    for i in errors:
        labels.append(Label(top, text=i, font=(("Gorgia"), 14)))
    for v in range(len(labels)):
        labels[v].grid(row=v + 1, column=0, sticky=W)
    ok = Button(top, text="OK", command= lambda: top.destroy())
    ok.grid(row= 10, column=0)
    errors = []
        
def reset():
    hire.selection_set(date.today())
    name.delete(0,END)
    receipt.delete(0, END)
    num.delete(0, END)
    clicked.set(droplist[0])

def entered():
    global identify
    global answer   #Uses previously defined answer
    identify +=1
    btn = identify  #Is whichever row its in and helps with identifying later on
    validity()  #Checkes the validity of all the entries
    confirm("enter")   #Double checks they want to do something
    global errors
    if errors == [] and answer:
        info.append(
            [btn, [
                Label(frame3, text=order.cget("text"), font=(("Gorgia"), 14)),
                Label(frame3, text=hire.get_date(), font=(("Gorgia"), 14)),
                Label(frame3, text=name.get(), font=(("Gorgia"), 14)),
                Label(frame3, text=receipt.get(), font=(("Gorgia"), 14)),
                Label(frame3, text=clicked.get(), font=(("Gorgia"), 14)),
                Label(frame3, text=num.get(), font=(("Gorgia"), 14)),
                Button(frame3, text="Edit", font=(("Gorgia"), 14), bg="Orange", command=lambda c=btn: edit(c)),
                    Button(frame3, text="Returned", font=(("Gorgia"), 14), bg="Red", command=lambda g=btn: returned(g))
                #The buttons each place btn (indentifier) into a variable to use in edit and return. (identifies it)
                ]
            ]
        )
        #Putting everything on the grid
        for y in range(len(info[-1][1])):
            info[-1][1][y].grid(row=len(info), column=y, sticky=W)
        #Updtaes scroll region
        updatescroll()
        #Resets all inputs
        reset()
    elif errors != [] and answer:
        error() #This is the pop up window function which will show the errors in the inputs

def updated(p):
    validity()
    global hasup
    confirm("update")
    if errors == [] and answer:
        #This will update the list, order date never changes as its not a most recent update function
        info[p][1][1].config(text = hire.get_date())
        info[p][1][2].config(text = name.get())
        info[p][1][3].config(text = receipt.get())
        info[p][1][4].config(text = clicked.get())
        info[p][1][5].config(text = num.get())
        reset()
        update.destroy()
        enter.grid(row=4, column=6, sticky=W)
        hasup -= 1
    elif errors != []:
        error()

def edit(e):
    #This will allow Julie to edit the orders she's already logged
    global hasup
    reset()
    for y,x in enumerate(info):
        if x[0] == e:
            i = y
    toedit = [] #Stores all the inputed values from list
    #This gives the previously inputed values
    for y in range(0, 6):
        toedit.append(info[i][1][y].cget("text"))
    #This places previously inputed values into the entry boxes and drop down list
    hire.selection_set(toedit[1])
    name.insert(0, toedit[2])
    receipt.insert(0, toedit[3])
    clicked.set(toedit[4])
    num.insert(0, toedit[5])
    #Changes the enter button to update button
    enter.grid_forget()
    global update
    update = Button(frame1, text="Update", font=(("Gorgia"), 14), bg="Yellow", command=lambda: updated(i))
    update.grid(row=4, column=6, sticky=W)
    hasup += 1

def returned(r):
    #This will allow Jullie to return (and as such delete) orders
    global hasup
    confirm("reutrn")
    if answer:
        #Ensures the program still functions if you return what you're trying to edit
        if hasup == 1:
            global update
            update.destroy()
            hasup -= 1
            enter.grid(row=4, column=6, sticky=W)
        reset()
        back = int(r)   #This is to make the number an integer
        for i in info:
            index = info.index(i)   #This gets the index of the current group
            if back == i[0]:
                for a in range(0, 8):
                    info[index][1][a].destroy() #This destroys the desired index 
                del info[index]     #Deletes the group from the list
                break
        #Moves all labels into correct positions
        for y in range(len(info)):
            if index <= y:
                for t in range(len(info[-1][1])):
                    info[y][1][t].grid(row=y + 1, column=t, sticky=W)
        #Updtaes scroll region
        updatescroll()

#Creating constant labels and giving the page a title
root.title("Julie's Party Hire")
title = Label(frame1, text="Julie's Party Hire", font=(("Gorgia"), 20)) #Main title
lblorder = Label(frame1, text="Date ordered", font=(("Gorgia"), 16))
lblhire = Label(frame1, text="Date hired", font=(("Gorgia"), 16))
lblname = Label(frame1, text="Full name", font=(("Gorgia"), 16))
lblitem = Label(frame1, text="Item hired", font=(("Gorgia"), 16))
lblreceipt = Label(frame1, text="Receipt number", font=(("Gorgia"), 16))
lblnum = Label(frame1, text="Item amount", font=(("Gorgia"), 16))

dorder = Label(frame1, text="Date ordered", font=(("Gorgia"), 14))
dhire = Label(frame1, text="Date hired", font=(("Gorgia"), 14))
dname = Label(frame1, text="Full name", font=(("Gorgia"), 14))
ditem = Label(frame1, text="Item hired", font=(("Gorgia"), 14))
dreceipt = Label(frame1, text="Receipt", font=(("Gorgia"), 14))
dnum = Label(frame1, text="Item amount", font=(("Gorgia"), 14))

#Creating entry boxes and label for date grab and calendar
order = Label(frame1, text=f"{date:%d, %B, %Y}", font=(("Gorgia"), 14)) #Text gotten from date which was defined at the top of page
hire = Calendar(frame1, slectmode="day", font=(("Gorgia"), 6), date_pattern='dd/MM/yyyy', mindate= date)    #The date chosen cannot be before the current date
name = Entry(frame1, font=(("Gorgia"), 14), width=12)
receipt = Entry(frame1, font=(("Gorgia"), 14), width=12)
num = Entry(frame1, font=(("Gorgia"), 14), width=12)

#Creating button
enter = Button(frame1, text="Enter", font=(("Gorgia"), 14), bg="Green", command=entered)

#Dropdown list
dropdown = OptionMenu(frame1, clicked, *droplist)

#placing all the labels
title.grid(row=0, column=3, columnspan=2)
lblorder.grid(row=1, column=0, sticky=W)
lblhire.grid(row=1, column=4, sticky=W+E)
lblname.grid(row=2, column=0, sticky=W)
lblitem.grid(row=2, column=2, sticky=W)
lblreceipt.grid(row=3, column=0, sticky=W)
lblnum.grid(row=3, column=2, sticky=W)

dorder.grid(row=5, column=0, sticky=W)
dhire.grid(row=5, column=1, sticky=W)
dname.grid(row=5, column=2, sticky=W)
dreceipt.grid(row=5, column=3, sticky=W)
ditem.grid(row=5, column=4, sticky=W)
dnum.grid(row=5, column=5, sticky=W)

#Placeing the entry boxes
order.grid(row=1, column=1, sticky=W)
hire.grid(row=2, column=4, rowspan=3, columnspan=2)
name.grid(row=2, column=1, sticky=W)
receipt.grid(row=3,column=1, sticky=W)
num.grid(row=3, column=3, sticky=W)

#Placing buton
enter.grid(row=4, column=6, sticky=W)

#placeing dropdown list
dropdown.grid(row=2, column=3, sticky=W)

root.geometry("1300x600")
root.mainloop()