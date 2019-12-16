from selenium import webdriver
from datetime import datetime
import csv
import math
import sys
import time
import os
current_dir = os.getcwd()
input_dir = input("enter the directory\n")
if len(input_dir.strip()) != 0:
    current_dir = input_dir
urllists = ['https://www.wsj.com/market-data/bonds/tips','https://www.wsj.com/market-data/bonds/treasuries']
xpaths = ['//*[@id="root"]/div/div/div/div[2]/div/div/div[3]/table','//*[@id="root"]/div/div/div/div[2]/div/div/div[4]/div/table']
print(len(sys.argv))
print("coming here -------")
if len(sys.argv) == 2:
    folder = sys.argv[1].rstrip("/")
else:
    folder = ""
for idx in range(len(urllists)):

    url = urllists[idx]
    xpath = xpaths[idx]

    # Instantiate the WebDriver object for Chrome
    # uncomment the following line if using Linux
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver')

    # the following is for Windows. Replace the string after r with the path of your chromedriver
    driver = webdriver.Chrome(r"/users/jaypatel/downloads/chromedriver")
   
    # Direct the driver to the url
    driver.get(url)
    time.sleep(5)
    table = driver.find_element_by_xpath(xpath)

    rows_to_write = list()

    headings = table.find_elements_by_tag_name("th")

    templist = []
    for heading in headings:
        templist.append(heading.text)
    rows_to_write.append(templist)

    rows = table.find_elements_by_tag_name( "tr") # get all of the rows in the table
    required_date = driver.find_element_by_class_name("WSJBase--card__timestamp--2xDXNOQk ").text
    date_object = datetime.strptime(required_date, "%A, %B %d, %Y")
    required_date_string = date_object.strftime("%Y-%m-%d")
    csv_name = folder+"/"+required_date_string+"-"+url.split('/')[-1]+".csv"

    for row in rows:
        templist = []
        elements = row.find_elements_by_tag_name("td")
        if len(elements) == 0:
            continue
        elements = [x.text for x in elements]
        format_date = elements[0]
        if idx == 0:
            frac, whole = math.modf(float(elements[2]))
            elements[2] = str(whole + frac/32)
            frac, whole = math.modf(float(elements[3]))
            elements[3] = str(whole + frac/32)
            format_date = datetime.strptime(elements[0],'%Y %b %d').strftime('%m/%d/%Y')
        templist.append(format_date)
        templist += elements[1:]
        rows_to_write.append(templist)

    with open(current_dir+csv_name, "w+", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows_to_write)

### extract treasury bills
url = urllists[1]
xpath = xpaths[1]
driver.get(url)
time.sleep(5)
label = "Treasury Bills";
driver.find_element_by_xpath("//button[contains(.,'" + label + "')]").click()
table = driver.find_element_by_xpath(xpath)
rows_to_write = list()
headings = table.find_elements_by_tag_name("th")


templist = []
for heading in headings:
    templist.append(heading.text)
rows_to_write.append(templist)

required_date = driver.find_element_by_class_name("WSJBase--card__timestamp--2xDXNOQk ").text
date_object = datetime.strptime(required_date, "%A, %B %d, %Y")
required_date_string = date_object.strftime("%Y-%m-%d")
csv_name = folder+"/"+required_date_string+"-"+url.split('/')[-1]+"-tbill.csv"

rows = table.find_elements_by_tag_name( "tr")

for row in rows:
    templist = []
    elements = row.find_elements_by_tag_name("td")
    if len(elements) == 0:
        continue
    elements = [x.text for x in elements]
    format_date = elements[0]
    if idx == 0:
        frac, whole = math.modf(float(elements[2]))
        elements[2] = str(whole + frac/32)
        frac, whole = math.modf(float(elements[3]))
        elements[3] = str(whole + frac/32)
        format_date = datetime.strptime(elements[0],'%Y %b %d').strftime('%m/%d/%Y')
    templist.append(format_date)
    templist += elements[1:]
    rows_to_write.append(templist)

with open(current_dir+csv_name, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows_to_write)

