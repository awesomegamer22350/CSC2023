from tkinter import *
from tkinter import ttk
from datetime import datetime

root = Tk()
root.title("Julie's Party")
root.geometry("1400x800")

def removefromgrid(removethis):
	removethis.grid_remove()

def update(rownum, btnid):
	for x in range(len(biglist)):
		if biglist[x][0]==rownum:
			biglist[x][1][btnid-1][0].configure(text=editEntrybox.get())
			biglist[x][1][4][0].configure(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

			if btnid==1:
				biglist[x][1][0][1].configure(text=f'Update Receipt {editEntrybox.get()}')
				del sortlist[x]
				pp=biglist.pop(x)

				receiptnum=int(editEntrybox.get())
				print(receiptnum)
				receiptposition=-1; a=0
				for receiptposition, y in enumerate(sortlist):
					if receiptnum<y:
						a=1
						break
				if a==0:
					receiptposition+=1
				sortlist.insert(receiptposition, receiptnum)
				biglist.insert(receiptposition, pp)
				for x, y in enumerate(biglist):
					for p, q in enumerate(y[1]):
						q[0].grid(row=3*x+1, column=p)
						q[1].grid(row=3*x+2, column=p)
					y[2].grid(row=3*x+2)
					y[3].grid(row=3*x+3)
	#if len(editEntrybox.get()) >= 23:
	#	toolonglbl.grid()
	#	root.after(3000, lambda: removefromgrid(toolonglbl))
	#	return
	#if btnid==3:
	#	if Entrybox.get().strip().isdigit() == FALSE:
	#		notanintlbl.grid()
	#		root.after(3000, lambda: removefromgrid(notanintlbl))
	#		return
	updateScrollRegion()


def log(*args):
	global identification
	identification+=1
	rownum=identification
	receiptnum=int(ReceiptEntrybox.get())

	receiptposition=-1; a=0
	for receiptposition, y in enumerate(sortlist):
		if receiptnum<y:
			a=1
			break
	if a==0:
		receiptposition+=1
	sortlist.insert(receiptposition, receiptnum)
	biglist.insert(receiptposition, [rownum, [
	[Label(Frame3, text=receiptnum, font=("Arial", 13, "bold"), height=1),
	Button(Frame3, text=f"Update Receipt {receiptnum}", command=lambda btnid=1: update(rownum, btnid))],
	[Label(Frame3, text=CustomernameEntrybox.get()),
	Button(Frame3, text=f"Update Name", command=lambda btnid=2: update(rownum, btnid))],
	[Label(Frame3, text=ItemHiredEntrybox.get()),
	Button(Frame3, text=f"Update Item", command=lambda btnid=3: update(rownum, btnid))],
	[Label(Frame3, text=NumHiredEntrybox.get()),
	Button(Frame3, text=f"Update hired no.", command=lambda btnid=4: update(rownum, btnid))],
	[Label(Frame3, text=datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
  	Button(Frame3, text="Delete Receipt", command=lambda: deletegroup(rownum))]
	], 
	Label(Frame3, text='', height=2), ttk.Separator(Frame3)])
	for x, y in enumerate(biglist):
		for p, q in enumerate(y[1]):
			q[0].grid(row=3*x+1, column=p)
			q[1].grid(row=3*x+2, column=p)
			if isedit==0 and p!=4:
				q[1].grid_remove()
		y[2].grid(row=3*x+2, column=5)
		y[3].grid(row=3*x+3, column=0, columnspan=999, sticky="ew")

	updateScrollRegion()


# delete a group
def deletegroup(row):
	# tracks that this group has been deleted
	for x in range(len(biglist)):
		if biglist[x][0] == row:
			saved = biglist[x]
			del sortlist[x]
			del biglist[x]
			break
	# update text
	for x, y in enumerate(biglist):
		for p, q in enumerate(y[1]):
			q[0].grid(row=3*x+1)
			q[1].grid(row=3*x+2)
			if isedit==0 and p!=4:
				q[1].grid_remove()
		y[2].grid(row=3*x+2)
		y[3].grid(row=3*x+3)
	for line in saved[1]:
		line[0].destroy()
		line[1].destroy()
	saved[2].destroy()
	saved[3].destroy()

	updateScrollRegion()



def editmode():
	global isedit
	isedit=1
	Receiptlbl.grid_remove()
	ReceiptEntrybox.grid_remove()
	Customernamelbl.grid_remove()
	CustomernameEntrybox.grid_remove()
	ItemHiredlbl.grid_remove()
	ItemHiredEntrybox.grid_remove()
	NumHiredlbl.grid_remove()
	NumHiredEntrybox.grid_remove()
	Logbtn.grid_remove()
	editTextbox.grid()
	editEntrybox.grid()
	editbtn.place_forget()
	exitEdit.place(x=0, y=750)
	for x in biglist:
		for y in x[1]:
			y[1].grid()

def exitedit():
	global isedit
	isedit=0
	editTextbox.grid_remove()
	editEntrybox.grid_remove()
	Receiptlbl.grid()
	ReceiptEntrybox.grid()
	Customernamelbl.grid()
	CustomernameEntrybox.grid()
	ItemHiredlbl.grid()
	ItemHiredEntrybox.grid()
	NumHiredlbl.grid()
	NumHiredEntrybox.grid()
	Logbtn.grid()
	editbtn.place(x=0, y=750)
	exitEdit.place_forget()
	for x in biglist:
		for y, z in enumerate(x[1]):
			if y!=4:
				z[1].grid_remove()

def validity():
	# Label for invalid input for integers
	notanintlbl = Label(Frame1, text="Not an int or is negative", fg='red')
	notanintlbl.grid(row=0, column=2)
	notanintlbl.grid_remove()

	# Label for inputs that are too long
	toolonglbl = Label(Frame1, text="your input is too long, it must be under 23 characters", fg='red')
	toolonglbl.grid(row=0, column=2)
	toolonglbl.grid_remove()

	# Label for input if not between 5-10 campers
	outsiderangelbl = Label(Frame1, text="Warning: there should be between 5-10 campers", fg='red')
	outsiderangelbl.grid(row=0, column=3)
	outsiderangelbl.grid_remove()

def updateScrollRegion():
	canvas.update_idletasks()
	canvas.config(scrollregion=Frame3.bbox())
	
# prevents allowing unessesary scrolling with mousewheel over scrollbar
def whentoscroll(*arguments):
	if Frame3.winfo_height() > canvas.winfo_height():
		canvas.yview(*arguments)

def bindToCanvas(*args):
    root.bind_all("<MouseWheel>", lambda event: whentoscroll('scroll', -1*event.delta, 'units'))

def unbindToCanvas(*args):
	root.unbind_all("<MouseWheel>")



categorylist = ["Receipt no.", "Customer Name: ", "Item Hired: ", "Number of Items Hired: ", "Last Updated: "]
biglist = []
sortlist = []
identification=-1
isedit=0

Frame1 = Frame(root)
Frame1.place(x=0, y=5)

Receiptlbl = Label(Frame1, text='Receipt')
Receiptlbl.grid(row=0, column=0)

ReceiptEntrybox = Entry(Frame1)
ReceiptEntrybox.grid(row=0, column=1)

Customernamelbl = Label(Frame1, text='Customer Name')
Customernamelbl.grid(row=0, column=2)

CustomernameEntrybox = Entry(Frame1)
CustomernameEntrybox.grid(row=0, column=3)

ItemHiredlbl = Label(Frame1, text='Item Hired')
ItemHiredlbl.grid(row=0, column=4)

ItemHiredEntrybox = Entry(Frame1)
ItemHiredEntrybox.grid(row=0, column=5)

NumHiredlbl = Label(Frame1, text='Number Hired')
NumHiredlbl.grid(row=0, column=6)

NumHiredEntrybox = Entry(Frame1)
NumHiredEntrybox.grid(row=0, column=7)

Logbtn = Button(Frame1, text= 'Log Receipt', command=log)
Logbtn.grid(row=0, column=8)



editTextbox = Label(Frame1, text='Input below and then press an "update" button')
editTextbox.grid(row=0, column=0)


editEntrybox = Entry(Frame1)
editEntrybox.grid(row=1, column=0)

#validity()

# Frame 2 keeps the grid of the below stuff in different columns than the stuff in Frame 1
Frame2 = Frame(root)
Frame2.place(x=0, y=100)
# create a canvas
canvas = Canvas(Frame2, width=1200, height=600, highlightthickness=0)
canvas.pack(fill=BOTH, side=LEFT, expand=TRUE)
# create scrollbar
scrollbar = Scrollbar(Frame2, orient=VERTICAL, command=whentoscroll)
scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)


# configure canvas
canvas['yscrollcommand']=scrollbar.set
# create another frame inside canvas
Frame3 = Frame(canvas)
canvas.create_window(10, 0, window=Frame3, anchor=NW, width=1200)
Frame3.bind("<Enter>", lambda event: bindToCanvas())
Frame3.bind("<Leave>", lambda event: unbindToCanvas())

# Text for Catagories
for i in range(len(categorylist)):
	Label(Frame3, text=categorylist[i], width=20, height=2, font=("Arial", 14, "bold")).grid(row=0, column=i)


editbtn = Button(root, text="Edit", command=editmode)
exitEdit = Button(root, text="Exit Edit", command=exitedit)
exitedit()

root.mainloop()