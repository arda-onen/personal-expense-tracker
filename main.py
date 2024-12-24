# AUTHOR : ARDA ÖNEN
# CENG 1009 SECTION 2

import datetime # using datetime to check if a date is valid or not
import turtle # using turtle to draw chart
from os import system, name # importing system to clear the terminal for better visual and name to understand which OS we are using


CATEGORIES:list[str] = []
#constant variables
BORDER:int = 10
WIDTH:int = 50

budgets:list[str] = [] # an array which set at the start of the program and could be changable
expenses:list[str] = [] # an array which set at the start of the program and gets saved at the end

splittedBudget:list[list[str]] = []
splittedExpenses:list[list[str]] = []

currentMoney:dict[str,float] = { } # A dictionary to store the sum of the money variable in each category
currentBudget:dict[str,int] = { } # A dictionary to store the budget of the person

# Please note that try is used to handle all the error parts in the program

# Used with to avoid any problems may occur at closing the file
# Example => there could be a problem at reading the file and in that situation the file may be forgotten open due to error. 
# Using with deals with that problem because it automatically closes the file upon COMPLETION or FAILURE.

def saveBudgets() -> None: # this function saves all budgets from dictionary to txt file
    try:
        temp =  []
        for category in CATEGORIES:
            temp.append(category + "\t" + str(currentBudget[category]) + "\n")
        with open("budget.txt","w") as file:
            file.writelines(temp)
    except:
        print("An error occured")
        pass

def setupDicts() -> None: # sets all of the dictionaries with given categories
    global currentBudget
    global currentMoney
    for category in CATEGORIES:
        currentBudget[category] = 0
        currentMoney[category] = 0.0

def getExpenses() -> list[str]: # returns the expenses array from expenses.txt
    tempExpenses:list[str] = []
    try:
        # We are opening the file using with to avoid any errors that could occur awhile closing the file process.    
        with open('expenses.txt',mode='r') as file: # Mode is selected as 'r' to read the file.
            tempExpenses = file.readlines() # getting the data from our expenses.txt file
            if(tempExpenses == []): #checking if the file is empty
                raise FileNotFoundError
            
            if("\n" not in tempExpenses[-1]): #checking if there is \n at the end of the string to avoid errors at future
                tempExpenses[-1] += "\n"
    except FileNotFoundError: #if there is no file named expenses.txt then its the first time the user enters to the application
        print("Could not able to find any expenses. Welcome to the Personal Expense tracker!")
    except Exception as e: # for any kind of error
        print("There was an error occured. Please contact support for further information. Error code is : " + str(e))
    return tempExpenses

def createBudgets() -> list[str]: #made this function to avoid writing the same code twice
    global CATEGORIES
    tempBudget:list[str] = []
    if(CATEGORIES == []):
        CATEGORIES = ["Food","Housing","Transportation","Education","Entertainment","Shopping","Other"]
    for category in CATEGORIES: #we are going to create the budget.txt file in this for loop
        while True:
            try: 
                amount: int = int(input("Please enter the amount of budget for the " + category + " category : ")) #getting amount
                tempBudget.append(category + "\t" + str(amount)+"\n")
                break
            except ValueError: #avoiding value errors
                print("\nPlease only enter an integer as a budget.\n")
                continue 
            except Exception as e: # for any kind of error
                print("There was an error occured. Please contact support for further information. Error code is : " + str(e))
                continue
    try:
        with open("budget.txt",mode="w") as file: #opening the file in write mode
            file.writelines(tempBudget) # saving the budget.txt file
            print("\nBudgets successfully added to the system.")
    except: #if there is an error occured
        print("There was an error occured when creating your budget.txt file. Please contact support for further information.")
        return createBudgets() #using recursive to retry the
    
    return tempBudget

def getBudgets() -> list[str]: # returns the budget array from budget.txt
    tempBudget:list[str] = []
    try:
        with open('budget.txt',mode='r') as file: #opening budget.txt file
            tempBudget = file.readlines() #reading file
            if(tempBudget == []): #if file is empty
                raise FileNotFoundError
    except FileNotFoundError:
        print("Could not able to find budgets. Lets create some budgets for all the categories.")
        tempBudget = createBudgets() #if there is no file then create one
    print("")
    return tempBudget

