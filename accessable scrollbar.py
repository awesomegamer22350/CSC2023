from tkinter import *
from tkinter import ttk
from datetime import datetime

root = Tk()
root.title("Julie's Party Hire")
root.geometry("1400x800")


#log/create a new reciept
def log(*args):
	global identification
	if isedit==1: #if in edit mode, you shouldn't be able to make new receipt
		return
	identification+=1
	rowid=identification
	entryboxlist=[
		ReceiptEntrybox.get().strip(), 
	    CustomernameEntrybox.get().strip(), 
		ItemHiredEntrybox.get().strip(), 
		NumHiredEntrybox.get().strip()]

	#validity
	for inputs in entryboxlist:
		if inputs =='':
			isemptylbl.grid(row=2, column=0, columnspan=10, sticky=W)
			root.after(2000, lambda: removefromgrid(isemptylbl))
			return
		if len(inputs)>14:
			toolonglbl.grid(row=2, column=0, columnspan=10, sticky=W)
			root.after(2000, lambda: removefromgrid(toolonglbl))
			return
	try: #checks if Receipt Number input and Number hired input is an integer
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

	receiptposition = sortreceipt(entryboxlist[0]) #finds which row the receipt should be inserted into
	#create new row with all the widgets inside
	biglist.insert(receiptposition, [rowid, [
	[Label(receiptframe, text=entryboxlist[0], font=("Arial", 13, "bold"), height=1),
	Button(receiptframe, text=f"Update Receipt\n{entryboxlist[0]}", command=lambda btnnum=1: edit(rowid, btnnum))],
	[Label(receiptframe, text=entryboxlist[1]),
	Button(receiptframe, text=f"Update Name", command=lambda btnnum=2: edit(rowid, btnnum))],
	[Label(receiptframe, text=entryboxlist[2]),
	Button(receiptframe, text=f"Update Item", command=lambda btnnum=3: edit(rowid, btnnum))],
	[Label(receiptframe, text=entryboxlist[3]),
	Button(receiptframe, text=f"Update hired no.", command=lambda btnnum=4: edit(rowid, btnnum))],
	[Label(receiptframe, text=datetime.now().strftime("%d/%m/%Y %H:%M:%S")),
  	Button(receiptframe, text="Delete Receipt", command=lambda: deletegroup(rowid))]
	], 
	Label(receiptframe, text='', height=3), ttk.Separator(receiptframe)])
	#clear input fields
	ReceiptEntrybox.delete(0, 'end')
	CustomernameEntrybox.delete(0, 'end')
	ItemHiredEntrybox.delete(0, 'end')
	NumHiredEntrybox.delete(0, 'end')
	resortrows()

# deletes a receipt
def deletegroup(rowid):
	for row in range(len(biglist)):
		if biglist[row][0] == rowid: #biglist[row][0] stores the identification given to every row, rowid is the number given to this button to identify which row its in
			#destroy all the widgets
			for line in biglist[row][1]:
				line[0].destroy()
				line[1].destroy()
			biglist[row][2].destroy()
			biglist[row][3].destroy()
			#remove the row from the lists
			del sortlist[row]
			del biglist[row]
			break
	updateScrollRegion() #updates how big the scrolling area is

#update/edit something stored in the table
def edit(rowid, btnnum):
	for row in range(len(biglist)):
		if biglist[row][0]==rowid: #biglist[row][0] stores the identification given to every row, rowid is the number given to this button to identify which row its in
			editbox = editEntrybox.get()

			#validity
			if editbox =='':
				isemptylbl.grid(row=2, column=0, columnspan=10, sticky=W)
				root.after(2000, lambda: removefromgrid(isemptylbl))
				return
			if len(editbox)>14:
				toolonglbl.grid(row=2, column=0, columnspan=10, sticky=W)
				root.after(2000, lambda: removefromgrid(toolonglbl))
			if btnnum==1 or btnnum==4:
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
			if btnnum==1 and editbox in sortlist:
				alreadyexistslbl.grid(row=2, column=0, columnspan=10, sticky=W)
				root.after(2000, lambda: removefromgrid(alreadyexistslbl))
				return
			
			biglist[row][1][btnnum-1][0].configure(text=editEntrybox.get())
			biglist[row][1][4][0].configure(text=datetime.now().strftime("%d/%m/%Y %H:%M:%S"))
			if btnnum==1: #if the receipt number is being changed, record which row it should be moved to in sortlist for resortrows
				biglist[row][1][0][1].configure(text=f'Update Receipt\n{editEntrybox.get()}')
				del sortlist[row]
				contents=biglist.pop(row)
				receiptposition = sortreceipt(editbox)				
				biglist.insert(receiptposition, contents)
			break #ends loop here

#finds which row the receipt should be inserted into
def sortreceipt(receiptnumber):
	receiptposition=-1; endoflist=1
	for receiptposition, receipt in enumerate(sortlist): #increments receiptposition until it matches the index of where the receipt should go
		if receiptnumber<receipt: #if the receipt in the list is bigger than the receipt we are adding, save the index as receipt number
			endoflist=0
			break
	if endoflist==1: #if it reaches the end of the list, increment by one as it should go on the end of the list
		receiptposition+=1
	sortlist.insert(receiptposition, receiptnumber) #add the receipt to the list that keeps track of the receipt positions
	return receiptposition

