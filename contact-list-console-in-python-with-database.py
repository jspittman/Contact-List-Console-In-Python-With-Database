import msvcrt as m  # a Windows Specific Library used to create Press Any Key to Continue Functionality
import time # for time.sleep() functionality
from psycopg2 import * # to interact with the database
from tabulate import tabulate # for formatted list output
import os # to use clear screen function

#This program is a contact list that allows a user to add, delete, edit, and show all of their contacts into their list
# The program begins with a intro screen that runs once, then proceeds into a user menu where the user can perform the add,
# delete, edit and show actions.  The import msvcrt requires a Windows based system to opperate correctly.

### CONSTANTS ###

# Covers January through December
ALLOWABLE_BIRTHDAY_MONTH_ARRAY = ["01","02","03","04","05","06","07","08","09","10","11","12"] 
# Covers Days 01 through 31.  Some months do have certain days, however the program doens't currently correct for that.
ALLOWABLE_BIRTHDAY_DAY_ARRAY = ["01","02","03","04","05","06","07","08","09","10","11","12","13","14","15",
    "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31"]
# Allows for 00 - 99.  Covers a 100 year period.
ALLOWABLE_BIRTHDAY_YEAR_ARRAY = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15",
    "16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33","34","35","36","37",
    "38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56","57","58","59",
    "60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79","80","81",
    "82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99"]
# for those with birthdays in February
ALLOWABLE_BIRTHDAY_DATES_FEBRUARY = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15",
    "16","17","18","19","20","21","22","23","24","25","26","27","28","29"]
# For months with 30 days in them
ALLOWABLE_BIRTHDAY_DATES_30_DAYS = ["00","01","02","03","04","05","06","07","08","09","10","11","12","13","14","15",
    "16","17","18","19","20","21","22","23","24","25","26","27","28","29", "30"]
# Account for April, June, September, and November.  All 30 day months
ALLOWABLE_30_DAY_MONTHS = ["04","06","09","11"]
# business or personal relationship type
ALLOWABLE_RELATIONSHIP_TYPE_ARRAY = ["b","p","B","P"] 
# allowable genders, placed in array for future modification if needed
ALLOWABLE_GENDER_ARRAY = ["m","f","o","M","F","O"] 
# Allowable ages are 0 years of age - 120 years of age
ALLOWABLE_AGE_ARRAY = ["00","0","01","1","02","2","03","3","04","4","05","5","06","6","07","7","08","8","09","9","10",
    "11","12","13","14","15","16","17","18","19","20","21","22","23","24","25","26","27","28","29","30","31","32","33",
    "34","35","36","37","38","39","40","41","42","43","44","45","46","47","48","49","50","51","52","53","54","55","56",
    "57","58","59","60","61","62","63","64","65","66","67","68","69","70","71","72","73","74","75","76","77","78","79",
    "80","81","82","83","84","85","86","87","88","89","90","91","92","93","94","95","96","97","98","99","100","101","102",
    "103","104","105","106","107","108","109","110","111","112","113","114","115","116","117","118","119","120"]
REQUIRED_EMAIL_ADDRESS_CONTENTS = ["@","."]

### END CONSTANTS  ###

### BEGIN CLASSES AND METHODS ###

class Contact:
    """Called to Create an Additional Instance of a Contact."""
    def __init__(self, p_id_number_for_contact = 0, p_contact_first_name = "none", p_contact_last_name = "none", p_age_of_contact = 0,
                p_phone_number_of_contact = 0, p_email_of_contact = "", p_gender_of_contact = "", p_birthday_of_contact_month = "",
                p_birthday_of_contact_day = "", p_birthday_of_contact_year = "", p_business_or_personal_relationship = ""):
        self.id_number_for_contact = p_id_number_for_contact # Item ID set by Database
        self.contact_first_name = p_contact_first_name  # First Name
        self.contact_last_name = p_contact_last_name  # Last Name
        self.age_of_contact = p_age_of_contact # Age
        self.phone_number_of_contact = p_phone_number_of_contact # Phone Number
        self.email_of_contact = p_email_of_contact  # Email Address
        self.gender_of_contact = p_gender_of_contact  # Gender
        self.birthday_of_contact_month = p_birthday_of_contact_month  # Birthday of Contact Month
        self.birthday_of_contact_day = p_birthday_of_contact_day # Birthday of Contact Day
        self.birthday_of_contact_year = p_birthday_of_contact_year # Birthday of Contact Year
        self.business_or_personal_relationship = p_business_or_personal_relationship  # Business or Personal Relationship

    def show_contact_list(self):
        print("Contact ID Number: {}".format(self.id_number_for_contact))
        print("First Name: {}".format(self.contact_first_name))
        print("Last Name: {}".format(self.contact_last_name))
        print("Age: {}".format(self.age_of_contact))
        print("Phone Number: {}".format(self.phone_number_of_contact))
        print("Email Address: {}".format(self.email_of_contact))
        print("Gender: {}".format(self.gender_of_contact))
        print("Birthday: {}/{}/{}".format(self.birthday_of_contact_month, self.birthday_of_contact_day, self.birthday_of_contact_year))
        #print("Birthday Day: {}".format(self.birthday_of_contact_day)) # birthday format consolidated into single line output
        #print("Birthday Year: {}".format(self.birthday_of_contact_year)) # birthday format consolidated into single line output
        print("Business or Personal Relationship: {}".format(self.business_or_personal_relationship))

