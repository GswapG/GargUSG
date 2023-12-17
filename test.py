from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://app.pyaribitiya.in/login")

#SET USERNAME AND PASSWORD HERE
username = ""
password = ""

username_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[1]/input")
username_input.send_keys()
time.sleep(0.5)
password_input = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[2]/input")
password_input.send_keys()

time.sleep(1)

login_button = driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[3]/button")
login_button.click()

time.sleep(5)

driver.quit()