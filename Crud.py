import psycopg2

class CRUD:
    
    def update(connObj,table,colName,newVal,col,id):
        cursor = connObj.cursor()
        try:
            cursor.execute(f''' update public."{table}" set "{colName}"='{newVal}' where "{col}"='{id}' ''')
            connObj.commit()
            count = cursor.rowcount
            return count
        except psycopg2.Error as e:
            print("Unable to update data into the table:", e)

    def delete(connObj, table, col ,id):
        cursor = connObj.cursor()
        try:
            t=cursor.execute(f'''delete from public."{table}" where "{col}"='{id}' ''')
            connObj.commit()
            count = cursor.rowcount
            return count
        except psycopg2.Error as e:
            print("Unable to delete data into the table:", e)
        
    def insert(connObj, table, values):
        cursor = connObj.cursor()
        try:
            cursor.execute(f'insert into public."{table}" values {values}')
            connObj.commit()
            count = cursor.rowcount
            return count
        except psycopg2.Error as e:
            print("Unable to insert data into the table:", e)

    def fetchRecord(connObj,values,tableName):
       cursor=connObj.cursor()
       sqlQuery = f'Select * from public."{tableName}" where '
 
       for field, data in values.items():
          data = "'" + data + "'"
          sqlQuery = sqlQuery + field + '=' + data + ' and '
 
       sqlQuery = sqlQuery[:-5]
       cursor.execute(sqlQuery)
       record = cursor.fetchall()
       return record

 