def checkWhitespaces(liste:list[str]) -> list[str]: # returns a string list that is stripped
    tempList:list[str] = []
    for item in liste:
        item = item.strip(" ")
        if(item == "\n"):
            continue
        tempList.append(item)
    return tempList

def splitVariables(liste:list[str]) -> list[list[str]]: #returns the splitted value of the list given
    temp:list[list[str]] = []
    for item in liste:
        temp.append(item.split("\t")) 
    return temp

def checkMaxBudget(category:str) -> int: # returns the budget of a specific category
    return currentBudget[category]

def addExpense(date:str,amount:float,category:str,description:str) -> None: # appends a new expense to expenses array
    #making currentMoney variable global because we are going to update its values to use it in other functions
    global currentMoney
    string:str = date + "\t" + "{price:.2f}" + "\t" + category + "\t" + description + "\n" # this is the string which will be appended to the expenses array
    expenses.append(string.format(price=amount)) #appending to the expenses array
    print("\nExpense successfully added to the system. \n")
    currentMoney[category] += amount #we are increasing currentmoneys related categorys key with the amount
    maxBudget = checkMaxBudget(category=category) # getting the budget for the category

    if(currentMoney[category] > maxBudget and maxBudget != 0): # checking if it is higher than the budget
        notifyUser(category=category,amount=float(currentMoney[category]-maxBudget)) #giving user an alert

def viewAllExpenses() -> None: #shows all the expenses as list
    if(expenses == []): #check if there is any expenses
        print("Could not able to find any expenses. Going back to the menu...\n")
        return
    print("All of the expenses are :")
    print("Date\tAmount\tCategory\tDescription")
    for text in expenses: #getting every expense in expenses
        text = text.replace("\n","") #getting rid of the \n at the end of each text
        print("- " + text)
    print("")
    
def viewExpenses() -> None: #shows all the expenses by category
    if(expenses == []): #checking if there is any expenses
        print("Could not able to find any expenses. Going back to the menu...\n")
        return
    for category in CATEGORIES: 
        isData:bool = False # this variable is used to know that if there is any data avaiable in the category
        print("****", category,"****\n")
        for expense in splittedExpenses:
            if(expense[2] == category):
                print("- " + "\t".join(expense).replace("\n",""))
                isData = True # setting true to let the program know that this category is not empty
        if(isData == False): #check if this category is empty or not
            print("Unable to find any data in this category...")
        print("")

def searchFilter( search:str ) -> None: # prints the search results according to the description and category
    isFound:bool = False # this variable is used to let the program uunderstand that is there are data or not
    print("Search results for '" + search + "' are : ")
    for expense in splittedExpenses:
        if(search.lower() in (expense[2].lower() + expense[3].lower())): # using lower to avoid any uppercase misunderstandings
            print("- " + "\t".join(expense).replace("\n",""))
            isFound = True # there is data!
    if(isFound == False): # check if there are any results
        print("Could not find any results...")
    print("")

def saveChanges() -> None: # save the expenses.txt file
    try:
        with open("expenses.txt",mode="w") as file: #opening expenses file to save the changes
            file.writelines(expenses) # writing expenses array to the file
            print("Expenses successfully saved to the system.")
    except:
        print("There was an error occured when saving your expenses. Please contact support.\n")

def exit() -> None: # call save function
    print("Saving the changes...")
    saveChanges()
    print("Exiting...")
        
def notifyUser( category:str , amount:float ) -> None: # prints a notification according to the variables given
    #format used for clean code
    print("You exceeded the limit in the {category} category with {price:.2f} dollars\n".format(category=category.upper(),price=amount))

def checkAlerts() -> None: # checks if there are any alerts to show
    isAlert:bool = False # to let the program know is there any alerts to show
    for category in CATEGORIES:
        maxBudget:int = checkMaxBudget(category=category) # getting the budget of this category
        money = currentMoney[category]
        if(money > maxBudget and maxBudget != 0): # check if it is higher than the budget
            notifyUser(category=category,amount=float(money - maxBudget)) # give an alert text
            isAlert=True # there is alert!
        if(money == maxBudget and maxBudget != 0):
            isAlert = True
            print("You are at the limit of",category,"category.\n")
    if(isAlert == False): #checking if there are any alerts
        print("No category was found for which you exceeded the limit.\n")

