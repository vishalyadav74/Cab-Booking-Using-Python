from Crud import CRUD
from Connection import Connection
from SensitiveData import SensitiveData
from datetime import datetime, timezone 
from Services import Services
from Logger import logger
from termcolor import colored, cprint
from prettytable import PrettyTable
import re

# from Main import Main

connObj = None
connCursor= None
table='G5_EMPLOYEE'
col='E_Id'
# d_id =None

class Employee:
    @Services.timer_func
    def initialiseConn(self,connObjTemp):
        global connObj
        global connCursor
        # global d_id
        connObj=connObjTemp
        connCursor=connObj.cursor()
        #print("inside employee")

    @Services.timer_func
    def menu(connObjTemp):
        objEmp=Employee()
        objEmp.initialiseConn(connObjTemp)
        cprint("\n\n---------Welcome Employee----------\n", 'green')
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        option = ''
        try:
            option = int(input('\nEnter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
               Employee.register() 
        elif option == 2:
                Employee.login()
        elif option == 3:
                pass
        # elif option == 4:
        #         print('Thanks message before exiting')
        #         Connection.close(connObj, connCursor)
        #         exit()
        else:
                print('Invalid option. Please enter a number between 1 and 4.')      

    @Services.timer_func
    def register():
        cprint("\n\n----------EMPLOYEE REGISTRATION---------\n", 'green')
        try:
            print("\nPlease fill the below details for the registration process:\n")
            id_pattern = r'^[eE]\d+$'
            while True:
                e_id = input('Enter your Employee Id: ')
                if re.match(id_pattern, e_id):
                    break
                else:
                    logger.warning(f'Warning !! user entered invalid Employee Id {e_id} at the time of registration')
                    print("Invalid employee id!!")

            name_pattern = r"^[A-Za-z\s'-]+$"
            while True:
                f_name = input('Enter your First Name: ')
                if re.match(name_pattern, f_name):
                    break
                else:
                    logger.warning(f'Warning !! user entered invalid First Name {f_name} at the time of registration')
                    print("Invalid fisrt name. Please use only letters, spaces, hyphens, and apostrophes!!")
            while True:
                l_name = input('Enter your Last Name: ')
                if re.match(name_pattern, l_name):
                    break
                else:
                    logger.warning(f'Warning !! user entered invalid Last Name {l_name} at the time of registration')
                    print("Invalid last name. Please use only letters, spaces, hyphens, and apostrophes!!")

            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            while True:
                email = input('Enter your Email: ')
                if re.match(email_pattern, email):
                    break
                else:
                    logger.warning(f'Warning !! user entered invalid Email {email} at the time of registration')
                    print("Invalid email address!!")

            contact_pattern = r'^\d{10}$'
            while True:
                contact = input('Enter your Contact: ')
                if re.match(contact_pattern, contact):
                    break
                else:
                    logger.warning(f'Warning !! user entered invalid Contact{contact} at the time of registration')
                    print("Invalid contact number!! Please enter 10 digits")

            address = input('Enter your Address: ')
            pass_pattern =r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%^&+=]).{8,}$'
            while True:  
               password = input('Enter your Password: ')
               if re.match(pass_pattern, password):
                break
               else:
                logger.warning(f'Warning !! Password rules not match at the time of registration')
                print("Password must contains atleast one upper case, one lower case ,one digit and one special character!!")
            
            status=0

            encypt_pass=SensitiveData.encryption(password)

            vals1=(e_id, f_name, l_name, email, contact, address,status)

            CRUD.insert(connObj, table, vals1)
            vals2=(e_id, encypt_pass)
            CRUD.insert(connObj, 'G5_SENSITIVE_DATA', vals2)
            # logger.info({f_name} ,{l_name} ,"registered successfully")
            cprint("\nEmployee registered successfully!!\n", 'yellow')
        except:
           print("Enter Valid Details!!")

    @Services.timer_func
    def login():
        cprint("\n\n----------LOGIN---------\n\n", 'green')
        id = input('Enter your Employee Id: ')
        password = input('Enter your Password: ')           
        encypt_pass=SensitiveData.encryption(password)
        sql = '''select * from public."G5_SENSITIVE_DATA" where "ID"= %s and "PASSWORD"=%s'''
    
        connCursor.execute(sql, (id,encypt_pass))             
        result = connCursor.fetchone()
        
        if result is not None:
            # logger.info({id}  ,"Login successfully")
            cprint("\nLogin successful!\n", 'yellow')
            cprint("\n\n---------Welcome ----------\n\n", 'green')
            print("1. Update")
            print("2. Delete")
            print("3. Book Cab")
            print("4. Exit")

            choice = ''
            try:
                choice = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number ...')
            
            if choice == 1:
                Employee.update(connObj, table, id)
                    
            elif choice == 2:
                CRUD.delete(connObj, table, col, id)                    
                CRUD.delete(connObj,"G5_SENSITIVE_DATA","ID",id)
            elif choice == 3:
                # print("hello")
                c1="Status"
                c2="E_Id"
                # connCursor.execute(f'''   SELECT {c2} FROM public."G5_EMPLOYEE" WHERE "{c1}" = 1     ''')
                connCursor.execute(f'''  SELECT EXISTS ( SELECT 1 FROM public."G5_EMPLOYEE" WHERE "{c2}"='{id}' AND "{c1}" = 1 )    ''')
                result=connCursor.fetchone()[0]
                # print(result)
                if result==True:
                    Employee.bookCab(id)
                else:
                    cprint("\nYou are not approved by admin\n", 'red')
            elif choice == 4:
                pass
            else:
                print('Invalid choice. Please enter a number between 1 and 4.')
                return True
        else:
            print("Wrong e_id or password!")
            logger.error(f'Error login user {id}:')
            return False          

    @Services.timer_func
    def update(connObj, table, id):
            print("\nEnter column no:")
            print("1. First Name")
            print("2. Last Name")
            print("3. Email")
            print("4. Contact")
            print("5. Address")
            print("6. Password")
            print("7. Exit")

            colName=''
            newVal=''
            choice = ''
            try:
                choice = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number ...')
     
            if choice == 1:
                while True:
                  name_pattern = r"^[A-Za-z\s'-]+$"
                  newVal=input("Enter your Updated First Name:")
                  if re.match(name_pattern, newVal):
                     break
                  else:
                   print("Invalid fisrt name.")
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
                newVal=input("Enter your Updated Address:")
                colName="Address"
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
                pass
            else:
                print('Invalid choice. Please enter a number between 1 and 4.')

   

    @Services.timer_func
    def bookCab(id):
        c1="E_ID"
        connCursor.execute(f'''  SELECT EXISTS ( SELECT 1 FROM public."G5_BOOKING" WHERE "{c1}" = '{id}' )    ''')
        result=connCursor.fetchone()[0]

        global d_id

        if result==False :
            cprint("\n\n----------BOOKING RIDE---------\n", 'green')
            source=input("Enter Source:")
            destination=input("Enter Destination:")
            src=Services.lower_replace(source)
            dest=Services.lower_replace(destination)
            c1="Source"
            c2="Destination"
            c3="AvailableSeats"
        
            connCursor.execute(f''' SELECT * from  public."G5_DRIVER" where "{c1}"='{src}' AND "{c2}"='{dest}'  AND "{c3}" >0    ''')
            records= connCursor.fetchall()
            t = PrettyTable(['ID', 'Name', 'Contact', 'Source', 'Destination', 'CabNumber'])
            if records:
                d_id=records[0][0]
                print("\n\n------ List of Available Cabs -----\n\n", 'green')

                for row in records:
                    t.add_row([row[0],row[1],row[4],row[5],row[6],row[7]])
                cprint(t, 'yellow')
                choice = None
                try:
                    choice = int(input('Confirm Booking ? \n1.YES \n2. NO'))
                except:
                    print('Wrong input. Please enter a number ...')
               
                if choice == 1:
                    table="G5_BOOKING"
                    g_id=None
                    try:
                         generator=str(next(Services.get_next_booking_id()))
                         print("emp:",generator)
                         g_id=generator
                         print(g_id)
                    except Exception as error:
                         print("Error while inserting data", error)

                    vals=(g_id,id,d_id,'Progress')
                    CRUD.insert(connObj, table, vals)
                    # INSERT INTO BOOKING HISTORY USE TIMESTAMP
                    table1="G5_BOOKING_HISTORY"
                    dt = str(datetime.now())
                    vals1=(g_id,id,d_id, dt) 
                    CRUD.insert(connObj, table1, vals1)
                    c1="Driver_Id"
                    c2="AvailableSeats"
                    connCursor.execute(f''' UPDATE public."G5_DRIVER" SET "{c2}"="{c2}"-1 where "{c1}"='{d_id}'    ''')
                    connObj.commit()
                    print("Booking Successfull !! Enjoy your ride !! HAppY JouRnEy :)")
                elif choice == 2: 
                    pass

            else:
                print("OOPS !! Sorry for inconvenience, try after sometime...No Cabs available :| ")
        else:
            try:
                choice = int(input('\n\nRide in Progress !! Do you want to Finish the ride ?? \n1.YES \n2. NO\n'))
                if choice == 1:                        
                    c1="Driver_Id"
                    c2="AvailableSeats"
                        
                    connCursor.execute(f''' UPDATE public."G5_DRIVER" SET "{c2}"="{c2}"+1 where "{c1}"='{d_id}'    ''')
                    connObj.commit()
                    #  DELEETE FROM BOOKING TABLE
                    CRUD.delete(connObj,"G5_BOOKING","E_ID",id)
                elif choice == 2:
                    print('Thanks !! your ride is in progress...Have a Safe Journey :) ')
                    Connection.close(connObj, connCursor)
                    exit()
            except:
                pass
        
            
            



        
        
         
            


            
            


    

        
