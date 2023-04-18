import pyodbc
import pandas as pd

def create_table_from_excel_file(excel_file, table_name, database_name, schema_name, server_name, port, user_name, password):
    # create a connection to the database
    conn = pyodbc.connect("DRIVER={ODBC Driver 17 for SQL Server};SERVER="+server_name+";PORT="+port+";DATABASE="+database_name+";UID="+user_name+";PWD="+password)
    # create a cursor
    cursor = conn.cursor()
    # read the excel file
    df = pd.read_excel(excel_file)
    # create a table in the database
    df.to_sql(table_name, conn, schema=schema_name, if_exists='replace', index=False)
    # close the connection
    conn.close()





