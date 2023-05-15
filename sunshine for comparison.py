from tkinter import *

root = Tk()
root.title("Julie's Party")
root.geometry("1400x800")
categorylist = ["Group no.", "Leader: ", "Location: ", "No. of campers: ", "Weather Conditions: "]
categorytracker = 0
biglist = []

def removefromgrid(removethis):
	removethis.grid_remove()

def update(rownum, btnid):
	if len(Entrybox.get()) >= 23:
		toolonglbl.grid()
		root.after(3000, lambda: removefromgrid(toolonglbl))
		return
	if btnid==3:
		if Entrybox.get().strip().isdigit() == FALSE:
			notanintlbl.grid()
			root.after(3000, lambda: removefromgrid(notanintlbl))
			return
		if 5 > int(Entrybox.get().strip()) or 10 < int(Entrybox.get().strip()):
			outsiderangelbl.grid()
			root.after(3000, lambda: removefromgrid(outsiderangelbl))
			return
	for x in range(len(biglist)):
		if biglist[x][0]==rownum:
			biglist[x][1][btnid][0].configure(text=Entrybox.get())

def addgroup(*arguements):
	global identification
	identification+=1
	rownum=identification
	biglist.append(
	[rownum, [
	[Label(Frame3, text=f"Group {len(biglist)+1}:", font=("Arial", 13, "bold"), height=1),
	Label(Frame3, text="", height=2)],
	[Label(Frame3, text="Leader"),
	Button(Frame3, text=f"Update Leader {len(biglist)+1}", command=lambda btnid=1: update(rownum, btnid))],
	[Label(Frame3, text="Location"),
	Button(Frame3, text=f"Update Location {len(biglist)+1}", command=lambda btnid=2: update(rownum, btnid))],
	[Label(Frame3, text="Student count"),
	Button(Frame3, text=f"Update Campers {len(biglist)+1}", command=lambda btnid=3: update(rownum, btnid))],
	[Label(Frame3, text="Weather Conditions"),
	Button(Frame3, text=f"Update Weather {len(biglist)+1}", command=lambda btnid=4: update(rownum, btnid))],
	[Label(Frame3, text=""),
  	Button(Frame3, text="Delete Group", command=lambda: deletegroup(rownum))]
	]])
	for y in range(len(biglist[-1][1])):
		biglist[-1][1][y][0].grid(row=2*len(biglist)+1, column=y)
		biglist[-1][1][y][1].grid(row=2*len(biglist)+2, column=y)
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
	for x in range(len(biglist)):
		biglist[x][1][0][0].configure(text=f"Group {x+1}:")
		biglist[x][1][1][1].configure(text=f"Update Leader {x+1}")
		biglist[x][1][2][1].configure(text=f"Update Location {x+1}")
		biglist[x][1][3][1].configure(text=f"Update Campers {x+1}")
		biglist[x][1][4][1].configure(text=f"Update Weather {x+1}")
		for y in biglist[x][1]:
			y[0].grid(row=2*x+1)
			y[1].grid(row=2*x+2)
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


Frame1 = Frame(root)
Frame1.place(x=0, y=5)

Textbox = Label(Frame1, text='Input below and then press an "update" button')
Textbox.grid(row=0, column=0)

Entrybox = Entry(Frame1)
Entrybox.grid(row=1, column=0)

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
canvas = Canvas(Frame2, width=1200, height=600)
canvas.pack(fill=BOTH, side=LEFT, expand=TRUE)
# create scrollbar
scrollbar = Scrollbar(Frame2, orient=VERTICAL, command=whentoscroll)
scrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)


# configure canvas
canvas.config(yscrollcommand=scrollbar.set, highlightthickness=0)
# create another frame inside canvas
Frame3 = Frame(canvas)
canvas.create_window(0, 0, window=Frame3, anchor=NW, width=1200)
Frame3.bind("<Enter>", lambda event: bindToCanvas())
Frame3.bind("<Leave>", lambda event: unbindToCanvas())

# Text for Catagories
for i in range(len(categorylist)):
	Label(Frame3, text=categorylist[i], width=20, height=2, font=("Arial", 14, "bold"),anchor=W).grid(row=0, column=i)

identification=-1
for row in range(7):
	addgroup()

addgroupbtn = Button(root, text="Add Group", command=addgroup)
addgroupbtn.place(x=0, y=750)
root.bind("<z>", addgroup)

root.mainloop()