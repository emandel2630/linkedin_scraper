import json
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from .objects import Experience, Education, Scraper, Honor, Project, Volunteer, Skill, Organization, Publication, Patent, Language, Certification
from .employer import Employer
import os
from linkedin_scraper import selectors
from dateutil.parser import parse
import random
import pygetwindow as gw



from selenium.webdriver.common.action_chains import ActionChains
import time
"""
def random_scroll_and_mouse_movement(driver):

    # Get scroll height.
    last_height = driver.execute_script("return document.body.scrollHeight")

    actions = ActionChains(driver)

    while True:
        # Generate a random scroll position within the bounds of the page height.
        random_scroll_position = random.randint(0, last_height)
        
        # Scroll down to the random position.
        driver.execute_script(f"window.scrollTo(0, {random_scroll_position});")

        # Wait to load page. Adjust this to your preferred range.
        time.sleep(random.uniform(0.5, 1.0))

        # Calculate new scroll height and compare with last scroll height.
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # If height didn't change, break out of the loop.
        if new_height == last_height:
            break

        last_height = new_height

        # Generate random X and Y coordinates within the dimensions of the window.
        random_x = random.randint(0, driver.get_window_size()["width"])
        random_y = random.randint(0, driver.get_window_size()["height"])

        # Move the mouse to the random position on the screen.
        actions.move_by_offset(random_x, random_y).perform()
        actions.reset_actions()
"""
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
class Person(Scraper):

    __TOP_CARD = "pv-top-card"
    __WAIT_FOR_ELEMENT_TIMEOUT = 1000

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


    def get_experiences(self):
        url = os.path.join(self.linkedin_url, "details/experience")
        self.driver.get(url)


        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        #random_scroll_and_mouse_movement(self.driver)
        """self.random_linear_scroll()
        """
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
        if(random.random()<.15):
            self.randPage()
        

        for dataClassMem in listOfExp:
            linkedin_url = getattr(dataClassMem, "linkedin_url")
            institution_desc = None
            industry = None
            institution_size = None
            institution_url = None
            institution_specialties = None

            """if(linkedin_url!= None and "/company/" in linkedin_url):
                url = linkedin_url + "about"
                self.driver.get(url)


                self.focus()
                main = None
                try:
                    main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
                except:
                    print("Page Unavailable")
                
                industry = None
                institution_desc = None
                institution_size = None
                institution_specialties = None
                institution_url = None
                if(main!= None):
                    self.random_linear_scroll()
                    
                    main_list= self.wait_for_element_to_load(name="mb6", base=main)
                    pageList = main_list.find_elements(By.CLASS_NAME,'ember-view')


                    overviewPage = None
                    for x in pageList:
                        if(x.get_attribute("class") == "ember-view"):
                            overviewPage = x
                            break
                        


                    desiredSection = overviewPage.find_element(By.CLASS_NAME,"artdeco-card").text
                    companyAbout = desiredSection.split("\n")

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
                            institution_specialties = companyAbout[i+1]"""


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
                try: #Hot fix for employer bugs. Actually improve this later. Thanks me from the future
                    company = Employer(linkedin_url = linkedin_url,driver=self.driver)
                    if(str(company) != ""):
                        companyDict = json.loads(str(company))
                        institution_desc = companyDict[key]["Description"]
                        industry = companyDict[key]["Industry"]
                        institution_size = companyDict[key]["Company Size"]
                        institution_url = companyDict[key]["Employer Url"]
                        institution_specialties = companyDict[key]["Specialities"]
                        json_append("Employer_Database.json",companyDict)
                except:
                    print(linkedin_url + " failed to scrape")
                    

            

            setattr(dataClassMem,"institution_desc", institution_desc)
            setattr(dataClassMem,"industry", industry)
            setattr(dataClassMem,"institution_url", institution_url)
            setattr(dataClassMem,"institution_size", institution_size)
            setattr(dataClassMem,"institution_specialties", institution_specialties)


            self.add_experience(dataClassMem)
            
                        
                


    def get_educations(self):
        url = os.path.join(self.linkedin_url, "details/education")
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")

        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        
        self.random_linear_scroll()


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

        if(random.random()<.15):
            self.randPage()
        
            

    def get_volunteering(self):
        url = os.path.join(self.linkedin_url, "details/volunteering-experiences")
        self.driver.get(url)
        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")

        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        
        self.random_linear_scroll()
        
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
        if(random.random()<.15):
            self.randPage()
    

    def get_projects(self):
        url = os.path.join(self.linkedin_url, "details/projects")
        self.driver.get(url)


        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")

        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        self.random_linear_scroll()
        
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
        if(random.random()<.15):
            self.randPage()

    def get_organizations(self):
        url = os.path.join(self.linkedin_url, "details/organizations")
        self.driver.get(url)


        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")

        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        self.random_linear_scroll()
        
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
        if(random.random()<.15):
            self.randPage()

    def get_certifications(self):
        url = os.path.join(self.linkedin_url, "details/certifications")
        self.driver.get(url)


        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")

        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        self.random_linear_scroll()
        
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
        if(random.random()<.15):
            self.randPage()


    def get_publications(self):
        url = os.path.join(self.linkedin_url, "details/publications")
        self.driver.get(url)


        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")

        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        self.random_linear_scroll()
        
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
        if(random.random()<.15):
            self.randPage()

    def get_patents(self):
        url = os.path.join(self.linkedin_url, "details/patents")
        self.driver.get(url)


        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")

        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        self.random_linear_scroll()
        
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
        if(random.random()<.15):
            self.randPage()

    def get_languages(self):
        url = os.path.join(self.linkedin_url, "details/languages")
        self.driver.get(url)


        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        self.random_linear_scroll()
        
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
        if(random.random()<.15):
            self.randPage()

    def get_honors(self):
        url = os.path.join(self.linkedin_url, "details/honors")
        self.driver.get(url)


        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        self.random_linear_scroll()
        
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
        if(random.random()<.15):
            self.randPage()

    def get_skills(self):
        url = os.path.join(self.linkedin_url, "details/skills")
        self.driver.get(url)


        self.focus()
        main = self.wait_for_element_to_load(by=By.TAG_NAME, name="main")
        #See if page is empty
        if(self.nothing_to_see_for_now_check()):
            return 0
        self.random_linear_scroll()
        

        

        try:
            main_list = self.wait_for_element_to_load(name="pvs-list", base=main)
            
        except:
            return
            
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

        if(random.random()<.15):
            self.randPage()

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

        self.random_linear_scroll()

        #self.open_to_work = self.is_open_to_work()

        # get about
        self.get_about()

        
        funcLis = [self.get_experiences,self.get_educations,self.get_volunteering,self.get_honors,self.get_skills,self.get_publications,self.get_patents,self.get_languages,self.get_organizations,self.get_certifications,self.get_projects]
        random.shuffle(funcLis)

        for i in funcLis:
            self.wait(random.uniform(3, 5))
            i()


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
        
