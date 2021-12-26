#################
#Aya Al Sabahi Term Project
#Fall 2021, 15-112
#Carnegie Mellon Qatar
#asabahi@andrew.cmu.edu
#################
import tkinter as tk
from tkinter import Label, StringVar
from tkinter import Button, Canvas, Checkbutton, Entry, Frame, Listbox, Radiobutton, Text, messagebox

#only reason I am importing tkk is to be able to use it for the scroll bar feature in the canvas later on
#I have to make sure to do tk.frame because tkk.Frame does not support style changes such as background colors
from tkinter import ttk
from functools import partial
import time
import datetime
import random 
import math
from tkinter.constants import ANCHOR, FIRST

#################
bigFont = "Times 35"
colors = {"home page": "#B8D8D8",
"settings":"#7A9E9F",
"manual":"#4F6367",
"tracker":"#EEF5DB",
"sticky notes":"#BC9382",
"statistics":"#E8E8E8",
"OH":"#A7A6BA"}
buttonsFont = "times 25"

subjectColors = ["red","blue","orange","yellow","violet", "light blue"]

stickyNoteColors = ["#EFEEEE","#E9CCB1","#D3C4BE","#E4DAC2","#F4EEE1","#EBCFC4"]

#(column, row) positions for easy access
stickyNotePos = [(0,2),(1,2),(2,2),(0,3),(1,3),(2,3)]

#corresponds to the sticky note at that index
flags = [0,0,0,0,0,0,0]

currentPage = "homePage"
##################

generatorChoice = ""

window = tk.Tk()
window.title("freshman Immigration Productivity App")
window.config(bg= "black")

config = {}
config["courseList"] = {}
config["Affirmations"] = ["Human, go back to work.","Drive. Power. \nHungry. Devour. \nYou know the deal.",
"YOU are the problem! -Prof. Khaled"]
config["toDo"] = [[]] * 6

config["noteIdentities"] = [None] * 6
# global timerStarted
timerStarted = False

timelineAllCourses = []
percentageOfTime = []

config["officeHours"] = {"Sunday": [], "Monday":[], "Tuesday":[],
"Wednesday":[],"Thursday":[], "Friday":[], "Saturday":[]}

totalTime = 0

currentPieChartChoice = "day"



homeFrame = tk.Frame(window, bg = colors["home page"], width = 800, height = 800)
settingsFrame = tk.Frame(window, bg = colors["settings"], width = 800, height = 800)
trackerFrame = tk.Frame(window, bg = colors["tracker"], width = 800, height = 800)
manualFrame = tk.Frame(window, bg = colors["manual"], width = 800, height = 800)
stickyNotesFrame = tk.Frame(window, bg = colors["sticky notes"], width = 800, height = 800)
OHFrame = tk.Frame(window, bg = colors["OH"], width = 800, height = 800)
statisticsFrame = tk.Frame(window, bg = colors["statistics"], width = 800, height = 800)


#same color as settings because in the end it is part of settings,
#frames below are an extension of settings
coursesFrame = tk.Frame(window, bg = colors["settings"], width = 800, height = 800)
officeHoursSettingsFrame = tk.Frame(window, bg = colors["settings"], width = 800, height = 800)
allTimeStatsFrame = tk.Frame(window, bg = colors["settings"], width = 800, height = 800)


#initially I would have to grid everything right, but at firsttttt I only show the homepage! 
homeFrame.grid(row = 0, column = 0)
settingsFrame.grid(row = 0, column=0)
trackerFrame.grid(row=0,column =0)
manualFrame.grid(row = 0, column = 0)
stickyNotesFrame.grid(row = 0, column = 0)
OHFrame.grid(column= 0, row = 0)
statisticsFrame.grid(row = 0, column = 0)

#same color as settings because in the end it is part of settings,
#frames below are an extension of settings
coursesFrame.grid(row = 0, column= 0)
officeHoursSettingsFrame.grid(row = 0, column = 0)
allTimeStatsFrame.grid(row = 0, column = 0)


#main pages
trackerFrame.grid_propagate(False)
manualFrame.grid_propagate(False)
stickyNotesFrame.grid_propagate(False)
homeFrame.grid_propagate(False)
statisticsFrame.grid_propagate(False)
OHFrame.grid_propagate(False)

#what relates to settings
settingsFrame.grid_propagate(False)
coursesFrame.grid_propagate(False)
officeHoursSettingsFrame.grid_propagate(False)
allTimeStatsFrame.grid_propagate(False)


#the model of how things initially start out
def homePage(window):
    #configuring the home page to be able to center
    homeFrame.grid_columnconfigure(0, weight=1)
    homeFrame.grid(column = 0, row = 0,sticky="")

    homePageLabel = tk.Label(homeFrame, text = "Freshman Immigration Planner",
    fg="black", font = bigFont, bg = colors["home page"])
    homePageLabel.grid(row = 0,column =0)
   
    createHomePageButtons(window)
    
    timeToday = calculateTimeToday()
    homePagetext = "Good job on making it this far\n\
    I believe in you!"
    homePageAffirmation = tk.Label(homeFrame,text = homePagetext,
    font = "Times 27",bg = colors["home page"],fg = "black")
    homePageAffirmation.grid(column = 0, row = 7, pady = 15)

#gives us the formatted version of how long has been spent 
def calculateTimeToday():
    totalTime = 0
    for course in config["courseList"]:
        timeSpentDay = 0
        timeSpentDay = config["courseList"][course].get(currDate, 0)
        totalTime+= timeSpentDay
    h = totalTime//3600
    m = (totalTime - h*3600)//60
    s = (totalTime - h*3600 - m*60)
    timerText = f"{m}:{m}:{s:.2f}"
    return timerText

