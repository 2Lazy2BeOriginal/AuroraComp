from selenium import webdriver
from selenium.webdriver.common.by import By
import time

def getElement(courseIndex, colNum):
    # //*[@id="table1"]/tbody/tr[1]/td[5]
    xPath = '//*[@id="table1"]/tbody/tr[{}]/td[{}]'
    xPath = xPath.format(courseIndex, colNum)
    code = Web.find_element(By.XPATH, xPath)
    return code.text

def collectData(txtFile, sem):
    # number of search results, can use a forloop
    numResults = Web.find_element(By.XPATH, '// *[@id="results-terms"]/div/h3/span/span')
    numResults = numResults.text.split(" ")
    semCourseCount = int(numResults[0])
    pageIndex = 1
    courseCounted = 0
    while courseCounted < semCourseCount:
        # courseNum
        code = getElement(pageIndex, "4")
        # section
        section = getElement(pageIndex, "5")
        # num seats and waitlist
        seatsStr = getElement(pageIndex, "6").replace("\n", " ")
        seatsArr = seatsStr.split(" ")
        # print(seatsArr)
        enrollActual = seatsArr[0]
        if (enrollActual == "FULL:"):
            enrollActual = '0'
            capacity = seatsArr[3]
        else:
            capacity = seatsArr[2]
        # linked, MWF... end is the time, can prob use tokenizer
        # timeStr = getElement(pageIndex, "7")
        # timeArr = timeStr.split(" ")
        # print(timeStr)
        # startTime = timeArr[7]
        # endTime = timeArr[10]
        # prof names (some say primary so remove that)
        instructorArr = getElement(pageIndex, "8").split(" ")
        instructStr = ' '.join(instructorArr)
        instructStr = instructStr.replace('\n', " ")
        print(f'{code},{section},{capacity},{enrollActual},{instructStr.replace("(Primary)", "")}')
        toWrite = f'{code},{section},{capacity},{enrollActual},{instructStr.replace("(Primary)", "")},{sem}\n'
        txtFile.write(toWrite)
        # move to next course in the webpage
        pageIndex += 1
        courseCounted += 1
        if (courseCounted % 10 == 0):
            pageIndex = 1
            Web.find_element(By.XPATH, '//*[@id="searchResultsTable"]/div[2]/div/button[3]').click()
            time.sleep(0.5)

def moveAnotherYear():
    pass

Web = webdriver.Chrome()
def mainLoop(site, year):
    # open the main website
    Web.get(site)
    Web.find_element(By.XPATH, '//*[@id="classSearchLink"]').click()
    while True:
        x = input("enter file name")
        courseInfo = open(x, "w")
        collectData(courseInfo,x)
        courseInfo.close()

mainLoop("https://aurora-registration.umanitoba.ca/StudentRegistrationSsb/ssb/classSearch/classSearch", "2005")