class ContactList:
    def __init__(self):
        """Creates the Contact List Array"""
        self.contact_list_array = []  # creates an empty contact list array

    # add a contact by appending to contact list
    def add_contact(self, contact_data):
        """Adds a Contact to the Contact List"""
        self.contact_list_array.append(contact_data)

    # delete a contact
    def remove_contact(self, id_number_for_contact):
        """Removes a Contact From the Contact List"""
        found = False
        for i in self.contact_list_array:
            if i.id_number_for_contact == id_number_for_contact:
                found = True
                self.contact_list_array.remove(i)
                prYellow('''

                            Contact #{} Removed! 
                                                   '''.format(id_number_for_contact))
                time.sleep(.75)
        if found == False:
            prRed('''    
            
                            Contact Not Found in List.  No Action Taken.
                            
                                                                            ''')
            time.sleep(.75)

    # edit a contact
    def edit_contact(self, contact_data, id_to_delete = 0, show_success = False):
        """Edits a Contact Within the Contact List"""
        found = False
        for i in range(len(self.contact_list_array)):
            if self.contact_list_array[i].id_number_for_contact == contact_data.id_number_for_contact:
                found = True
                self.contact_list_array[i].contact_first_name = contact_data.contact_first_name
                self.contact_list_array[i].contact_last_name = contact_data.contact_last_name
                self.contact_list_array[i].age_of_contact = contact_data.age_of_contact
                self.contact_list_array[i].phone_number_of_contact = contact_data.phone_number_of_contact
                self.contact_list_array[i].email_of_contact = contact_data.email_of_contact
                self.contact_list_array[i].gender_of_contact = contact_data.gender_of_contact
                self.contact_list_array[i].birthday_of_contact_month = contact_data.birthday_of_contact_month
                self.contact_list_array[i].birthday_of_contact_day = contact_data.birthday_of_contact_day
                self.contact_list_array[i].birthday_of_contact_year = contact_data.birthday_of_contact_year
                self.contact_list_array[i].business_or_personal_relationship = contact_data.business_or_personal_relationship
                if show_success == True:
                    prYellow('''
                
                                    Contact {} Updated!
                                    
                                                                
                                                                                                '''.format(id_to_delete))
                    time.sleep(.75)
        if found == False:
            prRed('''
            
                                ID Number Not Found in Contact List. Nothing modified.
                                
                                                            
                                                                                            ''')
            time.sleep(.75)
        return found

    # list all contacts
    def print_contact_list(self):
        """Prints the User's Contact List"""
        print("     \nYour Contact List\n")
        if len(self.contact_list_array) > 0:
            for i in self.contact_list_array:
                i.show_contact_list()
                print("\n")
        else:
            prYellow('''
                
                
                                    Your Contact List is Empty 
                
                                                                        
                                                                                    ''')
            time.sleep(.75)
            return False

### END CLASSES AND METHODS ###

### BEGIN GLOBAL SCOPE FUNCTIONS ###

def clear_console_screen():
    """Clears the console screen. Returns None."""
    os.system('cls' if os.name=='nt' else 'clear')
    return None

### BEGIN DATABASE ACTIONS ###

def open_the_database():
    """Called to open the database connection to the contacts.contact table.  Returns value my_cursor, which is an open database connection."""
    my_connection = connect(user = "postgres",
                            password = "P@ssw0rd",
                            host = "localhost",
                            port = "5432",
                            database = "contacts")

    my_cursor = my_connection.cursor()
    return my_cursor, my_connection

def commit_to_the_database(p_my_connection):
    """Called to commit (agree to) the changes proposed to the database.  Returns None."""
    p_my_connection.commit()
    return None

def close_the_database(p_my_cursor, p_my_connection):
    """Called to close the current open database connection.  Returns None."""
    p_my_cursor.close()
    p_my_connection.close()
    return None

def add_contact_to_the_database(p_my_cursor, p_add_single_new_contact):
    """Called to add a contact to the database.  Returns None."""
    sql = f"INSERT INTO contacts.contact (firstname, lastname, age, phonenumber, emailaddress, gender, birthday, relationshiptype) VALUES \
          ('{p_add_single_new_contact.contact_first_name}', '{p_add_single_new_contact.contact_last_name}',\
           '{p_add_single_new_contact.age_of_contact}', '{p_add_single_new_contact.phone_number_of_contact}',\
           '{p_add_single_new_contact.email_of_contact}','{p_add_single_new_contact.gender_of_contact}',\
           '{p_add_single_new_contact.formated_birthday_string}','{p_add_single_new_contact.business_or_personal_relationship}')"
    p_my_cursor.execute(sql)
    return None

