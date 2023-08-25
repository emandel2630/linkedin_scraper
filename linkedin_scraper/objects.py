from dataclasses import dataclass
from time import sleep

from selenium.webdriver import Chrome

from . import constants as c

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
from pyHM import mouse
import ctypes
from ctypes_window_info import get_window_infos
import pyautogui



@dataclass
class Contact:
    name: str = None
    occupation: str = None
    url: str = None

@dataclass
class Honor:
    award: str = None
    issuer: str = None
    date: str = None
    association: str = None
    description: str = None

@dataclass
class Project:
    name: str = None
    from_date: str = None
    to_date: str = None
    url: str = None
    association: str = None
    description: str = None

@dataclass
class Organization:
    name: str = None
    position: str =None
    from_date: str = None
    to_date: str = None
    association: str = None
    description: str = None

@dataclass
class Skill:
    name: str = None
    usage: str = None

@dataclass
class Language:
    lang: str = None
    proficiency: str =None

@dataclass
class Publication:
    title: str = None
    publisher: str =None
    date: str = None
    url: str = None
    description: str = None

@dataclass
class Certification:
    title: str = None
    issuer: str =None
    from_date: str = None
    to_date: str = None
    expired: str = None
    credID: str = None
    url: str = None
    associated_skills: str = None

@dataclass
class Patent:
    title: str = None
    applicationNo: str =None
    status: str = None
    url: str = None
    date: str = None
    description: str = None

@dataclass
class Institution:
    institution_name: str = None
    linkedin_url: str = None
    website: str = None
    industry: str = None
    type: str = None
    headquarters: str = None
    company_size: int = None
    founded: int = None

@dataclass
class Hirer:
    company_name: str = None
    industry: str = None
    institution_size: str = None
    institution_desc: str = None
    institution_specialities: str = None
    institution_url: str = None
    linkedin_url: str = None


@dataclass
class Volunteer:
    organization: str = None
    role: str = None
    cause: str = None
    from_date: str = None
    to_date: str = None
    duration: str = None
    url: str = None
    description: int = None

@dataclass
class Experience:
    position_title: str = None
    institution_name: str = None
    industry: str = None
    from_date: str = None
    to_date: str = None
    duration: str = None
    location: str = None
    location_type: str = None
    employment_type: str = None
    description: str = None
    associated_skills: str = None
    linkedin_url: str = None
    institution_desc: str = None
    institution_size: str =None
    institution_specialties: str = None
    institution_url: str = None
    

@dataclass
class Education:
    institution_name: str = None
    degree: str = None
    from_date: str = None
    to_date: str = None
    grade: str = None
    activities: str = None
    description: str = None
    associated_skills: str =None
    linkedin_url: str = None


@dataclass
class Interest(Institution):
    title = None


@dataclass
class Accomplishment(Institution):
    category = None
    title = None


