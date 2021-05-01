# Scheduler window widgets spacing logic is badly coded, but it works

import tkinter as tk
from scheduler_driver import driver
import json

global schedulerQueueNumber
schedulerQueueNumber = 1

class CreateField:
    def __init__(self, row):
        self.row = row

    def createSchedule(self, scheduleFrame, schedulesList, optionsList=None, fill1=None, fill2=None, fill3=None, fill4=None, fill5=None):
        if (self.row > 10):
            print("Max number of scheduled Meetings reached")
            return

        variable = tk.StringVar()
        # variable.set(LIST[0]) # default value

        DEFAULT = [""]
        OPTIONS = optionsList

        # Add queue number to schedule (this is an other, independent variable from row number)
        global schedulerQueueNumber
        number = tk.Label(scheduleFrame, text=str(schedulerQueueNumber) + ".")
        number.grid(row=self.row, column=0, sticky="we")
        schedulerQueueNumber += 1

        if (optionsList != None):
            entry1 = tk.OptionMenu(scheduleFrame, variable, *OPTIONS)
            entry1.config(width=17, indicatoron=0, font=("Arial", 8), anchor="w")
            entry1.grid(row=self.row, column=1, columnspan=2, padx=5)
        else:
            entry1 = tk.OptionMenu(scheduleFrame, variable, *DEFAULT)
            entry1.config(width=17, indicatoron=0, font=("Arial", 8), anchor="w")
            entry1.grid(row=self.row, column=1, columnspan=2, padx=5)

        entry2 = tk.Entry(scheduleFrame, width=30)
        entry2.grid(row=self.row, column=3, columnspan=3, padx=5)

        entry3 = tk.Entry(scheduleFrame, width=10)
        entry3.grid(row=self.row, column=6, padx=5)

        entry4 = tk.Entry(scheduleFrame, width=10)
        entry4.grid(row=self.row, column=7, padx=5)

        entry5 = tk.Entry(scheduleFrame, width=10)
        entry5.grid(row=self.row, column=8, padx=5)

        if (fill1 != "" or fill2 != "" or fill3 != "" or fill4 != "" or fill5 != ""):
            if (fill1 != None):
                variable.set(fill1)
                entry2.insert(0, fill2)
                entry3.insert(0, fill3)
                entry4.insert(0, fill4)
                entry5.insert(0, fill5)

        # Append fields to list to use them later
        entryList = [variable, entry1, entry2, entry3, entry4, entry5, number]
        schedulesList.append(entryList)

    def createSaved(self, savedFrame, savesList, fill1=None, fill2=None):
        if (self.row > 15):
            print("Max number of saved Meetings reached")
            return

        entry1 = tk.Entry(savedFrame, width=20)
        entry1.grid(row=self.row, column=0, padx=5)

        entry2 = tk.Entry(savedFrame, width=30)
        entry2.grid(row=self.row, column=1, padx=5)

        if (fill1 != None):
            entry1.insert(0, fill1)
            entry2.insert(0, fill2)

        entryList = [entry1, entry2]
        savesList.append(entryList)

global opened
opened = False

def runScheduler(application, root, languageApp):
    # Checks if Scheduler window is already opened
    global opened
    if (opened == False):
        opened = True
        scheduler(application, root, languageApp)
    else:
        print("Scheduler already opened")