#developer note: without lambda, the functions would automatically run on their own
def createHomePageButtons(window):
    stickyNoteButton = Button(homeFrame,text = "Sticky Notes",
        command = lambda: changeTostickyNotes(),font = buttonsFont, width = 13)
    stickyNoteButton.grid(column = 0, row = 1, pady=20)
    manuautton = Button(homeFrame,text = "Manual",
        command = lambda: changeToManual(),font = buttonsFont,width = 13)
    manuautton.grid(column = 0, row = 5, pady=20)
    trackerButton = Button(homeFrame,text = "Time Tracker",
        command = lambda: changeToTracker(),font = buttonsFont,width = 13)
    trackerButton.grid(column = 0, row = 2, pady=20)
    settingsButton = Button(homeFrame,text = "Settings",
        command = lambda: changeToSettinsg(),font = buttonsFont,width = 13,bg = "#757C88")
    settingsButton.grid(column = 0, row = 6, pady=20)
    statatisticsButton = Button(homeFrame, text = "Statistics",
        command = lambda: changeToStatsPage(), font = buttonsFont,width = 13)
    statatisticsButton.grid(column = 0, row = 4, pady = 20)
    OHButton = Button(homeFrame, text = "Office Hours",
        font = buttonsFont, command = lambda: changeToOHPage(),width = 13)
    OHButton.grid(column = 0, row = 3, pady = 20)

def trackerPage():
    trackerFrame.grid(column = 0, row = 0,sticky="")
    trackerLabel = Label(trackerFrame, text = "Select a course to time.",
        font = bigFont,bg = colors["tracker"],fg = "Black")
    trackerLabel.grid(column=0,row=0, pady = 15, sticky = "ew")
    global timerFrame
    timerFrame = Frame(trackerFrame, width = 800, height= 150, bg = colors["tracker"])
    timerFrame.columnconfigure(0,weight = 1)
    timerFrame.grid(column=0, row = 2,pady = 10)
    timerFrame.grid_propagate(False)
    trackerRadioButtons()
    trackerAffirmations()
    trackerOtherButtons()

def trackerOtherButtons():
    startNStopFrame = Frame(trackerFrame, height = 100, bg = colors["tracker"])
    startNStopFrame.grid(column = 0, row = 3, sticky = "", pady = 30)
    
    startButton = Button(startNStopFrame, text = "Start",
    font = buttonsFont, command = lambda: start())
    startButton.grid(row = 0, column = 0, padx = 15, sticky = "")


    endButton = Button(startNStopFrame, font = buttonsFont,
        text = "End", command = lambda: endTimer())
    endButton.grid(column=1,row=0,padx = 15, sticky = "")


    homeButton = Button(trackerFrame, text = "Home",
    font = buttonsFont, command = lambda: changeToHome(),bg = "#4D4E4F")
    homeButton.grid(column = 0, row = 4, sticky = "")

#please forgive me for declaring a local variable global
#however, I want the time when the start button is pressed
#and i wanna use it elsewhere too :)

def start():
    global currDate
    currDate = (time.gmtime()[2],time.gmtime()[1],time.gmtime()[0])
    global startingTime
    startingTime = time.time()
    global timerStarted
    if timerStarted == True:
        messagebox.showwarning("warning", "timer was already running\n\
        You have restarted.")
    
    # to access a global variable, just call it by its name
    #however, to change it, you have to call it through "global" variable
    #to ensure that timer does not get called multiple times
    else:
        timerStarted = True
        displayTimer()

def displayTimer():
    #to Nour, who told me to never define a function within a function... I am sorry.
    #after method calls function every 100 milliseconds, without suspending other executions
    #updates the timer
    def calculateTime():
        global timeTaken
        timeTaken = time.time() - startingTime
        hoursCounted = timeTaken//3600
        minutesCounted = (timeTaken - hoursCounted*3600)//60
        secondsCounted = (timeTaken - hoursCounted*3600 - minutesCounted*60)
        timerText = f"{hoursCounted}:{minutesCounted}:{secondsCounted:.1f}"
        global timeLabel
        timeLabel = Label(timerFrame,text = timerText,fg = "dark grey", font = "Times 50", bg = colors["tracker"], width = 800)
        timeLabel.grid(column = 0, row = 0, sticky = "")
        
        #Note: THE LAMBDA MAKES IT WORK. DO NOT REMOVE.
        #OTHERWISE IT WILL BE LIKE REGULAR RECURSION. 
        #AND THEN MAXIMUM RECURSION DEPTH.
        #LAMBDA HOLDS THE FUNCTION CALL.
        #LOOK AT TKINTER AFTER() DOCUMENTATION.

        #while the timer should still be running
        if timerStarted == True:
            trackerFrame.after(100, lambda: calculateTime())        
        
        else: 
            timeTaken = 0
        
    if timerStarted == True:
        calculateTime()

#when the end button is pressed
def endTimer():
    global timerStarted
    global timeTaken
    global timeLabel
    timerStarted = False

    config["courseList"][courseChosen.get()][currDate] = \
    config["courseList"][courseChosen.get()].get(currDate,0) + timeTaken
    
    timeTaken = 0

#starts the tracker buttons!
def trackerRadioButtons():
    radioButtonframe = Frame(trackerFrame,bg = colors["tracker"],width = 400,
        height = 300, pady= 15)
    radioButtonframe.grid_propagate(False)
    radioButtonframe.grid(column = 0, row = 1, sticky = "w")
    indexButtons = 0

    #formats it into a list for easier access
    #bc config["courseList"] is a dictionary
    helperList = []

    for course in config["courseList"]:
        helperList.append(course)
    global courseChosen
    courseChosen = tk.StringVar(value = helperList[0])
    
    for course in helperList:
        courseRB = Radiobutton(radioButtonframe, text = course,
        value = course, variable = courseChosen, fg = "Black", bg = colors["tracker"],
        font = "Times 25", highlightthickness = 0)
        courseRB.grid(column = 0, row = indexButtons, sticky = "w")
        indexButtons += 1

