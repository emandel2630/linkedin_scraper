############# JUST FOR GETTING PROFILE #################


import sys

# adding Folder_2 to the system path
from linkedin_scraper_headless import actions, ConnectionList, Person_v2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json
import os
from dotenv import load_dotenv
import time
from webdriver_manager.chrome import ChromeDriverManager


print(sys.path)
env_path= os.getcwd() + "/linkedin_login.env"
load_dotenv(env_path)

email = os.getenv('EMAIL')
password = os.getenv('PASSWORD')
options = webdriver.ChromeOptions()

#Open window on right side of screen selenium


# Adding argument to disable the AutomationControlled flag 
options.add_argument("--disable-blink-features=AutomationControlled") 

# Exclude the collection of enable-automation switches 
options.add_experimental_option("excludeSwitches", ["enable-automation"]) 

# Turn-off userAutomationExtension 
options.add_experimental_option("useAutomationExtension", False) 

s = Service(ChromeDriverManager().install())

################################################

def json_append(filename,appendContent):
    dictObj = []
    
    # Read JSON file
    with open(filename) as fp:
        dictObj = json.load(fp)
    
    dictObj.update(appendContent)
    
    with open(filename, 'w') as json_file:
        json.dump(dictObj, json_file, 
                            indent=4,  
                            separators=(',',': '))
    

driver = webdriver.Chrome(service=s,options=options)

actions.login(driver, email, password,timeout= 30,botnum=1) # if email and password isnt given, it'll prompt in terminal

#Make sure there is no final slash after userID 

url = "https://www.linkedin.com/in/ethan-mandel-eece"
person = Person_v2(url+"/", driver=driver)


driver.quit()

print(person)
