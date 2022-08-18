from termcolor import colored
import getpass
from passwords import passwordManager
import shelve

# These are the basic individual profiles that you can store on the computer
class User:
    def __init__(self):
        self.name ='none'
        self.first_name = "none"
        self.last_name = "none"
        self.age = 0
        self.pw = "none"
        self.userName ="none"
        self.shortHand ="none"

    def updateUserName(self):
        #works
        length = 20
        helper = 'w'
        while helper !='q':
            try:
                name = input("\nEnter a new user name ({} characters max, 3 chacters minimum): ".format(length))
                if len(name) > length:
                    print("User name is too long @ {} characters".format(len(name)))
                elif len(name) <= length and len(name)>3:
                    self.userName = name
                    helper = 'q'
                else:
                    print("User name is too short @ {} characters".format(len(name)))

            except ValueError:
                print(ValueError)


    def updateAge(self):
        self.age = int(input("Enter new age: "))

    def updatePassword(self,val,pw):
        self.pw = passwordManager(val,self.pw) 


# Used to update User name (both new and old Users)
# Also checks to see if name is taken first
    def changeName(self,userList=None): 
       
        nameChanged = False
        helper ='w'
        while helper !='q':

            try:

                name = input("\nEnter new name, or 'q' to exit.\nFirst name must be 3 characters or more. Format| first last: ")
                if name == 'q':
                    break

                for user in userList: 
                    if name == user.name:
                        print(colored("User named '{}' already exists.".format(user.name),"red"))
                        name = "failedAttempt0101"
                        break
                if name == 'failedAttempt0101': #helps restart loop if name is taken, probably could just use continue
                    continue
                
                self.name = name
                names = self.name.split() #list of first and last names
                self.first_name = names[0] #sets name
                self.last_name = names[1] #sets name
                self.shortHand = self.first_name[:3] +" "+ self.last_name[:1] +'.'
                nameChanged = True
                helper = "q"
            
            except (IndexError, ValueError) as error:
                print(colored(error,"red"))

        return nameChanged

# Admin is a object that Inherits from User class
# Added to meet inheritence requirement for initial project,
# TODO: could update CPU to keep an admin list and store 3 admins

class Admin(User):
    def __init__(self):
        User.__init__(self)
        self.adminID = "0" #4 digit num for overrides


# Class used to manage and store all users
# TODO: Add methods to upload users in bulk via file, at least by name
        #Add method to make a current user Admin 
         #only if there are no admins
        #Add forgot admin pin functionality 

class CPU:
    def __init__(self):
        self.user_list = []
        self.adminCount = 0
        self.admin = None

# Adds admin and returns admin, or returns the user given so 
# calling function can continue on with adding a new user
    def addAdmin(self, user):

        #Case 1: Admin already exists, exit this function and create new user
        # to adapt for multiple, TODO change this to check admin count + add admin list
        if self.admin is not None:
            print(colored("Admin {} already exists. You can only have 1. Adding new user."
                .format(self.admin.name),"red"))
            return user

        #Case 2: if an admin doesn't exist, add and return admin
        if self.adminCount == 0: 
            user = Admin()#create new admin
            self.adminCount = 1
            self.admin = user

            while 1: 
                user.adminID = input(colored("Enter a 4 digit number for Admin ID: ",'green'))

                if len(str(user.adminID)) != 4: #checks admin ID (probably could remove str function)
                    print(colored("ID must be 4 digits exactly.","red"))
                    continue
                else:
                    break

        return user

# Adds user to CPU list based on updateUserMode: 1 for name, 2 for all qualities
# Also maps to addAdmin if chosen: # if an admin exists, since you can only have 1,
# addAdmin returns the Normal user
    def addUser(self, updateUserMode):
        
        newUserAdded = False
        helper = 'w'
        newUser = User()

        while helper != 'q':

            #What kind of user to add #Admin check fucntion
            userChoice = int(input("Add Admin (1) or Normal User(2)?: "))

            #Case 1: They want to add an Admin
            if userChoice == 1:
                newUser = self.addAdmin(newUser)

            #Case2: Actually whether newUser is Admin or Normal User, 
            # start setting Name or attributes based on updateUserMode
            newUserAdded = newUser.changeName(self.user_list)
                
            #Case 3: If name was added and more attributes are desired
            if updateUserMode == 2 and newUserAdded == True: 
                newUser.updateUserName()
                newUser.updateAge()
                newUser.updatePassword(False,newUser.pw) #false means password doesn't exist for user

            if newUserAdded:
                print("New user '{}' added!".format(newUser.name))
                helper = 'q'
                self.user_list.append(newUser)
            else:
                print("Failed to add new user!")