#sorts the receipts into their correct rows in ascending order of receipt number
def resortrows():
	for rowindex, row in enumerate(biglist):
		for widgettype, widget in enumerate(row[1]):
			widget[0].grid(row=3*rowindex+1, column=widgettype)
			widget[1].grid(row=3*rowindex+2, column=widgettype)
			if widgettype!=4:
				widget[1].grid_remove()
		row[2].grid(row=3*rowindex+2, column=5)
		row[3].grid(row=3*rowindex+3, column=0, columnspan=999, sticky="ew")
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
	exitEdit.place(x=30, y=720)
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
	editbtn.place(x=30, y=720)
	exitEdit.place_forget()
	resortrows()

def updateScrollRegion(): #updates the region you can scroll in according to the size of the frame
	canvas.update_idletasks()
	canvas.config(scrollregion=receiptframe.bbox())

def whentoscroll(*arguments): #when the frame is smaller than the canvas it can still scroll, this prevents the unessessary scrolling
	if receiptframe.winfo_height() > canvas.winfo_height():
		canvas.yview(*arguments)

def bindToCanvas(*args): #when entering the region of the canvas, bind the scrollbar to scroll
    root.bind_all("<MouseWheel>", lambda event: whentoscroll('scroll', -1*delta(event), 'units'))
    root.bind_all("<Button-4>", lambda event: whentoscroll('scroll', -1*delta(event), 'units'))
    root.bind_all("<Button-5>", lambda event: whentoscroll('scroll', -1*delta(event), 'units'))

def unbindToCanvas(*args): #unbind when leaving
	root.unbind_all("<MouseWheel>")
	root.unbind_all("<Button-4>")
	root.unbind_all("<Button-5>")

def delta(event): #for scrolling up or down and accounts for the operating system
	if event.num == 5 or event.delta<0:
		return -1
	return 1

def removefromgrid(removethis): #root.after cannot directly have '.grid_remove' inside it so I put it into a function
	removethis.grid_remove()

biglist = [] #holds the widgets that hold the receipts
sortlist = [] #stores the position of where each receipt should be
identification=-1
isedit=0

topframe = Frame(root)
topframe.place(x=20, y=10)

#widgets for logging receipt 
Receiptlbl = Label(topframe, text='Receipt')
Receiptlbl.grid(row=0, column=0)

ReceiptEntrybox = Entry(topframe)
ReceiptEntrybox.grid(row=0, column=1)

Customernamelbl = Label(topframe, text='Customer Name')
Customernamelbl.grid(row=0, column=2)

CustomernameEntrybox = Entry(topframe)
CustomernameEntrybox.grid(row=0, column=3)

ItemHiredlbl = Label(topframe, text='Item Hired')
ItemHiredlbl.grid(row=0, column=4)

ItemHiredEntrybox = Entry(topframe)
ItemHiredEntrybox.grid(row=0, column=5)

NumHiredlbl = Label(topframe, text='Number Hired')
NumHiredlbl.grid(row=0, column=6)

NumHiredEntrybox = Entry(topframe)
NumHiredEntrybox.grid(row=0, column=7)

Logbtn = Button(topframe, text= 'Log Receipt', command=log)
Logbtn.grid(row=0, column=8)
root.bind('<Return>', log)

#widgets for edit receipts 
editTextbox = Label(topframe, text='Input below and then press an "update" button')
editTextbox.grid(row=0, column=0)

editEntrybox = Entry(topframe)
editEntrybox.grid(row=1, column=0)


#widgets for validity
# Label for invalid input for integers
isemptylbl = Label(topframe, text="Do not leave any inputs empty", fg='red')

# Label for invalid input for integers
notanintlbl = Label(topframe, text="Do not input non-integers", fg='red')

# Label for invalid input for integers
negativeintlbl = Label(topframe, text="Do not input negative integers", fg='red')

# Label for inputs that are too long
toolonglbl = Label(topframe, text="Do not input anything longer than 14 characters", fg='red')

# Label for invalid input for integers
alreadyexistslbl = Label(topframe, text="A Receipt with this number already exists", fg='red')


# bottomframe holds the receipts and the scrollbar
bottomframe = Frame(root)
bottomframe.place(x=10, y=120)
# tkinter can allowing scrolling of the contents of a canvas, so a canvas is used to store a frame with the widgets
canvas = Canvas(bottomframe, width=1100, height=600, highlightthickness=0)
canvas.pack(fill=BOTH, side=LEFT, expand=TRUE, padx = (0, 20))
# create scrollbar
scrollbar = Scrollbar(bottomframe, orient=VERTICAL, command=whentoscroll)
scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
# configure canvas
canvas['yscrollcommand']=scrollbar.set
# create a frame inside canvas to hold the widgets for the receipts
receiptframe = Frame(canvas)
canvas.create_window(10, 0, window=receiptframe, anchor=NW, width=1100)
receiptframe.bind("<Enter>", lambda event: bindToCanvas()) #bind scrolling method
receiptframe.bind("<Leave>", lambda event: unbindToCanvas())
receiptframe.columnconfigure(0, weight=2) #make receiptnumber column bigger

categorylist = ["Receipt no.", "Customer Name: ", "Item Hired: ", "Number of Items Hired: ", "Last Updated: "]
# Create widgets for the headers for each category
for categorynum in range(len(categorylist)):
	Label(receiptframe, text=categorylist[categorynum], width=20, height=2, font=("Arial", 14, "bold")).grid(row=0, column=categorynum)
	if categorynum!=0:
		receiptframe.columnconfigure(categorynum, weight=1)

#create edit and exit buttons
editbtn = Button(root, text="Edit", command=editmode, height=3, font=("Arial", 16), bg='yellow')
exitEdit = Button(root, text="Exit Edit and Save", command=exitedit, height=3, font=("Arial", 16), bg='yellow')
exitedit() #start in logging mode

root.mainloop()
#commit