def calculateMoney() -> None: # calculates the current money according to the loaded expenses array AT START
    #Please_NOTE THAT this function can only be called at the start!!!!
    #making currentMoney global to change its value outside of the function too
    global currentMoney
    for expense in splittedExpenses:
        money:float = float(expense[1]) #getting the price variable from the text as float
        currentMoney[expense[2]] += money; #adding the value to the related categorys value/key

def writeTexts( t:turtle.Turtle , firstPos:tuple[float,float] , lastPos:tuple[float,float] , height:float , category:str , margin:float ) -> None: # writes money and category to the bar
    t.penup() # using penup to avoid drawing while changing the position
    t.goto(firstPos[0],firstPos[1]+BORDER) # using goto with a margin of BORDER at y axis
    t.write(str(height) + " / " + str(currentBudget[category])) # writing money value
    t.goto(lastPos[0] - WIDTH, lastPos[1] - margin) # using goto with a margin of WIDTH at x and margin at y axis
    t.write(category) # writing category
    t.goto(lastPos) # using goto to return to original position
    t.pendown() #letting turtle to draw again

def drawBar( t:turtle.Turtle , height:float , category:str , margin:float ) -> None: # draws the bar for the given category
    t.begin_fill() #begin to fill
    t.left(90)
    t.forward(height) 
    firstPos:tuple[float,float] = t.pos() # getting the position to write the value on top of the bar
    t.right(90)
    t.forward(WIDTH)
    t.right(90)
    t.forward(height)
    t.left(90)
    t.end_fill() # end fill
    lastPos:tuple[float,float] = t.pos() # getting the position to return to the original position after writing
    t.backward(WIDTH)
    writeTexts(t=t,firstPos=firstPos,lastPos=lastPos,height=height,category=category,margin=margin) #write money and category
    t.forward(BORDER) # giving some space for better visual

def drawBarChart() -> None: # prepares screen and creates turtle object to draw a bar chart
    if(expenses == []): # check if there are any expenses
        print("There are no data to create bar chart...\n")
        return
    wn = turtle.Screen() #creating the screen
    wn.bgcolor("black")
    maxHeight:float = max(currentMoney.values()) # getting the max value of the money for the height of the screen
    wn.setworldcoordinates(0-BORDER,0-maxHeight/20,(WIDTH + BORDER)*len(CATEGORIES) + BORDER ,maxHeight+maxHeight/20 + BORDER) # setting coordinates
    
    t = turtle.Turtle() #creating the turtle
    t.pencolor("white")
    t.pensize(3) #setting the pensize for more visibility
    t.speed(0) # increasing the speed for faster debugging
    t.fillcolor("red") # changing fillcolor to get better visual
    for category in CATEGORIES:
        drawBar(t,currentMoney[category],category,maxHeight/20) # draw bar for each category

    wn.exitonclick() # used this to avoid the instant closure after drawing everything
    try:
        turtle.bye() # we are using bye function to ensure the turtle window is close so that if this function is called again there wont be any errors occured by turtle
    except:
        pass

def updateBudget()-> list[str]: # updates the budget to the users value
    tempBudget:list[str] = createBudgets() #recreating budget.txt
    print("")
    return tempBudget

def waitForInput(isFirstTime:bool) -> None: # makes the program more responsive to user by clearing the terminal after every request
    print("Press enter to continue...")
    if(isFirstTime == False):
        input() # waiting for enter
    if(name == 'nt'): # if it is windows
        system("cls") # execute code in terminal
    else:
        system("clear") # for linux/mac

def setBudgetDict() -> None: # changes the values of the Budget dict
    global currentBudget
    for budget in splittedBudget:
        currentBudget[budget[0]] = int(budget[1])

def getCategories() -> None: # this function gets all of the categories that user created at the start of the program
    global CATEGORIES
    CATEGORIES = []
    for budget in splittedBudget:
        CATEGORIES.append(budget[0])

