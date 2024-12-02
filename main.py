# AUTHOR : ARDA ÖNEN
# CENG 1009 SECTION 2

from datetime import date # using datetime to get today's date
import turtle # using turtle to draw chart
from os import system, name # importing os to clear the terminal for better visual

#constant values
CATEGORIES:list[str]=["Food","Housing","Transportation","Education","Entertainment","Shopping","Other"]
BORDER:int=10
WIDTH:int=50

budgets:list[str]=[] # an array which set at the start of the program and could be changable
expenses:list[str]=[] # an array which set at the start of the program and gets saved at the end

currentMoney:dict[str,float] = { # A dictionary to store the sum of the money variable in each category

    "Food" : 0.0,
    "Housing": 0.0,
    "Transportation": 0.0,
    "Education": 0.0,
    "Entertainment":0.0,
    "Shopping":0.0,
    "Other":0.0
}

# Please note that try is used to handle all the error parts in the program

# Used with to avoid any problems may occur at closing the file
# Example => there could be a problem at reading the file and in that situation the file may be forgotten open due to error. 
# Using with deals with that problem because it automatically closes the file upon COMPLETION or FAILURE.

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
        raise e
    return tempExpenses

def createBudgets() -> list[str]: #made this function to avoid writing the same code twice
    tempBudget:list[str] = []
    for category in CATEGORIES: #we are going to create the budget.txt file in this for loop
        try: 
            amount: int = int(input("Please enter the amount of budget for the " + category + " category : ")) #getting amount
            tempBudget.append(category + "\t" + str(amount)+"\n")
        except ValueError: #avoiding value errors
            print("\nPlease only enter an integer as a budget.\n")
            return createBudgets() #using recursive to start all over again
        except Exception as e: # for any kind of error
            print("There was an error occured. Please contact support for further information. Error code is : " + str(e))
            raise e
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

def checkMaxBudget(category:str) -> int: # returns the budget of a specific category
    maxBudget:int = 0
    for budget in budgets:
        splittedText:list[str] = budget.split("\t") #splitting the string to parts which 0 is category and 1 is budget
        if(splittedText[0] == category):
            maxBudget = int(splittedText[1].replace("\n","")) #used replace to avoid any problems when converting into int
    return maxBudget

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
        for expense in expenses:
            if(expense.split("\t")[2] == category): #used split to get all 4 variables of the text
                print("- " + expense.replace("\n","")) 
                isData = True # setting true to let the program know that this category is not empty
        if(isData == False): #check if this category is empty or not
            print("Unable to find any data in this category...")
        print("")

def searchFilter( search:str ) -> None: # prints the search results according to the description and category
    isFound:bool = False # this variable is used to let the program uunderstand that is there are data or not
    print("Search results for '" + search + "' are : ")
    for expense in expenses:
        expenseDetails:list[str] = expense.split("\t")
        if(search.lower() in (expenseDetails[2].lower() + expenseDetails[3].lower())): # using lower to avoid any uppercase misunderstandings
            print("- " + expense.replace("\n",""))
            isFound = True # there is data!
    if(isFound == False): # check if there are any results
        print("Could not find any results...")
    print("")

def exit() -> None: # saves expenses.txt with the data expenses array
    print("Saving the changes...")
    try:
        with open("expenses.txt",mode="w") as file: #opening expenses file to save the changes
            file.writelines(expenses) # writing expenses array to the file
            print("Expenses successfully saved to the system.")
    except:
        print("There was an error occured when saving your expenses. Please contact support.\n")
        
def notifyUser( category:str , amount:float ) -> None: # prints a notification according to the variables given
    #format used for clean code
    print("You exceeded the limit in the {category} category with {price:.2f} dollars\n".format(category=category.upper(),price=amount))

def checkAlerts() -> None: # checks if there are any alerts to show
    isAlert:bool = False # to let the program know is there any alerts to show
    for category in CATEGORIES:
        maxBudget:int = checkMaxBudget(category=category) # getting the budget of this category
        if(currentMoney[category] > maxBudget and maxBudget != 0): # check if it is higher than the budget
            notifyUser(category=category,amount=float(currentMoney[category] - maxBudget)) # give an alert text
            isAlert=True # there is alert!
    if(isAlert == False): #checking if there are any alerts
        print("No category was found for which you exceeded the limit.\n")

