from tkinter import *

root = Tk()
root.title("Sunshine Camp Tracker")
root.geometry("1400x800")
list1 = ('Customer Name','Receipt', 'Item Hired', 'Number Hired')
Label(root).grid(row=0)
for x,y in enumerate(list1):
    print(y)
    Label(root, text= y).grid(column=x*2,row=1)
    Entry(root).grid(column=x*2+1,row=1)
Button(root,text= "Log Receipt").grid(column=9,row=1)
root.mainloop()