def addCategory() -> None: # this function adds category to CATEGORIES, currentBudget and currentMoney
    #making variables global to change theirs value globally
    global CATEGORIES
    global currentBudget
    global currentMoney
    while True:
        try:
            categoryName = input("Please enter the name of the category you want to add (Enter '!abort' to abort) : ")
            if(categoryName == "!abort"):
                break
            categoryName = categoryName.capitalize()
            if(categoryName == ""):
                print("\nPlease enter a string...\n")
                continue
            if(categoryName in CATEGORIES):
                print("\nPlease enter a non-existing category\n")
                continue
            categoryBudget = int(input("Please enter the budget of " + categoryName + " (Enter '-1' to abort) : "))
            if(categoryBudget == -1):
                break
            if(categoryBudget < 0):
                print("\nPlease enter a positive number\n")
                continue

            if(categoryName in CATEGORIES):
                raise Exception
            CATEGORIES.append(categoryName)
            currentBudget[categoryName] = categoryBudget
            currentMoney[categoryName] = 0.0

            saveBudgets()
            print("Category added successfully...")
            break
        except:
            print("Please try again...")
            continue

def viewBudgets() -> None: # prints the currentMoney and currentBudget for all categories
    print("Your Sum Is :")
    for category in CATEGORIES:
        print(category + "\t" + str(currentMoney[category]) + "/" + str(currentBudget[category]))
    print("")

def deleteCategory() -> None: # this function deletes the category from CATEGORIES, currentBudget and currentMoney. it also deletes the expenses of the category
    global CATEGORIES
    global expenses
    global splittedExpenses
    global currentBudget
    global currentMoney
    if(len(CATEGORIES) < 2):
        print("You are not allowed to delete all categories. Please create a new one first to delete!!!")
        return
    while True:
            
            print("All categories are : \n")    
            for category in CATEGORIES:
                print(category)
            print("\nPlease note that deleting a category will also remove all expenses in that category!!!")
            categoryName = input("Please enter the name of the category that you want to delete (Enter '!abort' to abort) : ")
            if(categoryName == "!abort"):
                break
            categoryName = categoryName.capitalize()
            if(categoryName not in CATEGORIES):
                raise ValueError
            
            deletes = []

            for i in range(0,len(splittedExpenses)):
                if(splittedExpenses[i][2] == categoryName):
                    deletes.append(expenses[i])
            
            for delete in deletes:
                expenses.remove(delete)

            del currentMoney[categoryName]
            del currentBudget[categoryName]
            CATEGORIES.remove(categoryName)

            saveBudgets()
            print("Successfully deleted the category from the system. All of the expenses in this category is deleted as well.")
            break

def deleteExpense() -> None: # this function deletes the selected expense and substracts the amount from currentMoney.
    global currentMoney
    global expenses
    global splittedExpenses
    while True:
        try:
            print("All of your expenses are numbered : ")
            for i in range(len(expenses)):
                print(str(i+1) + " - " + expenses[i],end="")
            number = int(input("Please enter the number of the expense that you want to delete (Enter '0' to abort) : "))
            if(number == 0):
                break
            currentMoney[splittedExpenses[number-1][2]] -= float(splittedExpenses[number-1][1])
            del expenses[number-1]
            print("Successfully deleted the expense...")
            break
        except:
            print("\nPlease try again...\n")
            continue