#pust out a motivational quote every 15 minutes
def trackerAffirmations():
    affirmationFrame = Frame(trackerFrame,bg = colors["tracker"], width = 400, height = 300)
    affirmationFrame.grid_propagate(False)
    affirmationFrame.grid(column = 0, row =1, sticky = "e")
    affirmationFrame.grid_columnconfigure(0, weight = 1)
    affirmationFrame.grid_columnconfigure(2, weight = 1)
    affirmationFrame.grid_rowconfigure(0, weight =1)
    affirmationFrame.grid_rowconfigure(2,weight =1)
    indexAffirmation = random.randint(0,len(config["Affirmations"])-1)
    textArf = textFormatter(config["Affirmations"][indexAffirmation])
    afrLabel = Label(affirmationFrame,text = textArf, font =  buttonsFont,
    bg = colors["tracker"],fg = "black")
   
    afrLabel.grid(column = 1, row = 1)

    trackerFrame.after(900000, lambda: trackerAffirmations())
    
#formatts the word so that it is always sized nicely within my frame! :)
#it adds lines!
def textFormatter(sentance):
    returnStr = ""
    spaceCounter = 1
    #first splits by number of spaces!
    for c in sentance:
        if c == " ":
            spaceCounter +=1 
        if spaceCounter % 5 == 0:
            spaceCounter = 1
            returnStr += c + "\n"
        else:
            returnStr+=c
    return returnStr

#the plain settings page
def settingsPage():
    settingsFrame.columnconfigure(0, weight =1)
    
    settingsLabel = Label(settingsFrame, text = "Settings Page",font = "Times 40", bg = colors["settings"], fg = "black")
    settingsLabel.grid(column = 0, row = 0, pady = 20)

    homeButton = Button(settingsFrame, text = "Home", font = buttonsFont, bg = "#757C88",
        command = lambda: changeToHome(), width = 15)

    homeButton.grid(column = 0, row = 1, pady = 15)

    courseEntry = Button(settingsFrame, text = "Enter Courses",
        command = lambda: changeToCoursePage(), font = buttonsFont, width = 15)
    
    courseEntry.grid(column = 0, row = 2, pady = 15)

    enterOfficeHours = Button(settingsFrame, text = "Enter Office Hours",
        command = lambda: changeToOHSettingsPage(), font = buttonsFont, width = 15)

    enterOfficeHours.grid(column = 0, row = 3, pady = 15)

    enterAllTimeStats = Button(settingsFrame, text = "All Time Statistics",
        command = lambda: changeTOAllTimeStats(), font = buttonsFont,width = 15)

    enterAllTimeStats.grid(column = 0, row = 4, pady = 15)
    
    deleteAllButton = Button(settingsFrame, text = "Reset Settings", 
        command = lambda: deleteAll(), font = buttonsFont, width = 15)

    deleteAllButton.grid(column = 0, row = 5, pady = 15)

    wrnTxt = "Only press \"reset settings\" if you are absolutely sure\n\
    you would like to delete all your data."
    warningLabel = Label(settingsFrame, text = wrnTxt, font = "Times 28",
    bg = colors["settings"], fg = "white")
    warningLabel.grid(column = 0, row = 6, pady = 15)

#resets all configurations
def deleteAll():
    global timerStarted
    global timelineAllCourses
    global percentageOfTime
    global totalTime
    global flags
    global lb
    global listOfBoxes

    #restting all values in config
    config["courseList"] = {}
    config["toDo"] = [[]] * 6
    flags = [0,0,0,0,0,0,0]

    #destorys all the sticky notes
    for i in range(len(config["noteIdentities"])):
        if config["noteIdentities"][i] != None:
            config["noteIdentities"][i][0].destroy()

    config["noteIdentities"] = [None] * 6
    config["officeHours"] = {"Sunday": [], "Monday":[], "Tuesday":[],
    "Wednesday":[],"Thursday":[], "Friday":[], "Saturday":[]}
    
    for lbbb in listOfBoxes:
        lbbb[2].delete(0,tk.END)

    config["officeHours"] = {"Sunday": [], "Monday":[], "Tuesday":[],
        "Wednesday":[],"Thursday":[], "Friday":[], "Saturday":[]}

    #resetting all other values
    timerStarted = False
    lb.delete(0,tk.END)
    timelineAllCourses = []
    percentageOfTime = []
    totalTime = 0
    window.update()

#helper function to calculate total time per subject
def allTimeStatsPage():
    helperFrame = Frame(allTimeStatsFrame,bg = colors["settings"])
    helperFrame.grid(column = 0, row =  1,padx = 20, pady = 20)
    
    homeButton = Button(helperFrame, text = "home", font = buttonsFont,
    bg = "black", command = lambda: changeToHome())
    homeButton.grid(column = 1, row = 0, padx = 10)

    settingsButton = Button(helperFrame, text = "settings",font = buttonsFont,
    command = lambda: changeToSettinsg(), bg = "black")
    settingsButton.grid(column = 0, row = 0, padx = 10)

def updateAllTimeStats():
    allTimeStatsFrame.columnconfigure(0,weight =1)
    myTimeCalculations = allTimeStatsCalculator()
    titleLabel = Label(allTimeStatsFrame, text = "All Time Statistics", font = "Times 45",
    bg = colors["settings"],fg = "black")
    titleLabel.grid(column = 0, row =0,pady = 15)
    counter = 2
    for element in myTimeCalculations:
        niceText = element[0] + " - " + element[1]
        lab = Label(allTimeStatsFrame, text = niceText, font = "Times 43",
        bg = colors["settings"], fg = "black")
        lab.grid(column = 0, row = counter, padx = 15)
        counter+=1

def allTimeStatsCalculator():
    allTime = []
    for course in config["courseList"]:
        timeSpent = 0
        for dates in config["courseList"][course]:
            timeSpent += config["courseList"][course][dates]
            hoursCounted = timeSpent//3600
            minutesCounted = (timeSpent - hoursCounted*3600)//60
            secondsCounted = (timeSpent - hoursCounted*3600 - minutesCounted*60)
            timerText = f"{hoursCounted}:{minutesCounted}:{secondsCounted:.1f}"
            allTime.append((course,timerText))
    return allTime
        
