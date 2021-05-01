# Modified version of driver.py, for scheduler. Uses functions from driver.py

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from time import sleep
import json
from datetime import datetime
import random

from driver import randomSleep, checkIfMutedVideo, getData, autoLogin, joinedInMeeting

def getScheduledData():
    dataList = []
    try:
        with open('saved_meetings.json', 'r') as file:
            data = json.load(file)
            for i in data["scheduled"]:
                schedule = []
                schedule.append(i["saved"])
                schedule.append(i["link"])
                schedule.append(i["join_time"])
                schedule.append(i["people"])
                schedule.append(i["leave_time"])
                dataList.append(schedule)
        return dataList
    except: return False# Means no saved data yet

def getSavedData(title):
    with open('saved_meetings.json', 'r') as file:
        data = json.load(file)
        for i in data["saved"]:
            if (i["title"] == title):
                return i["link"]

def timer(application, driver, url, join_time, people, leave_time):
    print("Starting timer")
    while(True):
        sleep(1)
        now = datetime.now()
        time = now.strftime("%Y-%m-%d %H:%M:%S")
        time2 = now.strftime("%Y-%m-%d")
        current_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        future = datetime.strptime(time2 + " {}:{}:{}".format(join_time[0] + join_time[1], join_time[3] + join_time[4], join_time[6] + join_time[7]), "%Y-%m-%d %H:%M:%S")
        current = str(future - current_time)
        print(current)
        if (current == "0:00:00"):
            print("Trying to join...")
            info = attemptJoining(application, driver, url, people, leave_time)
            return info

def attemptJoining(application, driver, url, people, leave_time):
    refreshCount = 0
    firstRun = True
    resizeFailed = 0

    try:
        randomSleep(0, 1)
        driver.minimize_window()
        randomSleep(1, 3)
        driver.maximize_window()
        randomSleep(1, 3)
        firstRun = False
    except:
        return 4 # Means Chrome was closed manually and returns as a fail

    # Navigate to URL
    try:
        driver.get(url)
    except:
        print("Invalid URL or you closed Chrome, skipping meeting")
        return 5
    randomSleep(1, 3)

    while (True):

        # Avoid minimizing and maximizing the page twice
        if (firstRun == False):
            try:
                driver.minimize_window()
                randomSleep(1, 3)
                driver.maximize_window()
                randomSleep(1, 3)
            except:
                print("Failed resizing Chrome") # In case user resizes the window by hand and interrupts script resizing
                resizeFailed += 1
                if (resizeFailed > 2): # If script failes 3 times, then return fail
                    return 4

        # Check for leave time
        if (leave_time != None):
            now = datetime.now()
            print("Time now: " + now.strftime("%H:%M:%S") + ", Leave time: " + leave_time)
            if (leave_time < now.strftime("%H:%M:%S")):
                print("Couldn't join Meeting, quitted this attempt due to reaching leave time")
                return 3

        try:
            driver.switch_to.window(driver.window_handles[0])
        except: return 4 # Means Chrome was closed

        randomSleep(10, 25)
        print("Refresh count: " + str(refreshCount))
        try:
            # Tries to find the "This meeting hasn't started yet" screen first, in case it was directed there
            element = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[1]')
            if ("started yet" in element.get_attribute('innerHTML')):
                print("Found 'This meeting hasn't started yet' screen")
                randomSleep(1, 3)
                driver.get(url)
                randomSleep(5, 10)
        except:
            pass
        try:
            url = driver.current_url
            driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[1]').click() # Click random place to stay active
            randomSleep(1, 3)
            driver.refresh()
            #driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[3]/div[1]/button/div[2]').click()
            refreshCount += 1
            randomSleep(4, 6)
            checkIfMutedVideo(driver)
            randomSleep(0, 1)
            driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span').click()
            randomSleep(2, 5)
            print("Joining meeting from 1st exception")
            info = joinedInMeeting(application, driver, people, leave_time=leave_time, fromScheduler=True)
            return info
        except:
            try:
                checkIfMutedVideo(driver)
                randomSleep(1, 3)
                driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span').click()
                print("Joining meeting from 2nd exception")
                info = joinedInMeeting(application, driver, people, leave_time=leave_time, fromScheduler=True)
                return info
            except:
                print("Error joining meeting from both exceptions")

def driver(application):

    #try:
    opt = Options()
    opt.add_argument("--disable-infobars")
    opt.add_argument("--disable-extensions")
    opt.add_argument("--disk-cache-size=0")
    opt.add_experimental_option("prefs", { \
        "profile.default_content_setting_values.media_stream_mic": 1,
        "profile.default_content_setting_values.media_stream_camera": 1,
        "profile.default_content_setting_values.notifications": 1 
    })

    path = "C:/Users/krist/Desktop/Python projektid/Google Meet automated exit tool/chromedriver.exe"
    driver = webdriver.Chrome(chrome_options=opt, executable_path=path)
    driver.get('http://classroom.google.com/u') #http://localhost/Test%20site%20for%20amazon%20scraper/

    # Check for auto filling
    auto = getData("autofill")
    if (auto):
        autoLogin(driver)

    # Run Meetings
    schedulesList = getScheduledData()
    if (schedulesList == False):
        driver.quit()
        print("Couldn't start Meetings, no schedules yet")
        application(app_message="Failed to start Meetings: no schedules", message_color="red")

    finishedInfoList = []

    for i in schedulesList:

        name = "" # Can be URL or title for finishWindow final report
        url = ""
        join_time = i[2]
        leave_time = i[4]

        if (i[3] == ""):
            people = None
        else:
            people = int(i[3])

        if (i[4] == ""):
            leave_time = None

        if (i[0] != ""):
            name = i[0]
            url = getSavedData(i[0])

        if (i[1] != ""):
            name = "URL: " + i[1]
            url = i[1]

        print("Starting Meeting: " + name)
        print("Exit when there are less people than: " + str(people))

        info = timer(application, driver, url, join_time, people, leave_time)

        # Create list to send to application finishWindow final report
        subList = []
        subList.append(name)
        if (info == 1):
            subList.append("Meeting finished successfully by people")
            subList.append("green")
        if (info == 2):
            subList.append("Meeting finished successfully by time")
            subList.append("green")
        if (info == 3):
            subList.append("Failed to join Meeting")
            subList.append("red")
        if (info == 4):
            subList.append("Failed (Chrome was closed)")
            subList.append("red")
        if (info == 5):
            subList.append("Invalid URL or you closed Chrome")
            subList.append("red")

        finishedInfoList.append(subList)

    print(finishedInfoList)
    print("All Meetings finished")

    application(app_message="Meetings finished", finished=finishedInfoList)
    # except:
    #     print("Closed Chrome")
    #     if (getData("start_app_on_chrome_close")):
    #         application(app_message="Closed Chrome")