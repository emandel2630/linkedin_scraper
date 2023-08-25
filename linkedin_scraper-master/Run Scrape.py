from linkedin_scraper import Person, actions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import json

#options = webdriver.ChromeOptions()
#options.add_argument("headless")
driver = webdriver.Chrome()#options=options

email = #EMAIL
password = #Password


actions.login(driver, email, password,timeout= 30) # if email and password isnt given, it'll prompt in terminal
#person = Person("https://www.linkedin.com/in/joey-sham-aa2a50122", driver=driver)
person = Person("https://www.linkedin.com/in/ethan-mandel-61b549221/", driver=driver)
#person = Person("https://www.linkedin.com/in/jordanzucker/", driver=driver)
#person = Person("https://www.linkedin.com/in/joey-sham-aa2a50122", driver=driver)

print(str(person))

personDict = json.loads(str(person))


with open("Output.json", "w", encoding= "utf-8") as outfile:
    json.dump(personDict, outfile, indent= 4)

"""with open("Output.txt", "w", encoding="utf-8") as text_file:
    text_file.write(str(person))"""