@dataclass
class Scraper:
    driver: Chrome = None
    WAIT_FOR_ELEMENT_TIMEOUT = 15
    TOP_CARD = "pv-top-card"

    @staticmethod
    def wait(duration):
        sleep(int(duration))

    def focus(self):
        self.driver.execute_script('alert("Focus window")')
        self.driver.switch_to.alert.accept()

    def mouse_click(self, elem):
        action = webdriver.ActionChains(self.driver)
        action.move_to_element(elem).perform()

    def wait_for_element_to_load(self, by=By.CLASS_NAME, name="pv-top-card", base=None):
        base = base or self.driver
        return WebDriverWait(base, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    by,
                    name
                )
            )
        )

    def wait_for_all_elements_to_load(self, by=By.CLASS_NAME, name="pv-top-card", base=None):
        base = base or self.driver
        return WebDriverWait(base, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
            EC.presence_of_all_elements_located(
                (
                    by,
                    name
                )
            )
        )


    def is_signed_in(self):
        try:
            WebDriverWait(self.driver, self.WAIT_FOR_ELEMENT_TIMEOUT).until(
                EC.presence_of_element_located(
                    (
                        By.CLASS_NAME,
                        c.VERIFY_LOGIN_ID,
                    )
                )
            )

            self.driver.find_element(By.CLASS_NAME, c.VERIFY_LOGIN_ID)
            return True
        except Exception as e:
            pass
        return False

    def scroll_to_half(self):
        self.driver.execute_script(
            "window.scrollTo(0, Math.ceil(document.body.scrollHeight/2));"
        )
        
    def get_browser_window_coords(self,browserKeyword):
        boundingbox = (0, 0, 0, 0)

        for g in get_window_infos():
            if "Chrome_WidgetWin" in g.class_name:
                if sum(g.coords_win) > 0:
                    if(browserKeyword in g.windowtext):
                        boundingbox = (
                            g.coords_win[0],
                            g.coords_win[2],
                            g.coords_win[1],
                            g.coords_win[3],
                        )
                        break
        
        offset_x = boundingbox[0]
        offset_y = boundingbox[1]
        height = boundingbox[3] - boundingbox[1]
        width = boundingbox[2] - boundingbox[0]
        center = offset_x + width // 2, offset_y + height // 2
        vara = {
            "offset_x": offset_x,
            "offset_y": offset_y,
            "height": height,
            "width": width,
            "center": center,
        }
        if(boundingbox == (0,0,0,0)):
            vara = None
            return vara
        else:
            return vara


    def find_color_position(self,color, topLeft,bottomRight):
        time.sleep(1)

        # Capture the screen image
        screenshot = pyautogui.screenshot()

        # Loop through each pixel to find the desired color
        for x in range(topLeft[0],bottomRight[0]):
            for y in range(topLeft[1],bottomRight[1]):
                pixel_color = screenshot.getpixel((x, y))
                if pixel_color == color:
                    return [x,y]
        

        return None


    

    def slow_scroll_to_element(self, element, increment = None):
        # Get the current scroll position
        scroll_y = self.driver.execute_script("return window.scrollY;")
        
        # Get the position of the element
        element_y = element.location['y']
        
        # Calculate the viewport height
        viewport_height = self.driver.execute_script("return window.innerHeight;")
        
        # Check if the element's top is within the viewport
        if scroll_y <= element_y <= scroll_y + viewport_height:
            return
        
        document_height = self.driver.execute_script("return document.documentElement.scrollHeight;")
        inner_width = self.driver.execute_script("return window.innerWidth;")
        
        # Calculate the scroll direction (up or down)
        scroll_direction = -1 if element_y < scroll_y else 1
        
        # Scroll slowly to the element using JavaScript with delays
        if increment ==None:
            scroll_increment = random.randint(15,20)
        else:
            scroll_increment = increment  
        scroll_duration = random.uniform(.005,.01)
        total_scroll = abs(element_y - scroll_y - viewport_height // 2)  # Total amount of scroll needed
        current_scroll = 0  # Current scroll position

        # Scroll until the element is in view
        while current_scroll < total_scroll:
            # Calculate the remaining scroll and the scroll amount for this increment
            remaining_scroll = total_scroll - current_scroll
            scroll_amount = min(scroll_increment, remaining_scroll) * scroll_direction

            # Calculate the new scroll position
            new_scroll_position = current_scroll + abs(scroll_amount)
            if new_scroll_position > total_scroll:
                scroll_amount = remaining_scroll * scroll_direction

            # Execute the JavaScript scroll with the scroll amount
            self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_amount)

            # Wait for the scroll to take effect
            time.sleep(scroll_duration)

            # Update the current scroll position
            current_scroll += abs(scroll_amount)

            # Check if the bounds of the webpage are reached
            if current_scroll >= document_height or current_scroll <= 0:
                break

    def slow_scroll_to_bottom(self, increment= None):
        inner_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        viewport_height = self.driver.execute_script("return window.innerHeight")
        if increment ==None:
            scroll_increment = random.randint(15,20)
        else:
            scroll_increment = increment  
        scroll_duration = random.uniform(.005,.01)  # Duration of each scroll increment (in seconds)
        current_scroll = 0  # Current scroll position

        # Scroll until the bottom of the page is reached
        while current_scroll < inner_height - viewport_height:
            # Calculate the remaining scroll and the scroll amount for this increment
            remaining_scroll = inner_height - viewport_height - current_scroll
            scroll_amount = min(scroll_increment, remaining_scroll)

            # Execute the JavaScript scroll with the scroll amount
            self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_amount)

            # Wait for the scroll to take effect
            time.sleep(scroll_duration)

            # Update the current scroll position
            current_scroll += scroll_amount

    
    def random_scroll(self,increment=None):
        document_height = self.driver.execute_script("return document.documentElement.scrollHeight;")
        viewport_height = self.driver.execute_script("return window.innerHeight;")
        
        # Calculate the maximum scroll position
        max_scroll_y = document_height - viewport_height

        # Scroll randomly around the page
        if increment ==None:
            scroll_increment = random.randint(15,20)
        else:
            scroll_increment = increment  
        scroll_duration = random.uniform(.005,.01)
        num_scrolls = random.randint(1,5)

        total =0
        while total<= num_scrolls:
            # Calculate a random scroll position
            target_scroll_y = random.randint(0, max_scroll_y)

            # Get the current scroll position
            current_scroll_y = self.driver.execute_script("return window.scrollY;")
            
            # Calculate the scroll direction (up or down)
            scroll_direction = -1 if target_scroll_y < current_scroll_y else 1

            # Calculate the total amount of scroll needed
            total_scroll = abs(target_scroll_y - current_scroll_y)
            current_scroll = 0  # Current scroll position

            # Scroll to the target position
            while current_scroll < total_scroll:
                # Calculate the remaining scroll and the scroll amount for this increment
                remaining_scroll = total_scroll - current_scroll
                scroll_amount = min(scroll_increment, remaining_scroll) * scroll_direction

                # Calculate the new scroll position
                new_scroll_position = current_scroll + abs(scroll_amount)
                if new_scroll_position > total_scroll:
                    scroll_amount = remaining_scroll * scroll_direction

                # Execute the JavaScript scroll with the scroll amount
                self.driver.execute_script("window.scrollBy(0, arguments[0]);", scroll_amount)

                # Wait for the scroll to take effect
                time.sleep(scroll_duration)

                # Update the current scroll position
                current_scroll += abs(scroll_amount)

                total+=1
            time.sleep(2)


        





    def position_of_click(self, element,browserKeyword):
        time.sleep(1)

        browserCoords = self.get_browser_window_coords(browserKeyword)
        if(browserCoords != None):
            topLeft = [browserCoords["offset_x"], browserCoords["offset_y"]]
            bottomRight = [browserCoords["offset_x"]+browserCoords["width"], browserCoords["offset_y"]+browserCoords["height"]]
        else:
            return None


        
        self.slow_scroll_to_element(element)

        blueBlock = '''
        var blueBlock = document.createElement('div');
        blueBlock.style.width = '100%';
        blueBlock.style.height = '100%';
        blueBlock.style.backgroundColor = 'blue';
        blueBlock.style.position = 'fixed';
        blueBlock.style.top = '0';
        blueBlock.style.left = '0';
        blueBlock.style.zIndex = '9999';
        document.body.appendChild(blueBlock);
        '''
        self.driver.execute_script(blueBlock)

        redDot = """
                    var dot = document.createElement('div');
                    dot.style.height = '10px';
                    dot.style.width = '10px';
                    dot.style.background = '#FE0101';
                    dot.style.position = 'absolute';
                    dot.style.top = arguments[0] + 'px';
                    dot.style.left = arguments[1] + 'px';
                    document.body.appendChild(dot);
                    dot.id = 'click-dot';
                    dot.style.zIndex = '999999';
                    """

        # Execute the script to create the dot at the element location
        self.driver.execute_script(redDot, element.location['y']+5, element.location['x']+15)

        target_color = (254, 1, 1)  # Red color

        position = self.find_color_position(target_color, topLeft,bottomRight)

        self.driver.execute_script("var blueBlock = document.querySelector('div[style*=\"background-color: blue;\"]'); if(blueBlock) blueBlock.remove();")
        remove_script = "var dot = document.getElementById('click-dot'); if(dot) dot.remove();"
        self.driver.execute_script(remove_script)

        return position


    def random_mouse_movement(self,browserKeyword,numMoves=1):
        browserCoords = self.get_browser_window_coords(browserKeyword)
        if(browserCoords != None):
            topLeft = [browserCoords["offset_x"], browserCoords["offset_y"]]
            bottomRight = [browserCoords["offset_x"]+browserCoords["width"], browserCoords["offset_y"]+browserCoords["height"]]
            try:
                for i in range(0,numMoves):
                    mouse.move(random.uniform(topLeft[0], bottomRight[0]), random.uniform(topLeft[1], bottomRight[1]), random.uniform(.75, 1.1))
                    time.sleep(.5)
            except:
                pass

    def click_or_rand_move(self, pos, element, browserKeyword,numRandMoves):
        if(pos!= None):
            current_url = self.driver.current_url
            try:
                mouse.move(pos[0]+20,pos[1]+5,random.gauss(.55,.7))
                mouse.click()
            except:
                print("Click Failed")

            time.sleep(4)
            new_url = self.driver.current_url

            if(current_url == new_url):
                print("Click missed")
                url = element.get_attribute('href')

                #self.random_mouse_movement(browserKeyword,numRandMoves)
                return url

            else:
                return None
        else:
            url = element.get_attribute('href')
            self.random_mouse_movement(browserKeyword,numRandMoves)
            return url
        




            
    def randPage(self):
        #Timeout Error
       # find all the 'a' elements (links) on the page
        links = self.driver.find_elements(By.TAG_NAME, 'a')

        # get a list of all the href attributes of the found 'a' elements
        links = [link.get_attribute('href') for link in links if link.get_attribute('href') is not None]

        # choose a random link
        random_link = random.choice(links)

        # navigate to the random link
        self.driver.get(random_link)

        time.sleep(1)
        # if(random.random()>.3):
        #     for i in range(random.randint(1,3)):
        #         time.sleep(.5)
        #         mouse.move(random.gauss(2560/2, 400), random.gauss(1440/2, 200),multiplier=random.uniform(.35,.55))

        

    #Click home
   #artdeco-button artdeco-button--circle artdeco-button--muted artdeco-button--3 artdeco-button--tertiary ember-view 
    def nothing_to_see_for_now_check(self):
        time.sleep(random.uniform(1,1.5)) 
        emptyCheck=self.driver.find_elements(By.CSS_SELECTOR, ".full-width.artdeco-empty-state.ember-view")

        #Random number uniformly distributed between 1 and 1.5
        if(len(emptyCheck)>0):
            return True
        else:
            return False

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);"
        )

    def scroll_class_name_element_to_page_percent(self, class_name:str, page_percent:float):
        self.driver.execute_script(
            f'elem = document.getElementsByClassName("{class_name}")[0]; elem.scrollTo(0, elem.scrollHeight*{str(page_percent)});'
        )

    def __find_element_by_class_name__(self, class_name):
        try:
            self.driver.find_element(By.CLASS_NAME, class_name)
            return True
        except:
            pass
        return False

    def __find_element_by_xpath__(self, tag_name):
        try:
            self.driver.find_element(By.XPATH,tag_name)
            return True
        except:
            pass
        return False

    def __find_enabled_element_by_xpath__(self, tag_name):
        try:
            elem = self.driver.find_element(By.XPATH,tag_name)
            return elem.is_enabled()
        except:
            pass
        return False

    @classmethod
    def __find_first_available_element__(cls, *args):
        for elem in args:
            if elem:
                return elem[0]




"""driver = webdriver.Chrome()
driver.get("https://en.wikipedia.org/wiki/Miles_Davis")
element = driver.find_element(By.CLASS_NAME, "infobox-caption").find_element(By.TAG_NAME,'a')
x = Scraper(driver=driver)

pos = x.position_of_click(element, "Miles")
x.click_or_rand_move(pos,element,"Miles",random.randint(1,5))
x.slow_scroll_to_bottom()
time.sleep(2)
driver.quit()"""
