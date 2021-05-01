# Made by Kristjan Tiido aka Hullumeelne
# Do not distribute yourself

from selenium import webdriver
from time import sleep
import tkinter as tk
import json
from driver import driver
import subprocess
from scheduler import scheduler

# Get data from config.json
def getData(option):
    with open('config.json') as file:
        data = json.load(file)
        var = data[option]
    return var

def saveData(data1=None, option1=None, data2=None, option2=None):
    with open('config.json', 'r') as file:
            data = json.load(file)
            with open('config.json', 'w') as file2:
                if (data1 != None):
                    data[option1] = data1
                if (data2 != None):
                    data[option2] = data2
                json.dump(data, file2, indent=4)

def application(app_message = None, message_color = None, alert_box = None, finished = None):
      
    eng = ["Leave when number of Meet participants is less than: ", "Change", "Saved", "Invalid value", "Set time to start a Meeting (optional):",
        "SET", "UNSET", "Joining Google Meeting in - (press Start and", "log-in to Google now)", "Invalid time value, format: hh:mm:ss", "ᐅ Advanced settings",
        "ᐁ Advanced settings", "Meet scheduler", "    Start Meet    ", "•  Enable auto-fill on Chrome start", "SAVE", "•  Open this window when Chrome is closed",
        "•  Number of people to raise the hand with"]

    est = ["Lahku Meetist, kui osavõtjaid on vähem kui: ", "Muuda", "Salvestatud", "Vigane number", "Kellaaeg Meetiga liitumiseks (valikuline):", "SISESTA",
        "TÜHISTA", "Liitumine Google Meetiga: - (vajuta Start ja", "logi Google'isse sisse)", "Vigane kellaaeg, vorming: hh:mm:ss", "ᐅ Täpsemad seaded", "ᐁ Täpsemad seaded",
        "Meet planeerija", "   Alusta Meeti   ", "•  Automaatne täitmine Chrome käivitamisel", "SALV.", "•  Ava see aken, kui Chrome sulgeb", "•  Tõsta Meetis käsi kindla arvu inimestega"]

    ppl = getData("people_amount_to_leave")
    root = tk.Tk()
    root.title("Google Meet automated tool")
    root.geometry("360x200")
    root.minsize(360, 200)
    root.maxsize(360, 200)

    root.iconphoto(True, tk.PhotoImage(file='C:/Users/krist/Desktop/Python projektid/Google Meet automated exit tool/icon.png'))

    def saveFields(gmail, password):
        saveData(str(gmail), "gmail", str(password), "password")

    def runDriver(timer=None):
        # Destroy GUI app
        root.withdraw()
        # Run driver
        driver(application, timer) # Pass application method as argument so driver.py can use it

        exit()

    def runScheduler():
        from scheduler import runScheduler
        runScheduler(application, root, getData("language"))

    def finishWindow(finishedList=None, single=None):
        window = tk.Toplevel()
        window.title("Finish report - Google Meet automated tool")
        geometryY = 100
        window.geometry("400x" + str(geometryY))
        if (single != None):
            label = tk.Label(window, text=single)
            label.pack()
        elif (finishedList != None):
            rowCount = 0
            for i in finishedList:
                label = tk.Label(window, text="Meeting status: ")
                label.grid(row=rowCount, column=0, pady=5, sticky="w")
                status = tk.Label(window, text=i[1], fg=i[2])
                status.grid(row=rowCount, column=1, sticky="w")
                title = tk.Label(window, text="(" + i[0] + ")")
                title.grid(row=rowCount, column=2, sticky="w")
                rowCount += 1
                geometryY += 20
                window.geometry("400x" + str(geometryY))

    def expandApp():
        langApp = getData("language")
        if (langApp == "english"):
            lang = eng
        elif (langApp == "estonia"):
            lang = est

        root.minsize(360, 450)
        root.maxsize(360, 450)
        root.geometry("360x450")
        createOptions()
        advanced.config(text=lang[11])
        advanced.config(command=shrinkApp)

    def shrinkApp():
        langApp = getData("language")
        if (langApp == "english"):
            lang = eng
        elif (langApp == "estonia"):
            lang = est

        root.minsize(360, 200)
        root.maxsize(360, 200)
        root.geometry("360x200")
        advanced.config(text=lang[10])
        advanced.config(command=expandApp)

    def createOptions(returnFieldData=None):
        def toggleOption(option, label):
            with open('config.json', "r") as file:
                data = json.load(file)
                if (data[option]):
                    label.config(state=tk.DISABLED)
                    data[option] = False
                    with open('config.json', "w") as file2:
                        json.dump(data, file2, indent=4)
                else:
                    label.config(state=tk.NORMAL, fg="green")
                    data[option] = True
                    with open('config.json', "w") as file2:
                        json.dump(data, file2, indent=4)

        optionsFrame = tk.Frame(root, height=300, width=500)
        optionsFrame.place(x=10, y=210)

        # Widgets in optionsFrame
        langApp = getData("language")

        if (langApp == "estonia"):
            lang = est
        if (langApp == "english"):
            lang = eng

        label1 = tk.Label(optionsFrame, text=lang[14])
        label1.grid(row=0, column=0, pady=10, padx=65, sticky="w", columnspan=6)
        input1 = tk.Entry(optionsFrame)
        input1.grid(row=1, column=0, columnspan=2, sticky="w")
        gmail, password = getData("gmail"), getData("password")
        input1.insert(0, gmail)
        input2 = tk.Entry(optionsFrame, show="*")
        input2.grid(row=1, column=2, padx=2, columnspan=2)
        input2.insert(0, password)
        toggle1 = tk.Button(root, text="ON/OFF", command=lambda: toggleOption("autofill", label1))
        toggle1.place(x=10, y=218, height=25, width=60)
        save = tk.Button(root, text=lang[15], command=lambda: saveFields(input1.get(), input2.get()))
        save.place(x=300, y=252, height=23, width=55)
        if (langApp == "estonia"):
            save.config(font=("Kefa", 9))
        elif (langApp == "english"):
            save.config(font=("Kefa", 9))

        label2 = tk.Label(optionsFrame, text=lang[16])
        label2.grid(row=2, column=0, padx=65, pady=10, columnspan=6, sticky="w")
        toggle2 = tk.Button(root, text="ON/OFF", command=lambda: toggleOption("start_app_on_chrome_close", label2))
        toggle2.place(x=10, y=283, height=25, width=60)

        label3 = tk.Label(optionsFrame, text=lang[17])
        label3.grid(row=3, column=0, padx=65, pady=2, columnspan=10, sticky="w")
        toggle3 = tk.Button(root, text="ON/OFF", command=lambda: toggleOption("raise_hand", label3))
        toggle3.place(x=10, y=318, height=25, width=60)

        langButton = tk.Button(root, text="", command=lambda: language(startup=False))
        langButton.place(x=10, y=415, width=60, height=23)

        if (langApp == "english"):
            langButton.config(text="ENG")
        elif (langApp == "estonia"):
            langButton.config(text="EST")
        

        def assignOptions(option, label):
            # Assign values to options from config.json options are created
            with open('config.json', "r") as file:
                    data = json.load(file)
                    if (data[option]):
                        label.config(state=tk.NORMAL, fg="green")
                    else:
                        label.config(state=tk.DISABLED)
        
        assignOptions("autofill", label1)
        assignOptions("start_app_on_chrome_close", label2)
        assignOptions("raise_hand", label3)
        
    def changePeople():
        lang = getData("language")
        # Check for language
        if (lang == "english"):
            text1 = eng[3]
            text2 = eng[2]
            text3 = eng[0]
        else:
            text1 = est[3]
            text2 = est[2]
            text3 = est[0]
        userInput = peopleInput.get()
        valid = "1234567890"
        # Error handlers
        if (userInput != ""):
            for i in userInput:
                if (not i in valid or userInput[0] == "0"):
                    labelError = tk.Label(root, text=text1, fg="red", anchor="w")
                    labelError.place(x=150, y=28, width=100, height=20)
                    labelError.after(2000, labelError.destroy)
                    return

            labelSucc = tk.Label(root, text=text2, fg="green")
            labelSucc.place(x=150, y=28)
            labelPeople.config(text=text3 + str(userInput))
            labelSucc.after(2000, labelSucc.destroy)
            peopleInput.delete(0, tk.END)
            
            # Change data in config.json
            with open('config.json', "r") as file:
                data = json.load(file)
                data["people_amount_to_leave"] = int(userInput)
                with open('config.json', "w") as file2:
                    json.dump(data, file2, indent=4)
                    print("Number of participants updated to: " + userInput)

    def setTimer():
        userInput = timerInput.get()
        language = getData("language")
        if (language == "english"):
            lang = eng
        elif (language == "estonia"):
            lang = est
        labelTimerError = tk.Label(root, text=lang[9], fg="red")
        # Error handlers
        valid = "1234567890:"
        for i in userInput:
            if (i in valid):
                continue
            else:
                labelTimerError.place(x=5, y=90)
                labelTimerError.after(5000, labelTimerError.destroy)
                print("Invalid time value")
                return
        if (userInput != "" and len(userInput) == 8):
            if (userInput[2] == ":" and userInput[5] == ":" and (int(userInput[0] + userInput[1]) < 24) and (int(userInput[3] + userInput[4]) < 60) and (int(userInput[6] + userInput[7]) < 60)):

                from datetime import datetime
                from threading import Thread

                labelTimerStarted = tk.Label(root, text=lang[7], fg="green")
                labelTimerStarted.grid(row=3, column=0, padx=5, columnspan=3, sticky="w")
                labelTimerStarted2 = tk.Label(root, text=lang[8], fg="green")
                labelTimerStarted2.grid(row=4, column=0, padx=5, columnspan=1, sticky="w")

                def clock():
                    while(True):
                        sleep(1)
                        now = datetime.now()
                        time = now.strftime("%Y-%m-%d %H:%M:%S")
                        time2 = now.strftime("%Y-%m-%d")
                        current_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                        future = datetime.strptime(time2 + " {}:{}:{}".format(userInput[0] + userInput[1], userInput[3] + userInput[4], userInput[6] + userInput[7]), "%Y-%m-%d %H:%M:%S")
                        current = str(future - current_time)
                        if ("-" in current):
                            # Split string and get HH:MM:SS only
                            split = current.split()
                            current = split[2]
                        print(current)

                        try:
                            if (language == "english"):
                                text1 = "Joining Google Meeting in "
                                text2 = " (start Chrome and"
                            elif (language == "estonia"):
                                text1 = "Liitumine Google Meetiga: "
                                text2 = " (vajuta Start ja"

                            labelTimerStarted.config(text=text1 + str(current) + text2)
                        except:
                            return

                Thread(target=clock, daemon=True).start() # if daemon=True, then this thread will terminate when the main thread (application) is closed
                def unsetTimer():
                    exit()
                print("Started clock")
                buttonStart.config(command=lambda: runDriver(userInput))
                buttonSetTimer.config(text=lang[6], command=unsetTimer)
                dummy.destroy()
                return
        labelTimerError.place(x=5, y=90)
        labelTimerError.after(5000, labelTimerError.destroy)
        print("Invalid timer value")

    # Widgets in root
    labelPeople = tk.Label(root, width=48, anchor="w")
    labelPeople.grid(row=0, column=0, columnspan=3, padx=5, pady=3)

    peopleInput = tk.Entry(root, width=8)
    peopleInput.grid(row=1, column=0, padx=10, sticky="w")

    buttonChange = tk.Button(root, command=changePeople)
    buttonChange.place(x=78, y=28, height=23, width=60)

    labelTimer = tk.Label(root)
    labelTimer.grid(row=2, column=0, padx=5, pady=10, columnspan=3, sticky="w")

    timerInput = tk.Entry(root, width=8)
    timerInput.grid(row=2, column=2, sticky="w", padx=2)
    
    buttonSetTimer = tk.Button(root, command=setTimer)
    buttonSetTimer.place(x=305, y=60, height=23, width=50)

    dummy = tk.Label(root, text="                                   ")
    dummy.grid(row=3, column=0)
    dummy2 = tk.Label(root, text="                                   ")
    dummy2.grid(row=4, column=0)

    advanced = tk.Button(root, text="ᐅ Advanced settings", command=expandApp, borderwidth=0)
    advanced.place(x=10, y=165)
    advanced.config(font=("Kefa", 8))

    buttonScheduler = tk.Button(root, text="Meet scheduler", command=runScheduler)
    buttonScheduler.grid(row=5, column=0, columnspan=2, padx=15, pady=20, sticky="e")

    buttonStart = tk.Button(root, text="     Start Meet     ", command=runDriver)
    buttonStart.grid(row=5, column=0, columnspan=3, padx=3, pady=20, sticky="e")

    if (app_message != None):
        messageLabel = tk.Label(root, text=app_message, fg="green")
        messageLabel.place(x=5, y=100)
        messageLabel.after(8000, messageLabel.destroy)
        if (message_color != None):
            messageLabel.config(fg=message_color)
        
    if (alert_box != None):
        from tkinter import messagebox
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        tk.messagebox.showinfo(title="Google Meet automated tool", message="Left Google Meet successfully at " + current_time + ", at " + str(ppl) + " people.")

    if (finished != None):
        if (finished == 0):
            finishWindow(single="Meeting finished successfully")
        elif (finished != None):
            finishWindow(finishedList=finished)

    def language(startup):
        lang = getData("language")
        import tkinter.font as font
        def setEnglish():
            labelPeople.config(text=eng[0] + str(ppl))
            buttonChange.config(text=eng[1])
            labelTimer.config(text=eng[4])
            buttonSetTimer.config(text=eng[5], font=("Kefa", 9))
            advanced.config(text=eng[10])
            buttonScheduler.config(text=eng[12])
            buttonStart.config(text=eng[13])
            saveData("english", "language")
            print("Language: english")

        def setEstonia():
            #smallerFont = font.Font(size=8)
            labelPeople.config(text=est[0] + str(ppl))
            buttonChange.config(text=est[1])
            labelTimer.config(text=est[4])
            buttonSetTimer.config(text=est[5], font=("Kefa", 8))
            advanced.config(text=est[10])
            buttonScheduler.config(text=est[12])
            buttonStart.config(text=est[13])
            saveData("estonia", "language")
            print("Language: estonian")

        if (startup):
            if (lang == "english"):
                setEnglish()
            elif (lang == "estonia"):
                setEstonia()
        else:
            if (lang == "english"):
                setEstonia()
            elif (lang == "estonia"):
                setEnglish()

        createOptions()
        
    def close():
        root.destroy()
        print("Closed application")
        exit()

    language(startup=True)

    root.protocol("WM_DELETE_WINDOW", close)
    root.mainloop()

application()