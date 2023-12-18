from selenium import webdriver
from selenium.webdriver.common.by import By
import time

class filler_helper():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def login(self,username,password):
        self.driver.get("https://app.pyaribitiya.in/login")
        self.driver.maximize_window()

        username_input = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[1]/input")
        username_input.send_keys(username)
        time.sleep(0.5)
        password_input = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[2]/input")
        password_input.send_keys(password)

        time.sleep(1)

        login_button = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[3]/button")
        login_button.click()

        time.sleep(5)
        self.driver.quit()
    
    def fill_form(self):
        pass