def delete_contact_from_the_database(p_my_cursor, p_id_number_to_remove):
    """Called to delete a contact from the database.  Returns None."""
    sql = f"DELETE FROM contacts.contact WHERE id={p_id_number_to_remove}"
    p_my_cursor.execute(sql)
    return None

def edit_contact_in_the_database(p_my_cursor, p_contact_data):
    """Called to edit a single contact within the database.  Returns None."""
    sql = f"UPDATE contacts.contact SET firstname='{p_contact_data.contact_first_name}', lastname='{p_contact_data.contact_last_name}', \
    age='{p_contact_data.age_of_contact}', phonenumber='{p_contact_data.phone_number_of_contact}', \
    emailaddress='{p_contact_data.email_of_contact}', gender='{p_contact_data.gender_of_contact}', \
    birthday='{p_contact_data.formatted_birthday_string}', relationshiptype='{p_contact_data.business_or_personal_relationship}'\
    WHERE id='{p_contact_data.id_number_for_contact}'"
    p_my_cursor.execute(sql)
    return None

def read_from_the_database(p_my_cursor, p_do_not_display_any_key_to_continue = False):
    """Called to read the existing data stored in the database.  May give uncommitted (non-finalized data) if called prior to a commit statement.  Returns None."""
    p_my_cursor.execute("SELECT * FROM contacts.contact ORDER BY id")
    data_rows = p_my_cursor.fetchall()
    prYellow(f"\n\n                             There are {p_my_cursor.rowcount} contacts in your database.\n")
    if p_my_cursor.rowcount == 0:
        prYellow("                  Please use the 'A' or 'a' key to add a contact to your database.\n")
        return False
    else:
        pass
 
    formatting_table = []
    for row in data_rows:
        id_number_of_contact_output = row[0]
        first_name_of_contact_output = row[1]
        last_name_of_contact_output = row[2]
        age_of_contact_output = row[3]
        phone_number_of_contact_output = row[4]
        email_address_of_contact_output = row[5]
        gender_of_contact_output = row[6]
        birthday_of_contact_output = row[7]
        relationship_type_of_contact_output = row[8]

        id_number_of_contact_output = str(id_number_of_contact_output)
        first_name_of_contact_output = str(first_name_of_contact_output)
        last_name_of_contact_output = str(last_name_of_contact_output)
        age_of_contact_output = str(age_of_contact_output)
        phone_number_of_contact_output = str(phone_number_of_contact_output)
        email_address_of_contact_output = str(email_address_of_contact_output)
        gender_of_contact_output = str(gender_of_contact_output)
        birthday_of_contact_output = str(birthday_of_contact_output)
        relationship_type_of_contact_output = str(relationship_type_of_contact_output)

        to_append = [id_number_of_contact_output, first_name_of_contact_output, last_name_of_contact_output, age_of_contact_output, phone_number_of_contact_output,
                     email_address_of_contact_output, gender_of_contact_output, birthday_of_contact_output, relationship_type_of_contact_output]
        formatting_table.append(to_append)
 
    headers=['ID', 'First Name', 'Last Name', 'Age', 'Phone Number', 'eMail Address', 'Gender', 'Birthday', 'Relationship Type']
    if len(formatting_table) > 0:
        prYellow(tabulate(formatting_table, headers=headers, tablefmt="pretty"))
    if p_do_not_display_any_key_to_continue == False:
        print("\n\n           Press any key to continue")
        wait()
    return None

def id_in_database_check(p_my_cursor, p_id_number_to_remove):
    """Called to check if id number is present in the database.  Returns True if ID found, returns false if ID not found."""
    sql = f"SELECT * FROM contacts.contact WHERE id={p_id_number_to_remove}"
    p_my_cursor.execute(sql)
    data_rows = p_my_cursor.fetchall()

    # return true if row found in database
    if len(data_rows) > 0:
        return True
    else:
        return False

def format_birthday_for_database(p_birthday_of_contact_month, p_birthday_of_contact_day, p_birthday_of_contact_year):
    """Takes an input of contact's birthday month, day, and year and creates a string to insert into the contacts database."""
    formated_birthday_string = p_birthday_of_contact_month + "/" + p_birthday_of_contact_day + "/" + p_birthday_of_contact_year
    return formated_birthday_string

### END DATABASE ACTIONS ###

### BEGIN COLOR CHANGE TEXT FUNCTIONS ###
# prints text in red color output
def prRed(skk):
    """Prints Red Text to Console"""
    print("\033[91m{} \033[00m" .format(skk))

# prints text in green color output
def prGreen(skk):
    """Prints Green Text to Console"""
    print("\033[92m{} \033[00m" .format(skk))

# print text in yellow color output
def prYellow(skk):
    """Prints Yellow text to Console"""
    print("\033[93m{}\033[00m".format(skk))

### END COLOR CHANGE TEXT FUNCTIONS ###