#has a button for back home and back to settings
def courseEntryPage():
    coursesText = "     Please insert what courses\
    \n you are taking this semester here."
    insertCoursesLabel = tk.Label(coursesFrame,text = coursesText,
    font = bigFont, bg = colors["settings"], fg = "black")
    insertCoursesLabel.grid(column = 0, row = 0, pady = 7)

    coursesFrame.columnconfigure(0,weight = 1)

    #creating the entry widget
    global lb
    listEntryWidget = Entry(coursesFrame, bd = 5, font = "Times 40")
    lb = Listbox(coursesFrame, height = 8,width = 30, bd=5, font = ("Times",25))
    lb.grid(column = 0, row =1,pady = 30)
    listEntryWidget.grid(column = 0, row = 2,pady = 7)


    #the settings frame buttons
    addNDeleteFrame = Frame(coursesFrame,bg = colors["settings"])
    addNDeleteFrame.grid(column = 0, row = 3)
    addButton = Button(addNDeleteFrame, text = "add", font = buttonsFont,
        command = lambda: addToList())
    addButton.grid(column = 0, row =0, padx = 15)
    deleteButton = Button(addNDeleteFrame, text = "delete", font = buttonsFont,\
        command = lambda: deleteFromList())
    deleteButton.grid(column = 1, row = 0,padx = 15)

    
    helperFrameChangerFrame = Frame(coursesFrame, bg = colors["settings"])
    helperFrameChangerFrame.grid(column = 0, row = 4, pady = 10)

    homeButton = Button(helperFrameChangerFrame, bg = "#757C88",
    text = "home",command = lambda: changeToHome(),font = buttonsFont)
    homeButton.grid(column=0,row = 1,padx = 10)

    settingsButton = Button(helperFrameChangerFrame, bg = "black",
    text = "settings",command = lambda: changeToSettinsg(),font = buttonsFont)
    settingsButton.grid(column = 0, row = 0, padx = 10, pady = 5)
    

    #adds to the list box
    def addToList():
        course = listEntryWidget.get()
        if course == "":
            messagebox.showwarning("warning", "Please enter a course")
        elif course in config["courseList"]:
            messagebox.showwarning("warning", "already have that course") 
        else:
            lb.insert(tk.END, course)
            listEntryWidget.delete(0,tk.END)

            config["courseList"][course] = {}

            

    #deleting from the list box
    def deleteFromList():
        course = lb.get(lb.curselection())
        lb.delete(tk.ANCHOR)
        del config["courseList"][course] 

        #ensures we delete it from the office hours list too!
        for day in config["officeHours"]:
            for c in config["officeHours"][day]:
                if c[0] == course:
                    del config["officeHours"][c]
    
#where the user views office hours by day!
def officeHoursPage():
    OHFrame.columnconfigure(0,weight = 1)
    OHFrame.columnconfigure(3,weight=1)
    titleLabel = Label(OHFrame,text = "Office Hours", font = "Times 35", fg = "black", bg = colors["OH"])
    titleLabel.grid(column = 0, row = 0, pady = 15, columnspan = 2) 
    createOHButtons()

#creates the day to select from for office hours
def createOHButtons():
    helperFrame = Frame(OHFrame, bg = colors["OH"])
    helperFrame.grid_columnconfigure(0, weight = 1)
    helperFrame.grid(column = 0, row = 1)

    counter = 1
    for day in config["officeHours"]:
        dayButton = Button(helperFrame, text = day, font = buttonsFont,
        command = partial(raiseDayFrame, counter -1), width = 12)
        dayButton.grid(column = 0, row = counter, pady = 15, padx = 5)
        counter +=1

    homeButton = Button(helperFrame, text = "Home", font = buttonsFont,bg = "#757C88",
    command = lambda: changeToHome(), width = 12)

    homeButton.grid(column = 0, row = 8, pady = 15, padx = 5)
    
    #initial frame, select a day to get started!

#creates the frames that have the office hours in them,
def createFramesOH():
    global framesOHDay
    framesOHDay = []
    counter = 1
    for day in config["officeHours"]:
        frameDay = Frame(OHFrame, width = 600, height = 600, bg = colors["OH"])
        frameDay.columnconfigure(0,weight = 1)
        frameDay.grid_propagate(False)
        
        dayLab = Label(frameDay, text = day, font = bigFont, fg = "#4D4E4F", bg = colors["OH"])
        dayLab.grid(column = 0, row = 0)
        if len(config["officeHours"][day]) == 0:
            txt = "No office hours today!"
            lab = Label(frameDay, text = txt, font = "Times 38", bg = colors["OH"],fg = "black")
            lab.grid(column = 0, row = 1, pady = 7)

        else:
            temp = {}
            for element in config["officeHours"][day]:
                getterEl = temp.get(element[0],[])
                getterEl.append(element[1])
                temp[element[0]] = getterEl
            
            for subjects in temp:
                title = Label(frameDay, text = subjects, font = "Times 35",fg = "#404040", bg = colors["OH"])
                title.grid(column = 0, row = counter, pady = 4)
                counter += 1
                if temp[subjects] != None:
                    for timings in temp[subjects]:
                        officeHTime = Label(frameDay, text = "‣" + timings, font = "Times 30",
                        fg = "black", bg = colors["OH"])
                        officeHTime.grid(column = 0, row = counter, pady = 3)
                        counter += 1
        frameDay.grid(column = 1, row = 1)
        framesOHDay.append(frameDay)
    
#we raise the frame OH depending on which day user selects
def raiseDayFrame(i):
    framesOHDay[i].tkraise()

