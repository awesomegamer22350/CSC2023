import time
from tkinter import *
from tkinter import ttk
from sys import platform

# mkFrame(framelist, positionlist)
def mkFrame(l, p, g):
	l.append([])
	i = next(i for i, e in enumerate(sorted(p) + [ None ], 0) if i != e)
	p.append(i)

	l[-1].append(ttk.Frame(groupframe, padding="3 3 3 3", borderwidth=2,
							  relief="solid", style="red.TFrame"))
	l[-1][0].grid(column=0, row = len(l)-1, sticky=EW, padx=3, pady=3)
	l[-1][0].bind("<Button-1>", lambda event: toggleGroupInfo(i, l, p))
	l[-1][0].columnconfigure(0, weight=1)
	l[-1][0].columnconfigure(1, weight=1)
	l[-1][0].columnconfigure(2, weight=1)

	l[-1].append(ttk.Label(l[-1][0], text=len(l)-1))
	l[-1][1].grid(column=0, row=0, sticky=W)
	l[-1][1].bind("<Button-1>", lambda event: toggleGroupInfo(i, l, p))

	l[-1].append(ttk.Label(l[-1][0], text=time.asctime()))
	l[-1][2].grid(column=1, row=0, sticky=W)
	l[-1][2].bind("<Button-1>", lambda event: toggleGroupInfo(i, l, p))

	l[-1].append(ttk.Button(l[-1][0], text="close",
							   command=lambda: rmFrame(i, l, p, g)))
	l[-1][3].grid(column=2, row=0, padx=3, pady=3, sticky=E)


	l[-1].append(False)
	#l[n][4] group info visibility status
	
	l[-1].append(ttk.Label(l[-1][0], textvariable=g[-2][0]))
	l[-1][5].grid(column=1, row=1, sticky=W)
	l[-1][5].bind("<Button-1>", lambda event: toggleGroupInfo(i, l, p))
	l[-1][5].grid_remove()
	
	l[-1].append(ttk.Label(l[-1][0], textvariable=g[-2][1]))
	l[-1][6].grid(column=1, row=2, sticky=W)
	l[-1][6].bind("<Button-1>", lambda event: toggleGroupInfo(i, l, p))
	l[-1][6].grid_remove()
	
	l[-1].append(ttk.Label(l[-1][0], textvariable=g[-2][2]))
	l[-1][7].grid(column=1, row=3, sticky=W)
	l[-1][7].bind("<Button-1>", lambda event: toggleGroupInfo(i, l, p))
	l[-1][7].grid_remove()

# rmFrame(id, framelist, positionlist)
def rmFrame(i, l, p, g):
	j = p.index(i)
	l[j][0].destroy()
	del l[j]
	del p[j]
	del g[j]
	if j < len(p):
		for i in range(j, len(l)):
			l[i][0].grid(row = i)
			l[i][1]["text"] = str(i)

def toggleGroupInfo(i, l, p):
	j = p.index(i)
	if l[j][4]:
		l[j][5].grid_remove()
		l[j][6].grid_remove()
		l[j][7].grid_remove()
		l[j][4] = False
	else:
		l[j][5].grid()
		l[j][6].grid()
		l[j][7].grid()
		l[j][4] = True

def updateCanvas(groupframeID):
	groupcanvas["scrollregion"] = groupcanvas.bbox("all")
	groupcanvas.itemconfigure(groupframeID, width=groupcanvas.winfo_width()-3)

def scrollCanvas(*args):
	if groupcanvas.yview() == (0.0, 1.0):
		return
	groupcanvas.yview(*args)

def mousewheelCanvas(event, scroll=None):
	if groupcanvas.yview() == (0.0, 1.0):
		return
	if platform == "linux" or platform == "linux2":
		groupcanvas.yview_scroll(int(scroll), "units")
	if platform == "Windows":
		groupcanvas.yview_scroll(int(-1*(event.delta/120)), "units")
	else:
		groupcanvas.yview_scroll(-1*event.delta, "units")

def bindToCanvas(*args):
	if platform == "linux" or platform == "linux2":
		root.bind_all("<Button-4>", lambda event: mousewheelCanvas(event, -1))
		root.bind_all("<Button-5>", lambda event: mousewheelCanvas(event, 1))
	else:
		root.bind_all("<MouseWheel>", lambda event: mousewheelCanvas(event))
	
