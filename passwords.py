from termcolor import colored
import re
import getpass

#This module holds all of my password related functions,
# Initially, this project was only submitted in one long file
# but I've recently tried to organize it some.
#The next step may be adding them as class methods if that makes more sense

# located here because only this file uses it 
# bmade because of project requirements at time of creation
class RequirementError(Exception):
    def __init__(self, value):
        self.value = value

def print_password_menu():
    print(colored("\n---- | Choose Option | ----\n", "red"))
    print("To Set Password Choose: 1 ")
    print("To Change Password Choose: 2 ")
    print("To Exit Password Manager Choose: 3")

# Used to provide switch functionality for password manager without
# having to print the password menu everytime
def passwordSwitch():
    num = 0
    helper = 'q'
    while helper != 'w':
        try:
            num = int(input("Enter a number to Update Password (1, 2, or 3 to quit): ")) #value error
            if num == 1:
                return 1

            elif num == 2:
                return 2

            elif num == 3:
                return 3

            else:
                raise ValueError("\nInvalid Input")

        except ValueError as excpt:
            print(excpt)
            

def print_password_reqirements():
    # decoration
    print(colored("\n---- | Password Validation | ----\n", "red"))
        # information
    print(colored("Requirements: ","green"))
    print("1. The password must contain at least one uppercase character.")
    print("2. The password must contain at least one lowercase character.")
    print("3. The password must contain at least one number.")
    print("4. The password must contain at least one special character (!, ?, *, #).")
    print("5. The password must be at least 8 characters in length.\n")

#Function checks 5 requirements for password, credit to Swiss Codes
def validate(pw):
    
    passwordReqs = [r"[a-z]{1,}", r"[A-Z]{1,}", r"[0-9]{1,}", r"[\!\?\*\#]{1,}"]
    try:
        validation_count = 0
        if len(pw) >= 8: #1
            validation_count += 1
            for i in passwordReqs:
                if re.search(i, pw):
                    validation_count += 1
        else:
            raise RequirementError(colored("\nYour password length is too short!\n", "red"))

        if validation_count == 5:
            print(colored("\nYour password satisfies every requirement!\n", "green"))
            return True
        else:
            raise RequirementError(colored("\nYour password does not satisfy one of the requirements 1 to 4!\n","red"))

    except RequirementError as excpt:
        print(excpt)
        print("Unable to validate password.")
        return False

# Takes in old and new potential passwords', validates new one and verifies it's what the user
# intended to enter and allows user to restart by entering 'q', which will exit this funciton, returning 
# a false value and the original pw in a tuple, which then causes the updatePassword
# function to grab another potential pw from the user, and then call this function again.
def verifyNewPassword(pw, newAttempt):
    validatedPw = validate(newAttempt)
    helper = 'q'
    if validatedPw == True:     #new password met requirements
        while helper == 'q':
            try:
                currentPassword = getpass.getpass("Re enter new password for verification or 'q' to start over: ")  # Enter the current verified password
                if newAttempt == currentPassword:
                    pw = newAttempt
                    helper = 'w'

                elif(currentPassword == 'q'): #exits function
                    validatedPw = False
                    break

                elif newAttempt != currentPassword:
                    raise RequirementError("Re entered password does not match new password\n")

            except RequirementError as excpt:
                print(excpt)
    return validatedPw, pw

# Takes a password parameter, makes sure entered password matches old one (for security purposes)
# then asks for new password (using validate fucntion), if validated, it's checked twice
# outer most loop checks old password matches security check, inner while loop validates
# and verifies new password,
def changePassword(pw):
    
    print(colored("\n---- | Updating Password | ----\n", "red"))

    helper = 'q' # while loop value, only changes when new passwrod is set
    while helper == 'q':
        currentPassword = getpass.getpass("Enter current password for varification: ")  # Enter the current verified password

        if pw == currentPassword: # Matching passwords sends program to validate function
            print(colored("Passwords match!\n", "green"))
            validatedPw = False       # Captures value of validate function

            while validatedPw == False: #goes until user enters viable,verified new password
                try:
                    passwordAttempt = getpass.getpass("Password will not appear on screen.\nEnter your new password: ")
                    if passwordAttempt == pw:
                        raise RequirementError("New Password matches old one.\n")

                except RequirementError as excpt:
                    print(excpt)
                    continue

                validatedPw,pw = verifyNewPassword(pw,passwordAttempt)
                if validatedPw == True: #break loops after setting new password
                    helper = 'w'
        else:
            print("Does not match current password.")
    return pw
 
# controls pasword set and update, currently returns nothing
# calls all other pasword related functions
# takes truth value in case password already exists
# made this function so everything password related could have one hub
def passwordManager(hasPassword,userPw):
   
    userPassword = userPw

    print_password_menu()
    userSelection = passwordSwitch() #Prints Menu, returns user selection for Branching

    while userSelection != 3:
        if userSelection == 1 : # Set Initial Password
            if hasPassword == True:
                print("You've already set your password. If you would like to change it, select option 2.\n")
                userSelection = passwordSwitch() #returns user selection for Branching
                continue
            
            #loop will run for those who dont correctly verify their new password
            print_password_reqirements() # Password Menu
            while hasPassword == False:
                    # user password input
                passwordAttempt = getpass.getpass("Password will not appear on screen.\nEnter your password: ")
                    #Captures truth validation success / failure - new / old password
                hasPassword,userPassword = verifyNewPassword(userPw,passwordAttempt)

        elif userSelection == 2: #Changing Current Password
            if userPassword == 'none':
                print(colored("First you must create a password to then change later. Choose option 1.\n","red"))
            else:
               userPassword = changePassword(userPassword)
               print_password_menu()

        userSelection = passwordSwitch() #returns user selection for Branching
    print() #style
    return userPassword
