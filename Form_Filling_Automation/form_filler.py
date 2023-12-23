from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from datetime import datetime
import excel_assist

##STEP 1
#Date : //*[@id="EntryDate"]
#Patient Name : //*[@id="PatientName"]
#Age : //*[@id="PatientAge"]
#Do you have children:  //*[@id="add_child"]
#child age XPATH format : //input[@name="child[name][number]"] {number starts from 0}
#child gender XPATH format : //input[@name="child[gender][number]" and @value="M/F"] {value is M for male, F for female}
#add child button : //*[@id="add_child_row"]
#Husband name : //*[@id="FatherName"]
#Address: //*[@id="step-1"]/div[7]/div/textarea
#Contact number: //*[@id="step-1"]/div[8]/div/input
#Next button : //*[@id="step-1"]/div[10]/div/div[2]/button

##STEP2
#Name of doctor(refered) : //*[@id="DoctorName"]
#Address of doctor : //*[@id="DoctorAddress"]
#Weeks of pregnancy : //*[@id="Pregnancy"]
#Next button : //*[@id="step-2"]/div[6]/div/div[2]/button

##STEP3
#Noninvasive radio button : //*[@id="non_invasive"]
#Noninvasive 16 : //*[@id="non_invasive_fields"]/div[1]/div/ul/li[16]/div/input
#Procedure Carried out : //*[@id="procedure_ultrasound"]
#Next Button : //*[@id="step-3"]/div[6]/div[2]/button

##STEP4
#Date: //*[@id="DateOfProcedure"]
#Date: //*[@id="single_cal3"]
#Result: //*[@id="txtProcedure"]
#Conveyed to (patient): //*[@id="step-4"]/div[4]/div/input
#Date: //*[@id="ConveyedOn"]
#MTP: //*[@id="message"]
#Submit button : //*[@id="form_f_submit"]

#XPATH for step-2 wizard button : //*[@id="tab_content2"]/div[2]/div/div/div[2]/a

##IDEAS
#IDEA 1: 
#I can use the class attribute of Pending and Add New html elements
#The class attribute becomes active whenever a particular tab is present.
#Upon submitting the form, Pending tab is opened, that is the class attribute of this tab becomes active. 
#DRAWBACK: If someone opens pending before submitting, then bt

#IDEA 2:
#Use the active or inactive state of step-buttons (1,2,3,4)
#Check that the last primary button was 4, current primary button is 1 and rest of the buttons are inactive(disabled)
#This ensures that the last form was submitted and now we are in new form 

class custom_exception(Exception):
    def __init__(self,message):
        self.message = message

class submit_success(object):
    def __init__(self):
        pass
    
    def __call__(self, driver):
        try:
            element = driver.find_element(By.XPATH, '//*[@id="tab_content2"]/div[2]/div/div/div[2]/a')
            return element.get_attribute('disabled') == 'disabled'
        except:
            return False


