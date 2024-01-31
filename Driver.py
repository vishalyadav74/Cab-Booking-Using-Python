from Connection import Connection
from SensitiveData import SensitiveData
from Crud import CRUD
from Services import Services
from UploadIdentity import upload_file
from termcolor import colored, cprint
from prettytable import PrettyTable
import re

connObj = None
connCursor= None
table='G5_DRIVER'
col='Driver_Id'

class Driver:
    @Services.timer_func
    def initialiseConn(self, connObjTemp):
        global connObj
        global connCursor
        connObj=connObjTemp
        connCursor=connObj.cursor()
      
    @Services.timer_func
    def menu(connObjTemp):
        objEmp=Driver()
        objEmp.initialiseConn(connObjTemp)
        cprint("\n\n---------Welcome Driver----------\n", 'green')
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
               Driver.register() 
        elif option == 2:
                Driver.login()
        elif option == 3:
                pass
        else:
                print('Invalid option. Please enter a number between 1 and 4.')      
    @Services.timer_func
    def register():
        cprint("\n\n----------DRIVER REGISTRATION---------\n", 'green')
        print("Please fill the below details for the registration process:")
        id_pattern = r'^[dD]\d+$'
        while True:
            d_id = input('Enter your Driver Id: ')
            if re.match(id_pattern, d_id):
                break
            else:
               print("Invalid driver id!!")
        name_pattern = r"^[A-Za-z\s'-]+$"
        while True:
            f_name = input('Enter your First Name: ')
            if re.match(name_pattern, f_name):
                break
            else:
                print("Invalid first name. Please use only letters, spaces, hyphens, and apostrophes!!")
        while True:
            l_name = input('Enter your Last Name: ')
            if re.match(name_pattern, l_name):
               break
            else:
               print("Invalid last name. Please use only letters, spaces, hyphens, and apostrophes!!")
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        while True:
            email = input('Enter your Email: ')
            if re.match(email_pattern, email):
                break
            else:
                print("Invalid email address!!")
        contact_pattern = r'^\d{10}$'
        while True:
            contact = input('Enter your Contact: ')
            if re.match(contact_pattern, contact):
               break
            else:
               print("Invalid contact number!! Please enter 10 digits")
        src = input('Enter your Source Location: ')
        dest = input('Enter your Destination Location: ')
        source=Services.lower_replace(src)
        destination=Services.lower_replace(dest)
        cabNo = input('Enter your Cab No: ')
        seats = int(input('Enter total no of seats in your Cab: '))
        pass_pattern =r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$'
        while True:  
            password = input('Enter your Password: ')
            if re.match(pass_pattern, password):
               break
            else:
               print("Password must contains atleast one upper case, one lower case ,one digit and one special character!!")
        status=0
        available_seats=seats
    
        encypt_pass=SensitiveData.encryption(password)

        vals1=(d_id, f_name, l_name, email, contact, source, destination, cabNo, available_seats,seats, status)

        CRUD.insert(connObj, table, vals1)
        vals2=(d_id, encypt_pass)
        CRUD.insert(connObj, 'G5_SENSITIVE_DATA', vals2)
        cprint("\n\n Register Successful\n\n", 'yellow')

    @Services.timer_func
    def login():
        print("----------LOGIN---------")
        id = input('Enter your Driver Id: ')
        password = input('Enter your Password: ')
        encypt_pass=SensitiveData.encryption(password)
        sql = '''select * from public."G5_SENSITIVE_DATA" where "ID"= %s and "PASSWORD"=%s'''
        connCursor.execute(sql, (id,encypt_pass)) 
        result = connCursor.fetchone()
       
        if result is not None:
            cprint("\nLogin successful!\n", 'yellow')
            cprint("\n---------Welcome ----------\n", 'green')
            print("1. Update")
            print("2. Delete")
            print("3. Check available booking")
            print("4. Upload Identity Proof Documnents")
            print("5. Exit")

            choice = ''
            try:
                choice = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number ...')
         
            if choice == 1:
                Driver.update(connObj, table, id)
                
            elif choice == 2:
                CRUD.delete(connObj, table, col, id)
                CRUD.delete(connObj,"G5_SENSITIVE_DATA","ID",id)
            elif choice == 3:
                c1="Status"
                c2="Driver_Id"
                connCursor.execute(f'''  SELECT EXISTS ( SELECT 1 FROM public."G5_DRIVER" WHERE "{c2}"='{id}' AND "{c1}" = 1 )    ''')
                result=connCursor.fetchone()[0]
                # print(result)
                if result==True:
                    Driver.employeesToRide(id)
                else:
                    cprint("\nYou are not approved by admin\n", 'red')
            elif choice == 4:
                upload_file(connObj)
            elif choice == 5:
                pass
            else:
                    print('Invalid choice. Please enter a number between 1 and 4.')
            return True
        else:
            print("Wrong e_id or password!")
            return False
        
    @Services.timer_func
    def update(connObj, table, id):
            print("\nEnter column no:")
            print("1. First Name")
            print("2. Last Name")
            print("3. Email")
            print("4. Contact")
            print("5. Location")
            print("6. Password")
            print("7. Cab No")
            print("8. Exit")

            colName=''
            newVal=''
            choice = ''
            try:
                choice = int(input('\nEnter your choice: '))
            except:
                print('Wrong input. Please enter a number ...')
     
            if choice == 1:
                while True:
                  name_pattern = r"^[A-Za-z\s'-]+$"
                  newVal=input("Enter your Updated First Name:")
                  if re.match(name_pattern, newVal):
                     break
                  else:
                   print("Invalid first name.")
                colName="First_Name"
                CRUD.update(connObj,table,colName,newVal,col,id)   
            elif choice == 2:
                while True:
                    name_pattern = r"^[A-Za-z\s'-]+$"
                    newVal=input("Enter your Updated Last Name:")
                    if re.match(name_pattern, newVal):
                      break
                    else:
                       print("Invalid last name.")
                colName="Last_Name"
                CRUD.update(connObj,table,colName,newVal,col,id) 
            elif choice == 3:
                email_pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
                while True:
                    newVal = input('Enter your Email: ')
                    if re.match(email_pattern, newVal):
                       break
                    else:
                       print("Invalid email address!!")
                colName="Email"
                CRUD.update(connObj,table,colName,newVal,col,id) 
            elif choice == 4:
                contact_pattern = r'^\d{10}$'
                while True:
                   newVal=input("Enter your Updated Contact:")
                   if re.match(contact_pattern, newVal):
                      break
                   else:
                     print("Invalid contact number!! Please enter 10 digits")
                colName="Contact"
                CRUD.update(connObj,table,colName,newVal,col,id)
            elif choice == 5:
                newVal=input("Enter your Updated Location:")
                colName="Location"
                CRUD.update(connObj,table,colName,newVal,col,id)
            elif choice == 6:
                pass_pattern =r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$'
                while True:  
                    newVal=input("Enter your Updated Password:")
                    if re.match(pass_pattern, newVal):
                       break
                    else:
                       print("Password must contains atleast one upper case, one lower case ,one digit and one special character!!")
                encypt_pass=SensitiveData.encryption(newVal)
                CRUD.update(connObj,'G5_SENSITIVE_DATA','PASSWORD',encypt_pass,'ID',id)
            elif choice == 7:
                newVal=input("Enter your Updated Cab No:")
                colName="Cab_No"
                CRUD.update(connObj,table,colName,newVal,col,id)
            # elif choice == 8:
            #     cab_name_pattern= 'r^[A-Za-z]{2}\d{4}'
            #     while True:
            #         newVal=input("Enter your Updated Cab Name:")
            #         if re.match(cab_name_pattern,newVal):
            #            break
            #         else:
            #           print("Enter valid cab name!!")
            #     colName="Cab_Name"
            #     CRUD.update(connObj,table,colName,newVal,col,id)
            elif choice == 8:
                pass
            else:
                print('Invalid choice. Please enter a number between 1 and 4.')

    @Services.timer_func
    def employeesToRide(id):
        c1="D_ID"
        connCursor.execute(f''' SELECT * from  public."G5_BOOKING" where "{c1}"='{id}' ''')
        records= connCursor.fetchall()

        if records:
            # select from booking table which are ready to ride or book a cab
            cprint("\n\n---------- List of Available Employess that book the cab ----------\n ", 'green')
            t = PrettyTable(['Booking ID', 'Employee Id', 'Driver Id'])
            for row in records:
                t.add_row([row[0], row[1], row[2]])
            cprint(t, 'yellow')
            try:
                choice = int(input('\n\nRide in Progress !! Do you want to Finish the ride ?? \n1.YES \n2. NO'))
            except:
                print('Wrong input. Please enter a number ...')
            
            if choice == 1:
                # delete from booking table where d_id equals and update driver seats column
                c1="Driver_Id"
                c2="AvailableSeats"
                connCursor.execute(f''' UPDATE public."G5_DRIVER" SET "{c2}"="{c2}"+1 where "{c1}"='{id}'    ''')
                connObj.commit()
                #  DELEETE FROM BOOKING TABLE
                CRUD.delete(connObj,"G5_BOOKING","D_ID",id)
                cprint('\nRide Finish :) \n', 'yellow') 
            elif choice == 2:
                cprint('\nThanks !! your ride is in progress...Have a Safe Journey :) \n', 'yellow')                
                Connection.close(connObj, connCursor)
                exit()
        else:
             cprint("\nNo Booking yet\n", 'yellow')

        
