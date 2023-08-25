import json
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Scraper, Hirer
import os
from linkedin_scraper import selectors
from dateutil.parser import parse
import time


#Why am I getting this error TypeError: Employer.__init__() got an unexpected keyword argument 'driver'

class Employer_Headless(Scraper):

    __TOP_CARD = "pv-top-card"
    __WAIT_FOR_ELEMENT_TIMEOUT = 1000

    def __init__(
        self,
        employer = None,
        linkedin_url = None,
        get=True,
        scrape=True,
        driver=None,
        close_on_complete=False,
        time_to_wait_after_login=0,
        alreadyOnPage =False,
    ):
        self.alreadyOnPage = alreadyOnPage
        self.linkedin_url = linkedin_url
        self.employer = employer or []

        if driver is None:
            try:
                if os.getenv("CHROMEDRIVER") == None:
                    driver_path = os.path.join(
                        os.path.dirname(__file__), "drivers/chromedriver"
                    )
                else:
                    driver_path = os.getenv("CHROMEDRIVER")

                driver = webdriver.Chrome(driver_path)
            except:
                driver = webdriver.Chrome()

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def add_employer(self, employer):
        self.employer.append(employer)

    
    def scrape(self, close_on_complete=False):
        if self.is_signed_in():
            self.scrape_logged_in(close_on_complete=close_on_complete)
        else:
            print("you are not logged in!")

    def _click_see_more_by_class_name(self, class_name):
        try:
            _ = WebDriverWait(self.driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, class_name))
            )
            div = self.driver.find_element(By.CLASS_NAME, class_name)
            div.find_element(By.TAG_NAME, "button").click()
        except Exception as e:
            pass

    def is_open_to_work(self):
        try:
            return "#OPEN_TO_WORK" in self.driver.find_element(By.CLASS_NAME,"pv-top-card-profile-picture").find_element(By.TAG_NAME,"img").get_attribute("title")
        except:
            return False


    def get_employer(self):
        #print("GETTING EMPLOYER")
        
        linkedin_url = self.linkedin_url 

        company_name = None
        industry = None
        institution_desc = None
        institution_size = None
        institution_specialties = None
        institution_url = None

        #Protect against hidden unavailable pages
        currentUrl = self.driver.current_url
        if(currentUrl == "https://www.linkedin.com/company/unavailable/"):
            employer = "BAD URL"
            self.driver.back()
            self.add_employer(employer)
        elif(linkedin_url!= None and "/company/" in linkedin_url):
            if(self.alreadyOnPage == False):

            
                url = linkedin_url + "about"
                self.driver.get(url)


                self.focus()
                main = None
                try:
                    main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                except:
                    print("Page Unavailable")
                    self.driver.back()
                    if(self.alreadyOnPage == True):
                        self.driver.back()
                    return 0
            
                
            if(self.alreadyOnPage == True):
                self.focus()
                
                aboutTab = self.wait_for_element_to_load(by=By.CLASS_NAME, name ="org-page-navigation__items")
                children = aboutTab.find_elements(By.XPATH, './/*')

                elementFound = False
                for element in children:
                    if(element.get_attribute('href')!= None):
                        if element.get_attribute('href').split("/")[-2] == "about":
                            url = element.get_attribute('href')
                            self.driver.get(url)
                            self.alreadyOnPage = False
                            time.sleep(1)
                            elementFound= True
                            break
                
                if elementFound == False:
                    print("Company page failed")
                    self.driver.back()
                    if(self.alreadyOnPage == True):
                        self.driver.back()
                    return 0



                #Get href of element selenium

                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                self.random_scroll()
                
            
            
            company_name = None
            industry = None
            institution_desc = None
            institution_size = None
            institution_specialties = None
            institution_url = None

            if(main!= None):
                self.random_scroll()

                

                headerList = self.wait_for_element_to_load(name="org-module-card__margin-bottom", base=main)
                headerItemsList = headerList.find_elements(By.CLASS_NAME,'ember-view')
                


                header = None
                for x in headerItemsList:
                    if(x.get_attribute("class") == "ember-view"):
                        nameTag = x.find_elements(By.CLASS_NAME,'ember-view')
                        for y in nameTag:
                            parent = y.find_element(By.XPATH,"..")
                            parentName = parent.get_attribute("class")
                            if(y.text!= None and parentName ==""):
                                header = y.text
                                break

                company_name = header

                main_list= self.wait_for_element_to_load(name="mb6", base=main)
                pageList = main_list.find_elements(By.CLASS_NAME,'ember-view')
                

                overviewPage = None
                for x in pageList:
                    if(x.get_attribute("class") == "ember-view"):
                        overviewPage = x
                        break
                
                
                aboutSection = overviewPage.find_element(By.CLASS_NAME,"artdeco-card").text
                companyAbout = aboutSection.split("\n")

                for i in range(0,len(companyAbout)):
                    if (companyAbout[i].strip() == "Overview"):
                        institution_desc = companyAbout[i+1]
                    if (companyAbout[i].strip() == "Industry"):
                        industry = companyAbout[i+1]
                    if (companyAbout[i].strip() == "Website"):
                        institution_url = companyAbout[i+1]
                    if (companyAbout[i].strip().lower() == "Company Size".lower()):
                        institution_size = companyAbout[i+1]
                    if (companyAbout[i].strip() == "Specialties"):
                        institution_specialties = companyAbout[i+1]
            
            employer = Hirer(
                company_name= company_name,
                industry= industry,
                institution_desc = institution_desc,
                institution_url= institution_url,
                institution_size = institution_size,
                institution_specialities= institution_specialties,
                linkedin_url= linkedin_url
            )

            self.driver.back()
            if(self.alreadyOnPage == True):
                self.driver.back()
            
            self.add_employer(employer)

            
                         
    def scrape_logged_in(self, close_on_complete=False):
        driver = self.driver
        duration = None
        
        self.focus()

        # get experience
        self.get_employer()
        
        if close_on_complete:
            driver.quit()

    def __repr__(self):
        if(len(self.employer)>0 and self.employer[0]!= "BAD URL"):

            emp =self.employer[0]

            companyDict = {emp.linkedin_url.split("/")[-2] :{"Name": emp.company_name, "Industry" : emp.industry,"Company Size":emp.institution_size,"Description":emp.institution_desc,"Specialities":emp.institution_specialities,"Employer Url":emp.institution_url}}
            

            json_object = json.dumps(companyDict, indent = 4) 
            return json_object
        else:
            return ""
        
