from tkinter import *

root = Tk()
root.title("Julie's Party")
root.geometry("1400x800")

def removefromgrid(removethis):
	removethis.grid_remove()

def update(rownum, btnid):
	if len(editEntrybox.get()) >= 23:
		toolonglbl.grid()
		root.after(3000, lambda: removefromgrid(toolonglbl))
		return
	#if btnid==3:
		if Entrybox.get().strip().isdigit() == FALSE:
			notanintlbl.grid()
			root.after(3000, lambda: removefromgrid(notanintlbl))
			return
	for x in range(len(biglist)):
		if biglist[x][0]==rownum:
			biglist[x][1][btnid-1][0].configure(text=editEntrybox.get())

def log(*args):
	global identification
	identification+=1
	rownum=identification
	receiptnum=int(ReceiptEntrybox.get())

	receiptposition=-1; a=0
	for receiptposition, y in enumerate(sortlist):
		if receiptnum<=y:
			a=1
			break
	if a==0:
		receiptposition+=1

	print(receiptposition)
	sortlist.insert(receiptposition, receiptnum)
	print(sortlist)
	biglist.insert(receiptposition, [rownum, [
	[Label(Frame3, text=receiptnum, font=("Arial", 13, "bold"), height=1),
	Button(Frame3, text=f"Update Receipt {receiptnum}", command=lambda btnid=1: update(rownum, btnid))],
	[Label(Frame3, text=CustomernameEntrybox.get()),
	Button(Frame3, text=f"Update Name", command=lambda btnid=2: update(rownum, btnid))],
	[Label(Frame3, text=ItemHiredEntrybox.get()),
	Button(Frame3, text=f"Update Item", command=lambda btnid=3: update(rownum, btnid))],
	[Label(Frame3, text=NumHiredEntrybox.get()),
	Button(Frame3, text=f"Update hired no.", command=lambda btnid=4: update(rownum, btnid))],
	[Label(Frame3, text=""),
  	Button(Frame3, text="Delete Receipt", command=lambda: deletegroup(rownum))]
	], 
	Label(Frame3, text='', height=2)])

	for x, y in enumerate(biglist):
		for p, q in enumerate(y[1]):
			q[0].grid(row=2*x+1, column=p)
			q[1].grid(row=2*x+2, column=p)
		y[2].grid(row=2*x+2, column=5)

	updateScrollRegion()

# delete a group
def deletegroup(row):
	# tracks that this group has been deleted
	for x in range(len(biglist)):
		if biglist[x][0] == row:
			saved = biglist[x][1]
			del biglist[x]
			break
	# update text
	for x, y in enumerate(biglist):
		for q in y[1]:
			q[0].grid(row=2*x+1)
			q[1].grid(row=2*x+2)
		y[2].grid(row=2*x+2)
	for line in saved:
		line[0].grid_remove()
		line[1].grid_remove()
	updateScrollRegion()

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



categorylist = ["Receipt no.", "Customer Name: ", "Item Hired: ", "Number of Items Hired: "]
biglist = []
sortlist = []
identification=-1


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

Logbtn = Button(Frame1, text= 'Log Receipt', command= log)
Logbtn.grid(row=0, column=8)



editTextbox = Label(Frame1, text='Input below and then press an "update" button')
editTextbox.grid(row=0, column=0)
editTextbox.grid_remove()


editEntrybox = Entry(Frame1)
editEntrybox.grid(row=1, column=0)
editEntrybox.grid_remove()



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
	Label(Frame3, text=categorylist[i], width=20, height=2, font=("Arial", 14, "bold"),anchor=W).grid(row=0, column=i)


root.mainloop()