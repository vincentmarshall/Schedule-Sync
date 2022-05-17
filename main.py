import time
import datetime
import create_event
import re
import list_events

from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from datetime import datetime
import chromedriver_autoinstaller

chromedriver_autoinstaller.install()

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)


driver = webdriver.Chrome()

driver.get('https://t11.ultipro.ca/')

print('Please enter your username')
username = input()
print('Please enter your password')
password = input()

id_box = driver.find_element(By.ID, 'ctl00_Content_Login1_UserName')
id_box.send_keys(username)



pass_box = driver.find_element(By.ID, 'ctl00_Content_Login1_Password')
pass_box.send_keys(password)

login_box = driver.find_element(By.ID, 'ctl00_Content_Login1_LoginButton')
login_box.click()

time.sleep(5)

driver.get('https://t11.ultipro.ca/Customs/CNPLX/Pages/View/WorkBrainSSO.aspx?USParams=PK=ESS!MenuID=81!PageRerId=5000005!ParentRerId=81!wbsso=employee!environment=production')

schedule_box = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.LINK_TEXT, "Work Schedule")))
schedule_box.click()


page = driver.page_source

soup = BeautifulSoup(page, 'lxml')

gdp_table = soup.find("table", attrs={"class": "etmScheduleTable"})
gdp_table_data = gdp_table.tbody.find_all("tr")  # contains 2 rows

headings = []

for td in gdp_table_data[0].find_all("tr"):

    headings.append(td.b.text.replace('\n', ' ').strip())

print(headings)

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


soup = BeautifulSoup(page, 'lxml')

gdp_table = soup.find("table", attrs={"class": "etmScheduleTable"})
gdp_table_data = gdp_table.tbody.find_all("td", "calTD-NoShift")  # contains 2 rows
gdp_table_data_sched = gdp_table.tbody.find_all("td", "calendarCellRegularFuture")  

yearFind = soup.find("span", attrs={"class" : "pageTitle"})

dateList = []
workingList = []
testList = []

working = list_events.main()

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

for k in gdp_table_data_sched:
    timeSched = k.find('span', {'class' : 'calendarCellRegularFuture etmNoBorder'})
    posSched = k.find('span', {'class' : 'calendarTextSchedDtlFuture'})
    sched = k.find('span', {'class' : 'calendarDateNormal'})

    lastVal = re.sub('\D', '', timeSched.text.strip())

    timeChunk = [lastVal[i:i+2] for i in range(0, len(lastVal), 2)]

    startValHr = timeChunk[0]
    startValMn = timeChunk[1]
    endValHr = timeChunk[2]
    endValMn = timeChunk[3]

    timeVal = str(yearFind.text).split()
    monthVal = month_string_to_number(timeVal[0])
    yearVal = timeVal[1]

    if workingList:
        for value in workingList:
            newDate1 = datetime.strptime(value,'%d').strftime('%d')
            newDate2 = datetime.strptime(sched.text.strip(),'%d').strftime('%d')
            print(newDate1)
            print(newDate2)
            if newDate2 in workingList:
                print("event in calendar already, skipping")
            else:
                print("not in sched, creating")
                create_event.main(sched.text, monthVal, yearVal, startValHr, startValMn, endValHr, endValMn, posSched.text)
    else:
        print("no events found, creating all")
        create_event.main(sched.text, monthVal, yearVal, startValHr, startValMn, endValHr, endValMn, posSched.text)




