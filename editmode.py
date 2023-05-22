from tkinter import *
from tkinter import ttk
from datetime import datetime

root = Tk()
root.title("Julie's Party")
root.geometry("1400x800")

def removefromgrid(removethis): #for root.after
	removethis.grid_remove()


def sortreceipt(receiptnum):
	receiptposition=-1; a=0
	for receiptposition, y in enumerate(sortlist):
		if receiptnum<y:
			a=1
			break
	if a==0:
		receiptposition+=1
	sortlist.insert(receiptposition, receiptnum)
	return receiptposition



def update(rownum, btnid):
	for x in range(len(biglist)):
		if biglist[x][0]==rownum:
			editbox = editEntrybox.get()

			if editbox =='':
				isemptylbl.grid(row=2, column=0, columnspan=10, sticky=W)
				root.after(2000, lambda: removefromgrid(isemptylbl))
				return
			
			if len(editbox)>14:
				toolonglbl.grid(row=2, column=0, columnspan=10, sticky=W)
				root.after(2000, lambda: removefromgrid(toolonglbl))

			if btnid==1 or btnid==4:
				try:
					editbox = int(editbox)
				except:
					notanintlbl.grid(row=2, column=0, columnspan=10, sticky=W)
					root.after(2000, lambda: removefromgrid(notanintlbl))
					return
	
				if editbox<0:
					negativeintlbl.grid(row=2, column=0, columnspan=10, sticky=W)
					root.after(2000, lambda: removefromgrid(negativeintlbl))
					return

			if btnid==1 and editbox in sortlist:
				alreadyexistslbl.grid(row=2, column=0, columnspan=10, sticky=W)
				root.after(2000, lambda: removefromgrid(alreadyexistslbl))
				return					

			biglist[x][1][btnid-1][0].configure(text=editEntrybox.get())
			biglist[x][1][4][0].configure(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))

			if btnid==1:
				biglist[x][1][0][1].configure(text=f'Update Receipt {editEntrybox.get()}')
				del sortlist[x]
				contents=biglist.pop(x)

				receiptposition = sortreceipt(editbox)				
				biglist.insert(receiptposition, contents)
				for x, y in enumerate(biglist):
					for p, q in enumerate(y[1]):
						q[0].grid(row=3*x+1, column=p)
						q[1].grid(row=3*x+2, column=p)
					y[2].grid(row=3*x+2)
					y[3].grid(row=3*x+3)
			break
	updateScrollRegion()


def log(*args):

	global identification
	identification+=1
	rownum=identification
	entryboxlist=[
		ReceiptEntrybox.get().strip(), 
	    CustomernameEntrybox.get().strip(), 
		ItemHiredEntrybox.get().strip(), 
		NumHiredEntrybox.get().strip()]

	for x in entryboxlist:
		if x =='':
			isemptylbl.grid(row=2, column=0, columnspan=10, sticky=W)
			root.after(2000, lambda: removefromgrid(isemptylbl))
			return
		if len(x)>14:
			toolonglbl.grid(row=2, column=0, columnspan=10, sticky=W)
			root.after(2000, lambda: removefromgrid(toolonglbl))
			return

	try:
		entryboxlist[0]=int(entryboxlist[0])
		entryboxlist[3]=int(entryboxlist[3])
	except:
		notanintlbl.grid(row=2, column=0, columnspan=10, sticky=W)
		root.after(2000, lambda: removefromgrid(notanintlbl))
		return
	
	if entryboxlist[0]<0 or entryboxlist[3]<0:
		negativeintlbl.grid(row=2, column=0, columnspan=10, sticky=W)
		root.after(2000, lambda: removefromgrid(negativeintlbl))
		return

	if entryboxlist[0] in sortlist:
		alreadyexistslbl.grid(row=2, column=0, columnspan=10, sticky=W)
		root.after(2000, lambda: removefromgrid(alreadyexistslbl))
		return	

	receiptposition = sortreceipt(entryboxlist[0])

	biglist.insert(receiptposition, [rownum, [
	[Label(Frame3, text=entryboxlist[0], font=("Arial", 13, "bold"), height=1),
	Button(Frame3, text=f"Update Receipt {entryboxlist[0]}", command=lambda btnid=1: update(rownum, btnid))],
	[Label(Frame3, text=entryboxlist[1]),
	Button(Frame3, text=f"Update Name", command=lambda btnid=2: update(rownum, btnid))],
	[Label(Frame3, text=entryboxlist[2]),
	Button(Frame3, text=f"Update Item", command=lambda btnid=3: update(rownum, btnid))],
	[Label(Frame3, text=entryboxlist[3]),
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
root.bind('<Return>', log)




editTextbox = Label(Frame1, text='Input below and then press an "update" button')
editTextbox.grid(row=0, column=0)


editEntrybox = Entry(Frame1)
editEntrybox.grid(row=1, column=0)


# Label for invalid input for integers
isemptylbl = Label(Frame1, text="Do not leave any inputs empty", fg='red')


# Label for invalid input for integers
notanintlbl = Label(Frame1, text="Do not input non-integers", fg='red')


# Label for invalid input for integers
negativeintlbl = Label(Frame1, text="Do not input negative integers", fg='red')


# Label for inputs that are too long
toolonglbl = Label(Frame1, text="Do not input anything longer than 14 characters", fg='red')

# Label for invalid input for integers
alreadyexistslbl = Label(Frame1, text="A Receipt with this number already exists", fg='red')






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