# Used to pause the program until any key is pressed -- Windows Specific Function
def wait():
    """Pauses the program until any key is typed into the keyboard."""
    m.getch() # Windows specific functionality
    return None

# Runs only once, at program load
def display_introduction_screen():
    """Loads the introduction screen for the contact list.  Should run only once per program instance."""
    prGreen('''        
    ######################################################################################
                            
                            Welcome to Your Contact List

        You contact list is a place to store information about those you want to stay
        in contact with.  In the next menu you'll be able to begin building your list.

            The following menu allows you to:
                    - Add contacts to your list      
                    - Delete contacts from your list                
                    - Edit contacts within your list
            And finally:
                    - Display all of your contacts in your list                     
                                                                                        
    ######################################################################################

                            Please press any key to continue
    ''')
    wait()  # this uses the imported code from msvcrt and enabled the press any key functionality
    print("\n\n\n\n\n\n")

# Gets the contacts first name from the console, and does error checking to confirm
def get_first_name():
    """Collects a Contact's First Name"""
    contact_first_name = input("First Name | Enter Your Contact\'s First Name, Then Press Enter: ") # First Name
    if contact_first_name.isalpha() == True:
        pass
    else:
        while contact_first_name.isalpha() == False:
            contact_first_name = input("\n---> Invalid Input - Value Must Be All Letters and No Spaces -- Please Enter Your Contact's First Name, Then Press Enter: ")
    return contact_first_name

# Get the contact's last name from the console, and does error checking to confirm
def get_last_name():
    """Collects a Contact's Last Name"""
    contact_last_name = input("Last Name | Enter Your Contact\'s Last Name, Then Press Enter: ") # Last Name
    if contact_last_name.isalpha() == True:
        pass
    else:
        while contact_last_name.isalpha() == False:
            contact_last_name = input("\n---> Invalid Input - Value Must Be All Letters and No Spaces -- Please Enter Your Contact's Last Name, Then Press Enter: ")
    return contact_last_name

# Get the contact's age from the console, and does error checking to confirm
def get_age_of_contact():
    """Collects a Contact's Age"""
    contact_age = input("Age | Enter Your Contact\'s Age, Then Press Enter: ") # Age
    while contact_age not in ALLOWABLE_AGE_ARRAY:
        contact_age = input("\n---> Invalid Input - Value Must Only Include Numbers Without Decminals -- Please Enter Your Contact's Age, Then Press Enter: ")
    return contact_age

# Get the contact's phone number from the console, and does error checking to confirm
def get_phone_number_of_contact():
    """Collect's a Contact's Phone Number"""
    contact_phone_number = input("Phone Number | Enter Your Contact\'s 10 Digit Phone Number, ex: 1235551212, Then Press Enter: ") # Phone Number
    length_of_contact_phone_number = len(contact_phone_number)
    if contact_phone_number.isdigit() == True and length_of_contact_phone_number == 10:
        pass
    else:
        while contact_phone_number.isdigit() == False or length_of_contact_phone_number != 10:
            contact_phone_number = input("\n---> Invalid Input - Value Must Include 10 Digits -- Please Enter Your Contact's Age, Then Press Enter: ")
            length_of_contact_phone_number = len(contact_phone_number)
    return contact_phone_number

# Get the contact's email address from the console, and does error checking to confirm
def get_email_of_contact():
    """Saves the Email Addresses of the Contact.  Error Checking is Performed to Determine Validity"""
    email_of_contact = input("Email Address | Enter Your Contact's Email Address, Then Press Enter: ")
    email_contains_required_elements = all(elem in email_of_contact for elem in REQUIRED_EMAIL_ADDRESS_CONTENTS)
    check_for_whitespace_count = 0
    # check for whitespace in string
    for a in email_of_contact:
        if (a.isspace()) == True:
            check_for_whitespace_count +=1      
    if check_for_whitespace_count == 0:
        whitespace_does_not_exist_in_string = True
    else:
        whitespace_does_not_exist_in_string = False
    while email_contains_required_elements == False or whitespace_does_not_exist_in_string == False:
            email_of_contact = input("\n---> Invalid Input - Email Address Must Contain a '@' and a '.', and Cannot Contain a Space. | Please Enter Your Contact's Email Address, Then Press Enter: ")
            email_contains_required_elements =  all(elem in email_of_contact for elem in REQUIRED_EMAIL_ADDRESS_CONTENTS)
            check_for_whitespace_count = 0
            # check for whitespace in string
            for a in email_of_contact:
                if (a.isspace()) == True:
                    check_for_whitespace_count +=1      
            if check_for_whitespace_count == 0:
                whitespace_does_not_exist_in_string = True
            else:
                whitespace_does_not_exist_in_string = False
    return email_of_contact

