__package__ = 'hovo'

import json
from datetime import datetime, timedelta
from time import sleep
import time

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException

from hovo import dot_user, option


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
    # Take some margin so that we are sure we won't be interrupted
    return current_datetime < expiration_datetime - timedelta(minutes=5)

def get_cookies(cookies_path, url):
    """Return a session with valid cookies.

    Returns:
        A session.
    """
    if option.refresh_cookies:
        cookies = []
    else:
        try:
            with open(cookies_path, 'r') as file:
                cookies = json.load(file)
        except FileNotFoundError:
            cookies = []

        for cookie in cookies:
            if not cookie_is_fresh(cookie):
                cookies = []
                break

    if len(cookies) == 0:
        with open(dot_user.PASSWD_PATH, 'r') as f:
            user = json.load(f)

        # Start a new browser session
        driver = webdriver.Chrome()

        # Navigate to the login page
        driver.get(url)

        # Set username
        if True:  # (Turn to True to activate)
            username_input = driver.find_element(By.NAME, 'identifier')
            username_input.send_keys(f"{user['login']}")
            username_input.send_keys(Keys.RETURN)

        # Set password
        if True:  # (Turn to True to activate)
            driver.implicitly_wait(5)
            password_input = driver.find_element(By.NAME, 'Passwd')
            password_input.send_keys(f"{user['passwd']}")
            password_input.send_keys(Keys.RETURN)

        # Click "Try another way"
        while True:  # (Turn to True to activate)
            driver.implicitly_wait(5)
            try:
                try_another_way_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[contains(., 'Try another way')]")))
            except Exception as e:
                print(f"Exception1: {str(e)}")
                sleep(0.5)
                continue
            try:
                sleep(2)
                try_another_way_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[contains(., 'Try another way')]")))
                try_another_way_link.click()
                break
            except Exception as e:
                print(f"Exception2: {str(e)}")
                continue
            
        # Click "Use your Security Key"
        while True:  # (Turn to True to activate)
            driver.implicitly_wait(5)
            try:
                use_your_key_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[text()='Use your Security Key']")))
            except Exception as e:
                print(f"Exception3: {str(e)}")
                sleep(0.5)
                continue
            try:
                sleep(1.5)
                use_your_key_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//div[text()='Use your Security Key']")))
                use_your_key_link.click()
                break
            except Exception as e:
                print(f"Exception4: {str(e)}")
                continue
            
        # Click the "Next" button
        while True:  # (Turn to True to activate)
            driver.implicitly_wait(5)
            try:
                sleep(0.5)
                next_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[contains(., 'Next')]")))
            except Exception as e:
                print(f"Exception5: {str(e)}")
                sleep(0.5)
                continue
            try:
                sleep(1.5)
                next_link = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//button[contains(., 'Next')]")))
                next_link.click()
                break
            except Exception as e:
                print(f"Exception6: {str(e)}")
                continue

        # Wait until the user has authenticated
        while False:
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

        # FIXME: we need to sleep so that the Partner Issue Tracker page
        # gets fully loaded including all necessary cookies.
        # Rather than waiting for 5 sec, we should be waiting for some
        # pattern.
        time.sleep(5)
        cookies = driver.get_cookies()
        driver.quit()
        with open(cookies_path, 'w') as f:
            json.dump(cookies, f)

    # Create a requests session
    session = requests.Session()
    # Add cookies to the requests session
    for cookie in cookies:
        session.cookies.set(cookie['name'], cookie['value'])

    return session