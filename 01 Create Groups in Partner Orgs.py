"""
Author: FellowBeginner
Blog: https://fellowbeginners.wordpress.com/

Automation Script: Create groups in partner organisations in CPQ instance
Application: Oracle CPQ
IDE: Python-Selenium

Prerequisite:
Account User: Admin access with ProxyLogin
"""

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

cpqInstanceName = "SiteName"
username = "username"
password = "password"
chromedriverPath = "\driver\chromedriver.exe" #path for selenium chromium driver

#Basic URL used
url = "https://" + cpqInstanceName + ".bigmachines.com"
proxylogout = url + "/logout.jsp?proxy_logout=true&amp;_bm_trail_refresh_=true"
exceptionListOfCompanies = []

def createGroup(companyName, groupName, groupVarName, addAllUsers = False):
    if (len(driver.find_elements_by_xpath("//td[text()='" + groupVarName + "']")) == 0):
        driver.find_element_by_xpath("//a[@id='add']").click()
        time.sleep(5)
        element = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "group-name|input")))
        driver.find_element_by_id("group-name|input").send_keys(groupName)
        time.sleep(3)
        driver.find_element_by_id("variable-name|input").send_keys(groupVarName)
        time.sleep(3)
        if(addAllUsers): #Click >> arrow button to add all users to the group
            driver.find_element_by_id("all-users-right-btn_oj2|text").click()  # select all users
            time.sleep(3)
        driver.find_element_by_id("save-btn_oj0|text").click()
        time.sleep(5)
        print("Group "+groupName+" added for " + companyName)
    else:
        print("Group "+groupName+" already exists for " + companyName)

# START
driver = webdriver.Chrome(chromedriverPath)
driver.implicitly_wait(1)
driver.maximize_window()
driver.get("https://" + cpqInstanceName + ".bigmachines.com/admin/company/list_external_companies.jsp")
driver.find_element_by_id("username").send_keys(username)
driver.find_element_by_id("psword").send_keys(password)
driver.find_element_by_id("log_in").click()

pagesCountStr = driver.find_element_by_xpath("//table[3]//td[@class='bottom-bar']").text
pagesCount = int(pagesCountStr.split(": ")[1]) // 100

# Skip the pages
noOfPagesToSkip = 0;
'''
for j in range(noOfPagesToSkip):
    ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.END).key_up(Keys.CONTROL).perform()
    driver.find_element_by_id("next_iter_link").click()
    time.sleep(5)
'''

# Extract all the partner orgs available in the page
for i in range(pagesCount + 1):
    print("pageNo :", i)

    if(i<noOfPagesToSkip):
        continue
    elif(i==noOfPagesToSkip):
        for j in range(i + 1):
            ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.END).key_up(Keys.CONTROL).perform()
            driver.find_element_by_id("next_iter_link").click()
            time.sleep(5)

    count = 1
    list_of_companies = [[x.get_attribute('href'), x.text] for x in
                         driver.find_elements_by_xpath("//td[1]//a[@class='list-field']")]
    list_of_companiesProxy = [x.get_attribute('href') for x in
                              driver.find_elements_by_xpath("//td[8]//a[@class='list-field']")]

    for company, proxyLink in zip(list_of_companies, list_of_companiesProxy):
        companyID = company[0].replace(
            "https://" + cpqInstanceName + ".bigmachines.com/admin/company/edit_external_company.jsp?id=", "")
        companyName = company[1]
        print(count, companyName)

        # Check if the partners arepresent in exceptionList
        if companyID not in exceptionListOfCompanies:
            # List of Users: print(url+"/admin/users/list_users.jsp?company_id="+companyID)
            # ProxyLogin: print(proxyLink)
            driver.get(proxyLink)
            time.sleep(2)
            driver.get(url + "/admin/groups/list_groups.jsp?_bm_trail_refresh_=true")
            time.sleep(2)

            createGroup(companyName, "User", "user",True)
            createGroup(companyName, "Manager", "manager")

            driver.get(proxylogout)
            time.sleep(5)
        else:
            print("This company " + companyName + " is in exclusion list..")

        count = count + 1

    if (count > 100):
        for j in range(i + 1):
            ActionChains(driver).key_down(Keys.CONTROL).key_down(Keys.END).key_up(Keys.CONTROL).perform()
            driver.find_element_by_id("next_iter_link").click()
            time.sleep(5)