def mainCycle(): # MAIN PROGRAM CYCLE
    #making expenses and budgets global to change their values globally
    global expenses
    global budgets
    #making splitted lists global too to change their values globally
    global splittedBudget
    global splittedExpenses
    while True:
        try:
            expenses = getExpenses() #getting the expenses from expenses.txt
            budgets = getBudgets() # getting the budgets from budget.txt
            expenses = checkWhitespaces(expenses)
            budgets = checkWhitespaces(budgets)
            waitForInput(True) # giving it true to avoid input
            splittedExpenses = splitVariables(expenses)
            splittedBudget = splitVariables(budgets)
            getCategories()
            setupDicts()
            setBudgetDict() # sets the values to the dictionary
            calculateMoney() # calculating the money for each category
            break # if all things are ok, program will continue to the other while loop
        except Exception as e:
            print("\nThere was an error occured. Error is :",e,"\n")
            waitForInput(False)
    while True: # using while to make the program a cycle
        try:
            print()
            print("ARDA ONEN's PERSONAL EXPENSE TRACKER SYSTEM".center(200,"*"))
            value:int = int(input("\nPlease Select an option\n\n1:View Expenses\n2:Search Expenses\n3:Add Expense\n4:Create Bar Chart of Expenses\n5:Update Budget\n6:Check for Alerts\n7:Save Expenses\n8:Add Category\n9:View Sum of Expenses For All Categories\n10:Delete Expense\n11:Delete Category\n12:Exit\n\nYour choice : "))
            print("")
            if(value==1):
                while True:
                    which:str = str(input("If you want to view the expenses grouped by category then please enter 'category'. If not then please enter 'all'. (Enter '!abort' to abort) : "))
                    if(which == "!abort"):
                        break
                    if(which.lower() != "category" and which.lower() != "all"):
                        print("\nYou entered a wrong string please try again.\n")
                        continue
                    print("")
                    if(which.lower() == "all"):
                        viewAllExpenses()
                    elif(which.lower() == "category"):
                        viewExpenses()
                    break
            elif(value==2):
                filter:str = str(input("Please enter the search filter : ")) #getting the filter
                print("")
                searchFilter(filter) #search using the filter
            elif(value==3):
                abort:bool = False 
                category:str = ""
                while True and not abort:
                    try:
                        for category in CATEGORIES:
                            print(" - " + category)
                        category:str = str(input("Please enter the category of your expense (Enter '!abort' to abort) : ")) # getting the category
                        if(category == "!abort"):
                            abort = True
                            break
                        if(category.capitalize() not in CATEGORIES): # checking if it is valid
                            print("Please create the category first to add an expense.")
                            continue
                        break
                    except ValueError:
                        print("\nPlease enter a valid category...\n")
                        continue
                amount:float = 0
                while True and not abort:
                    try:
                        amount:float = float(input("Please enter the amount of your expense (Enter '-1' to abort) : ")) #getting price
                        if(amount == -1):
                            abort = True
                            break
                        if(amount<0): #check if it is positive
                            raise ValueError
                        break
                    except ValueError:
                        print("\nPlease enter a valid amount...\n")
                        continue
                description:str = ""
                while True and not abort:
                    try:
                        description:str = str(input("Please enter the description of your expense (Enter '!abort' to abort) : ")) # getting a description
                        if(description == "!abort"):
                            abort = True
                            break
                        if(description == ""): # checking if it is empty to avoid any errors at split() function
                            raise ValueError
                        break
                    except ValueError:
                        print("\nPlease enter a valid description\n")
                        continue
                transaction_date:datetime.date = None
                while True and not abort:
                    try:
                        date:str = str(input("Please enter the date of your expense ('YYYY-MM-DD') (Enter '!abort' to abort) : ")) # getting the date
                        if(date == "!abort"):
                            abort = True
                            break
                        transaction_date:datetime = None  # setting the date variable
                        transaction_date = datetime.datetime.strptime(date, "%Y-%m-%d")
                        break
                    except ValueError:
                        print("Please enter a valid date\n")
                        continue
                if(abort):
                    waitForInput(False)
                    continue
                addExpense(category=category.capitalize(),date=str(transaction_date.date()),amount=amount,description=description) #adds expense
                splittedExpenses = splitVariables(expenses)
            elif(value==4):
                drawBarChart() # prepare to draw a chart
            elif(value==5):
                budgets = updateBudget() # overwriting or creating a budget.txt file
                splittedBudget = splitVariables(budgets) # splitting the budget again to avoid confusion
                setBudgetDict() # setting the budget dictionary again
            elif(value==6):
                checkAlerts() # check if there are some alerts because of the budget
            elif(value==7):
                saveChanges()
            elif(value==8):
                addCategory()
            elif(value==9):
                viewBudgets()
            elif(value==10):
                deleteExpense()
                splittedExpenses = splitVariables(expenses) # splitting again
            elif(value==11):
                deleteCategory()
                splittedExpenses = splitVariables(expenses) # splitting again
            elif(value==12):
                break # to exit to program
            else:
                print("Please enter one of the given options...\n")
        except ValueError: # covering all value errors
            print("\nPlease enter a valid value\n")
        except Exception as e:
            print("There was an error occured. Please contact support for further help. Exception : ",e)
        waitForInput(False)
    exit() # save and quit

if __name__ == "__main__":
    mainCycle()