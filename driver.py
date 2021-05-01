from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import json
from datetime import datetime
import random

def getData(option):
    with open('config.json') as file:
        data = json.load(file)
        var = data[option]
    return var

def randomSleep(min, max):
    sleep(random.uniform(min, max))

def autoLogin(driver):
    try:
        gmail = getData("gmail")
        password = getData("password")
        gmail_field = driver.find_element_by_xpath('//*[@id="identifierId"]')
        gmail_field.send_keys(gmail)
        randomSleep(0, 1)
        driver.find_element_by_xpath('//*[@id="identifierNext"]/div/button/div[2]').click()
        randomSleep(1, 3)
        try:
            password_field = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')
            password_field.send_keys(password)
            randomSleep(0, 1)
            driver.find_element_by_xpath('//*[@id="passwordNext"]/div/button/div[2]').click()
        except:
            print("Failed to login, (most likely because that client was directed to another website)")
    except:
        print("Failed to login")

def raiseHand(driver, handRaised):
    try:
        hands = driver.find_elements_by_xpath("XB7ZFf")
        print(len(hands))
        handCount = len(hands)

        for i in hands:
            if (i.get_attribute("aria-hidden") == "true"):
                handCount += 1
        limit = getData("hands")

        if (handCount > limit and handRaised == False):
            print("RAISE HAND")
            handRaised = True
            return handRaised

        elif (handCount < limit and handRaised):
            print("LOWER HAND")
            handRaised = False
            return handRaised
    except:
        print("Failed to find hands elements")

def joinedInMeeting(application, driver, ppl, leave_time=None, fromScheduler=None):

    # Check if scheduled Meeting start has given number of people
    if (ppl == None):
        ppl = 9999

    canLeave = False
    switched_to_tab_1 = False
    while (True):

        # Check for leave time if Meeting is started by scheduler
        if (fromScheduler != None and leave_time != None):
            now = datetime.now()
            print("Time now: " + now.strftime("%H:%M:%S") + ", Leave time: " + leave_time)
            if (leave_time < now.strftime("%H:%M:%S")):
                randomSleep(2, 3)
                driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[9]/div[2]/div[2]/div').click()
                print("Quitted Meeting successfully by reaching time")
                return 2

        # Raise hand
        hand = getData("raise_hand")
        if (hand):
            handRaised = False
            handRaised = raiseHand(driver, handRaised)

        tabs = 0
        randomSleep(1, 3)
        try:
            tabs = len(driver.window_handles)
            element = driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[1]/div[3]/div/div[2]/div[1]/span/span/div/div/span[2]') #rKOYsc
            people = int(element.get_attribute('innerHTML'))
            print("People: " + str(people) + " | Tabs: " + str(tabs) + " | Can leave: " + str(canLeave))

            if (people > ppl):
                canLeave = True
                continue

            elif (people < ppl and canLeave):
                print("People: " + str(people) + ", quitting the meeting...")
                driver.find_element_by_xpath('//*[@id="ow3"]/div[1]/div/div[9]/div[3]/div[9]/div[2]/div[2]/div').click()
                
                if (fromScheduler):
                    return 1
                else:
                    application(app_message="Successfully quitted", finished=0)
                break
        except:
            if (tabs > 1):
                switched_to_tab_1 = False
                continue
            elif (tabs == 1 and switched_to_tab_1 == False):
                randomSleep(0, 1)
                driver.switch_to.window(driver.window_handles[0])
                print("Switched to tab 0")
                switched_to_tab_1 = True
            elif (tabs == 1 and switched_to_tab_1):
                continue
            else:
                # Means the window was closed manually
                driver.quit()
                return 4 # Return as failed (chrome closed)

def checkIfMutedVideo(driver):

    try: # Join button
        driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span')
    except: # Means script wasn't on joining screen
        return

    try:
        randomSleep(0, 1)
        mic = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[1]/div/div/div')
        if (mic.get_attribute("data-is-muted") == "false"):
            mic.click()
            print("Disabled microphone")
        else:
            print("Already disabled microphone")
        randomSleep(0, 1)
    except:
        print("Failed to find microphone button")
        driver.refresh()
        randomSleep(3, 6)
        pass
    try:
        randomSleep(0, 1)
        video = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[1]/div[1]/div/div[4]/div[2]/div/div')
        if (video.get_attribute("data-is-muted") == "false"):
            video.click()
            print("Disabled video")
        else:
            print("Already disabled video")
        randomSleep(0, 1)
    except:
        print("Failed to find video button")
        driver.refresh()
        randomSleep(3, 6)
        pass

def driver(application, timer=None):
    try:
        ppl = getData("people_amount_to_leave")

        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("--disable-extensions")
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

        print("Exit when there are less people than: " + str(ppl))

        # Driver logic
        if (timer != None):
            # When user sets a timer
            print("Starting timer")
            while(True):

                # Check if driver still exists (isn't closed)
                try:
                    _getDriver = driver.find_element_by_xpath("/html") # _ ignores unused var
                except:
                    break

                now = datetime.now()
                time = now.strftime("%Y-%m-%d %H:%M:%S")
                time2 = now.strftime("%Y-%m-%d")
                current_time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
                future = datetime.strptime(time2 + " {}:{}:{}".format(timer[0] + timer[1], timer[3] + timer[4], timer[6] + timer[7]), "%Y-%m-%d %H:%M:%S")
                current = str(future - current_time)
                if ("-" in current):
                    split = current.split() # Split string and get HH:MM:SS only
                    current = split[2]

                if (current == "0:00:00"):
                    print("Trying to join...")
                    break

            url = ""
            refreshCount = 0

            while (True):
                driver.switch_to.window(driver.window_handles[0])
                randomSleep(4, 6)
                print("Refresh count: " + str(refreshCount))
                try:
                    # Tries to find the "This meeting hasn't started yet" screen first, in case it was directed there
                    element = driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[1]')
                    if ("started yet" in element.get_attribute('innerHTML')):
                        print("Found 'This meeting hasn't started yet' screen")
                        randomSleep(2, 3)
                        driver.get(url)
                        randomSleep(1, 3)
                        driver.switch_to.window(driver.window_handles[0])
                        driver.close()
                        randomSleep(1, 3)
                        driver.switch_to.window(driver.window_handles[0])
                        randomSleep(2, 3)
                        print("Successfully navigated to new tab")
                except:
                    pass
                try:
                    url = driver.current_url
                    driver.refresh()
                    #driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div[2]/div[3]/div[1]/button/div[2]').click()
                    refreshCount += 1
                    randomSleep(5, 6)
                    checkIfMutedVideo(driver)
                    randomSleep(0, 1)
                    driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span').click()
                    randomSleep(2, 5)
                    print("Joining meeting from 1st exception")
                    joinedInMeeting(application, driver, ppl)
                except:
                    try:
                        checkIfMutedVideo(driver)
                        randomSleep(0, 1)
                        driver.find_element_by_xpath('//*[@id="yDmH0d"]/c-wiz/div/div/div[9]/div[3]/div/div/div[2]/div/div[1]/div[2]/div/div[2]/div/div[1]/div[1]/span/span').click()
                        print("Joining meeting from 2nd exception")
                        joinedInMeeting(application, driver, ppl)
                    except:
                        print("Error joining meeting from both exceptions")
        else:
            joinedInMeeting(application, driver, ppl)
    except:
        print("Closed Chrome")
        if (getData("start_app_on_chrome_close")):
            application(app_message="Closed Chrome")