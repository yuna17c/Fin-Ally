from tkinter import *
import sqlite3
from expenses import Expenses

categoryList=[
    "Personal",
    "Food",
    "Transportation",
    "Housing",
    "Utilities",
    "Clothing",
    "Insurance",
    "Medical",
    "Entertainment",
    "Other"]

conn = sqlite3.connect(':memory:')       
c = conn.cursor()

#creates the financial_info table 
c.execute("""CREATE TABLE financial_info2 (
            name TEXT,
            price DECIMAL,
            category TEXT
            )""")

def insert_item (item):     
    with conn:
        c.execute("INSERT INTO financial_info2 VALUES (:name,:price,:category)", 
                {'name':item.name, 'price':item.price, 'category':item.category})

root = Tk()
root.title('Fin-Ally')
root.geometry("1100x650")
root.iconbitmap('money.ico')

myLabel = Label(root,text="Enter your expenses.",font=("Calibri 18"))
myLabel.grid(row=0, column=1)

#name
labelName = Label(root, text="What is your expense?",font=("Calibri 13"),anchor="w", width=33)
labelName.grid(row=1, column=1,padx=15,pady=2)
eName=Entry(root,width=42, bg="#ffe6a1",fg="black",font=("Calibri 11"), borderwidth=2)
eName.grid(row=2,column=1)

#price
labelPrice = Label(root, text="How much did you spend on this expense?",font=("Calibri 13"),anchor="w",width=33)
labelPrice.grid(row=3, column=1,padx=15,pady=2)
ePrice=Entry(root,width=42, bg="#ffe6a1",fg="black",font=("Calibri 11"), borderwidth=2)
ePrice.grid(row=4,column=1)
ePrice.insert(0,"$")

#category
labelCat = Label(root, text="Choose the expense category.",font=("Calibri 13"),anchor="w", width=33)
labelCat.grid(row=5, column=1,padx=15,pady=2)

def add_cat():
    global categoryList
    newCat=eNewCat.get()
    categoryList.append(newCat.capitalize())

labelAddCat = Label(root, text="Add an expense category.",font=("Calibri 13"),anchor="w", width=20)
labelAddCat.grid(row=5,column=2,columnspan=2)

eNewCat=Entry(root,width=20, bg="white",fg="black",font=("Calibri 11"), borderwidth=2)
eNewCat.grid(row=6,column=2)

plusButton=Button(root, text="+", padx=5, font=("Calibri 9"),command=add_cat, fg="black", bg="white")
plusButton.grid(row=6,column=3)

clicked=StringVar()
clicked.set(categoryList[0])
drop = OptionMenu(root, clicked, *categoryList)
drop.config(width=37, bg="#ffe6a1",fg="black",font=("Calibri 11"), anchor="w", borderwidth=2)
drop.grid(row=6,column=1)

def myClick():
    inputName = eName.get()
    inputPrice = ePrice.get()
    inputCat = clicked.get()
    itemLabel = Expenses(inputName,inputPrice,inputCat)
    print(itemLabel)
    insert_item (itemLabel)
    eName.delete(0,END)
    ePrice.delete(0,END)
    c.execute("SELECT * FROM financial_info2")
    print(c.fetchall())
    # inputName.grid(row=1,column=2)
    # inputPrice.grid(row=2,column=2)
    # inputCat.grid(row=3, column=2)
    
#submit button
labelRow = Label(root, text=" ",pady=6).grid(row=7,column=1)
submitButton=Button(root, text="Submit", padx=11,pady=5, font=("Calibri 11"),command=myClick, fg="black", bg="white")
submitButton.grid(row=8,column=1)


labelEmpty = Label(root, text="    ",font=("Calibri 18"),padx=6).grid(row=0,column=4)

#expenses summary (by category)
labelTop = Label(root, text="Expenses Summary",font=("Calibri 18"),padx=10,anchor="w", width=40)
labelTop.grid(row=0,column=5,columnspan=4,pady=10)

for i in range(0,round(len(categoryList)/2)):
    categoryLabel = Label(root, text=categoryList[i], font=("Calibri 13"),padx=6,anchor="w", width=14).grid(row=i+1,column=5)
    pricePerCatLabel = Label(root, text="$", font=("Calibri 13"),anchor="w", width=9).grid(row=i+1,column=6)

for i in range(round(len(categoryList)/2),len(categoryList)):
    categoryLabel = Label(root, text=categoryList[i], font=("Calibri 13"),padx=6,anchor="w", width=14).grid(row=i+1-round(len(categoryList)/2),column=7)
    pricePerCatLabel = Label(root, text="$", font=("Calibri 13"),anchor="w", width=9).grid(row=i+1-round(len(categoryList)/2),column=8)


root.mainloop()

conn.close()