#where the user is able to add office hours per subject!
def officeHoursSettingsPage():
    courseRadioButtons()
    
    global listOfBoxes
    listOfBoxes = listBoxframesInitializer()
    dayRadioButtons(listOfBoxes)

    helperFrame = Frame(officeHoursSettingsFrame, bg = colors["settings"], height = 200)

    homeButton = Button(helperFrame,text = "home", bg = "black", font = buttonsFont,
    command = lambda: changeToHome())
    homeButton.grid(column = 1, row = 0)
    SettingsButton = Button(helperFrame,text = "settings", font = buttonsFont,
    command = lambda: changeToSettinsg(), bg = "black")
    SettingsButton.grid(column = 0, row = 0, pady = 10,padx = 10)

    helperFrame.grid(column = 0, row = 3, pady = 10, columnspan=3)

    officeHoursLabel = Label(officeHoursSettingsFrame,text = "Add Office Hours!",
    bg = colors["settings"], font = "Times 30",fg = "black")
    officeHoursLabel.grid(column = 0, row = 0, columnspan = 3,pady = 10 )

    helperText = "Hint: add in office hours with the CA/TA\nFor example 12:30-1:30 Professor xyz."

    helperLabel = Label(officeHoursSettingsFrame, text = helperText, font = buttonsFont, bg = colors["settings"], fg = "white")
    helperLabel.grid(column = 0, row = 2, sticky = "ew", columnspan = 3, pady = 10)

#creates the radio buttons that will allow us to choose
#to choose the day to add OH
def dayRadioButtons(L):
    radioButtonframe = Frame(officeHoursSettingsFrame,bg = colors["settings"],width = 248,
        height = 350, pady= 15)
    radioButtonframe.grid_propagate(False)
    radioButtonframe.grid(column = 0, row = 1,pady = 15)
    indexButtons = 0

    #formats it into a list for easier access
    #bc config["courseList"] is a dictionary
    helperList = []

    for day in config["officeHours"]:
        helperList.append(day)

    global dayChosen

    dayChosen = tk.StringVar(value = helperList[0])
    
    for day in helperList:
        dayRB = Radiobutton(radioButtonframe, text = day,
        value = day, variable = dayChosen, fg = "Black", bg = colors["settings"],
        font = "Times 24", highlightthickness = 0, command = lambda:dayRadioPressed(L))
        dayRB.grid(column = 0, row = indexButtons, sticky = "w")
        indexButtons += 1

def dayRadioPressed(L):
    global userPressedRadioDay
    userPressedRadioDay = True
    raiseCorrectFrameOH(L)

#creates radio buttons that will allow us to choose the subject
#we want to add OH for
def courseRadioButtons():
    radioButtonframe = Frame(officeHoursSettingsFrame,bg = colors["settings"],width = 250,
        height = 300, pady= 15)
    radioButtonframe.grid_propagate(False)
    radioButtonframe.grid(column = 1, row = 1)
    indexButtons = 0

    #formats it into a list for easier access
    #bc config["courseList"] is a dictionary
    helperList = []

    for course in config["courseList"]:
        helperList.append(course)

    global courseChosenForOhSettings

    if len(helperList) != 0:
        courseChosenForOhSettings = tk.StringVar(value = helperList[0])
    
    for day in helperList:
        dayRB = Radiobutton(radioButtonframe, text = day,
        value = day, variable = courseChosenForOhSettings, fg = "Black", bg = colors["settings"],
        font = "Times 24", highlightthickness = 0)
        dayRB.grid(column = 0, row = indexButtons, sticky = "w")
        indexButtons += 1

#initialized the frames with the list boxes to enter office hours
#0 index refers to Sudnay, 1 Monday...
#[[frame,day label, listBox, EntryBox, addButton, deleteButton], [frame...]]
def listBoxframesInitializer():
    framesOHListEnterance = []
    counter = 0
    for day in config["officeHours"]:
        helperOHEntryFrame = Frame(officeHoursSettingsFrame,bg = "#2C3E4C",width = 250,
        height = 300)
        helperOHEntryFrame.grid(column = 2, row =1, pady = 15)
        helperOHEntryFrame.grid_columnconfigure(0, weight = 1)

        dayLabel = Label(helperOHEntryFrame, text = day, bg = "#2C3E4C",
        fg = "white", font = buttonsFont)
        dayLabel.grid(column = 0, row = 0)

        lb = Listbox(helperOHEntryFrame, height = 5, bd = 2, font = "Times 15")
        lb.grid(column = 0, row = 1, sticky = "ew")
        
        enterOH = Entry(helperOHEntryFrame, font = "Times 20",bd = 2, bg = "black")
        enterOH.grid(column = 0, row = 2)
        
        helperButtonsFrame = Frame(helperOHEntryFrame, bg = "#2C3E4C")
        helperButtonsFrame.grid(column = 0, row = 3)
        helperButtonsFrame.grid_columnconfigure(0, weight = 1)
        helperButtonsFrame.grid_columnconfigure(1, weight = 1)

        addButton = Button(helperButtonsFrame, font = "Times 20", text = "Add", bg = "black",
            command = lambda: addToOfficeHours())

        addButton.grid(column = 0, row = 0, pady = 5)

        deleteButton = Button(helperButtonsFrame,font = "Times 20", text = "Delete", bg = "black",
        command = lambda: deleteFromOfficeHours())
        deleteButton.grid(column = 1, row = 0)

        framesOHListEnterance.append([helperOHEntryFrame, dayLabel,lb,enterOH,addButton,deleteButton])
        counter +=1 
    return framesOHListEnterance

#raises the frame with respect to what day it is
def raiseCorrectFrameOH(L):
    helperKnowNumber = {"Sunday":0, "Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4,
    "Friday":5, "Saturday":6}

    day = dayChosen.get()
    pythonIsNotWorkingSoICreatedATempHere = L[helperKnowNumber[day]][0]
    pythonIsNotWorkingSoICreatedATempHere.tkraise()

