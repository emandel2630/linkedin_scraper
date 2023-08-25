import json
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Experience, Education, Scraper, Honor, Project, Volunteer, Skill, Organization, Publication, Patent, Language, Certification
from .employer_headless import Employer_Headless
import os
from linkedin_scraper import selectors
from dateutil.parser import parse
import random
import pygetwindow as gw
from pyHM import mouse



from selenium.webdriver.common.action_chains import ActionChains
import time

def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def checkKey(dic, key):
    if key in dic.keys():
        return True
    else:
        return False

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
class Person_Headless(Scraper):

    __TOP_CARD = "pv-top-card"
    __WAIT_FOR_ELEMENT_TIMEOUT = 100

    def __init__(
        self,
        linkedin_url=None,
        name=None,
        about=None,
        experiences=None,
        educations=None,
        volunteering= None,
        organization = None,
        certification = None,
        skill = None,
        language =None,
        publication = None,
        patent = None,
        honors = None,
        projects =None,
        company=None,
        job_title=None,
        contacts=None,
        driver=None,
        get=True,
        scrape=True,
        close_on_complete=False,
        time_to_wait_after_login=0,
    ):
        self.linkedin_url = linkedin_url
        self.name = name
        self.about = about or []
        self.experiences = experiences or []
        self.educations = educations or []
        self.volunteering = volunteering or []
        self.honors = honors or []
        self.skill = skill or []
        self.publication = publication or []
        self.patent = patent or []
        self.langauge = language or []
        self.organization = organization or []
        self.certification = certification or []
        self.projects = projects or []
        self.also_viewed_urls = []
        self.contacts = contacts or []

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

        if get:
            driver.get(linkedin_url)

        self.driver = driver

        if scrape:
            self.scrape(close_on_complete)

    def add_about(self, about):
        self.about.append(about)

    def add_experience(self, experience):
        self.experiences.append(experience)

    def add_education(self, education):
        self.educations.append(education)

    def add_volunteering(self, volunteering):
        self.volunteering.append(volunteering)
    
    def add_honor(self, honor):
        self.honors.append(honor)

    def add_organization(self, organization):
        self.organization.append(organization)

    def add_certification(self, certification):
        self.certification.append(certification)
    
    def add_patent(self, patent):
        self.patent.append(patent)
    
    def add_language(self, language):
        self.langauge.append(language)

    def add_skill(self, skill):
        self.skill.append(skill)

    def add_publication(self, publication):
        self.publication.append(publication)

    def add_project(self, project):
        self.projects.append(project)

    def add_interest(self, interest):
        self.interests.append(interest)

    def add_accomplishment(self, accomplishment):
        self.accomplishments.append(accomplishment)

    def add_location(self, location):
        self.location = location

    def add_contact(self, contact):
        self.contacts.append(contact)

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
        
    def read_footers_of_homepage(self,sectionKeyword):
        time.sleep(2)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        
        main_list = main.find_elements(By.CSS_SELECTOR, ".artdeco-card.ember-view.relative.break-words.pb3.mt2")
        listOfSectionNames= ["experience","education","volunteering_experience","skills","publications","languages","organizations","projects","patents","licenses_and_certifications","honors_and_awards"]
        time.sleep(1)

        for section in main_list:
            sectionName = section.find_element(By.CLASS_NAME,"pv-profile-card__anchor").get_attribute("id")
            if(sectionName not in listOfSectionNames):
                continue
            

            #self.random_scroll()
            #Get id of element selenium
            footer = section.find_elements(By.CSS_SELECTOR,".optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--standard.artdeco-button--2.artdeco-button--muted")
            if(sectionName == sectionKeyword):
                time.sleep(2)
                footerElement = footer[-1]
                self.slow_scroll_to_element(footerElement)
                return footerElement
    
    def read_img_links_of_exp_page(self,matchLink,main_list = None):
        self.focus()
        

        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            linkSource = position.find_elements(By.CSS_SELECTOR,'.optional-action-target-wrapper')
            if(len(linkSource)>0):
                linkedin_url = linkSource[0].get_attribute("href") 
                time.sleep(1)
                if(matchLink == linkedin_url):
                    return linkSource[0]


                


    def get_homepage(self):
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        
        #Set 10 variables equal to none in one line
        expUrl = eduUrl = volUrl = skillUrl = pubUrl = patUrl = langUrl = projUrl= orgUrl = honUrl = certUrl = None

        main_list = main.find_elements(By.CSS_SELECTOR, ".artdeco-card.ember-view.relative.break-words.pb3.mt2")

        random.shuffle(main_list)


        for elm in main_list:
            sectionName = elm.find_element(By.CLASS_NAME,"pv-profile-card__anchor").get_attribute("id")
            if(sectionName == "experience"):
                main_list.remove(elm)
                main_list.append(elm)
                break
        
        




        
        listOfSectionNames= ["experience","education","volunteering_experience","skills","publications","languages","organizations","projects","patents","licenses_and_certifications","honors_and_awards"]


        for section in main_list:
            time.sleep(1)
            sectionName = section.find_element(By.CLASS_NAME,"pv-profile-card__anchor").get_attribute("id")
            if(sectionName not in listOfSectionNames):
                continue
            section_main_list =section.find_element(By.CLASS_NAME,"pvs-list")

            self.slow_scroll_to_element(section_main_list,increment=60)
            #Get id of element selenium
            footer = section.find_elements(By.CSS_SELECTOR,".optional-action-target-wrapper.artdeco-button.artdeco-button--tertiary.artdeco-button--standard.artdeco-button--2.artdeco-button--muted")
            if(len(footer)>0):
                if(sectionName == "experience"):
                    expUrl = footer[-1].get_attribute("href")
                elif(sectionName == "education"):
                    eduUrl = footer[-1].get_attribute("href")
                elif(sectionName == "volunteering_experience"):
                    volUrl = footer[-1].get_attribute("href")
                elif(sectionName == "skills"):
                    skillUrl = footer[-1].get_attribute("href")
                elif(sectionName == "publications"):
                    pubUrl = footer[-1].get_attribute("href")
                elif(sectionName == "languages"):
                    langUrl = footer[-1].get_attribute("href")
                elif(sectionName == "organizations"):
                    orgUrl = footer[-1].get_attribute("href")
                elif(sectionName == "projects"):
                    projUrl = footer[-1].get_attribute("href")
                elif(sectionName == "patents"):
                    patUrl = footer[-1].get_attribute("href")
                elif(sectionName == "licenses_and_certifications"):
                    certUrl = footer[-1].get_attribute("href")
                elif(sectionName == "honors_and_awards"):
                    honUrl = footer[-1].get_attribute("href")
            else:
                if(sectionName == "experience"):
                   self.get_experiences(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "education"):
                    self.get_educations(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "volunteering_experience"):
                    self.get_volunteering(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "skills"):
                    self.get_skills(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "publications"):
                    self.get_publications(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "languages"):
                     self.get_languages(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "organizations"):
                    self.get_organizations(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "projects"):
                    self.get_projects(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "patents"):
                    self.get_patents(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "licenses_and_certifications"):
                    self.get_certifications(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                elif(sectionName == "honors_and_awards"):
                    self.get_honors(main_list = section_main_list, alreadyOnPage= True, pageIsConnectedToHome = True)
                
        
        linkList = [expUrl,eduUrl,volUrl,skillUrl,pubUrl,langUrl,orgUrl,projUrl,patUrl,certUrl,honUrl]
        
        
        filtered = [(item, corresponding_item) for item, corresponding_item in zip(listOfSectionNames, linkList) if corresponding_item != None]
        random.shuffle(filtered)

        try:
            sectionNamesFiltered, linkListFiltered = map(list, zip(*filtered))
        except:
            sectionNamesFiltered = []
            linkListFiltered = []


        #Go back to main page and recollect all footers and then go click on each of them
        if(len(linkListFiltered))>0:
            for i in range(0,len(linkListFiltered)):
                if(sectionNamesFiltered[i] == "experience"):
                    footerElement = self.read_footers_of_homepage("experience")

                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))

                    if url == None:
                        self.get_experiences(alreadyOnPage= True)
                    else:
                        self.get_experiences(url = url)
        
                    self.driver.back()
                    time.sleep(random.randint(2,4))
                elif(sectionNamesFiltered[i] == "education"):
                    footerElement = self.read_footers_of_homepage("education")
                    
                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))
                    if url == None:
                        self.get_educations(alreadyOnPage= True)
                    else:
                        self.get_educations(url = url)
                    

                    self.random_scroll()
                    
                    self.driver.back()
                    time.sleep(random.randint(2,4))
                elif(sectionNamesFiltered[i] == "volunteering_experience"):
                    footerElement = self.read_footers_of_homepage("volunteering_experience")
                    

                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))

                    if url == None:
                        self.get_volunteering(alreadyOnPage= True)
                    else:
                        self.get_volunteering(url = url)
                    self.random_scroll()
                    self.driver.back()
                    time.sleep(random.randint(2,4))
                elif(sectionNamesFiltered[i] == "skills"):
                    footerElement = self.read_footers_of_homepage("skills")
                    
                        

                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))
                    if url == None:
                        self.get_skills(alreadyOnPage= True)
                    else:
                        self.get_skills(url = url)
                    self.random_scroll()
                    self.driver.back()
                    time.sleep(random.randint(2,4))
                elif(sectionNamesFiltered[i] == "publications"):
                    footerElement = self.read_footers_of_homepage("publications")
               
                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))
                    if url == None:
                        self.get_publications(alreadyOnPage= True)
                    else:
                        self.get_publications(url = url)
                    self.random_scroll()
                    self.driver.back()
                    time.sleep(random.randint(2,4))
                elif(sectionNamesFiltered[i] == "languages"):
                    footerElement = self.read_footers_of_homepage("languages")
                    
                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))
                    if url == None:
                        self.get_languages(alreadyOnPage= True)
                    else:
                        self.get_languages(url = url)
                    self.random_scroll()
                    self.driver.back()
                    time.sleep(random.randint(2,4))
                elif(sectionNamesFiltered[i] == "organizations"):
                    footerElement = self.read_footers_of_homepage("organizations")
                    
                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))
                    if url == None:
                        self.get_organizations(alreadyOnPage= True)
                    else:
                        self.get_organizations(url = url)
                    self.random_scroll()
                    self.driver.back()
                    time.sleep(random.randint(2,4))
                elif(sectionNamesFiltered[i] == "projects"):
                    footerElement = self.read_footers_of_homepage("projects")
                    
                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))
                    if url == None:
                        self.get_projects(alreadyOnPage= True)
                    else:
                        self.get_projects(url = url)
                    self.random_scroll()
                    self.driver.back()
                    time.sleep(random.randint(2,4))
                elif(sectionNamesFiltered[i] == "patents"):
                    footerElement = self.read_footers_of_homepage("patents")
                    
                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))
                    if url == None:
                        self.get_patents(alreadyOnPage= True)
                    else:
                        self.get_patents(url = url)
                    self.random_scroll()
                    self.driver.back()
                    time.sleep(random.randint(2,4))
                elif(sectionNamesFiltered[i] == "licenses_and_certifications"):
                    footerElement = self.read_footers_of_homepage("licenses_and_certifications")
                    
                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))
                    if url == None:
                        self.get_certifications(alreadyOnPage= True)
                    else:
                        self.get_certifications(url = url)
                    self.random_scroll()
                    self.driver.back()
                    time.sleep(random.randint(2,4))


                elif(sectionNamesFiltered[i] == "honors_and_awards"):
                    footerElement = self.read_footers_of_homepage("honors_and_awards")
                    
                    url = footerElement.get_attribute('href')
                    time.sleep(random.uniform(2,3))
                    if url == None:
                        self.get_honors(alreadyOnPage= True)
                    else:
                        self.get_honors(url = url)
                    self.random_scroll()
                    self.driver.back()
                    time.sleep(random.randint(2,4))




    def get_experiences(self,main_list = None,url= None, alreadyOnPage =False, pageIsConnectedToHome= False):
        #print("EXP")
        if(url!=None and alreadyOnPage == False):            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            self.random_scroll()
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                self.random_scroll()
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)

        

        listOfExp = []
        compPosLoc = []
        linkedin_urls = []
        
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')

            linkSource = position.find_elements(By.CLASS_NAME,'optional-action-target-wrapper')
            if(len(linkSource)>0):
                linkedin_url = linkSource[0].get_attribute("href") 
            else:
                linkedin_url =None
                        
            experienceElements =[]

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               experienceElements.append([text,parentName])

            position_title = None
            from_date = None
            to_date = None
            duration = None
            location = None
            description = None
            institution_name = None
            employment_type = None
            location_type = None
            associated_skills = None
            


            count =0
            for element in experienceElements:
                if("mr1 hoverable-link-text t-bold" in element[1]):
                    count+=1
            
            countAppearances = 0
            locAppearances = 0
            pos = []
            if(count >1):
                for element in experienceElements:
                    if("mr1 hoverable-link-text t-bold" in element[1] and countAppearances >0):
                        pos.append(element[0])
                        countAppearances +=1
                    if("mr1 hoverable-link-text t-bold" in element[1] and countAppearances ==0):
                        comp = element[0]
                        countAppearances +=1
                    if("t-14 t-normal t-black--light" in element[1] and locAppearances ==0):
                        loc = element[0]
                        locAppearances = 1
                compPosLoc.append([comp,pos,loc])
                continue
            
            
            
            if len(experienceElements) > 1:
                if(len(compPosLoc) > 0):
                    position_title = compPosLoc[0][1][0]
                    compPosLoc[0][1].pop(0)
                    institution_name = compPosLoc[0][0]
                    location = compPosLoc[0][2]
                    if(len(compPosLoc[0][1])==0):
                        compPosLoc.pop(0)
                else:
                    position_title = experienceElements[0][0] 


                for element in experienceElements:
                    associatedSkills = []

                    if ("t-14 t-normal t-black--light" in element[1] and is_date(element[0].split(" - ")[0])):
                        if(len(element[0].split(" - "))>1):
                            from_date = element[0].split(" - ")[0]
                            to_date = element[0].split(" - ")[1].split(" · ")[0]
                        else:
                            from_date = element[0].split(" · ")[0]
                            to_date = element[0].split(" · ")[0]

                        duration = element[0].split(" · ")[1]
                   

                    if(element[1] == "t-14 t-normal"):
                        institution_name = element[0]
                        if(" · " in element[0]):
                            employment_type = element[0].split(" · ")[1]
                        else:
                            employment_type = None

                    if("t-14 t-normal t-black--light" in element[1] and (not is_date(element[0].split(" - ")[0])) and (location == None)):
                        location = element[0].split(" · ")[0]
                        if(len(element[0].split(" · ")) >1):
                            location_type = element[0].split(" · ")[1]
                        else:
                            location_type =None
                    

                    if("display-flex align-items-center" in element[1]):
                        description = None
                        associatedSkills = []
                        if("Skills:" not in element[0]):
                            description = element[0]
                        if("Skills:" in element[0]):
                            listOfSkills = element[0][7:]
                            for skill in listOfSkills.split(" · "):
                                associatedSkills.append(skill)
                            associatedSkillsStr= str(associatedSkills)[1:-1]
                    
                    if len(associatedSkills)>0:
                        associated_skills = associatedSkillsStr
            
            # Check company section              

            
            experience = Experience(
                position_title = position_title,
                from_date = from_date,
                to_date = to_date,
                duration = duration,
                location = location,
                description = description,
                institution_name = institution_name,
                linkedin_url = linkedin_url,
                employment_type = employment_type,
                location_type = location_type,
                associated_skills = associated_skills
            )
            listOfExp.append(experience)

        
        for dataClassMem in listOfExp:
            
            
            linkedin_url = getattr(dataClassMem, "linkedin_url")
            institution_desc = None
            industry = None
            institution_size = None
            institution_url = None
            institution_specialties = None


            with open('Employer_Database.json') as json_file:
                companyDict = json.load(json_file)
            
            keysList = list(companyDict.keys())
            key = linkedin_url.split("/")[-2] 

            if(key in keysList):
                institution_desc = companyDict[key]["Description"]
                industry = companyDict[key]["Industry"]
                institution_size = companyDict[key]["Company Size"]
                institution_url = companyDict[key]["Employer Url"]
                institution_specialties = companyDict[key]["Specialities"]
            else:
                if("company" not in linkedin_url):
                    print("No company page")
                else:
                    #Handle reloading the page
                    if(pageIsConnectedToHome):
                        time.sleep(2)
                        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                        main_list = main.find_elements(By.CSS_SELECTOR, ".artdeco-card.ember-view.relative.break-words.pb3.mt2")
                        for elm in main_list:
                            sectionName = elm.find_element(By.CLASS_NAME,"pv-profile-card__anchor").get_attribute("id")
                            if(sectionName == "experience"):
                                section_main_list =elm.find_element(By.CLASS_NAME,"pvs-list")
                                break
                        
                        
                        
                        imgElement = self.read_img_links_of_exp_page(linkedin_url,main_list=section_main_list)
                        

                    else:
                        self.driver.refresh()
                        time.sleep(2)
                        self.slow_scroll_to_bottom()
                        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                        main_list2 = self.wait_for_element_to_load(name="pvs-list", base=main)
                        imgElement = self.read_img_links_of_exp_page(linkedin_url,main_list=main_list2)

                    self.slow_scroll_to_element(imgElement)
                    url = imgElement.get_attribute('href')

                    #Hot fix for employer bugs. Actually improve this later. Thanks me from the future
                    company = Employer_Headless(linkedin_url = linkedin_url,driver=self.driver,alreadyOnPage=False)
                    if(str(company) != ""):
                        companyDict = json.loads(str(company))
                        institution_desc = companyDict[key]["Description"]
                        industry = companyDict[key]["Industry"]
                        institution_size = companyDict[key]["Company Size"]
                        institution_url = companyDict[key]["Employer Url"]
                        institution_specialties = companyDict[key]["Specialities"]
                        json_append("Employer_Database.json",companyDict)

                            
                    

            

            setattr(dataClassMem,"institution_desc", institution_desc)
            setattr(dataClassMem,"industry", industry)
            setattr(dataClassMem,"institution_url", institution_url)
            setattr(dataClassMem,"institution_size", institution_size)
            setattr(dataClassMem,"institution_specialties", institution_specialties)


            self.add_experience(dataClassMem)


        #Go back home
        #Get current url selenium
        """if alreadyOnPage == False or "company" not in self.driver.current_url:
            self.driver.back()"""


    
                


    def get_educations(self, url = None, main_list=None, alreadyOnPage = False, pageIsConnectedToHome= False ):
        #print("EDU")
        if(url!=None and alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)

        

        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):
            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')

            linkSource = position.find_elements(By.CLASS_NAME,'optional-action-target-wrapper')
            if(len(linkSource)>0):
                linkedin_url = linkSource[0].get_attribute("href") 
            else:
                linkedin_url =None
                        
            educationElements =[]

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               educationElements.append([text,parentName])

            from_date=None
            to_date=None
            description=None
            degree=None
            grade = None
            activities = None
            institution_name=None
            associated_skills = None
            linkedin_url=linkedin_url
            
            institution_name = educationElements[0][0] 
            for element in educationElements:
                
                if(element[1] == "t-14 t-normal"):
                    degree = element[0]
                
                if ("t-14 t-normal t-black--light" in element[1] and is_date(element[0].split(" - ")[0])):
                    if(len(element[0].split(" - "))>1):
                        from_date = element[0].split(" - ")[0]
                        to_date = element[0].split(" - ")[1]

                
                if("inline-show-more-text" in element[1]):
                    if("Grade:" in element[0]):
                        grade = element[0][6:]
                    if("Activities and societies:" in element[0]):
                        activities = element[0][25:]


                if("display-flex align-items-center" in element[1] and "t-14 t-normal t-black" in element[1]):
                    associatedSkills = []
                    if("Skills:" not in element[0]):
                        description = element[0]
                    if("Skills:" in element[0]):
                        listOfSkills = element[0][7:]
                        for skill in listOfSkills.split(" · "):
                            associatedSkills.append(skill)
                        associatedSkillsStr= str(associatedSkills)[1:-1]
                    
                    if len(associatedSkills)>0:
                        associated_skills = associatedSkillsStr


            education = Education(
                from_date=from_date,
                to_date=to_date,
                description=description,
                degree=degree,
                grade = grade,
                activities = activities,
                institution_name=institution_name,
                associated_skills = associated_skills,
                linkedin_url=linkedin_url
                
            )
            self.add_education(education)


        
            

    def get_volunteering(self, url = None, main_list=None, alreadyOnPage = False, pageIsConnectedToHome= False ):
        #print("VOL")
        if(url!=None and alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
            
        
        
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):
            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')

            linkSource = position.find_elements(By.CLASS_NAME,'optional-action-target-wrapper')
            if(len(linkSource)>0):
                linkedin_url = linkSource[0].get_attribute("href") 
            else:
                linkedin_url =None
                        
            volunteerElements =[]

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               volunteerElements.append([text,parentName])

            organization= None
            role =None
            from_date = None
            to_date= None
            duration= None
            description= None
            cause = None
            
            role = volunteerElements[0][0] 
            for element in volunteerElements:
                
                if(element[1] == "t-14 t-normal"):
                    organization = element[0]
                
                if ("t-14 t-normal t-black--light" in element[1] and is_date(element[0].split(" - ")[0])):
                    if(len(element[0].split(" - "))>1):
                        from_date = element[0].split(" - ")[0]
                        to_date = element[0].split(" - ")[1].split(" · ")[0]
                        duration = element[0].split(" · ")[1]
                
                if ("t-14 t-normal t-black--light" in element[1] and not is_date(element[0].split(" - ")[0])):
                    cause = element[0]

                if("display-flex align-items-center" in element[1] and "t-14 t-normal t-black" in element[1]):
                    description = element[0]

            volunteer = Volunteer(
                organization= organization,
                role =role,
                cause = cause,
                from_date = from_date,
                to_date= to_date,
                duration= duration,
                url= linkedin_url,
                description= description
            )
            self.add_volunteering(volunteer)


    

    def get_projects(self, url = None, main_list=None, alreadyOnPage = False, pageIsConnectedToHome= False ):
        #print("PROJ")
        if(url!=None and alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)

        
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')

            linkSource = position.find_elements(By.CLASS_NAME,'pv2')
            if(len(linkSource)>0):
                url = linkSource[0].find_element(By.XPATH,"*").find_element(By.XPATH,"*").get_attribute("href")
            else:
                url =None
            

            name = None
            from_date = None
            to_date = None
            url = None
            association = None
            description = None
            projectElements =[]

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               projectElements.append([text,parentName])

            if len(projectElements) > 1:
                name = projectElements[0][0]

                if(projectElements[1][1]== "t-14 t-normal"):
                    from_date = projectElements[1][0].split(" - ")[0]
                    to_date = projectElements[1][0].split(" - ")[1]
                else:
                    from_date = None
                    to_date = None
                           
                for element in projectElements:
                    if("display-flex align-items-center" in element[1] and "Associated with" in element[0]):
                        association = element[0].split("Associated with ")[1]
                    else:
                        association = None
                    if("display-flex align-items-center" in element[1] and "Associated with" not in element[0]):
                        description = element[0]
                    else:
                        description = None

            elif(len(projectElements) == 1):
                name = projectElements[0][0]
                from_date = None
                to_date = None
                url = None
                association = None
                description = None


            project = Project(
                name = name,
                from_date = from_date,
                to_date = to_date,
                url = url,
                association = association,
                description = description,
            )
            self.add_project(project)



    def get_organizations(self, url = None, main_list=None, alreadyOnPage = False, pageIsConnectedToHome= False ):
        #print("ORG")
        if(url!=None and alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        
        
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')

            position = None
            from_date = None
            to_date = None
            orgElements =[]

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               orgElements.append([text,parentName])


            if len(orgElements) > 1: 
                name = orgElements[0][0]

                if(orgElements[1][1]== "t-14 t-normal"):
                    if((" · ") in orgElements[1][0]):
                        position = orgElements[1][0].split(" · ")[0]
                        from_date = orgElements[1][0].split(" · ")[1].split(" - ")[0]
                        to_date = orgElements[1][0].split(" · ")[1].split(" - ")[1]
                    elif((" - ") in orgElements[1][0]):
                        from_date = orgElements[1][0].split(" - ")[0]
                        to_date = orgElements[1][0].split(" - ")[1]
                        position= None
                    else:
                        position =orgElements[1][0]
                        from_date =None
                        to_date = None
                           
                for element in orgElements:
                    if("display-flex align-items-center" in element[1] and "Associated with" in element[0]):
                        association = element[0].split("Associated with ")[1]
                    else:
                        association = None
                    if("display-flex align-items-center" in element[1] and "Associated with" not in element[0]):
                        description = element[0]
                    else:
                        description = None

            elif(len(orgElements) == 1):
                name = orgElements[0][0]
                position=None
                from_date= None
                to_date= None
                association = None
                description = None
            else:
                name= None
                position=None
                from_date= None
                to_date= None
                association= None
                description= None

            organization = Organization(
                name= name,
                position=position,
                from_date= from_date,
                to_date= to_date,
                association= association,
                description= description,
            )
            self.add_organization(organization)


    def get_certifications(self, url = None, main_list=None, alreadyOnPage = False, pageIsConnectedToHome= False ):
        #print("CERT")
        if(url!=None and alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')

            linkSource = position.find_elements(By.CLASS_NAME,'pv2')
            if(len(linkSource)>0):
                url = linkSource[0].find_element(By.XPATH,"*").find_element(By.XPATH,"*").get_attribute("href")
            else:
                url =None
            
            title =  None
            issuer = None
            from_date =  None
            to_date = None
            credID = None
            expired = None
            associated_skills = None
            certElements =[]


            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               certElements.append([text,parentName])
            
            title = certElements[0][0]
            issuer = certElements[1][0]
                        
            for element in certElements:
                if("t-14 t-normal t-black--light" in element[1] and "Issued" in element[0] and " · " in element[0]):
                    from_date = (element[0].split(" · ")[0])[7:]
                    to_date = element[0].split(" · ")[1][8:]
                    if(element[0].split(" · ")[1][0:6] == "Expired"):
                        expired = "Yes"
                    else:
                        expired = "No"
                elif("t-14 t-normal t-black--light" in element[1] and "Issued" in element[0]):
                    from_date = element[0][7:]
                    to_date = None
                    expired = None

                if("t-14 t-normal t-black--light" in element[1] and "Credential ID" in element[0]):
                    credID = element[0][14:]

                if("display-flex align-items-center" in element[1] and "t-14 t-normal t-black" in element[1]):
                    associatedSkills = []
                    if("Skills:" in element[0]):
                        listOfSkills = element[0][7:]
                        for skill in listOfSkills.split(" · "):
                            associatedSkills.append(skill)
                        associatedSkillsStr= str(associatedSkills)[1:-1]
                    
                    if len(associatedSkills)>0:
                        associated_skills = associatedSkillsStr
                


            certification = Certification(
                title =  title,
                issuer = issuer,
                from_date =  from_date,
                to_date = to_date,
                expired = expired,
                credID = credID,
                url = url,
                associated_skills = associated_skills
            )
            self.add_certification(certification)
 



    def get_publications(self, url = None, main_list=None, alreadyOnPage = False, pageIsConnectedToHome= False ):
        #print("PUB")
        if(url!=None and alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
            
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')

            linkSource = position.find_elements(By.CLASS_NAME,'pv2')
            if(len(linkSource)>0):
                url = linkSource[0].find_element(By.XPATH,"*").find_element(By.XPATH,"*").get_attribute("href")
            else:
                url =None
            
            title= None
            publisher =None
            date= None
            url = None
            description= None
            publicationElements =[]

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               publicationElements.append([text,parentName])


            if len(publicationElements) > 1: 
                title = publicationElements[0][0]

                if(publicationElements[1][1]== "t-14 t-normal"):
                    if((" · ") in publicationElements[1][0]):
                        publisher = publicationElements[1][0].split(" · ")[0]
                        date = publicationElements[1][0].split(" · ")[1]
                    elif((",") in publicationElements[1][0]):
                        date = publicationElements[1][0]
                        publisher= None
                    else:
                        publisher =publicationElements[1][0]
                        date = None
                else:
                    publisher = None
                    date = None
                           
                for element in publicationElements:
                    if("display-flex align-items-center" in element[1] and "Associated with" not in element[0]):
                        description = element[0]
                    else:
                        description =None

            elif(len(publicationElements) == 1):
                title = publicationElements[0][0]
                publisher =None
                date = None
                description = None


            publication = Publication(
                title= title,
                publisher =publisher,
                date= date,
                url = url,
                description= description
            )
            self.add_publication(publication)


    def get_patents(self, url = None, main_list=None, alreadyOnPage = False, pageIsConnectedToHome= False ):
        #print("PAT")
        if(url!=None and alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')

            linkSource = position.find_elements(By.CLASS_NAME,'pv2')
            if(len(linkSource)>0):
                url = linkSource[0].find_element(By.XPATH,"*").find_element(By.XPATH,"*").get_attribute("href")
            else:
                url =None
            
            patentElements =[]

            title= None
            applicationNo = None
            status= None
            date= None
            description= None

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               patentElements.append([text,parentName])


            if len(patentElements) > 1: 
                title = patentElements[0][0]

                if(patentElements[1][1]== "t-14 t-normal"):
                    if((" · ") in patentElements[1][0]):
                        applicationNo = patentElements[1][0].split(" · ")[0]
                        dateAndStatus = patentElements[1][0].split(" · ")[1]
                        if("Filed" in dateAndStatus):
                            status = "Patent Pending"
                            date = dateAndStatus.split("Filed ")[1]
                        elif("Issued" in dateAndStatus):
                            status = "Patent Issued"
                            date = dateAndStatus.split("Issued ")[1]
                        
                    elif((",") in patentElements[1][0]):
                        date = patentElements[1][0].split(" · ")[1]
                        applicationNo= None
                    else:
                        applicationNo =patentElements[1][0]
                        date = None
                else:
                    applicationNo = None
                    date = None
                           
                for element in patentElements:
                    if("display-flex align-items-center" in element[1] and "Associated with" not in element[0]):
                        description = element[0]
                    else:
                        description =None

            elif(len(patentElements) == 1):
                title = patentElements[0][0]
                applicationNo = None
                status= None
                date= None
                description= None


            patent = Patent(
                title= title,
                applicationNo = applicationNo,
                status= status,
                date= date,
                url = url,
                description= description
            )
            self.add_patent(patent)


    def get_languages(self, url = None, main_list=None, alreadyOnPage = False, pageIsConnectedToHome= False):
        #print("LANG")
        if(url!=None or alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)

        
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')
            languageElements =[]

            lang= None
            proficiency = None

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               languageElements.append([text,parentName])


            if len(languageElements) > 1: 
                lang = languageElements[0][0]

                if(languageElements[1][1]=="t-14 t-normal t-black--light"):
                    proficiency = languageElements[1][0]

            elif(len(languageElements) == 1): 
                lang= languageElements[0][0]
                proficiency = None

            
            language = Language(
                lang = lang,
                proficiency = proficiency,
            )
            self.add_language(language)


    def get_honors(self, url = None, main_list=None, alreadyOnPage=False, pageIsConnectedToHome= False ):
        #print("HONORS")
        if(url!=None and alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)

        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome ==False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
                
                
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)


        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')
            honorElements =[]

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               honorElements.append([text,parentName])

            

            award =None
            issuer =None
            date = None
            association = None
            description = None

            if len(honorElements) > 1: 
                award = honorElements[0][0]

                if(honorElements[1][1]== "t-14 t-normal"):
                    if("Issued by" and "·" in honorElements[1][0]):
                        issuer= honorElements[1][0].split(" · ")[0]
                        issuer= issuer[9:]
                        date = honorElements[1][0].split(" · ")[1]
                    elif("Issued by" in honorElements[1][0]):
                        issuer= honorElements[1][0].split(" · ")[0]
                        issuer= issuer[9:]
                        date = None
                    else:
                        issuer =None
                        date = honorElements[1][0] 
                                   
                for element in honorElements:
                    if("display-flex align-items-center" in element[1] and "Associated with" in element[0]):
                        association = element[0]
                    else:
                        association = None
                    if("display-flex align-items-center" in element[1] and "Associated with" not in element[0]):
                        description = element[0]
                    else:
                        description = None

            elif(len(honorElements) == 1):
                award = honorElements[0][0]
                issuer =None
                date = None
                association = None
                description = None
            
            honor = Honor(
                award = award,
                issuer = issuer,
                date = date,
                association = association,
                description = description,
            )
            self.add_honor(honor)
        """if(random.random()<.15 and url != None):
            self.randPage()"""

        

    def get_skills(self, url = None, main_list=None, alreadyOnPage = False, pageIsConnectedToHome= False ):
        #print("SKILLS")
        if(url!=None and alreadyOnPage == False):
            
            self.driver.get(url)
            self.focus()
            main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
            #See if page is empty
            if(self.nothing_to_see_for_now_check()):
                return 0
            
            
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
        if(url == None and alreadyOnPage == True):
            if(pageIsConnectedToHome == False):
                self.focus()
                main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                #See if page is empty
                if(self.nothing_to_see_for_now_check()):
                    return 0
            
        
            
                main_list = self.wait_for_element_to_load(name="pvs-list", base=main)

        


            
        for position in main_list.find_elements(By.CLASS_NAME,"pvs-entity"):

            spans = position.find_elements(By.CLASS_NAME,'visually-hidden')
            skillElements =[]

            name= None
            usage = None

            for span in spans:
               parent = span.find_element(By.XPATH,"..")
               text= span.text
               parentName = parent.get_attribute("class")
               skillElements.append([text,parentName])

            if(len(skillElements) > 1):
                name = skillElements[0][0]
                usage = []
                for element in skillElements:
                    if("inline-show-more-text" in element[1]):
                        usage.append(element[0])
                if len(usage) == 0:
                    usage =None
                else:
                    usage = str(usage)

            elif(len(skillElements) == 1):
                name = skillElements[0][0]
                usage = None

            
            skill = Skill(
                name= name,
                usage = usage,
            )
            self.add_skill(skill)



    def get_name_and_location(self):
        top_panels = self.driver.find_elements(By.CLASS_NAME,"pv-text-details__left-panel")
        name = top_panels[0].find_elements(By.XPATH,"*")[0].text
        self.name = name.split("\n")[0]
        self.location = top_panels[1].find_element(By.TAG_NAME,"span").text


    def get_about(self):
        try:
            about = self.driver.find_element(By.ID,"about").find_element(By.XPATH,"..").find_element(By.CLASS_NAME,"display-flex").text
        except NoSuchElementException :
            about=None
        self.about = about

    def scrape_logged_in(self, close_on_complete=False):
        driver = self.driver
        duration = None

        root = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    By.CLASS_NAME,
                    self.__TOP_CARD,
                )
            )
        )
        self.focus()
        self.wait(1)

        # get name and location
        self.get_name_and_location()

        #self.open_to_work = self.is_open_to_work()
        # get about
        self.get_about()

        self.get_homepage()

        
        """funcLis = [self.get_experiences,self.get_educations,self.get_volunteering,self.get_honors,self.get_skills,self.get_publications,self.get_patents,self.get_languages,self.get_organizations,self.get_certifications,self.get_projects]
        random.shuffle(funcLis)

        for i in funcLis:
            self.wait(random.uniform(3, 5))
            i()"""


        # get connections
        """try:
            driver.get("https://www.linkedin.com/mynetwork/invite-connect/connections/")
            _ = WebDriverWait(driver, self.__WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "mn-connections"))
            )
            connections = driver.find_element(By.CLASS_NAME, "mn-connections")
            if connections is not None:
                for conn in connections.find_elements(By.CLASS_NAME, "mn-connection-card"):
                    anchor = conn.find_element(By.CLASS_NAME, "mn-connection-card__link")
                    url = anchor.get_attribute("href")
                    name = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__name").text.strip()
                    occupation = conn.find_element(By.CLASS_NAME, "mn-connection-card__details").find_element(By.CLASS_NAME, "mn-connection-card__occupation").text.strip()

                    contact = Contact(name=name, occupation=occupation, url=url)
                    self.add_contact(contact)
        except:
            connections = None"""

        if close_on_complete:
            driver.quit()

    @property
    def company(self):
        if self.experiences:
            return (
                self.experiences[0].institution_name
                if self.experiences[0].institution_name
                else None
            )
        else:
            return None

    @property
    def job_title(self):
        if self.experiences:
            return (
                self.experiences[0].position_title
                if self.experiences[0].position_title
                else None
            )
        else:
            return None

    def __repr__(self):

        personDict = {self.name :{"About" : self.about,"Experiences":{},"Educations":{},"Licenses_Certifications":{},"Volunteering_Experiences":{},"Skills":{},"Publications":{},"Patents":{},"Projects":{},"Honors_Awards":{},"Organizations":{},"Languages":{}}}

        count =0
        for dataClassMem in self.experiences:
            count +=1
            personDict[self.name]["Experiences"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Experiences"][count][field] = value
        
        count =0
        for dataClassMem in self.educations:
            count +=1
            personDict[self.name]["Educations"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Educations"][count][field] = value
        
        count =0
        for dataClassMem in self.certification:
            count +=1
            personDict[self.name]["Licenses_Certifications"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Licenses_Certifications"][count][field] = value
        
        count =0
        for dataClassMem in self.volunteering:
            count +=1
            personDict[self.name]["Volunteering_Experiences"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Volunteering_Experiences"][count][field] = value
        
        count =0
        for dataClassMem in self.skill:
            count +=1
            personDict[self.name]["Skills"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Skills"][count][field] = value

        count =0
        for dataClassMem in self.publication:
            count +=1
            personDict[self.name]["Publications"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Publications"][count][field] = value

        count =0
        for dataClassMem in self.patent:
            count +=1
            personDict[self.name]["Patents"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Patents"][count][field] = value
        
        count =0
        for dataClassMem in self.projects:
            count +=1
            personDict[self.name]["Projects"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Projects"][count][field] = value

        
        count =0
        for dataClassMem in self.honors:
            count +=1
            personDict[self.name]["Honors_Awards"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Honors_Awards"][count][field] = value
        
        count =0
        for dataClassMem in self.organization:
            count +=1
            personDict[self.name]["Organizations"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Organizations"][count][field] = value
        
        count =0
        for dataClassMem in self.langauge:
            count +=1
            personDict[self.name]["Languages"][count] = {}
            for field in dataClassMem.__dataclass_fields__:
                value = getattr(dataClassMem, field)
                personDict[self.name]["Languages"][count][field] = value
        
        json_object = json.dumps(personDict, indent = 4) 
        return json_object
        
