from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = ""

def initialise_driver():
    global driver 
    driver = webdriver.Chrome()

def login(username,password):
    global driver
    driver.get("https://app.pyaribitiya.in/login")
    driver.maximize_window()
    
    username_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[1]/input")
    username_input.send_keys()
    time.sleep(0.5)
    password_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[2]/input")
    password_input.send_keys()

    time.sleep(1)

    login_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[3]/button")
    login_button.click()


def fill_form(patient_data):
    pass

