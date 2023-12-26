# What is this repository?

I am using this repository as the collection spot for all applications and scripts i write to aid my Father.\
All scripts and application present here are quick-and-dirty projects i do whenever i find some free time, so keep in mind the code here is NOT pretty 🤧.\
For now, this repository contains 1 application(s) and 0 script(s), as follows:

1. Form Filling Automation
# Form Filling Automation

Using Python and Selenium to automate a boring administrative task.

## Purpose

This application is a simple yet useful and time saving tool for automatically filling an online form.\
There is a need to fill a form (Form F under the PCPNDT Act) on an online portal ("https://app.pyaribitiya.in") for many patients. All the data needed to fill this form is already filled once in an excel file by hand(Also required).\
Normally, these forms are filled online by hand : a redundant task.
This application uses data already filled into excel, to fill the online forms for each patient, as selected by the user from a list it displays.

## How does one use it?

1. When the application is opened for the first time, it asks for the user's login credentials for the online portal.
2. These credentials are stored for future use in a binary file.
3. Application asks the user to select a valid excel file that contains the data to be filled.
   The Excel files have a fixed data scheme and a name pattern 'PNDT excel file _month_ _year_'(Ex. 'PNDT excel file MAY 2021').
4. Data for the month is shown to the user in a table, from which user can select which entries are to be filled online.
5. User presses the 'Fill forms' button and press 'Okay' on the confirmation dialog, following which selenium takes over and 
starts filling the forms one by one. 
6. The program reports through a messagebox that the forms have been filled, or that an error occurred, accordingly.

The user also has 'Change Credentials' and 'Change Excel File' buttons to change the login credentials or select a different excel file if need be.

Many different scenarios have been thought through and appropriate error handling has been done.

## How does it work?

The program front-end is built on 'PyQt5', while the backend uses 'openpyxl' to deal with the excel file and 'selenium' webdriver (which is primarily used for testing purposes) to take control of a chrome session that fills the data in appropriate fields. 

## How to run this?

### Using the python interpreter
You need following python dependencies installed:

```
PyQt5
selenium
openpyxl
```

You ofcourse need your login credentials for the portal, which you enter whenever the program prompts you for them(You only need these to fill forms online, you can still look around the application without them).\
You will also need a valid Excel file for this to work.\
A 'sample.xlsx' file is included for with the file specifying the columns in the file.

Finally, to run the application, run 'gui.py'.

### Using the final executable provided

Unzip [AutomaticFormFiller.zip](packaged_applications/AutomaticFormFiller.zip) and run <b>FormFiller.exe</b>