#adds to office hours after user presses add to list
def addToOfficeHours():
    course = courseChosenForOhSettings.get()

    helperKnowNumber = {"Sunday":0, "Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4,
    "Friday":5, "Saturday":6}

    timeWord = listOfBoxes[helperKnowNumber[dayChosen.get()]][3]
    store = timeWord.get()

    global userPressedRadioDay

    strHelper = course + " "+ store
    listOfBoxes[helperKnowNumber[dayChosen.get()]][2].insert(tk.END,strHelper)
    config["officeHours"][dayChosen.get()].append((course, store))
    listOfBoxes[helperKnowNumber[dayChosen.get()]][3].delete(0, tk.END)

#deletes from listbox 
#first we get the day from selection, and we delete from the listbox
#then we delete it from the actual list
def deleteFromOfficeHours():
    helperKnowNumberReversed = {0:"Sunday", 1:"Monday", 2:"Tuesday", 3:"Wednesday", 4:"Thursday",
    5:"Friday", 6:"Saturday"}

    helperKnowNumber = {"Sunday":0, "Monday":1, "Tuesday":2, "Wednesday":3, "Thursday":4,
    "Friday":5, "Saturday":6}

    lb = listOfBoxes[helperKnowNumber[dayChosen.get()]][2]
    officeHourSelection = lb.get(lb.curselection())
    lb.delete(tk.ANCHOR)
    
    for i  in range(len(officeHourSelection)):
        if officeHourSelection[i] == " ":
            finder = i
            break
    
    course = officeHourSelection[0:i]
    date = officeHourSelection[i+1:]

    for i in range(len(config["officeHours"][dayChosen.get()])):
        if config["officeHours"][dayChosen.get()][i] == (course,date):
            config["officeHours"][dayChosen.get()].pop(i)
            return 

config["manual"] = ""

#opening the txt manual!
with open('manual.txt') as f:
    lines = f.readlines()

    for l in lines:
        l = l.lstrip(' ')
        config["manual"] += l

#self explanatory, page with the manual.
def manualPage():
    manualFrame.columnconfigure(0, weight = 1)
    instructions = Label(manualFrame, text = config["manual"], font = "Times 18", bg = colors["manual"])
    instructions.grid(column = 0, row = 0, pady = 5)

    homeButton = Button(manualFrame, text = "Home", font = "Times 23",
    command = lambda: changeToHome())

    homeButton.grid(column = 0, row = 1, pady = 5)

#generating the pie chart and all
def statisticsPage():
    statsFrames()
    createStatsButtons()
    createOtherStatsButtons()

#contains all the helper frames used in statistics page
def statsFrames():
    global choiceButtonsFrame
    choiceButtonsFrame = Frame(statisticsFrame, width = 800, height = 150,
    bg = colors["statistics"])
    choiceButtonsFrame.grid(row = 0, column = 0, sticky = "ew")
    choiceButtonsFrame.grid_propagate(False)
    choiceButtonsFrame.columnconfigure(0, weight=1)
    choiceButtonsFrame.columnconfigure(4,weight =1)
    choiceButtonsFrame.rowconfigure(0,weight =1)
    choiceButtonsFrame.rowconfigure(2,weight =1)

    global canvasFrame
    canvasFrame = Frame(statisticsFrame, bg = colors["statistics"],width = 800, height = 500)
    canvasFrame.grid(column = 0, row = 1)
    canvasFrame.grid_propagate(False)
    canvasFrame.columnconfigure(0,weight =1)
    canvasFrame.columnconfigure(2, weight = 1)
    canvasFrame.rowconfigure(0,weight =1)
    canvasFrame.rowconfigure(2, weight =1)

    global statsOtherButtonsFrame
    statsOtherButtonsFrame = Frame(statisticsFrame, width = 800, height= 150, bg = colors["statistics"])
    statsOtherButtonsFrame.grid_propagate(False)
    statsOtherButtonsFrame.columnconfigure(0, weight=1)
    statsOtherButtonsFrame.columnconfigure(4,weight =1)
    statsOtherButtonsFrame.rowconfigure(0,weight =1)
    statsOtherButtonsFrame.rowconfigure(2,weight =1)
    statsOtherButtonsFrame.grid(row = 2, column = 0)

#stats day/week/month buttons
def createStatsButtons():
    dayButton = Button(choiceButtonsFrame, text = "day", font = buttonsFont,
        command = lambda: dayCalculator())
    dayButton.grid(column = 1, row = 1, padx = 15)
    weekButton = Button(choiceButtonsFrame, text = "week", font = buttonsFont,
        command = lambda: weekCalculator())
    weekButton.grid(column = 2, row = 1, padx = 15)
    monthButton = Button(choiceButtonsFrame, text = "month", font = buttonsFont,
        command = lambda: monthCalculator())
    monthButton.grid(column = 3, row = 1, padx = 15)

#creates the buttons at the bottom, home & frame
def createOtherStatsButtons():
    generateButton = Button(statsOtherButtonsFrame, text = "generate",
        font = buttonsFont, command = lambda: generate())
    generateButton.grid(column = 1, row = 0, padx = 30)

    homeButton = Button(statsOtherButtonsFrame, text = "home",
        font = buttonsFont, command = lambda: changeToHome())
    homeButton.grid(column = 2, row = 0, padx = 30)

#returns a string formatted for the time!
def timeFormtter(t):
    hoursCounted = t//3600
    minutesCounted = (t - hoursCounted*3600)//60
    secondsCounted = (t - hoursCounted*3600 - minutesCounted*60)
    timerText = f"{hoursCounted}:{minutesCounted}:{secondsCounted:.1f}"
    return timerText
#calculates the time for the past week
def dayCalculator():
    global timelineAllCourses
    global totalTime
    global currentPieChartChoice

    global currDate
    currDate = (time.gmtime()[2],time.gmtime()[1],time.gmtime()[0])

    timelineAllCourses = []
    totalTime = 0
    currentPieChartChoice = "day"
    for course in config["courseList"]:
        timeSpentDay = 0
        timeSpentDay = config["courseList"][course].get(currDate, 0)
        totalTime+= timeSpentDay
        
        timelineAllCourses.append((course,timeSpentDay))
        
