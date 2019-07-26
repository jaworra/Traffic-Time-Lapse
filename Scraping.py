import time
import datetime
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime
import os
import numpy as np

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException


import cv2
print(cv2.__version__)
#exit(1)

def getScreenshot():
    _start = time.time()
    options = Options()
    options.add_argument("--headless") # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox') # # Bypass OS security model
    options.add_argument('start-maximized')
    options.add_argument('disable-infobars')
    options.add_argument("--disable-extensions")
    #other extensions
    #WINDOW_SIZE = "1920,1080"
    #options.add_argument("--window-size=%s" % WINDOW_SIZE)

    options.add_argument('start-maximized')

    driver = webdriver.Chrome(executable_path=r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

    currentDT = datetime.datetime.now()
    strNow = currentDT.strftime("%Y%m%d_%H%M_%S")
    strNow2 = currentDT.strftime("%H:%M %p")

    webSite=2 # 2 - This is my website of live incidents  1 - Google traffic


    if webSite == 1:
        driver.get('https://www.google.com/maps/@-27.5077927,152.9742909,10.5z/data=!5m1!1e1')
        #print ("currentDT")
        path='config/googleTraffic_'
        #saves the original image
        driver.save_screenshot(path+strNow+'.png')
        #path = "config/googleTraffic_'+strNow+'.png"

        #overwrite - with timestamp
        img = cv2.imread(path+strNow+'.png', 1)
        position = (10, (int)(img.shape[0]-10 ))

        font = cv2.FONT_HERSHEY_SIMPLEX
        font = cv2.FONT_HERSHEY_PLAIN
        #cv2.putText(img, strNow2, (10, 450), font, 2, (0, 255, 0), 2, cv2.LINE_AA)
        cv2.putText(img, strNow2, position, cv2.FONT_ITALIC, 0.8, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.imwrite(path+strNow+'.png', img)

    elif webSite  == 2:
        driver.get('https://public-test-road.s3-ap-southeast-2.amazonaws.com/RoadsOps-Live-Incidents.html')
        #wait for render....
        delay = 3  # seconds
        path = 'here_deckgl/deckglIncidents_'
        try:
            myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
            print("Page is ready!")
            driver.save_screenshot(path + strNow + '.png')

        except TimeoutException:
            print("Loading took too much time!")
            driver.save_screenshot(path + strNow + '.png')


        # saves the original image
        # path = "config/googleTraffic_'+strNow+'.png"

    _end = time.time()
    print(strNow)
    driver.quit()


print('Start Screenshot Application')
starttime=time.time()
while True:
    getScreenshot()
    tmeInterval = 300 #300 #60  #1200-20mins; 900-15mins; 600-10mins;300-5mins; 60-1min; 30-30secs;
    time.sleep(tmeInterval - ((time.time() - starttime) % tmeInterval))

exit(1)
