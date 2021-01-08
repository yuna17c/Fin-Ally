import sqlite3
from expenses import Expenses

conn = sqlite3.connect('finances.db')       
c = conn.cursor()

#creates the financial_info table 
c.execute("""CREATE TABLE financial_info (
            name TEXT,
            price DECIMAL,
            category TEXT
            )""")

#inserting a value to the table
def insert_item (item):     
    with conn:
        c.execute("INSERT INTO financial_info VALUES (:name,:price,:category)", 
                {'name':item.name, 'price':item.price, 'category':item.category})

#adding an expense category 
def add_expense (category):
    categoryList.append(category)

#gets the expenses input from the user
x=0
categoryList=["Personal","Food","Transportation","Housing","Utilities","Clothing","Insurance","Medical","Entertainment","Other"]
while True:        
    print("ITEM #%i" %(x+1))
    itemName = input("What is your expense?\n")
    
    while True:     #checks if the price is a numeric value.
        try:
            itemPrice = float(input("How much did you spend on this expense?\n$"))
            break
        except:
            print("Please enter a numeric value.")
    
    categoryString=""
    for i in range(0,len(categoryList)):
        categoryString+=str(categoryList[i])+", "

    while True:
        itemCategory = input("What is the category of your expense?\nCategories: " + categoryString[:-2]+"\n")
        if categoryList.count(itemCategory.capitalize()) == 0:
            print("Please enter a valid category.")
        else:
            break

    #adds the inputted item to the table
    itemLabel = Expenses(itemName.capitalize(),itemPrice,itemCategory.capitalize())
    insert_item (itemLabel)     
    
    #asks if the user wants to continue recording item
    cont = input("Would you like to record another item? (y/n) ").lower()
    if cont == "y" or cont=="n" or cont == "yes" or cont=="no":
        if cont=="y" or cont=="yes":
            x+=1
        else:
            break
    else:
        print("Please input \"y\" for yes and \"n\" for no" )
        cont = input("Would you like to record another item? (y/n) ")

#gets the total expense for each category
categoryPriceList =[]
def get_total_price (category):
    c.execute("SELECT price FROM financial_info WHERE category=:category", {'category':category})
    return c.fetchall()

for i in range (0,len(categoryList)):
    categorySum = 0
    for j in range (0,len(get_total_price(categoryList[i]))):
        categorySum+=get_total_price(categoryList[i])[j][0]
    categoryPriceList.append(categoryList[i]+": $"+str(round(categorySum,2)))

print(categoryPriceList)

# #find the most spent category
# options = input("Please enter the categories that you would like to compare.\n")
# optionList=options.split(", ")

# for i in range(0, len(optionList)):
#     if categoryList.count(optionList[i]) == 0:
#         print("Please enter valid categories.")
#     else:

conn.close()