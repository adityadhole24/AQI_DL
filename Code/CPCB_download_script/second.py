'''
Created on 30-Dec-2019

@author: Aditya Dhole

This script downloads the dataset in xls format from the CPCB website, provided 6 arguments on the
command line.

Specify Command Line arguments as follows:
1- State (e.g. Uttar Pradesh)
2- City (e.g. Kanpur)
3- Monitoring Station (e.g. Nehru Nagar, Kanpur - UPPCB) 
4- Granularity of observations (e.g. 1 Hour)
5- Starting date of Observations (e.g. 15 March 2018, 24 February 2016)
6- Ending Date of Observations (same as 5)

---- NAMES OF CITIES, STATES, STATIONS TO BE ENTERED EXACTLY AS PER CPCB WEBSITE, INCLUDING CASE ----

'''
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import sys

chromedriver_location = "C:/Users/Aditya Dhole/OneDrive/Desktop/chromedriver.exe"
browser = webdriver.Chrome(chromedriver_location)
browser.get('https://app.cpcbccr.com/ccr/#/caaqm-dashboard-all/caaqm-landing/data')

desired_date=""
desired_month=""
desired_year=""

def fill_station(state_city_station):
    browser.find_element_by_xpath('//ng-select[@class="select-box ng-untouched ng-pristine ng-invalid"]').click()
    browser.find_element_by_xpath(  "//li[contains(text(), '" +state_city_station+"')]/.").click()


    

def fill_date(desired_date,desired_month,desired_year,from_to_selector):
    print(desired_date + "\t" + desired_month + "\t" + desired_year)
    browser.find_element_by_xpath('(//i[@class="fa fa-calendar"])['+from_to_selector+']').click()
    while browser.find_element(By.XPATH, '(//div[@class="month-year"])['+from_to_selector+']').text !=desired_month:
        browser.find_element_by_xpath('(//i[@class="wc-next fa fa-angle-right"])['+ from_to_selector+']').click()
    
    while browser.find_element_by_xpath('(//div[@class="year-dropdown"])['+from_to_selector+']').text != desired_year: #replace by xpath
        flag=0
        browser.find_element_by_xpath('(//i[@class="fa fa-angle-down"])['+from_to_selector+']').click()
        while flag==0 :
            list_of_years = browser.find_element(By.CLASS_NAME,"years-list-view").find_elements(By.TAG_NAME, "span")
            for year in list_of_years:
                if year.text == desired_year :
                    year.click()
                    flag=1
                    break
            if flag==0 :
                browser.find_element_by_xpath('//div[@class="fa fa-angle-left prev"]').click()

    if from_to_selector=='1' :
        rows_of_calendar= browser.find_elements_by_css_selector("#date > angular2-date-picker > div > div.wc-date-popover.banner-true > table.calendar-days > tbody > tr")  
    else :
        rows_of_calendar= browser.find_elements_by_css_selector("#date2 > angular2-date-picker > div > div.wc-date-popover.banner-true > table.calendar-days > tbody > tr")
        
    #date2 > angular2-date-picker > div > div.wc-date-popover.banner-true > table.calendar-days > tbody > tr
    date_found=0
    for row in rows_of_calendar :
        list_of_tds = row.find_elements(By.TAG_NAME, "td")
       
        for col in list_of_tds :
            date_tag= col.find_element(By.TAG_NAME,"span")
            date = date_tag.text 
            print(date+"\n")   #get the date
            if(date== desired_date):
                date_tag.click()
                date_found=1
                break
             
        if date_found==1 :
            break            
    
    browser.find_element_by_xpath('(//div[@class="ok"])['+from_to_selector+']').click()

time.sleep(10)
fill_station(sys.argv[1])
fill_station(sys.argv[2])
fill_station(sys.argv[3])
#USING CSS SELECTOR, NEED TO SPECIFY THE INDEX OF OPTION
#browser.find_element_by_css_selector(".options >ul:nth-child(1) > li:nth-child(3)").click()

browser.find_element_by_xpath('//angular2-multiselect[@class="myclass custom-class ng-untouched ng-pristine ng-valid"]').click()
browser.find_element_by_css_selector(".pure-checkbox.select-all").click()
browser.find_element_by_xpath('//span[@class="fa fa-angle-up"]').click()
browser.find_element_by_xpath('(//ng-select[@class="select-box ng-untouched ng-dirty ng-valid"])[last()]').click()
browser.find_element_by_xpath("//li[contains(text(), '"+sys.argv[4]+"')]").click()

fill_date(sys.argv[5].split()[0], sys.argv[5].split()[1],sys.argv[5].split()[2],'1')
fill_date(sys.argv[6].split()[0], sys.argv[6].split()[1], sys.argv[6].split()[2],'2')

browser.find_element_by_xpath('//button[@class="btn btn-primary"]').click()
time.sleep(4)
browser.find_element_by_css_selector(".fa.fa-file-excel-o").click()







