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
itemsList = []

categoryPriceList=[]
def get_total_price (category):
    c.execute("SELECT price FROM financial_info2 WHERE category=:category", {'category':category})
    return c.fetchall()

def myClick():
    inputName = eName.get()
    inputPrice = ePrice.get()[1:]
    inputCat = clicked.get()
    itemLabel = Expenses(inputName,inputPrice,inputCat)
    insert_item (itemLabel)

    itemListLabel=inputName+", $"+inputPrice+", "+inputCat
    itemsList.append(itemListLabel)
    for i in range (0,len(itemsList)):
        listLabel = Label(root, text=itemsList[i],anchor="w",width=33,font=("Calibri 11")).grid(row=11+i,column=1)
    
    eName.delete(0,END)
    ePrice.delete(0,END)
    ePrice.insert(0,"$")

    # inputName.grid(row=1,column=2)
    # inputPrice.grid(row=2,column=2)
    # inputCat.grid(row=3, column=2)

def doneClick():
    print(itemsList)
    c.execute("SELECT * FROM financial_info2")
    print(c.fetchall())

    for i in range (0,len(categoryList)):
        categorySum = 0
        for j in range (0,len(get_total_price(categoryList[i]))):
            categorySum+=get_total_price(categoryList[i])[j][0]
        categoryPriceList.append(categoryList[i]+": $"+str(round(categorySum,2)))
    print(categoryPriceList)
    for i in range(0,round(len(categoryPriceList)/2)):
        dollarIndex = categoryPriceList[i].index("$")
        catPriceLabel = Label(root, text=categoryPriceList[i][dollarIndex:], font=("Calibri 13"),anchor="w", width=9)
        catPriceLabel.grid(row=i+1,column=6)

    for i in range(round(len(categoryPriceList)/2),len(categoryPriceList)):
        dollarIndex = categoryPriceList[i].index("$")
        catPriceLabel = Label(root, text=categoryPriceList[i][dollarIndex:], font=("Calibri 13"),anchor="w", width=9)
        catPriceLabel.grid(row=i+1-round(len(categoryPriceList)/2),column=8)


    #for j in range (0, len(categoryPriceList)):

#submit button
labelRow = Label(root, text=" ",pady=6).grid(row=7,column=1)
submitButton=Button(root, text="Submit", padx=11,pady=3, font=("Calibri 11"),command=myClick, fg="black", bg="white")
submitButton.grid(row=8,column=1)
labelRow = Label(root, text=" ",pady=6).grid(row=9,column=1)

#empty rows
for i in range (0, len(itemsList)+1):
    emptyRow = Label(root, text=" ",pady=6).grid(row=17+i,column=1)

#done button
doneButton=Button(root, text="Done", padx=11,pady=3, font=("Calibri 11"),command=doneClick, fg="black", bg="white")
doneButton.grid(row=17+len(itemsList)+1,column=1)

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