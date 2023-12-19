from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import excel_assist

##STEP 1
#Date : //*[@id="EntryDate"]
#Patient Name : //*[@id="PatientName"]
#Age : //*[@id="PatientAge"]
#Do you have children:
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

class filler_helper():
    def __init__(self):
        self.driver = webdriver.Chrome()

    def __del__(self):
        time.sleep(5)
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
        add_form_button = self.driver.find_element(By.XPATH, '//*[@id="profile-tab"]')
        add_form_button.click()

    def fill_selected_forms(self,values):
        if values:
            for entry in values:
                self.fill_form(entry)


    def fill_form(self,entry):
        time.sleep(1)
        date = str(entry[1])
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        date = date.strftime('%d/%m/%Y')
        #Step 1

        # date_field = self.driver.find_element(By.XPATH, r'//*[@id="EntryDate"]')
        # date_field.click()
        # date_field.send_keys(date)

        patient_name_field = self.driver.find_element(By.XPATH, r'//*[@id="PatientName"]')
        patient_name_field.send_keys(entry[2])

        age_field = self.driver.find_element(By.XPATH, '//*[@id="PatientAge"]')
        age_field.send_keys(str(entry[3])+'Y')

        husband_name_field = self.driver.find_element(By.XPATH, '//*[@id="FatherName"]')
        husband_name_field.send_keys(entry[4])

        address_phone_tuple = excel_assist.separate_address_and_phone(entry[5])

        address_field = self.driver.find_element(By.XPATH, '//*[@id="step-1"]/div[7]/div/textarea')
        address_field.send_keys(address_phone_tuple[0])

        phone_field = self.driver.find_element(By.XPATH, '//*[@id="step-1"]/div[8]/div/input')
        if address_phone_tuple[1]:
            phone_field.send_keys(address_phone_tuple[1])
        
        step1_next_button = self.driver.find_element(By.XPATH, '//*[@id="step-1"]/div[10]/div/div[2]/button')
        step1_next_button.click()

        time.sleep(0.1)

        #STEP 2
        doctor_name_field = self.driver.find_element(By.XPATH, '//*[@id="DoctorName"]')
        doctor_name_field.send_keys('a')

        doctor_address_field = self.driver.find_element(By.XPATH, '//*[@id="DoctorAddress"]')
        doctor_address_field.send_keys('a')

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
        date_field.click()
        date_field.send_keys(date)

        date_field = self.driver.find_element(By.XPATH, '//*[@id="single_cal3"]')
        date_field.click()
        date_field.send_keys(date)

        date_field = self.driver.find_element(By.XPATH, '//*[@id="ConveyedOn"]')
        date_field.click()
        date_field.send_keys(date)

        result_field = self.driver.find_element(By.XPATH, '//*[@id="txtProcedure"]')
        result_field.send_keys(entry[10])

        patient_field = self.driver.find_element(By.XPATH, '//*[@id="step-4"]/div[4]/div/input')
        patient_field.send_keys('PATIENT')

        mtp_field = self.driver.find_element(By.XPATH, '//*[@id="message"]')
        mtp_field.send_keys(entry[12])

        submit_button = self.driver.find_element(By.XPATH, '//*[@id="form_f_submit"]')

        time.sleep(100)