#calculates the time per subject for the past week
def weekCalculator():
    global timelineAllCourses
    global totalTime
    global currentPieChartChoice

    timelineAllCourses = []
    totalTime = 0
    currentPieChartChoice = "week"

    for course in config["courseList"]:
        timeSpent = 0
        for dates in config["courseList"][course]:
            for i in range(7):
                timeSearching = datetime.datetime.now() - datetime.timedelta(days=i)
                timeSearching = timeSearching.timetuple()
                timeSearching = (timeSearching[2],timeSearching[1],timeSearching[0])
                timeSpent += config["courseList"][course].get(timeSearching, 0)
        timelineAllCourses.append((course,timeSpent))
        totalTime += timeSpent

#calculates the days from the previous 30 days
def monthCalculator():
    global timelineAllCourses
    global totalTime
    global currentPieChartChoice

    timelineAllCourses = []
    totalTime = 0
    currentPieChartChoice = "month"

    for course in config["courseList"]:
        timeSpent = 0
        for dates in config["courseList"][course]:
            for i in range(30):
                timeSearching = datetime.datetime.now() - datetime.timedelta(days=i)
                timeSearching = timeSearching.timetuple()
                timeSearching = (timeSearching[2],timeSearching[1],timeSearching[0])
                timeSpent += config["courseList"][course].get(timeSearching, 0)
        timelineAllCourses.append((course,timeSpent))
        totalTime += timeSpent

#generates the pie chart.
def generate():
    dayCalculator()
    noDataText = "No data has been tracked yet.\n\
    Please track your work."
    noDataLabel = Label(canvasFrame,text = noDataText, font= bigFont,
    bg = colors["statistics"],fg = "black")

    #flag not tracked yet checks if the value is zero for all 
    #the values 
    flagNotTrackedYet = True

    for caculated in timelineAllCourses:
        if caculated[1] != 0:
            flagNotTrackedYet = False

    if flagNotTrackedYet == True:
        noDataLabel.grid(column = 1, row = 1)
    
    #we draw the pie chart now! :D
    else:
        mathForPieChart()
        drawingPieChart()

#calculates the angles to be able to draw the arc
def mathForPieChart():

    global percentageOfTime
    percentageOfTime = []
    for i in range(len(timelineAllCourses)):
        #no need for the if as it was accounted for in generate() but justttt in case :)
        #to prevent a divide by zero error
        if totalTime != 0:
            subject = timelineAllCourses[i][0]
            startAngle = round((timelineAllCourses[i][1]/totalTime*360))
            percentageOfTime.append((subject, startAngle, timeFormtter(timelineAllCourses[i][1])))

    #returns a list of hours and minutes for each subject, to use w the label

#calls the helper functions to put the goregous marvelous beautiful pie chart together
def drawingPieChart():
    canv = Canvas(canvasFrame, bg = "dark grey", width = 600, height = 600)
    canv.grid(row = 1, column =1)
    startAngle = 0
    #counter is to ensure the nice different color choices
    counter = 0
    for element in percentageOfTime:

        endAngle = element[1] + startAngle

        while endAngle >360:
            endAngle -=1

        if (startAngle != 0 or startAngle != 360) and endAngle == 359:
            endAngle = 360
        
        if startAngle == 0 and endAngle == 360:
            Canvas.create_oval(canv,100,50,500,450, fill = subjectColors[counter%len(subjectColors)])
        
        else:
            Canvas.create_arc(canv,100,50,500,450, start = startAngle,
            extent = endAngle - startAngle,fill = subjectColors[counter%len(subjectColors)])
            counter += 1
            startAngle = endAngle

    noPercent = ""   
    startAngle = 0
    #we create the labels afterwards so it sits on top of the arc
    for element in percentageOfTime:
        endAngle = element[1] + startAngle
        
        while endAngle > 360:
            endAngle -= 1

        if endAngle == startAngle:
            
            noPercent += element[0]+ "&... "
            
        else:
            createLabel(canv,startAngle,endAngle, element[0],element[2])
        startAngle = endAngle
    
    if noPercent != "":
        Canvas.create_text(canv,25,475,text = "0%: " + noPercent, anchor = "w")

#creates the label midway where the arc is positioned
def createLabel(c, angle1,angle2,word, time):
    percent = ((angle2 - angle1)/360 *100) 
    myAngle = angle1 + (angle2-angle1)//2
    percent = round(percent,2)

    #centerPoint plus a bit extra + calcualted x & y position
    posX = 300 + 245* math.cos(myAngle/180*math.pi)

    
    posY = 250  - 230* math.sin(myAngle/180*math.pi)
   
    Canvas.create_text(c, posX, posY, text = word + "\n"+str(percent) + "%" +"\n"+time)
    
    #also create a label for hours

#all of the "change to" will sort of be our page switch controller
def changeToHome():
    homeFrame.update()
    homeFrame.tkraise()

def changeToTracker():
    if len(config["courseList"]) == 0:
        tk.messagebox.showwarning(title=None, message = "You have not added any courses \n \
        please add at least one")
    else:
        trackerPage()
        trackerFrame.tkraise()
        
def stickyNotesPage():
    stickyNotesFrame.grid_columnconfigure(0, weight= 1, uniform = "column")
    stickyNotesFrame.grid_columnconfigure(2, weight = 1, uniform = 'column')
    
    buttonHome = Button(stickyNotesFrame, text = "Home",
    font = buttonsFont, command = lambda: changeToHome(), pady = 10, bg = "#4D4E4F")
    buttonHome.grid( column = 1, row = 0, pady = 10)

    newSticky = Button(stickyNotesFrame, text = "New Note",
     command = lambda: whenUserPressesNewNote(), font = buttonsFont)
    newSticky.grid(column= 1, row = 1, pady= 10)