# Get the contact's gender from the console, and does error checking to confirm
def get_gender_of_contact():
    """Saves the Gender of the Contact.  Error Checking is Performed to Determine Validity"""
    gender_of_contact = input("Gender | Enter Your Contact's Gender (M for male) (F for female) (O for other), Then Press Enter: ")
    if gender_of_contact in ALLOWABLE_GENDER_ARRAY:
        pass
    else:
        while gender_of_contact not in ALLOWABLE_GENDER_ARRAY:
            gender_of_contact = input("\n---> Gender needs to be either M (for male), F (for female), or O (for other).  Please Choose Only One and Reenter Contact Gender, Then Press Enter: ")
    gender_of_contact = gender_of_contact.capitalize()
    return gender_of_contact

# Get the month the contact was born from the console, and does error checking to confirm
def get_birthday_of_contact_month():
    """Saves the Birth Month of the Contact.  Error Checking is Performed to Determine Validity"""
    birthday_of_contact_month = input("Birthday Month | Enter Your Contact's Birthday Month as MM, ex: Type 01 For January or 08 For August, Then Press Enter: ")
    birthday_of_contact_month = str(birthday_of_contact_month)
    # This is a working while loop, and should remain in the program.
    while birthday_of_contact_month not in ALLOWABLE_BIRTHDAY_MONTH_ARRAY:
        birthday_of_contact_month = input("\n---> Invalid Input - Enter Your Contact's Birthday Month as MM, ex: Type 03 For March or 12 For December, Then Press Enter: ")
        birthday_of_contact_month = str(birthday_of_contact_month)
    return birthday_of_contact_month

# Get the day the contact was born from the console, and does error checking to confirm
def get_birthday_of_contact_day(p_birthday_of_contact_month):
    """Saves the Day of Birth of the Contact.  Error Checking is Performed to Determine Validity"""
    birthday_of_contact_day = input("Birthday Day | Enter Your Contact's Birthday Day as DD, ex: Type 01 For the First or 15 For the Fifteenth, Then Press Enter: ")
    birthday_of_contact_day = str(birthday_of_contact_day)
    if p_birthday_of_contact_month == "02":
        while birthday_of_contact_day not in ALLOWABLE_BIRTHDAY_DATES_FEBRUARY:
            birthday_of_contact_day = input("\n---> Invalid Input - Birthday Day | Enter Your Contact's Birthday Day as DD, ex: Type 01 For the First or 15 For the Fifteenth, Then Press Enter: ")
    if p_birthday_of_contact_month in ALLOWABLE_30_DAY_MONTHS:
        while birthday_of_contact_day not in ALLOWABLE_BIRTHDAY_DATES_30_DAYS:
            birthday_of_contact_day = input("\n---> Invalid Input - Birthday Day | Enter Your Contact's Birthday Day as DD, ex: Type 01 For the First or 15 For the Fifteenth, Then Press Enter: ")
    while birthday_of_contact_day not in ALLOWABLE_BIRTHDAY_DAY_ARRAY:
            birthday_of_contact_day = input("\n---> Invalid Input - Birthday Day | Enter Your Contact's Birthday Day as DD, ex: Type 01 For the First or 15 For the Fifteenth, Then Press Enter: ")
    return birthday_of_contact_day

# Get the year the contact was born from the console, and does error checking to confirm.
def get_birthday_of_contact_year():
    """Saves the Birth Year of the Contact.  Error Checking is Performed to Determine Validity"""
    birthday_of_contact_year = input("Birthday Year | Enter Your Contact's Birthday Year as YY, ex: Type 84 For 1984 or 01 For 2001, Then Press Enter: ")
    birthday_of_contact_year = str(birthday_of_contact_year)
    while birthday_of_contact_year not in ALLOWABLE_BIRTHDAY_YEAR_ARRAY:
        birthday_of_contact_year = input("\n---> Invalid Input - Birthday Year | Enter Your Contact's Birthday Year as YY, ex: Type 84 For 1984 or 01 For 2001, Then Press Enter: ")
    return birthday_of_contact_year

# Get the type of relationship that the user has to the contact.  Options are Business or Personal
def get_business_or_personal_relationship():
    """Saves as (B) or (P).  This is the relationship type the user has to the contact"""
    business_or_personal_relationship = input("Business or Personal | Enter Your Relationship to the Contact (enter B for business) or (enter P for personal), Then Press Enter: ")
    if business_or_personal_relationship in ALLOWABLE_RELATIONSHIP_TYPE_ARRAY:
        pass
    else:
        while business_or_personal_relationship not in ALLOWABLE_RELATIONSHIP_TYPE_ARRAY:
            business_or_personal_relationship = input("\n---> Invalid Input - Enter Your Relationship to the Contact (enter B for business) or (enter P for personal), Then Press Enter: ")
    business_or_personal_relationship = business_or_personal_relationship.capitalize()
    return business_or_personal_relationship

# The main interface for the program.  The menu will run until the user enters "Q" or "q", or manually exists the program.
# From here a user can add a contact, edit a contact, remove a contact, or view their contact list. 

