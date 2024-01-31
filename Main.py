from Admin import Admin
from Connection import Connection
from Employee import Employee
from Driver import Driver
from Services import Services
import os
from termcolor import colored, cprint

menu_options = {
    1: 'Option 1',
    2: 'Option 2',
    3: 'Option 3',
    4: 'Exit',
}
class Main:
 @Services.timer_func
 def print_menu():
    try:
        for key in menu_options.keys():
            print (key, '--', menu_options[key] )
    except NameError:
        print ('menu_options is not defined')

if __name__=='__main__':
    connection = Connection("adep_metadata", "postgres", "postgres", "illin4313", 5431)
    connObj = connection.connect() 
    connCursor= connObj.cursor()

    while(True):
        option = ''
        # os.system('cls')
        cprint("-----------CAB BOOKING SYSTEM---------",'light_red',attrs=['bold'])
        print("1. Admin")
        print("2. Employee")
        print("3. Driver")
        print("4. Exit")
    

        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        
        if option == 1:
           Admin.menu(connObj)
        elif option == 2:
            Employee.menu(connObj)
        elif option == 3:
            Driver.menu(connObj)
        elif option == 4:
            print('Thank you for using our cab service!!')
            Connection.close(connObj, connCursor)
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

