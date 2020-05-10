import pandas as pd
import pyodbc

def main():
    conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=13.82.21.132;'
                          'Database=VNPOST_Appointment_dev;'
                          'UID=service;'
                          'PWD=Service123;')

    sql = 'select * from FormTemplate'
    dataframe  = pd.read_sql(sql, conn)
    print(dataframe.head())

main()
