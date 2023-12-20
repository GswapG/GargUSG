import os 
import re
from datetime import datetime

## Columns in excel file next to their tuple index

# 0 S.NO.
# 1 DATE
# 2 PATIENT NAME
# 3 AGE (YRS)
# 4 W/O OR D/O
# 5 FULL ADDRESS
# 6 GEST. PERIOD
# 7 LIVE CHILDREN
# 8 None
# 9 INDICATION
# 10 RESULT
# 11 REFERRED BY
# 12 MTP ADVISED?
# 13 DATE OF MTP
# 14 DONE BY
# 15 None
# 16 None
# 17 None
# 18 None
# 19 None
# 20 None
# 21 None
# 22 None
# 23 None
# 24 None
# 25 None
# 26 None
# 27 None
# 28 None




path_to_excel = ".\\PNDT excel report NOVEMBER 2023.xlsm"
values = []

def is_valid_entry(entry): #entry is a tuple containing 15 columns + 1 excel row number column
    for col in entry:
        if col == None:
            return False
    if type(entry[0]) != type(1):
        return False
    if type(entry[1]) != type(datetime(2000,10,14)):
        return False
    return True

def convert_to_format(list_values): #converts values taken from excel file to list containing valid tuples
    values = []
    for value_tuple in list_values:
        temp_tuple = tuple(value_tuple[0:15])
        if is_valid_entry(temp_tuple):
            temp_tuple = temp_tuple + (list_values.index(value_tuple),)
            values.append(temp_tuple)
    return values
    
def print_entries(values): #utility function
    for entry in values:
        if is_valid_entry(entry):
            print(entry[-1])

def separate_address_and_phone(address_phone): #returns a tuple (address, phone number)
    phone_number_pattern = re.compile(r'\b\d{10}\b')
    phone_match = phone_number_pattern.findall(address_phone)

    phone = ""
    address = ""
    if phone_match:
        address = address_phone.replace(phone_match[0], '').strip()
        phone = phone_match[0]
        return (address, phone)
    else: #phone not found, so just return address with empty phone field
        return (address_phone, phone)

def extract_month_from_file_name(file_name):
    file_name = os.path.basename(file_name)
    pattern = re.compile(r'(?i)PNDT\s*excel\s*report\s*(\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|jun(?:e)?|jul(?:y)?|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\b)\s*(\d{4})')

    # Match the pattern in the file name
    match = pattern.search(file_name)

    if match:
        # Extract matched month and year
        month_name = match.group(1)
        year = match.group(2)

        # Convert month name to its corresponding number
        month_dict = {
            'jan': 1, 'january': 1,
            'feb': 2, 'february': 2,
            'mar': 3, 'march': 3,
            'apr': 4, 'april': 4,
            'may': 5,
            'jun': 6, 'june': 6,
            'jul': 7, 'july': 7,
            'aug': 8, 'august': 8,
            'sep': 9, 'september': 9,
            'oct': 10, 'october': 10,
            'nov': 11, 'november': 11,
            'dec': 12, 'december': 12
        }
        month_number = month_dict.get(month_name.lower())

        return (month_number, year)
    else:
        # Return None if no match is found
        return None

def filter(list_of_tuples,file_name):
    values = []
    criteria = extract_month_from_file_name(file_name)
    for tuple in list_of_tuples:
        date = str(tuple[1])
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        if str(date.month) == str(criteria[0]) and str(date.year) == str(criteria[1]):
            values.append(tuple)
    return values

def generate_selected_entries(list_values,display_values,starting_row,ending_row):
    values = []
    for value in display_values:
        if int(value[-1]) >= int(starting_row) and int(value[-1]) <= int(ending_row):
            values.append(list_values[int(value[-1])])
    return values

def separate_doctor_name_address(address_name: str) -> tuple:
    parts = address_name.split(',', 1)

    if len(parts) == 2:
        # Strip whitespace from both parts
        name = parts[0].strip()
        address = parts[1].strip()
        return (name, address)
    else:
        # Handle cases where the input string doesn't have a comma
        return (address_name.strip(), "")

def parse_ages(ages_string):
    age_tuples = []
    age_strings = str(ages_string).split(',')
    for age_string in age_strings:
        age_string = str(age_string).strip()
        year, month = map(int, age_string.split('.'))
        if year == 0 and month == 0:
            continue
        age_tuples.append((year, month))

    return age_tuples

#testing code    
if __name__ == "__main__":
    convert_to_format()
    # print_entries(values)
    # for value in values:
    #     print(separate_address_and_phone(str(value[5])))


