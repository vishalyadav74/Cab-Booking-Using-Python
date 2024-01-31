from ImportExport import import_csv
from Services import Services
from Connection import Connection
from termcolor import colored, cprint
from prettytable import PrettyTable
import csv

connObj = None
connCursor= None
 
class Admin:

    @Services.timer_func
    def initialiseConn(self, connObjTemp):
        global connObj
        global connCursor
        connObj=connObjTemp
        connCursor=connObj.cursor()

    def login():
        cprint("\n----------Please Login-----------\n", 'green',attrs=['bold'])
        user=input("Enter User Name: ")
        password1= input("Enter password: ")
        sql = '''select * from public."G5_ADMIN" where "USER_NAME"= %s and "PASSWORD"=%s'''
        connCursor.execute(sql, (user,password1))             
        result = connCursor.fetchone()
        
        if result is not None:
            cprint("\n\nLogin successful!", 'yellow',attrs=['bold'])
            cprint("\n\n----------Welcome Admin----------\n" ,'green',attrs=['bold'])
            print("1. Approve Driver")
            print("2. Approve Employee")
            print("3. for Export")
            print("4. for Import")
            print("5. for Log file Import to Database")
            print("6. Exit\n")
            choice = ''
            try:
                choice = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number ...')
            
            if choice == 1:
                Admin.is_Approve_driver()
            elif choice == 2:
                Admin.is_Approve_Emp()
            elif choice == 3:
                import_csv.fetchInCSV(connObj,'G5_EMPLOYEE')
            elif choice == 4:
                fileName = input("Enter file name")
                import_csv.importEmployeeData(connObj,fileName,'G5_EMPLOYEE')                    
            elif choice == 5:
                Admin.export_log()
            elif choice == 6:
                pass
            else:
                print('Invalid choice. Please enter a number between 1 and 4.')
                return True
        else:
            print("Wrong username or password!")

    def menu(conObjTemp):
        objAdmin=Admin()
        objAdmin.initialiseConn(conObjTemp)
        cprint("\n\n---------Welcome Admin----------\n",'green',attrs=['bold'])
        print("1. Login")
        print("2. Exit")

        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        if option == 1:
               Admin.login() 
        elif option == 2:
                print('Thanks message before exiting')
                Connection.close(connObj, connCursor)
                exit()
        else:
                print('Invalid option. Please enter only 1 and 2.')      
       
    
    @Services.timer_func
    def is_Approve_driver():
         cprint("\n\n-----------List of all drivers-------------\n\n",'green',attrs=['bold'])
         t = PrettyTable(['ID', 'Name', 'Contact', 'Source', 'Destination', 'CabNumber'])
         sql= ''' SELECT * FROM public."G5_DRIVER" WHERE "Status"=0  '''
         connCursor.execute(sql)             
         result = connCursor.fetchall()
         for row in result:
            t.add_row([row[0],row[1],row[4],row[5],row[6],row[7]])
         cprint(t, 'yellow')
         try:
                id=input("\nEnter driver id of driver which you want to approve: \n")
                c1="Driver_Id"
                c2="Status"
                c3="IdentityProof"
                connCursor.execute(f'''    Select "{c3}" from public."G5_DRIVER" where "{c1}"='{id}'     ''' )
                row=connCursor.fetchone()[0]
                BLOB=row
                with open("IdentityFile.pdf", 'wb') as file:
                     file.write(BLOB)

                print("\nAre you check with Driver's Identity Proofs Documents? Do you want to approve the Driver? \n 1.YES\n 2.NO\n\n")
                option = ''
                try:
                    option = int(input('Enter your choice: '))
                except:
                    print('Wrong input. Please enter a number ...')
                if option == 1:
                    connCursor.execute(f''' UPDATE public."G5_DRIVER" set "{c2}"= 1 WHERE "{c1}" = '{id}' ''')
                    connObj.commit()
                    cprint("Driver approved!!\n\n", 'yellow',attrs=['bold'])
                elif option == 2:
                    print("Not approved")

                else:
                        print('Invalid option. Please enter a number between 1 and 4.')
                
         except:
                print("Please enter valid driver id")
                
    @Services.timer_func    
    def is_Approve_Emp():
         cprint("\n\n-----------List of all employees-------------\n\n",'green',attrs=['bold'])
         sql=''' SELECT * FROM public."G5_EMPLOYEE" WHERE "Status"=0  '''
         connCursor.execute(sql)             
         result = connCursor.fetchall()
         t = PrettyTable(['ID', 'Name', 'Contact', 'Address'])
         for row in result:
            t.add_row([row[0],row[1],row[4],row[5]])
         cprint(t, 'yellow')
         try:
                id=input("Enter employee id of employee which you want to approve:\n")
                c1="E_Id"
                c2="Status"
                connCursor.execute(f''' UPDATE public."G5_EMPLOYEE" set "{c2}"= 1 WHERE "{c1}" = '{id}' ''')
                connObj.commit()
                cprint("Employee approved!!",  'yellow',attrs=['bold'])
         except:
                print("Please enter valid employee id")

    def export_log():
         # Open the log file for reading
        with open("file.log", "r") as log_file:
            lines = log_file.readlines()

        # Assuming each line in the log file is in CSV format
        # You can adjust the delimiter if needed
        data = [line.strip().split(",") for line in lines]

        # Write the data to a CSV file
        with open("file.csv", "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(data)

        fileName = input("\nEnter file name: ")
        import_csv.importLogData(connObj,fileName,'G5_LOG')

        