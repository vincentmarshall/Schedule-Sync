import selenium
import time
import datetime
import requests
import urllib.request
import create_event
import list_events
import re

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from datetime import datetime

def month_string_to_number(string):
    m = {
        'january': 1,
        'february': 2,
        'march': 3,
        'april':4,
         'may':5,
         'june':6,
         'july':7,
         'august':8,
         'september':9,
         'october':10,
         'november':11,
         'december':12
        }
    s = string.strip().lower()

    try:
        out = m[s]
        return out
    except:
        raise ValueError('Not a month')


fileopen = open("page.html", "rb")

contents = fileopen.read()

soup = BeautifulSoup(contents, 'lxml')

#print(soup.body.prettify())
gdp_table = soup.find("table", attrs={"class": "etmScheduleTable"})
gdp_table_data = gdp_table.tbody.find_all("td", "calTD-NoShift")  # contains 2 rows
gdp_table_data_sched = gdp_table.tbody.find_all("td", "calendarCellRegularFuture") 

yearFind = soup.find("span", attrs={"class" : "pageTitle"})

# Get all the headings of Lists
#, attrs={"class": "calTD-NoShift"}
#print(gdp_table_data)

print("---------------------------------------------")

#print(gdp_table_data_sched[0])

print("---------------------------------------------")

#date = gdp_table_data.find("td")

#schedule = gdp_table_data[1].find_all('span', {'class' : 'calCellData etmCalCellData'})

#for k in schedule:
#    print(k.text)

dateList = []
workingList = []
testList = []

working = list_events.main()
#working1 = str(working[0][0])

#testvar = [working1[i:i+8] for i in range(0, len(working1), 8)]

def every_second_element(values):
    second_values = []

    for index in range(1, len(values), 2):
        second_values.append(values[index])

    return second_values 

for value in working:

    value2 = value[0]

    for index in range(0, len(value2), 8):
        testList.append(value2[index : index + 8])

        i = 1

workingList = every_second_element(testList)

for h in gdp_table_data:
    dateNotSched = h.find_all('span', {'class' : 'calendarDateNormal'})
    sched = h.find_all('span', {'class' : 'calCellData etmCalCellData'})

    for values in dateNotSched:
        dateList.append(values.text.strip())
#    for values2 in sched:
#        workingList.append(values2.text)

for k in gdp_table_data_sched:
    timeSched = k.find('span', {'class' : 'calendarCellRegularFuture etmNoBorder'})
    posSched = k.find('span', {'class' : 'calendarTextSchedDtlFuture'})
    sched = k.find('span', {'class' : 'calendarDateNormal'})

    #for test in dateSched:
    lastVal = re.sub('\D', '', timeSched.text.strip())
    #print(lastval)

    timeChunk = [lastVal[i:i+2] for i in range(0, len(lastVal), 2)]

    startValHr = timeChunk[0]
    startValMn = timeChunk[1]
    endValHr = timeChunk[2]
    endValMn = timeChunk[3]

    #startVal = startVal[:2] + ":" + startVal[2:]
    #endVal = endVal[:2] + ":" + endVal[2:]

    #startVal = datetime.strptime(startVal,'%H:%M').strftime('%I:%M %p')
    #endVal = datetime.strptime(endVal,'%H:%M').strftime('%I:%M %p')

    #yearText = k.find('span', {'class' : 'pageTitle'})

    timeVal = str(yearFind.text).split()
    monthVal = month_string_to_number(timeVal[0])
    yearVal = timeVal[1]

    #print(sched.text)
    #print(monthVal)
    #print(yearVal)

    #print(startVal)
    #print(startValHr)
    #print(startValMn)
    #print(endValHr)
    #print(endValMn)
    #print(posSched.text)
    #print("-----------------")
    #print(workingList)
    #print(sched.text)
    #print("-----------------")
    #print(workingList)
    #print("=====================================")
    if workingList:
        for value in workingList:
            #print(value)
            #print("-------")
            #print(sched.text.strip())
            newDate1 = datetime.strptime(value,'%d').strftime('%d')
            newDate2 = datetime.strptime(sched.text.strip(),'%d').strftime('%d')
            print(newDate1)
            print(newDate2)
            if newDate2 in workingList:
                print("event in schedule already, skipping")
                #break
            else:
                print("not in sched, creating")
                create_event.main(sched.text, monthVal, yearVal, startValHr, startValMn, endValHr, endValMn, posSched.text)
    else:
        print("no events found, creating all")
        create_event.main(sched.text, monthVal, yearVal, startValHr, startValMn, endValHr, endValMn, posSched.text)
    #if int(sched.text) in workingList:
    #    print("Event already in calendar, skipping")
    #else:
    #    print("adding event on day " + sched.text)
    #create_event.main(sched.text, monthVal, yearVal, startValHr, startValMn, endValHr, endValMn, posSched.text)


#for i in range(3):
#    create_event.main()
#for values in val1:
 #   print(values.text)