def scheduler(application, root, languageApp):

    eng = [ "Schedule Meetings to be auto-joined and auto-leaved", "Choose from Saved", "or insert link manually",
            "Join time", "People less than", "/ Leave time", "Add", "People and Leave time can't both be empty",
            "Invalid number of people", "Invalid time value, format: hh:mm:ss (Check for whitespaces)",
            "Meeting title and link fields filled incorrectly (choose only one)", "Saved", "Save Meetings for repeated use", "Title",
            "Meeting link (if link is temporary)", "Add", "Save", "Start Scheduled Meeting" ]

    est = [ "Meetingud automaatsete liitumiste ja lahkumistega", "Salvestatud Meeting", "või sisesta käsitsi link",
            "Liitumise aeg", "Inimeste arv", "Lahkumise aeg", "Lisa", "Inimeste arv ja lahkumise aeg ei saa mõlemad olla tühjad",
            "Vigane inimeste arv", "Vigane kellaaeg, vorming: hh:mm:ss", "Vigane Meetingu pealkiri/link (vali ainult üks)", "Salvestatud",
            "Salvesta Meetinguid, et neid korduvalt kasutada", "Pealkiri", "Meetingu link (kui on püsiv)", "Lisa", "Salvesta", "Alusta Meetingud" ]

    global schedulesList
    global savesList
    schedulesList = []
    savesList = []
    global scheduleCount
    global savedCount
    global geometryY
    
    scheduleCount = 2
    savedCount = 2
    geometryY = 200
    window = tk.Toplevel()
    window.geometry("750x250")
    window.title("Scheduler - Google Meet automated tool")

    def close():
        global opened
        opened = False
        window.withdraw()

    window.protocol("WM_DELETE_WINDOW", close)

    def runDriver():
        global opened
        root.withdraw()
        window.withdraw()
        opened = False
        driver(application)

    def runCreateSchedule():
        options = getSavedMeetingsTitles()
        global scheduleCount
        global geometryY
        global schedulesList
        scheduleCount += 1
        createSchedule = CreateField(scheduleCount)
        createSchedule.createSchedule(scheduleFrame, schedulesList, optionsList=options)
        print("Added schedule, number of schedules now: " + str(len(schedulesList)))
        if (scheduleCount < 11):
            geometryY = 200 + len(savesList) * 20 + len(schedulesList) * 30
            window.geometry("750x" + str(geometryY))

    def runCreateSaved():
        global savedCount
        global geometryY
        global savesList
        savedCount += 1
        createSaved = CreateField(savedCount)
        createSaved.createSaved(savedFrame, savesList)
        if (savedCount < 16):
            if (len(savesList) != 0):
                geometryY = 200 + len(savesList) * 20 + len(schedulesList) * 30 + 40
                window.geometry("750x" + str(geometryY))
            else:
                geometryY = 200 + 20 + len(schedulesList) * 30

    def getSavedMeetingsTitles():
        options = []
        options.append("")
        try:
            with open('saved_meetings.json', 'r') as file:
                data = json.load(file)
                for i in data["saved"]:
                    options.append(i["title"])
            return options
        except:
            pass

    def checkValidTime(time):
        valid = "1234567890:"
        for i in time:
            if (i in valid):
                continue
            else:
                return False
        if (time != "" and len(time) == 8):
            if (time[2] == ":" and time[5] == ":" and (int(time[0] + time[1]) < 24) and (int(time[3] + time[4]) < 60) and (int(time[6] + time[7]) < 60)):
                return True
            else:
                return False
        else:
            return False

    def checkValidPeople(userInput):
        valid = "1234567890"
        for i in userInput:
            if (not i in valid or userInput[0] == "0"):
                return False

    def saveScheduledFields():

        def displayError(message):
            print(message)
            error = tk.Label(scheduleFrame, text=message, fg="red")
            error.grid(row=scheduleCount + 1, column=3, columnspan=5, sticky="w")
            error.after(5000, error.destroy)
            return

        def save(file):
            try:
                lang = ""
                if (languageApp == "english"):
                    lang = eng
                elif (languageApp == "estonia"):
                    lang = est

                data = json.load(file)
                data['scheduled'] = []
                for i in schedulesList:
                    print(len(schedulesList))
                    saved = i[0].get()
                    link = i[2].get()
                    join_time = i[3].get()
                    people = i[4].get()
                    leave_time = i[5].get()

                    # Error handlers
                    if (saved == "" and link == "" and join_time == "" and people == "" and leave_time == ""):
                        continue
                    if (people == "" and leave_time == ""):
                        displayError(lang[7])
                        return False
                    if (checkValidPeople(people) == False):
                        displayError(lang[8])
                        return False
                    if (checkValidTime(join_time) == False or checkValidTime(leave_time) == False):
                        displayError(lang[9])
                        return False
                    if ((saved == "" and link == "") or (saved != "" and link != "")):
                        displayError(lang[10])
                        return False

                    data['scheduled'].append({
                        'saved': str(saved),
                        'link': str(link),
                        'join_time': str(join_time),
                        'people': str(people),
                        'leave_time': str(leave_time)
                    })
            except:
                print("No Schedules to save")
                return

            # Display success and save data
            success = tk.Label(scheduleFrame, text=lang[11], fg="green")
            success.grid(row=scheduleCount + 1, column=8)
            success.after(5000, success.destroy)

            with open('saved_meetings.json', 'w') as file:
                json.dump(data, file, indent=4)
        try:
            with open('saved_meetings.json', 'x') as file:
                # Give info to saveSavedFields()
                if (save(file) == False):
                    return False
        except:
            with open('saved_meetings.json', 'r') as file:
                if (save(file) == False):
                    return False

    def fillScheduledFields(save=None):
        try:
            global schedulesList
            global scheduleCount
            with open('saved_meetings.json', 'r') as file:
                data = json.load(file)
                options = getSavedMeetingsTitles()
                global geometryY
                for i in data["scheduled"]:
                    createSchedule = CreateField(scheduleCount)
                    createSchedule.createSchedule(scheduleFrame, schedulesList, optionsList=options, fill1=i["saved"], fill2=i["link"], fill3=i["join_time"], fill4=i["people"], fill5=i["leave_time"])
                    scheduleCount += 1
                    if (save == None):
                        geometryY += 30
                window.geometry("750x" + str(geometryY))

        except:
            print("No schedules yet")
            # Create one scheduled field if there is none in the schedulesList
            global schedulerQueueNumber
            schedulerQueueNumber = 1 # Change to one to reset queue numbers
            options = getSavedMeetingsTitles()
            createSchedule = CreateField(scheduleCount)
            createSchedule.createSchedule(scheduleFrame, schedulesList, optionsList=options)

    def saveSavedFields():
        def save(file):
            data = json.load(file)
            data['saved'] = []
            for i in savesList:
                title = i[0].get()
                link = i[1].get()
                if (title == "" and link == ""):
                    continue
                else:
                    data['saved'].append({
                        'title': str(title),
                        'link': str(link)
                    })
            with open('saved_meetings.json', 'w') as file:
                json.dump(data, file, indent=4)
                print("Saved Meetings")
        try:
            with open('saved_meetings.json') as file:
                save(file)
        except:
            with open('saved_meetings.json', 'x') as file: # Create json file and dump lists to it
                data = {}
                data["scheduled"] = []
                data["saved"] = []
                with open('saved_meetings.json', 'w') as file3:
                    json.dump(data, file3, indent=4)
            with open('saved_meetings.json', 'r') as file:
                save(file)
            
        global scheduleCount
        global schedulesList
        global geometryY
        global savesList
        global savedCount
        global schedulerQueueNumber

        schedulerQueueNumber = 1 # Reset queue counter

        # Saved frame save button also saves scheduled fields (only one save button exists for both),
        # below is the code for it:

        if (saveScheduledFields() == False):
            return

        # Destroy previous widgets in schedulesList and savesList
        for i in schedulesList:
            i[1].destroy()
            i[2].destroy()
            i[3].destroy()
            i[4].destroy()
            i[5].destroy()
            i[6].destroy()

        for i in savesList:
            i[0].destroy()
            i[1].destroy()

        # Refresh scheduled meetings fields (create them again) when Meetings are saved
        scheduleCount = 2
        schedulesList = []
        savedCount = 2
        savesList = []
        
        fillScheduledFields(save=True)
        fillSavedFields(save=True)
        print("Schedules: " + str(len(schedulesList)))
        print("Saved Meetings: " + str(len(savesList)))
        if (len(savesList) != 0):
            window.geometry("750x" + str(200 + len(schedulesList) * 30 + len(savesList) * 20 + 10))
        else:
            window.geometry("750x" + str(200 + len(schedulesList) * 30 + 50))

    def fillSavedFields(save=None):
        try:
            global savesList
            global savedCount
            global geometryY
            # Create one scheduled field if there is none in the schedulesList
            # if (len(savesList) == 0):
            #     options = getSavedMeetingsTitles()
            #     createSchedule = Schedule(savedCount)
            #     createSchedule.createSchedule(savedFrame, savesList, optionsList=options)
            #     geometryY = 200 + len(savesList) * 20 + len(schedulesList) * 30
            #     window.geometry("750x" + str(geometryY))
            with open('saved_meetings.json', 'r') as file:
                data = json.load(file)
                for i in data["saved"]:
                    createSaved = CreateField(savedCount)
                    createSaved.createSaved(savedFrame, savesList, fill1=i["title"], fill2=i["link"])
                    savedCount += 1
                    if (save == None):
                        geometryY += 20
                window.geometry("750x" + str(geometryY))
        except:
            print("No saved Meetings yet")

    def language():
        def addText(lang):
            title.config(text=lang[0])
            label1.config(text=lang[1])
            label2.config(text=lang[2])
            label3.config(text=lang[3])
            label4.config(text=lang[4])
            label5.config(text=lang[5])
            btnAdd.config(text=lang[6])

            label6.config(text=lang[12])
            label7.config(text=lang[13])
            label8.config(text=lang[14])
            savedAdd.config(text=lang[15])
            savedSave.config(text=lang[16])
            start.config(text=lang[17])

        # Assign language to widgets
        if (languageApp == "english"):
            addText(eng)
        elif (languageApp == "estonia"):
            addText(est)

    # Scheduler frame widgets
    scheduleFrame = tk.Frame(window, width=650, height=400)
    scheduleFrame.place(relx=0.5, anchor="n")

    title = tk.Label(scheduleFrame, text="Schedule Meetings to be auto-joined and auto-leaved", font=("Kefa", 12))
    title.grid(row=0, column=0, columnspan=9, pady=10, sticky="w")

    label1 = tk.Label(scheduleFrame, text="Choose from Saved")
    label1.grid(row=1, column=1, columnspan=2)
    label2 = tk.Label(scheduleFrame, text="or inset link manually")
    label2.grid(row=1, column=3, columnspan=3)
    label3 = tk.Label(scheduleFrame, text="Join time")
    label3.grid(row=1, column=6)
    label4 = tk.Label(scheduleFrame, text="People less than")
    label4.grid(row=1, column=7)
    label5 = tk.Label(scheduleFrame, text="/ Leave time")
    label5.grid(row=1, column=8)

    btnAdd = tk.Button(scheduleFrame, text="Add", width=6, height=1, font=("Kefa", 7), command=runCreateSchedule)
    btnAdd.grid(row=2, column=9, padx=5, sticky="e")

    # Saved Meetings frame widgets
    savedFrame = tk.Frame(scheduleFrame, width=650, height=100)
    savedFrame.grid(row=999, column=0, columnspan=9, pady=20, padx=2, sticky="w") # 999 so it will always be below all the rows
    
    label6 = tk.Label(savedFrame, text="Save Meetings for repeated use", font=("Kefa", 12))
    label6.grid(row=0, column=0, pady=10, columnspan=2, sticky="w")
    label7 = tk.Label(savedFrame, text="Title")
    label7.grid(row=1, column=0)
    label8 = tk.Label(savedFrame, text="Meeting link (if link is temporary)")
    label8.grid(row=1, column=1)

    savedAdd = tk.Button(savedFrame, text="Add", width=6, height=1, font=("Kefa", 7), command=runCreateSaved)
    savedAdd.grid(row=2, column=2, rowspan=2, sticky="n")

    savedSave = tk.Button(savedFrame, text="Save", width=6, height=1, font=("Kefa", 7), command=saveSavedFields)
    savedSave.grid(row=2, column=3, padx=2, rowspan=2, sticky="n")

    start = tk.Button(savedFrame, width=24, text="Start scheduled Meeting", command=runDriver)
    start.grid(row=2, column=4, rowspan=2, sticky="ns", padx=10)

    # Check whether saved_meetings.json contains saved/scheduled Meetings and if first empty entry needs to be created
    try:
        with open('saved_meetings.json', 'r') as file:
            data = json.load(file)
            if (data["saved"][0]["title"] != "" or data["saved"][0]["link"] != ""):
                pass
            else:
                createSaved = CreateField(savedCount)
                createSaved.createSaved(savedFrame, savesList)
                geometryY += 20
            if (data["scheduled"][0]["saved"] != "" or data["scheduled"][0]["link"] != ""):
                pass
            else:
                createSchedule = CreateField(scheduleCount)
                createSchedule.createSchedule(scheduleFrame, schedulesList)
                geometryY += 30
    except:
        createSaved = CreateField(savedCount)
        createSaved.createSaved(savedFrame, savesList)
        geometryY += 20
        createSchedule = CreateField(scheduleCount)
        createSchedule.createSchedule(scheduleFrame, schedulesList)
        geometryY += 30

    language()

    fillScheduledFields()

    fillSavedFields()
