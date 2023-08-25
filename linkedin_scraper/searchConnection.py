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


#Why am I getting this error TypeError: Employer.__init__() got an unexpected keyword argument 'driver'

class ConnectionList(Scraper):

    __TOP_CARD = "pv-top-card"
    __WAIT_FOR_ELEMENT_TIMEOUT = 1000

    def __init__(
        self,
        listOfHits = None,
        linkedin_url = None,
        get=True,
        scrape=True,
        driver=None,
        close_on_complete=False,
        time_to_wait_after_login=0,
    ):
        self.linkedin_url = linkedin_url
        self.listOfHits = listOfHits or []

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

    def add_listOfHits(self, hits):
        self.listOfHits.append(hits)

    
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


    def get_hits(self):
        
        url = self.linkedin_url 
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        self.random_scroll()
        
        try:
            main_list = self.wait_for_element_to_load(name="reusable-search__entity-result-list", base=main)
            for position in main_list.find_elements(By.CLASS_NAME,"entity-result"):
                linkSource = position.find_elements(By.CLASS_NAME,'app-aware-link ')
                if(len(linkSource)>0):
                    linkedin_url = linkSource[0].get_attribute("href").split("?")[0] 
                else:
                    linkedin_url =None
                
                self.add_listOfHits(linkedin_url)
        except:
            print("DIDNT LOAD")
            self.add_listOfHits("")

        

        
    def scrape_logged_in(self, close_on_complete=False):
        driver = self.driver
        duration = None
        
        self.focus()

        # get experience
        self.get_hits()
        

        if close_on_complete:
            driver.quit()

    def listOut(self):

        if(len(self.listOfHits)>1):
            return self.listOfHits
        else:
            return []
        