def calculateMoney() -> None: # calculates the current money according to the loaded expenses array AT START
    #Please_NOTE THAT this function can only be called at the start!!!!
    #making currentMoney global to change its value outside of the function too
    global currentMoney
    for expense in expenses:
        splittedText:list[str] = expense.split("\t")
        money:float = float(splittedText[1]) #getting the price variable from the text as float
        currentMoney[splittedText[2]] += money; #adding the value to the related categorys value/key

def writeTexts( t , firstPos:tuple[float,float] , lastPos:tuple[float,float] , height:float , category:str , margin:float ) -> None: # writes money and category to the bar
    t.penup() # using penup to avoid drawing while changing the position
    t.goto(firstPos[0],firstPos[1]+BORDER) # using goto with a margin of BORDER at y axis
    t.write(height) # writing money value
    t.goto(lastPos[0] - WIDTH, lastPos[1] - margin) # using goto with a margin of WIDTH at x and margin at y axis
    t.write(category) # writing category
    t.goto(lastPos) # using goto to return to original position
    t.pendown() #letting turtle to draw again

def drawBar( t , height:float , category:str , margin:float ) -> None: # draws the bar for the given category
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

def waitForInput(bool:bool) -> None: # makes the program more responsive to user by clearing the terminal after every request
    print("Press enter to continue...")
    if(bool == False):
        input() # waiting for enter
    if(name == 'nt'): # if it is windows
        system("cls") # execute code in terminal
    else:
        system("clear")

def mainCycle(): # MAIN PROGRAM CYCLE
    #making expenses and budgets global to change their values globally
    global expenses
    global budgets
    expenses = getExpenses() #getting the expenses from expenses.txt
    calculateMoney() # calculating the money for each category
    budgets = getBudgets() # getting the budgets from budget.txt
    waitForInput(True) # giving it true to avoid input
    while True: # using while to make the program a cycle
        try:
            print()
            print("ARDA ONEN's PERSONAL EXPENSE TRACKER SYSTEM".center(200,"*"))
            value:int = int(input("\nPlease Select an option    1:View Expenses   2:Search Expenses   3:Add Expense   4:Create Bar Chart of Expenses   5:Update Budget   6:Check for Alerts   7:Exit\nYour choice : "))
            print("")
            if(value==1):
                which:str = str(input("If you want to view the expenses grouped by category then please enter 'category'. If not then please enter 'all' : "))
                if(which.lower() != "category" and which.lower() != "all"):
                    print("\nYou entered a wrong string please try again.\n") #avoiding any errors
                    waitForInput(False)
                    continue
                print("")
                if(which.lower() == "all"):
                    viewAllExpenses()
                elif(which.lower() == "category"):
                    viewExpenses()
            elif(value==2):
                filter:str = str(input("Please enter the search filter : ")) #getting the filter
                print("")
                searchFilter(filter) #search using the filter
            elif(value==3):
                category:str = str(input("Please enter the category of your expense : ")) # getting the category
                if(category.capitalize() not in CATEGORIES): # checking if it is valid
                    print("\nPlease enter a valid category...\n")
                    waitForInput(False)
                    continue
                amount:float = float(input("Please enter the amount of your expense : ")) #getting price
                if(amount<0): #check if it is positive
                    print("\nPlease enter a valid amount...\n")
                    waitForInput(False)
                    continue
                description:str = str(input("Please enter the description of your expense : ")) # getting a description
                if(description == ""): # checking if it is empty to avoid any errors at split() function
                    print("\nPlease enter a valid description\n")
                    waitForInput(False)
                    continue
                addExpense(category=category.capitalize(),date=str(date.today()),amount=amount,description=description) #adds expense
            elif(value==4):
                drawBarChart() # prepare to draw a chart
            elif(value==5):
                budgets = updateBudget() # overwriting or creating a budget.txt file
            elif(value==6):
                checkAlerts() # check if there are some alerts because of the budget
            elif(value==7):
                break # to exit to program we are calling a break to while
            else:
                print("Please enter one of the given options...\n")
        except ValueError: # covering all inputs value errors
            print("\nPlease enter a valid value\n")
        except:
            print("There was an error occured. Please contact support for further information.")
            break
        waitForInput(False)
    exit() # save and quit

if __name__ == "__main__":
    mainCycle()