#!/usr/local/bin/python3
# Citation: Adapted from @swisscoding on Instagram
# Code for running UI

from termcolor import colored
from time import sleep
from classes import CPU

if __name__ == "__main__":

    cpu1 = CPU()
    cpuOptions = 0 #1-3, 40 so program isnt easily exited by mistakenly pressing 4 
    print(colored("Starting CPU! Here are your options!\n","blue"))

    try:
        cpu1.getStorage()
        
    finally:

        cpu1.printCpuMenu()
        while cpuOptions !=6:
            try: 
                
                cpuOptions = int(input("Enter 1, 2, 3, 4, 5 (print menu), or 6: "))
                print()

                if cpuOptions == 1:
                    num = int(input("Add user by name(1) or all attributes(2): "))
                    cpu1.addUser(num)
                    print() #style
                    
                elif cpuOptions == 2:

                    if len(cpu1.user_list) >= 1:
                        cpu1.updateUser()
                    else:
                        print(colored("No user exist. Please add new user.","red"))

                    print() #style
                
                elif cpuOptions == 3:

                    if len(cpu1.user_list) >= 1:
                        num = int(input("Would you like the User List (1) or All User Data from Admin? (2): "))

                        if num == 1:
                            cpu1.getUserList()

                        elif num == 2:
                            if cpu1.admin is not None and cpu1.adminCount > 0:
                                adminId = input(colored("Enter 4 digit Admin ID: ",'green'))
                                if cpu1.admin.adminID == adminId:
                                    cpu1.getUserInfo()
                                else:
                                    print(colored("Incorrect Admin ID",'red'))

                            elif cpu1.adminCount==0:
                                print(colored("No Admin Exists.","red"))
                            '''
                            may be useful for multi admin implementation
                            for person in cpu1.user_list:
                                if hasattr(person, "adminID"):
                                    cpu1.adminCount = 1
                                    adminId = input(colored("Enter 4 digit Admin ID: ",'green'))
                                    if person.adminID == adminId:
                                        cpu1.getUserInfo()
                                    else:
                                        print(colored("Incorrect Admin ID",'red'))
                            '''
                            
                    else:
                        print(colored("No user exist. Please add new user.","red"))
                    print() #style
                
                elif cpuOptions == 4: 
                    if len(cpu1.user_list) >= 1:
                        name = input("Enter the full name of the user you wish to delete: ")
                        cpu1.removeUser(name) #throws some sort of error, caught by value
                    else:
                        print(colored("No user exist. Please add new user.","red"))


                elif cpuOptions == 5:
                    cpu1.printCpuMenu()
                    
                elif cpuOptions == 6:
                    cpu1.updateStorage()
                    print(colored("Powering off!","red")); sleep(1)
                    print(colored("Leaving Model UI program now.","red")) ;sleep(1)
                    #cpu1.getStorage()
                        
            except ValueError:
                print(colored("\nBe sure to enter an int.\n","red"))

# End