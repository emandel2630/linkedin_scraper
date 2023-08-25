import getpass
from . import constants as c
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import json
import time

def __prompt_email_password():
  u = input("Email: ")
  p = getpass.getpass(prompt="Password: ")
  return (u, p)

def page_has_loaded(driver):
    page_state = driver.execute_script('return document.readyState;')
    return page_state == 'complete'

def login(driver, email=None, password=None, cookies = None, timeout=60, botnum =-1):
    if cookies is not None:
        cookieSuccess = _login_with_cookie(driver, cookies)
        if(cookieSuccess == True):
            print("MMM Cookie")
            return True

    driver.delete_all_cookies() 
    driver.refresh()
    print("Cookies cleared")
    time.sleep(4)
    

    if not email or not password:
        email, password = __prompt_email_password()
  
    driver.get("https://www.linkedin.com/login")
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "username")))
  
    email_elem = driver.find_element(By.ID,"username")
    email_elem.send_keys(email)
  
    password_elem = driver.find_element(By.ID,"password")
    password_elem.send_keys(password)
    password_elem.submit()

    time.sleep(20)
  
    if driver.current_url == 'https://www.linkedin.com/checkpoint/lg/login-submit':
        remember = driver.find_element(By.ID,c.REMEMBER_PROMPT)
        if remember:
            remember.submit()
  
    element = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.CLASS_NAME, c.VERIFY_LOGIN_ID)))
    time.sleep(5)
    cookies = driver.get_cookies()
    if(botnum ==-1):
        with open("cookies.json", 'w') as filehandler:
            json.dump(cookies, filehandler)
    else:
        with open('cookies_' + str(botnum) + ".json", "w") as filehandler:
            json.dump(cookies, filehandler)

    time.sleep(2)
    if(str(driver.current_url) == "https://www.linkedin.com/login"):
        return False
    else:
        print("Login Success")
        return True
    
  
def _login_with_cookie(driver, cookies):
    driver.get("https://www.linkedin.com/login")
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.refresh()
    time.sleep(5)

    if(str(driver.current_url) == "https://www.linkedin.com/login"):
        driver.get("https://www.linkedin.com/login")
        driver.refresh()
        print("Cookie Failure")
        return False
    else:
        return True

    


