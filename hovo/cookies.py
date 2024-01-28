__package__ = 'hovo'

import json
import sys
from datetime import datetime, timedelta
from time import sleep

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from hovo import option

ISSUETRACKER_URL = 'https://partnerissuetracker.corp.google.com/'
COOKIES_FILE = 'cookies.json'
cookies = []
session = None
x_xsrf_token=""

def cookie_is_fresh(cookie):
    # Extract expiration date from the cookie
    if not 'expiry' in cookie:
        return True  # uh...
    expiration_timestamp = cookie['expiry']
    # Convert the timestamp to a datetime object
    expiration_datetime = datetime.utcfromtimestamp(expiration_timestamp)
    # Get the current UTC time
    current_datetime = datetime.utcnow()
    # Compare the expiration date with the current date
    return current_datetime < expiration_datetime - timedelta(hours=1)

def get_cookies():
    """Return fresh cookies for retrieving the Partner IssueTracker URL

    Returns:
        A list of cookies.
    """
    global cookies
    global session
    if option.refresh_cookies:
        cookies = []
    else:
        try:
            with open(COOKIES_FILE, 'r') as file:
                cookies = json.load(file)
        except FileNotFoundError:
            cookies = []

        for cookie in cookies:
            if not cookie_is_fresh(cookie):
                cookies = []
                break

    if len(cookies) == 0:
        # Start a new browser session
        driver = webdriver.Chrome()

        # Navigate to the login page
        driver.get(ISSUETRACKER_URL)

        # Set username
        if False:  # (Turn to True to activate)
            username_input = driver.find_element(By.NAME, 'identifier')
            username_input.send_keys('firstname.lastname@s3ns.io')
            username_input.send_keys(Keys.RETURN)

        # Set password
        if False:  # (Turn to True to activate)
            driver.implicitly_wait(5)
            password_input = driver.find_element(By.NAME, 'Passwd')
            password_input.send_keys('password')
            password_input.send_keys(Keys.RETURN)

        # Click "Try another way"
        while False:  # (Turn to True to activate)
            try:
                sleep(0.5)
                try_another_way_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[text()='Try another way']"))
                )
                try_another_way_link.click()
                break
            except:
                continue
            
        # Click "Use your Security Key"
        while False:  # (Turn to True to activate)
            try:
                sleep(0.5)
                use_your_key_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[text()='Use your Security Key']"))
                )
                use_your_key_link.click()
                break
            except:
                continue
            
        # Click the "Next" button
        while False:  # (Turn to True to activate)
            try:
                sleep(0.5)
                next_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//span[text()='Next']"))
                )
                next_link.click()
                break
            except:
                continue

        # Wait until the user has authenticated
        while True:
            try:
                sleep(0.5)
                issue_tracker_link = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//h1[text()='Partner IssueTracker']"))
                )
                issue_tracker_link.click()
                break
            except:
                continue

        cookies = driver.get_cookies()
        driver.quit()

    with open(COOKIES_FILE, 'w') as file:
        json.dump(cookies, file)


    # Create a requests session
    session = requests.Session()
    # Add cookies to the requests session
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    return

    # Create a requests session
    session = requests.Session()

    # Add cookies to the requests session
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])


    # Make a request using the requests session
    response = session.get('https://partnerissuetracker.corp.google.com/issues/304809707')

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        print("Successfully accessed the protected URL")
        print(len(response.text))
    else:
        print(f"Failed to access the protected URL. Status code: {response.status_code}")

    sys.exit(0)
    return