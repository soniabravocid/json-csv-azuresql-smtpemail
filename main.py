import pandas as pd
import pyodbc
from utilities import sender as s

# Input Files:  
# 1. db_classification.json: File that contains information about databases in the organization and their classification according to its data sensitivity level (high, medium, or low) /*
# 2. users.csv: File that contains information abouts users and their managers.


db_df = pd.read_json("input/db_classification.json").databases

users_df = pd.read_csv ("input/users.csv")

# Delete columns not used
del users_df['row_id']

# Database connection information
server = 'tcp:sqlserverinstance-dev.database.windows.net'
database = 'Development-DB'
username = 'soniabr'
password_db = '2121G5402!s'   
driver= '{ODBC Driver 17 for SQL Server}'

# Email parameters
smtp_server = "smtp.gmail.com"
sender_email = "soniabravodev@gmail.com"
password_email = "2121H5402s"

# sender class instance
sender_instance = s.sender(smtp_server,sender_email,password_email)

# Connect to a SQL database
with pyodbc.connect('DRIVER='+driver+';SERVER='+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password_db) as conn:
    
    with conn.cursor() as cursor:
       
        # Store or update users 
        for index, row in users_df.iterrows():
            
            cursor.execute(\
                "IF NOT EXISTS (SELECT * FROM dbo.users WHERE user_id=?)\
                    BEGIN\
                        INSERT INTO dbo.users (user_id,user_state,user_manager) values (?,?,?)\
                    END",row[0],row[0],row[1],row[2]
                    )
            conn.commit()
        
        # Store DB information
        for db in db_df:

            cursor.execute(\
                "IF NOT EXISTS (SELECT * FROM dbo.databases WHERE db_name =?)\
                    BEGIN\
                        INSERT INTO dbo.databases (db_name,data_classification,owner_id) values (?,?,?)\
                    END", db['db_name'], db['db_name'], db['data_classification'], db['owner_id']
                )
            conn.commit()

            if db['data_classification'] == 'High':

                # Get email manager
                cursor.execute("SELECT user_manager FROM dbo.users WHERE user_id=?",db['owner_id'])
                receiver_email = cursor.fetchone()

                message =  """Favor validar nivel de confidencialidad "High" de la base de datos """ + db['db_name']
                subject = "Validación Clasificación BD " + db['db_name']
        
                sender_instance.send_email(receiver_email[0], message, subject)
            