def unbindToCanvas(*args):
	if platform == "linux" or platform == "linux2":
		root.unbind_all("<Button-4>")
		root.unbind_all("<Button-5>")
	else:
		root.unbind_all("<MouseWheel>")

def addGroupSubmit():
	groupInfo.append([])
	groupInfo[-1].append(StringVar())
	groupInfo[-1].append(StringVar())
	groupInfo[-1].append(StringVar())
	groupName["textvariable"] = groupInfo[-1][0]
	groupLeader["textvariable"] = groupInfo[-1][1]
	groupLocation["textvariable"] = groupInfo[-1][2]
	mkFrame(groups, groupPosition, groupInfo)
	groupcanvas.grid()
	scrollbar.grid()
	addgroupframe.grid_remove()
	add.bind("<Button-1>", lambda event: addGroup())
	root.bind("<Return>", lambda event: addGroup())

def addGroup():
	groupcanvas.grid_remove()
	scrollbar.grid_remove()
	addgroupframe.grid()
	#groupInfo[-1][0].set(len(groups))
	add.bind("<Button-1>", lambda event: addGroupSubmit())
	root.bind("<Return>", lambda event: addGroupSubmit())

root = Tk()
root.geometry('700x700')
root.resizable(False,False)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

groups = []
groupPosition = []
# group name, leader name, location,
# number of campers, weather, latest time validated
groupInfo = []
groupInfo.append([])
groupInfo[-1].append(StringVar())
groupInfo[-1].append(StringVar())
groupInfo[-1].append(StringVar())

s = ttk.Style()
s.configure("red.TFrame", background="red")

mainframe = ttk.Frame(root, padding="3 3 3 3", borderwidth=2, relief="solid")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

groupcanvas = Canvas(mainframe, highlightthickness=0)
groupcanvas.grid(column=0, row=0, sticky=(N, W, E, S), padx=3, pady=3)
groupcanvas.columnconfigure(0, weight=1)
groupcanvas.rowconfigure(0, weight=0)

groupframe = ttk.Frame(groupcanvas)
groupframe.columnconfigure(0, weight=1)
groupframe.rowconfigure(0, weight=0)
groupframeID = groupcanvas.create_window((0, 0), window=groupframe, anchor=NW)

scrollbar = ttk.Scrollbar(mainframe, orient='vertical',
						  command=scrollCanvas)
scrollbar.grid(row=0, column=1, sticky=NS)
groupcanvas['yscrollcommand'] = scrollbar.set
groupcanvas.bind("<Configure>", lambda event: updateCanvas(groupframeID))
groupframe.bind("<Configure>", lambda event: updateCanvas(groupframeID))
groupcanvas.bind("<Enter>", lambda event: bindToCanvas())
groupcanvas.bind("<Leave>", lambda event: unbindToCanvas())

addgroupframe = ttk.Frame(mainframe)
addgroupframe.grid(column=0, row=0, padx=3, pady=3)
addgroupframe.columnconfigure(0, weight=1)
addgroupframe.columnconfigure(1, weight=1)
addgroupframe.rowconfigure(0, weight=0)
addgroupframe.grid_remove()

ttk.Label(addgroupframe, text="Group name:").grid(row=0, column=0, sticky=E, padx=3, pady=3)
groupName = ttk.Entry(addgroupframe, textvariable=groupInfo[-1][0])
groupName.grid(row=0, column=1, sticky=W)
ttk.Label(addgroupframe, text="Leader name:").grid(row=1, column=0, sticky=E, padx=3, pady=3)
groupLeader = ttk.Entry(addgroupframe, textvariable=groupInfo[-1][1])
groupLeader.grid(row=1, column=1, sticky=W)
ttk.Label(addgroupframe, text="Location:").grid(row=2, column=0, sticky=E, padx=3, pady=3)
groupLocation = ttk.Entry(addgroupframe, textvariable=groupInfo[-1][2])
groupLocation.grid(row=2, column=1, sticky=W)

add = ttk.Label(mainframe, text="add", borderwidth=2, padding="10 10 10 10",
				relief="solid", anchor="center")
add.grid(row=1, column=0, sticky=EW, columnspan=2, pady=3)
add.bind("<Button-1>", lambda event: addGroup())
root.bind("<Return>", lambda event: addGroup())

#testing

root.mainloop()