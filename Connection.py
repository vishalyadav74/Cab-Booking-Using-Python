import psycopg2
from Services import Services
from Logger import logger

class Connection:

    # Initialize the class with database parameters
    @Services.timer_func
    def __init__(self, dbname, user, password, host, port):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    # Define a method to connect to the database and return a cursor object
    @Services.timer_func
    def connect(self):
        try:
            self.conn = psycopg2.connect(dbname=self.dbname, user=self.user, password=self.password, host=self.host, port=self.port)
            self.cur = self.conn.cursor()
            logger.info(f'Connection set successfully')
            return self.conn
        except psycopg2.Error as e:
            logger.error(f'Unable to connect to the database')
            print("Unable to connect to the database:", e)
    
    @Services.timer_func
    def close(connObj, currObj):
        try:
            currObj.close()
            connObj.close()
            logger.info(f'Connection closed successfully')
            
        except psycopg2.Error as e:
            logger.error(f'Unable to close the connection')
            print("Unable to close the connection:", e)


   