#horrible function name i am sorry but it works 
def whenUserPressesNewNote():
    index = helperGetIndex()
    if index == None:
        messagebox.showwarning("warning", "maximum sticky notes reached: 6.")
    else:
        createNote(index)

#where the notes actually get constructed
def createNote(i):
    #this is the container for the other objects in the sticky note :)
    containerFrame = Frame(stickyNotesFrame, bd = 10, 
    bg = stickyNoteColors[i], width = 200, height = 200)
    containerFrame.grid(column = stickyNotePos[i][0],
    row = stickyNotePos[i][1], padx = 25, pady = 25)
    containerFrame.grid_columnconfigure(0,weight =1)
    containerFrame.grid_columnconfigure(2, weight = 1)
    containerFrame.grid_rowconfigure(0, weight = 1)
    containerFrame.grid_rowconfigure(4, weight = 1)
    containerFrame.grid_propagate(False)

    #the frame where checkboxes will be added,
    #tkinter frame object has no scrolar so we will have to add
    #the frame to a canvas first.
    #however, decided to omit the scrolar until further notice
    cHelper = Canvas(containerFrame, width = 180, height = 140, bg = "white")
    cHelper.grid(column = 1, row = 0)
    window.update()

    #the wrapper frame that will hold the checkboxes 
    wrapper = Frame(cHelper, bg = "white",width = 180, height = 140)
    wrapper.grid_propagate(False)
    wrapper.grid(column = 0, row = 0)

    #the text entry box
    textInputSpace = Entry(containerFrame, width = 20, font = "Times 10")
    textInputSpace.grid(column = 1, row = 1, pady = 5)

    #a helper frame to allow us to easily center our buttons
    helperButtonsframe = Frame(containerFrame, bg = stickyNoteColors[i])
    helperButtonsframe.grid_columnconfigure(0, weight = 1)
    helperButtonsframe.grid_columnconfigure(1, weight= 1)
    helperButtonsframe.grid(column = 1, row = 3)

    #the buttons add and delete sticky note.
    #note: partial is used to get what the value of i was at that instant :)
    adderButton = Button(helperButtonsframe, font = "Times 10", text = "add",
    command = partial(addToCheckList, i))
    adderButton.grid(column = 1, row = 0, padx = 5)

    clearButton = Button(helperButtonsframe, font = "Times 10", text = "delete note",
    command = partial(deleteStickyNote, i))
    clearButton.grid(column = 2, row = 0, padx = 5)

    # (0: containerFrame, 1: canvas, 2: wrapper frame,
    # 3: adderButton, 4:delete Button, 5: textINput, 6: how many ckeckBoxes so far)
    config["noteIdentities"][i] = [containerFrame, cHelper, wrapper, adderButton,clearButton,textInputSpace,0]

#when the user presses add
def addToCheckList(index):
    #5 refers to the textInput widget
    task = config["noteIdentities"][index][5].get()

    if task != "":
        config["toDo"][index].append(task)
        addingCheckboxes(index, task)
        config["noteIdentities"][index][6] +=1
        config["noteIdentities"][index][5].delete(0,tk.END)
     
#adds the checkboxes and accounts for position
def addingCheckboxes(index, task):
    var = tk.IntVar()
    frameToAddTo = config["noteIdentities"][index][2]
    checkBoxMaker = Checkbutton(frameToAddTo,text = task,variable = var, fg = "black",
    bg = "white", borderwidth = 0, highlightthickness = 0, bd = 0) 
    checkBoxMaker.grid(column = 0, row = config["noteIdentities"][index][6], sticky = "w")

#deletes the sticky note
def deleteStickyNote(index):
    #[0] refers to the container frame
    config["noteIdentities"][index][0].destroy()
    config["noteIdentities"][index] = []
    flags[index] = 0
    
#returns where a sticky note should be added next, 
#if no flags are found, it returns None instead
def helperGetIndex():
    for i in range(6):
        if flags[i] == 0:
            flags[i] = 1
            return i
    return None

def changeToManual():
    global currentPage 
    currentPage = "manual"
    manualFrame.tkraise()

def changeToSettinsg():
    global currentPage
    currentPage = "settings"
    settingsFrame.tkraise()

def changeTostickyNotes():
    global currentPage
    currentPage = "Sticky Notes"
    stickyNotesFrame.tkraise()
    
def changeToCoursePage():
    global currentPage
    currentPage = "courses"
    coursesFrame.tkraise()

def changeToStatsPage():
    global currentPage
    currentPage = "statistics"
    statisticsFrame.tkraise()
    statisticsPage()

def changeToOHSettingsPage():
    if len(config["courseList"]) == 0:
        messagebox.showwarning(title = None, message = "Please add courses first to edit office hours")
    else:
        global currentPage
        global userPressedRadioDay
        userPressedRadioDay = False
        currentPage = "officeHoursSettings"
        officeHoursSettingsFrame.tkraise()
        courseRadioButtons()
        helperOHEntryFrame = Frame(officeHoursSettingsFrame,bg = colors["settings"],width = 290,
        height = 300)
        helperOHEntryFrame.grid(column = 2, row = 1, pady = 15)

def changeToOHPage():
    createFramesOH()
    OHFrame.tkraise()
    frameDay = Frame(OHFrame, width = 600, height = 600, bg = colors["OH"])
    frameDay.grid(column = 1, row = 1)
    
def changeTOAllTimeStats():
    allTimeStatsFrame.tkraise()
    updateAllTimeStats()

#where we ensure that all the widegts initialize!
homeFrame.tkraise()
homePage(window)
settingsPage()
stickyNotesPage()
manualPage()
courseEntryPage()
officeHoursPage()
officeHoursSettingsPage()
allTimeStatsPage()
window.geometry("800x800")
window.mainloop()
