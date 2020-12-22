"""
# TODO: catch wrong password or username error
"""

from selenium import webdriver
from win10toast import ToastNotifier
from selenium.webdriver.firefox.options import Options
import time
import sys


def getEmailData():
    #READING USER CREDENTIALS FROM COMMAND LINE
    if len(sys.argv)== 3:
        user=sys.argv[1]
        pswd=sys.argv[2]
    else:
        sys.exit("Not enough or too much command line arguments")

    #SETUP BROWSER (headless mode (available with options) -> no browser window pops up)
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Firefox(firefox_options=options)
    emailUrl = "https://webmail.uni-saarland.de/"
    driver.get(emailUrl)

    #ENTERING USER CREDENTIALS
    username = driver.find_element_by_xpath('//*[@id="username"]')
    username.send_keys(user)
    password = driver.find_element_by_xpath('/html/body/div[2]/div/form/center/table/tbody/tr[3]/td[2]/input')
    password.send_keys(pswd)

    #LOGIN
    loginBtn = driver.find_element_by_xpath('//*[@id="submit"]')
    loginBtn.click()

    #GET EMAIL DATA
    time.sleep(2)
    messages = driver.find_elements_by_class_name("msglist")
    emailData = []
    for message in messages:
        msg = message.text
        emailData.append(msg)
    #always 4 categories returned: name, title, time, size of mail seperated by \n character -> counter keeps track of categories
    splittedEmailData = emailData[0].split("\n")
    numberOfNewMails = len(splittedEmailData)/4
    counter = 0
    resetCounter = False
    senderList = []
    titleList = []
    timeList = []
    for i in range(len(splittedEmailData)):
        if counter == 0:
            senderList.append(splittedEmailData[i])
        elif counter == 1:
            titleList.append(splittedEmailData[i])
        elif counter == 2:
            timeList.append(splittedEmailData[i])
        elif counter == 3:
            resetCounter = True
        if resetCounter==False:
            counter = counter + 1
        else:
            counter = 0
            resetCounter = False

    #QUITTING THE DRIVER
    driver.quit()

    #CALLING THE NOTIFICATION FUNCTION
    notifyWindows(senderList, titleList, timeList, numberOfNewMails)


def notifyWindows(senderList, titleList, timeList, numberOfNewMails):
    #INITIALITING NOTIFICATION
    toaster = ToastNotifier()

    #NOTIFICATION DATA
    if numberOfNewMails==0:
        toaster.show_toast(title="Du hast "+str(numberOfNewMails)+" neue E-Mails:",msg="Heute gibt's nichts Neues :)")
    else:
        toaster.show_toast(title="Du hast "+str(numberOfNewMails)+" neue E-Mails:",msg="<-- coming up -->")
        msgString = ""
        for i in range(len(senderList)):
            msgString = msgString+"Sender:\t"+senderList[i]+"\nBetreff:\t"+titleList[i]+"\nWann:\t"+timeList[i]+"\n"
            toaster.show_toast(title="E-Mail "+str(i+1),msg=msgString,duration=10)
            msgString=""


def main():
    getEmailData()


main()
