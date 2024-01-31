# Using standard Python csv
# Import pandas and sqlalchemy libraries
import pandas as pd
import sqlalchemy as sa
import psycopg2
import csv
from SensitiveData import SensitiveData
from Crud import CRUD
from Services import Services
# connObj = None
# connCursor= None

class import_csv:
        def importEmployeeData(connObj,csvFileName,tableName):
            try:
                with open(csvFileName, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    # Read the header row to get the column names
                    header = next(csv_reader)
                    column_names = ', '.join(header)
                
                    for record in csv_reader:
                        valueList=[]
                        for value in record:
                            valueList.append(value)
    
                        empId=valueList[0]
                        record=CRUD.fetchRecord(connObj,{'"E_Id"':empId},tableName)
                
                        if record==[]:
                            sensitiveRecords=valueList[7:]
    
                            passValue=sensitiveRecords[1]
                            passValue=SensitiveData.encryption(passValue)
                            sensitiveRecords[1]=passValue
                            sensitiveRecords=tuple(sensitiveRecords)
    
                            empRecords=tuple(valueList[0:7])
                        
                            CRUD.insert(connObj,tableName, empRecords)
                            CRUD.insert(connObj,'G5_SENSITIVE_DATA',sensitiveRecords)
                            print("Import completed successfully")
                        else:
                            print(f'record with id {empId} exist')
    
            except Exception as e:
                # print(e)
                print("Exception Occured", e)
        
        def fetchInCSV(connObj,tableName):
            # create a cursor
            cur = connObj.cursor()
            # execute a sql query
            try:
                cur.execute(f'''select * from public."{tableName}" inner join public."G5_SENSITIVE_DATA"  on "E_Id" = "ID"  ''')
                # fetch the results
                results = cur.fetchall()
                # open a file in the downloads folder
                with open("exported_data.csv", "w", newline="") as f:
                    # Create a CSV writer
                    writer = csv.writer(f)
                    # write the column names
                    headers = []
                    for i in range(len(cur.description)):
                        headers.append(cur.description[i][0])

                    headers = tuple(headers)
                    writer.writerow(headers)

                    writer.writerows(results)
                    print("File exported successfully")
        
            except Exception as e:
                print("Exception occured",e)

        
        def importLogData(connObj,csvFileName,tableName):
            try:
                with open(csvFileName, 'r') as csv_file:
                    csv_reader = csv.reader(csv_file)
                    # Read the header row to get the column names
                    header = next(csv_reader)
                    column_names = ', '.join(header)
                
                    for record in csv_reader:
                        valueList=[]
                        for value in record:
                            valueList.append(value)
    
                        empId=valueList[0]
                        record=CRUD.fetchRecord(connObj,{'"Time"':empId},tableName)
                
                        if record==[]:
                            # sensitiveRecords=valueList[7:]
    
                            # passValue=sensitiveRecords[1]
                            # passValue=SensitiveData.encryption(passValue)
                            # sensitiveRecords[1]=passValue
                            # sensitiveRecords=tuple(sensitiveRecords)
    
                            empRecords=tuple(valueList[0:2])
                            
                            CRUD.insert(connObj,tableName, empRecords)
                                # CRUD.insert(connObj,'G5_SENSITIVE_DATA',sensitiveRecords)
                            print("Import completed successfully")
                        else:
                            print(f'record with id {empId} exist')
    
            except Exception as e:
                # print(e)
                print("Exception Occured", e)
        