class filler_helper():
    def __init__(self,parent_window):
        self.driver = webdriver.Chrome()
        self.parent_window = parent_window

    def __del__(self):
        try:
            current_url = self.driver.current_url
            self.driver.quit()
        except:
            pass

    def close_driver(self):
        self.driver.quit()

    def login(self,username,password):
        self.driver.get("https://app.pyaribitiya.in/login")
        self.driver.maximize_window()

        username_input = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[1]/input")
        username_input.send_keys(username)
        time.sleep(0.5)
        password_input = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[2]/input")
        password_input.send_keys(password)

        time.sleep(0.5)

        login_button = self.driver.find_element(By.XPATH, "/html/body/div[2]/div/div[1]/section/form/div[3]/button")
        login_button.click()
        
    
    def goto_form_f(self):
        self.driver.get("https://app.pyaribitiya.in/fill_form_f")
        try:
            add_form_button = self.driver.find_element(By.XPATH, '//*[@id="profile-tab"]')
            add_form_button.click()
        except:
            raise custom_exception("too long")
        

    def fill_selected_forms(self,values):
        if values:
            for entry in values:
                add_form_button = self.driver.find_element(By.XPATH, '//*[@id="profile-tab"]')
                add_form_button.click()
                self.fill_form(entry)
        self.parent_window.indicate_forms_filled(values)

    def fill_children(self, children:tuple):
        male_children, female_children = children
        male_children = excel_assist.parse_ages(male_children)
        female_children = excel_assist.parse_ages(female_children)

        child_number = 0
        self.driver.find_element(By.XPATH, '//*[@id="add_child"]').click()

        for child_age in male_children:
            add_child_button = self.driver.find_element(By.XPATH, '//*[@id="add_child_row"]')
            if child_number != 0:
                add_child_button.click()
                time.sleep(0.1)
            age = ""
            if int(child_age[0]) != 0:
                age += str(child_age[0])
                age += 'Y'
            if int(child_age[1]) != 0:
                age += str(child_age[1])
                age += 'M'
            age_xpath = f'//input[@name="child[age][{child_number}]"]'
            age_column = self.driver.find_element(By.XPATH, age_xpath)
            age_column.send_keys(age)
            gender_button = self.driver.find_element(By.XPATH, f'//input[@name="child[gender][{child_number}]" and @value="M"]')
            gender_button.click()
            child_number += 1

        for child_age in female_children:
            add_child_button = self.driver.find_element(By.XPATH, '//*[@id="add_child_row"]')
            if child_number != 0:
                add_child_button.click()
                time.sleep(0.1)
            age = ""
            if int(child_age[0]) != 0:
                age += str(child_age[0])
                age += 'Y'
            if int(child_age[1]) != 0:
                age += str(child_age[1])
                age += 'M'
            age_xpath = f'//input[@name="child[age][{child_number}]"]'
            age_column = self.driver.find_element(By.XPATH, age_xpath)
            age_column.send_keys(age)
            gender_button = self.driver.find_element(By.XPATH, f'//input[@name="child[gender][{child_number}]" and @value="F"]')
            gender_button.click()
            child_number += 1
        
    def fill_form(self,entry):
        time.sleep(1)
        date = str(entry[1])
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date = date.strftime('%d/%m/%Y')
        print(date)
        #Step 1

        date_field = self.driver.find_element(By.XPATH, '//*[@id="EntryDate"]')
        date_field.clear()
        date_field.send_keys(date)

        patient_name_field = self.driver.find_element(By.XPATH, '//*[@id="PatientName"]')
        patient_name_field.send_keys(entry[2])

        age_field = self.driver.find_element(By.XPATH, '//*[@id="PatientAge"]')
        age_field.send_keys(str(entry[3])+'Y')

        phone_field = self.driver.find_element(By.XPATH, '//*[@id="step-1"]/div[8]/div/input')
        phone_field.click()

        if int(entry[7]) != 0 or int(entry[8]) != 0:
            if int(entry[7]) == 0:
                children_tuple = ('0.0',str(entry[16]))
            elif int(entry[8]) == 0:
                children_tuple = (str(entry[15]),'0.0')
            else:
                children_tuple = (str(entry[15]),str(entry[16]))
            print(children_tuple)
            self.fill_children(children_tuple)
        
        husband_name_field = self.driver.find_element(By.XPATH, '//*[@id="FatherName"]')
        husband_name_field.send_keys(entry[4])

        address_phone_tuple = excel_assist.separate_address_and_phone(entry[5])

        address_field = self.driver.find_element(By.XPATH, '//*[@id="step-1"]/div[7]/div/textarea')
        address_field.send_keys(address_phone_tuple[0])

        if address_phone_tuple[1]:
            phone_field.send_keys(address_phone_tuple[1])
        
        step1_next_button = self.driver.find_element(By.XPATH, '//*[@id="step-1"]/div[10]/div/div[2]/button')
        step1_next_button.click()

        time.sleep(0.1)

        #STEP 2
        doctor_name_address_tuple = excel_assist.separate_doctor_name_address(entry[11])
        doctor_name_field = self.driver.find_element(By.XPATH, '//*[@id="DoctorName"]')
        doctor_name_field.send_keys(doctor_name_address_tuple[0])

        doctor_address_field = self.driver.find_element(By.XPATH, '//*[@id="DoctorAddress"]')
        doctor_address_field.send_keys(doctor_name_address_tuple[1])

        weeks_field = self.driver.find_element(By.XPATH, '//*[@id="Pregnancy"]')
        weeks_field.send_keys(str(entry[6]) + 'W')

        step2_next_button = self.driver.find_element(By.XPATH, '//*[@id="step-2"]/div[6]/div/div[2]/button')
        step2_next_button.click()
        time.sleep(0.1)

        #STEP 3
        non_invasive_radio_button = self.driver.find_element(By.XPATH, '//*[@id="non_invasive"]')
        non_invasive_radio_button.click()

        no16_button = self.driver.find_element(By.XPATH, '//*[@id="non_invasive_fields"]/div[1]/div/ul/li[16]/div/input')
        no16_button.click()

        ultrasound_button = self.driver.find_element(By.XPATH, '//*[@id="procedure_ultrasound"]')
        ultrasound_button.click()

        step3_next_button = self.driver.find_element(By.XPATH, '//*[@id="step-3"]/div[6]/div[2]/button')
        step3_next_button.click()

        time.sleep(0.1)

        #STEP 4
        date_field = self.driver.find_element(By.XPATH, '//*[@id="DateOfProcedure"]')
        # date_field.click()
        date_field.clear()
        date_field.send_keys(date)

        date_field = self.driver.find_element(By.XPATH, '//*[@id="single_cal3"]')
        # date_field.click()
        date_field.clear()
        date_field.send_keys(date)

        date_field = self.driver.find_element(By.XPATH, '//*[@id="ConveyedOn"]')
        # date_field.click()
        date_field.clear()
        date_field.send_keys(date)

        result_field = self.driver.find_element(By.XPATH, '//*[@id="txtProcedure"]')
        result_field.send_keys(entry[10])

        patient_field = self.driver.find_element(By.XPATH, '//*[@id="step-4"]/div[4]/div/input')
        patient_field.send_keys('PATIENT')

        mtp_field = self.driver.find_element(By.XPATH, '//*[@id="message"]')
        mtp_field.send_keys(entry[12])

        submit_button = self.driver.find_element(By.XPATH, '//*[@id="form_f_submit"]')
        submit_button.click()
        print("filled")