def print_menu(main_list_of_contacts, p_id_number_itterate):  # this takes as a parameter "main_list_of_contacts", which is an instance of the class ContactList.
    """The main interface where the user interacts with their contact list.  Allowable actions are add, edit, delete, or list."""
    user_selected_action = " "  # the selection that the user will make within the menu
    user_added = False

    prGreen('''        
    ######################################################################################
                            
                            Contact List Main Menu

            ( A ) - To Add a Contact to Your List ------- Type the letter A or a

            ( D ) - To Delete a Contact From Your List -- Type the letter D or d

            ( E ) - To Edit a Contact On Your List ------ Type the letter E or e
            
            ( L ) - To View Your Contact List ----------- Type the letter L or l

            ( Q ) - To exit the program  ---------------- Type the letter Q or q

                                
                    - Press Enter After Typing Your Selection -                 
                                                                                        
    ######################################################################################
    ''')


    while user_selected_action != "a" and user_selected_action != "A" and user_selected_action != "q" and user_selected_action != "Q" and user_selected_action != "l" and user_selected_action != "L" and user_selected_action != "d" and user_selected_action != "D" and user_selected_action != "e" and user_selected_action != "E":
        user_selected_action = input('                 Please Make Your Selection From the Menu Above, Then Press Enter: ')
        if user_selected_action != "a" and user_selected_action != "A" and user_selected_action != "q" and user_selected_action != "Q" and user_selected_action != "l" and user_selected_action != "L" and user_selected_action != "d" and user_selected_action != "D" and user_selected_action != "e" and user_selected_action != "E":
            prRed('''\n\n\n                    Invalid Selection -- Please Select From the Menu Below\n''')
            return user_selected_action, user_added
        else:
            pass
        if user_selected_action == "a" or user_selected_action == "A":

            id_number_for_contact = p_id_number_itterate
            print("\n")
            print('''                     ------------------------------------------------------ 
                                        Add Contact to List
                     -------------------------------------------------------
                                                                                ''')
            contact_first_name = get_first_name()
            print("")
            contact_last_name = get_last_name()
            print("")
            age_of_contact = get_age_of_contact()
            print("")
            phone_number_of_contact = get_phone_number_of_contact()
            print("")
            email_of_contact = get_email_of_contact()
            print("")
            gender_of_contact = get_gender_of_contact()
            print("")
            birthday_of_contact_month = get_birthday_of_contact_month()
            print("")
            birthday_of_contact_day = get_birthday_of_contact_day(birthday_of_contact_month)
            print("")
            birthday_of_contact_year = get_birthday_of_contact_year()
            print("")
            business_or_personal_relationship = get_business_or_personal_relationship()
            formated_birthday_string = format_birthday_for_database(birthday_of_contact_month, birthday_of_contact_day, birthday_of_contact_year)
            add_single_new_contact = Contact()
            add_single_new_contact.id_number_for_contact = "ID-" + str(id_number_for_contact)
            add_single_new_contact.contact_first_name = contact_first_name
            add_single_new_contact.contact_last_name = contact_last_name
            add_single_new_contact.age_of_contact = age_of_contact
            add_single_new_contact.phone_number_of_contact = phone_number_of_contact
            add_single_new_contact.email_of_contact = email_of_contact
            add_single_new_contact.gender_of_contact = gender_of_contact
            add_single_new_contact.birthday_of_contact_month = birthday_of_contact_month
            add_single_new_contact.birthday_of_contact_day = birthday_of_contact_day
            add_single_new_contact.birthday_of_contact_year = birthday_of_contact_year
            add_single_new_contact.formated_birthday_string = formated_birthday_string # prepare birthday string for database
            add_single_new_contact.business_or_personal_relationship = business_or_personal_relationship
            main_list_of_contacts.add_contact(add_single_new_contact)

            # open database connections

            my_cursor, my_connection = open_the_database()
            add_contact_to_the_database(my_cursor, add_single_new_contact)
            commit_to_the_database(my_connection) # cannot use my_cursor for commiting
            close_the_database(my_cursor, my_connection)

            # end database connections

            prYellow('''                             
                            ----------------------------------------------

                                          Contact Added!
                                                    
                            -----------------------------------------------
                                                    ''')
            time.sleep(.75)
            user_added = True
        
        elif user_selected_action == "d" or user_selected_action == "D":  # remove (delete) contact from list
            user_added = False
            do_not_display_any_key_to_continue = True
            my_cursor, my_connection = open_the_database()
            does_database_contain_data = read_from_the_database(my_cursor, do_not_display_any_key_to_continue)
            if does_database_contain_data == False:
                prRed('''
                    
                            Database Is Empty.  Returning to Main Menu.
                                    
                                                                                ''')
                time.sleep(1)
                return user_selected_action, user_added
            prGreen("\n\n                                Delete a Contact From Your List\n\n")
            id_number_to_remove = input("Enter ID Number of Contact To Remove.  \n\nFor Example, Type 1 To Delete Your Contact With an ID of 1, or 5 To Delete Your Contact With an ID of 5, Then Press Enter: ")
            check_for_int_value =  id_number_to_remove.isnumeric()
            while check_for_int_value == False:
                id_number_to_remove = input("\nPlease Reenter ID Number of Contact To Remove.  \n\nFor Example, Type 1 To Delete Your Contact With an ID of 1, or 5 To Delete Your Contact With an ID of 5, Then Press Enter: ")
                check_for_int_value = id_number_to_remove.isnumeric()
            id_number_to_remove = str(id_number_to_remove)
            id_in_database_status = id_in_database_check(my_cursor, id_number_to_remove)
            if id_in_database_status == True:
                prGreen(f"\n\n            Contact ID #{id_number_to_remove} Will Be Removed From Your Contact List")
                #id_number_to_remove = id_number_to_remove.upper() # this is adjust id- to ID, or Id to ID to match casing
                confirm_delete_answer = input("\nAre You Sure You Want To Delete This Contact?  Type Y for Yes, or N for no, Then Press Enter: ")
                while confirm_delete_answer != "Y" and confirm_delete_answer != "y" and confirm_delete_answer != "N" and confirm_delete_answer != "n":
                    confirm_delete_answer = input("\n---> Invalid input: Please Type Y To Confirm Delete of Your Contact, or Type N to Reject Delete of Your Contact, Then Press Enter: ")
                if confirm_delete_answer == "Y" or confirm_delete_answer == "y":
                    delete_contact_from_the_database(my_cursor, id_number_to_remove)
                    commit_to_the_database(my_connection)
                    close_the_database(my_cursor, my_connection)
                    prYellow('''
                    
                                        Contact Removed Successfully.
                                    
                                                                                ''')
                    print("    Press Any Key to Continue")
                    wait()
                #main_list_of_contacts.remove_contact(id_number_to_remove)
                elif confirm_delete_answer == "N" or confirm_delete_answer == "n":
                    prRed('''
                    
                                        Delete Cancelled.  Nothing Done.
                                    
                                                                                ''')
                    time.sleep(.75)
            else:
                prRed('''
                    
                                    ID Not found in Database.  Nothing Done.
                                    
                                                                                ''')
                time.sleep(1)


            # commented out because used in list storage, not database storage
            """
            if main_list_of_contacts.print_contact_list() == False:
                pass
            else:
                prGreen("          Delete a Contact From Your List\n")
                id_number_to_remove = input("Enter ID Number of Contact To Remove.  For Example, Type ID-1 To Delete Your First Contact, or ID-5 To Delete Your Fifth Contact, Then Press Enter: ")
                id_number_to_remove = str(id_number_to_remove)
                id_number_to_remove = id_number_to_remove.upper() # this is adjust id- to ID, or Id to ID to match casing
                confirm_delete_answer = input("\nAre You Sure You Want To Delete This Contact?  Type Y for Yes, or N for no, Then Press Enter: ")
                while confirm_delete_answer != "Y" and confirm_delete_answer != "y" and confirm_delete_answer != "N" and confirm_delete_answer != "n":
                    confirm_delete_answer = input("\n---> Invalid input: Please Type Y To Confirm Delete of Your Contact, or Type N to Reject Delete of Your Contact, Then Press Enter: ")
                if confirm_delete_answer == "Y" or confirm_delete_answer == "y":
                    main_list_of_contacts.remove_contact(id_number_to_remove)
                elif confirm_delete_answer == "N" or confirm_delete_answer == "n":
                    prRed('''
                    
                                      Delete Cancelled.  Nothing Done.
                                    
                                                                             ''')
                    time.sleep(.75)
                else:
                    pass
                """

        # edit user in contact list
        elif user_selected_action == "e" or user_selected_action == "E":
            '''
            if main_list_of_contacts.print_contact_list() == False:
                pass
            else:
            '''
            my_cursor, my_connection = open_the_database()
            do_not_display_any_key_to_continue = True
            does_database_contain_data = read_from_the_database(my_cursor, do_not_display_any_key_to_continue)
            if does_database_contain_data == False:
                prRed('''
                    
                            Database Is Empty.  Returning to Main Menu.
                                    
                                                                                ''')
                time.sleep(1)
                return user_selected_action, user_added
            user_added = False
            prGreen("\n       Edit Contact In List\n")
            contact_data = Contact()
            id_number_for_contact = input("Enter the ID Number of the Contact You Want To Edit.\n\nFor Example, Type 1 For Your Contact With ID of 1, or Type 5 For Your Contact With ID 5, Then Press Enter: ")
            check_for_int_value =  id_number_for_contact.isnumeric()
            while check_for_int_value == False:
                id_number_for_contact = input("\nPlease Reenter ID Number of Contact To Edit.  \n\nFor Example, Type 1 To For Your Contact With ID of 1, or 5 For Your Contact With ID 5, Then Press Enter: ")
                check_for_int_value = id_number_for_contact.isnumeric()
            id_number_for_contact = str(id_number_for_contact)
            id_in_database_status = id_in_database_check(my_cursor, id_number_for_contact)
            if id_in_database_status == True:
                prGreen(f"\n\n            Contact ID #{id_number_for_contact} Will Be Edited")
                #id_number_to_remove = id_number_to_remove.upper() # this is adjust id- to ID, or Id to ID to match casing
                confirm_delete_answer = input("\nAre You Sure You Want To Edit This Contact?  Type Y for Yes, or N for no, Then Press Enter: ")
                while confirm_delete_answer != "Y" and confirm_delete_answer != "y" and confirm_delete_answer != "N" and confirm_delete_answer != "n":
                    confirm_delete_answer = input("\n---> Invalid input: Please Type Y To Confirm Edit of Your Contact, or Type N to Reject Edit of Your Contact, Then Press Enter: ")
                if confirm_delete_answer == "N" or confirm_delete_answer == "n":
                    prRed('''
                    
                                        Edit Cancelled.  Nothing Done.
                                    
                                                                                ''')
                    time.sleep(1)
                    return user_selected_action, user_added
            
                #contact_data.id_number_for_contact = id_number_for_contact
                '''
                if main_list_of_contacts.edit_contact(contact_data, id_number_for_contact) == False:
                    pass
                else:
                '''
                print("")
                contact_first_name = get_first_name()
                print("")
                contact_last_name = get_last_name()
                print("")
                age_of_contact = get_age_of_contact()
                print("")
                phone_number_of_contact = get_phone_number_of_contact()
                print("")
                email_of_contact = get_email_of_contact()
                print("")
                gender_of_contact = get_gender_of_contact()
                print("")
                birthday_of_contact_month = get_birthday_of_contact_month()
                print("")
                birthday_of_contact_day = get_birthday_of_contact_day(birthday_of_contact_month)
                print("")
                birthday_of_contact_year = get_birthday_of_contact_year()
                print("")
                business_or_personal_relationship = get_business_or_personal_relationship()
                formatted_birthday_string = format_birthday_for_database(birthday_of_contact_month, birthday_of_contact_day, birthday_of_contact_year)
                contact_data.id_number_for_contact = id_number_for_contact
                contact_data.contact_first_name = contact_first_name
                contact_data.contact_last_name = contact_last_name
                contact_data.age_of_contact = age_of_contact
                contact_data.phone_number_of_contact = phone_number_of_contact
                contact_data.email_of_contact = email_of_contact
                contact_data.gender_of_contact = gender_of_contact
                contact_data.birthday_of_contact_month = birthday_of_contact_month
                contact_data.birthday_of_contact_day = birthday_of_contact_day
                contact_data.birthday_of_contact_year = birthday_of_contact_year
                contact_data.formatted_birthday_string = formatted_birthday_string
                contact_data.business_or_personal_relationship = business_or_personal_relationship
                edit_contact_in_the_database(my_cursor, contact_data)
                commit_to_the_database(my_connection) # cannot use my_cursor for commiting
                close_the_database(my_cursor, my_connection)
                prYellow('''
                    
                                        Contact Edited Successfully.
                                    
                                                                                ''')
                time.sleep(1)
                #show_update_success = True
                #main_list_of_contacts.edit_contact(contact_data, id_number_for_contact, show_update_success)
            else:
                prRed('''
                    
                                    ID Not found in Database.  Nothing Done.
                                    
                                                                                ''')
                time.sleep(1)
        elif user_selected_action == "l" or user_selected_action == "L":
            user_added = False

            """
            if main_list_of_contacts.print_contact_list() == False:
                pass
            else:
                print("\n\n\n            Press any key to continue")
                wait()
            """

            # database connetions
            do_not_display_any_key_to_continue = True
            my_cursor, my_connection = open_the_database()
            read_from_the_database(my_cursor, do_not_display_any_key_to_continue)
            print("\n\n       Press Any Key To Continue")
            wait()
            close_the_database(my_cursor, my_connection)

    return user_selected_action, user_added


### END GLOBAL SCOPE FUNCTIONS ###


# This is the main entrance to the program.  The main_contact_list_instance variable is an instance of Class
# ContactList.  The while loop runs until the program reads the "q" or "Q" character via user input from the Main Menu, 
# at when point the main function returns None and the program exits.
def main():
    display_introduction_screen()
    main_menu_user_selection = " "
    id_number_itterate = 1
    main_contact_list_instance = ContactList()
    clear_console_screen()

    # this loop recevies the return value from the print_menu function, and evaluates the return to determine whether to continue running
    while main_menu_user_selection != "q" and main_menu_user_selection != "Q":
        print("")
        # this passes the created instance of Class "ContactList" as an argument into the function print_menu.  id_number_itterate is passed to increment by 1 for each added contact.
        main_menu_user_selection, user_added = print_menu(main_contact_list_instance, id_number_itterate) 
        if user_added == True:
            id_number_itterate += 1  # increases the user ID by 1 if flag is true.  The assignment of true is only made when adding a user.
        else:
            pass # do not itterate the id number if a contact has not been added
        clear_console_screen()
    return None

# This calls the main function, and this begins the program.
if __name__ == "__main__":
    main()
