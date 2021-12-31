from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC, select
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.service import Service


import time
import random
import datetime
import re
import os

import details_checker


USERNAME = os.getenv('SPIRE_USERNAME')
PASSWORD = os.getenv('SPIRE_PASSWORD')

PATH = "/home/xeze/Programs/chromedriver"
s = Service(PATH)
driver = webdriver.Chrome(service=s)

driver.get("https://spire.umass.edu")

def login_page_enter_details():
    try:
        user_bar = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "userid"))
        )
        pwd_bar = driver.find_element(By.ID, "pwd")
        go_button = driver.find_element(By.NAME,"Submit")
    except:
        log_error("Incorrect Login Page : " + driver.title)
        exit(-1)
    user_bar.send_keys(USERNAME)
    pwd_bar.send_keys(PASSWORD)
    time.sleep(random.random()*3 + 3) # To not make requests immediate
    go_button.click()

def go_to_home_page():
    try:
        home_button = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "pthdr2home"))
        )
        home_button.click()
    except:
        log_error("Can't find Login Page from : " + driver.title)
        exit(-1)


def home_page_to_search_for_classes():
    try:
        time.sleep(7)
        driver.switch_to.frame("ptifrmtgtframe")
        search_for_classes_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "DERIVED_SSS_SCL_SSS_GO_4$83$"))
        )
        search_for_classes_button.click()
    except:
        go_to_home_page()
        try:
            driver.switch_to.frame("ptifrmtgtframe")        
            search_for_classes_button = WebDriverWait(driver, 25).until(
                EC.presence_of_element_located((By.ID, "DERIVED_SSS_SCL_SSS_GO_4$83$"))
            )
            search_for_classes_button.click()
        except:
            log_error("Can't find Search for Classes Button : " + driver.title)
            exit(-1)

# Not useful
def search_for_class(class_number, section_number):
    try:
        class_bar = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "CLASS_SRCH_WRK2_CATALOG_NBR$8$"))
        )
        class_bar.send_keys(class_number)
        section_tab = driver.find_element(By.ID, "CLASS_SRCH_WRK2_CLASS_NBR$124$")
        section_tab.send_keys(section_number)        
        open_classes_checkbox = driver.find_element(By.ID, "CLASS_SRCH_WRK2_SSR_OPEN_ONLY").click()
        time.sleep(3)
        search_button = driver.find_element(By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH").click()
    except:
        log_error("Class time out or find_element error")
        exit(-1)

def start_new_search():
    try:
        start_new_search_button = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH"))
        ).click()
    except:
        log_error("Problem in finding a new search")


def search_open_CS_above_num(num):
    try:    
        class_bar = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "CLASS_SRCH_WRK2_CATALOG_NBR$8$"))
        ).send_keys(str(num))
        select_course_number_details = Select(driver.find_element(By.ID, "CLASS_SRCH_WRK2_SSR_EXACT_MATCH1")).select_by_value("G")
        select_by_class = Select(driver.find_element(By.ID,"CLASS_SRCH_WRK2_SUBJECT$108$")).select_by_value("COMPSCI")
        time.sleep(random.random()*3 + 1)
        search_button = driver.find_element(By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH").click()
    except:
        log_error("Problem in finding a new search or in selecting class")

def click_start_search_button():
    try:
        search_button = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH"))
        )
        time.sleep(random.random()*3 + 1)
        search_button.click()
    except:
        log_error("Problem in finding a new search")



def extract_class_details_in_series(num):
    try:
        regex = "[" + str(num) + "-6][0-8][0-9]|[" + str(num) + "-6]90."
        WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.ID, "DERIVED_CLSRCH_DESCR200$0"))
        )
        class_counter = 0
        details = []
        while True:
            class_id = "DERIVED_CLSRCH_DESCR200$" + str(class_counter)
            class_details = driver.find_element(By.ID, class_id).text
            instance_arr = re.findall(regex, class_details)
            if len(instance_arr) > 0:
                if int(instance_arr[0][:3]) > 600: # grad class
                    break
                details.append("CS" + instance_arr[0])
            class_counter += 1
    except:
        log_error("Might have no open classes or timeout error")
        exit(-1)
    
    file = open("files/current_details.txt", "w")
    file.truncate(0)
    for line in details:
        file.write(line + "\n")
    file.close()
    # Update other files
    details_checker.checker()

def return_to_start_new_search():
    try:
        start_new_search_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "CLASS_SRCH_WRK2_SSR_PB_NEW_SEARCH"))
        ).click()
    except:
        log_error("Problem in returning to search")
    

def log_error(err):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S - ")
    log_file = open("logs/scraper_errors.txt","a")
    log_file.write(dt_string + err + "\n")
    log_file.close()





login_page_enter_details()
home_page_to_search_for_classes()
search_open_CS_above_num(300)

while True:
    extract_class_details_in_series(3)
    time.sleep(random.random()*30 + 60)
    return_to_start_new_search()
    time.sleep(random.random()*10 + 10)
    click_start_search_button()

driver.close()
