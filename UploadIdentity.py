import psycopg2
import tkinter as tk
from tkinter import filedialog
# from Connection import Connection

def upload_file(conn):
    # connection = Connection("adep_metadata", "postgres", "postgres", "illin4313", 5431) # create an object of the Connection class
    # conn = connection.connect() # call the connect() method on the object
    cursor=conn.cursor()
   
    id= input("Enter your Driver id:")
    file_path = filedialog.askopenfilename()

    # Open the file in binary mode
    with open(file_path, 'rb') as file:
        # Read the file data
        BLOB_pdf = psycopg2.Binary(open(file_path, 'rb').read()) 
        cursor.execute(f'''update public."G5_DRIVER" set "IdentityProof"= {BLOB_pdf} where "Driver_Id"='{id}' ''')
        conn.commit()
        conn.close()

    # Create a root window
    root = tk.Tk()

    # Create a button that calls the upload_file function when clicked
    upload_button = tk.Button(root, text="Upload File", command=upload_file)
    upload_button.pack()

    # Start the Tkinter event loop
    root.mainloop()