# Used to update an existing users attributes: name, age, etc.
# made so you dont have to do it all the first time          
    def updateUser(self):

        name = input("Enter user's full name or 'q' to quit: ")
        userFound = False #helps now whether to continue or not
        helper = 'w'

        while helper !='q':

            if name == 'q': #if name = q, stops function
                break

            for user in self.user_list: #checks to see if name is taken
                if user.name == name:
                    userFound = True
                    pw = getpass.getpass("Enter password for security purposes (or anything if you haven't set one yet):")
                    if user.pw == pw or user.pw == "none": #pw checked, moving onto selection
                        
                        print(colored("What would you like to update?","red"))
                        print(colored("1. Full Name","green"))
                        print(colored("2. Username","green"))
                        print(colored("3. Password","green"))
                        print(colored("4. User Age","green"))
                        print(colored("5. To Print Menu","green"))
                        print(colored("6. To Quit","red"))
                        num = int(input(colored("Enter 1-6 to Update User (5 to print menu):","green")))

                        while num !=6:
                            try: 
                                if num == 1:
                                    val = user.changeName(self.user_list)
                                elif num == 2:
                                    user.updateUserName()
                                elif num == 3:
                                    if user.pw == "none":
                                        user.updatePassword(False,user.pw)
                                    else: 
                                        user.updatePassword(True,user.pw)
                                elif num == 4:
                                    user.updateAge()
                                elif num == 5:
                                    print(colored("What would you like to update?","red"))
                                    print(colored("1. Full Name","green"))
                                    print(colored("2. Username","green"))
                                    print(colored("3. Password","green"))
                                    print(colored("4. User Age","green"))
                                    print(colored("5. To Print Menu","green"))
                                    print(colored("6. To Quit\n","red"))

                                num = int(input(colored("Enter 1-6 to Update User (5 to print menu,6 to Quit):","green"))) 
                                if num == 6:
                                    helper = 'q'
                                    
                            except ValueError:
                                print(ValueError)
                    else:
                        print(colored("incorrect password\n","red"))

            if userFound == False:
                print(colored("User not found.","red"))
                name = input("Enter user's full name or 'q' to quit: ")
                print() #style
                continue

# Used to print out the name and amount of Users stored in User list by CPU
    def getUserList(self):
        #works, prints users
        i=1
        for user in self.user_list:
            print(colored("User #{} is {}".format(i,user.name),"blue"))
            i+=1

# Used to output all user info by Admin 
# could make it an admin member function, but control makes more sense from CPU 
# since it has the user list built in and manages all users, including Admin
    def getUserInfo(self):
        i=1

        for user in self.user_list:

            print(colored("\nUser #{} is {}".format(i,user.name),"blue"))
            print(" Username: {}".format(user.userName))
            print(" Age: {}".format(user.age))
            print(" Shorthand: {}".format(user.shortHand))
            print(" Password is: {}".format(user.pw))

            if hasattr(user, "adminID"):
                print(" AdminId is: {}".format(user.adminID))

            i+=1

# Removes User or Admin from CPU user List by full name (NOT by userName)
    def removeUser(self, name):
        
        successfulRemoval = False
        for user in self.user_list:
            if name == user.name:
                pw = getpass.getpass("Enter this user's password for security purposes (or anything if you haven't set one yet):")

                if user.pw == pw or user.pw == "none": #pw checked, moving onto selection
                    if hasattr(user,"adminID"): #if admin is removed, reset cpu.admin values
                        self.adminCount = 0
                        self.admin = None

                    self.user_list.remove(user)
                    successfulRemoval = True #1 user removed
                    print(colored("User {} has been deleted.\n".format(user.name),'red'))

                else:
                    print(colored("Incorrect password. Unable to remove user.",'red'))

        if successfulRemoval == False: #0 users removed
            print(colored("User not found in cpu. Nothing removed.\n","red"))

# Used to add persisten storage - specifically, assigns values from CPU object to keys
    def updateStorage(self):
        s = shelve.open('user_list.db')
        try:
            s['users'] = self.user_list
            s['adminCount'] = self.adminCount
            s['admin'] = self.admin

        finally:
            s.close()

# Used to add persisten storage - specifically, assigns values from storage to CPU object
    def getStorage(self):
        s = shelve.open('user_list.db')
        try:
            self.user_list = s['users']
            self.adminCount = s['adminCount']
            self.admin = s['admin']

        except:
            print("No history detected.\n")

        finally:
            s.close()


    def printCpuMenu(self):
        print(colored("1. Add New User.","green"))
        print(colored("2. Update Existing User.","green"))
        print(colored("3. Get User Info","green"))
        print(colored("4. Remove User","green"))
        print(colored("5. Print CPU Menu","green"))
        print(colored("6. Power Off CPU","red"))
        

