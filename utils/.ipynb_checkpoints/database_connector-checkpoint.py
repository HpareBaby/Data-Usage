#!/home/frontiir/.venv/bin/python 

from dotenv import load_dotenv
from pathlib import Path
import os
import sys
import pandas as pd
import psycopg2 as sql
from sqlalchemy import create_engine 
import psycopg2.extras as extras
from os.path import join, dirname
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class DBConn: 
    """ database connection for postgresql"""
    def __init__(self): 
        pass

    def connect(self):
        conn = None
        try: 
            conn=sql.connect(
                 host=os.getenv("HOST"),
                 database =os.getenv("DATABASE_NAME_DEVOPS"),
                 user = os.getenv("DATABASE_USER"),
                 password = os.getenv("DATABASE_SECRETE"))
        except (Exception, sql.DatabaseError) as error: 
            conn.close()
            sys.exit(1)
        return conn
       
    def query_to_postgresql(self,query):
        conn = self.connect()
        try:
            cursor = conn.cursor()
            cursor.execute(query)
        except (Exception, sql.DatabaseError) as error:
            cursor.close()
            conn.close()
            print(error)
            sys.exit(1) 

        # Naturally we get a list of tupples
        tupples = cursor.fetchall()
        cursor.close()
        conn.close()
        return tupples

    def execute_values(self,df, table):
        conn = self.connect()
        tuples = [tuple(x) for x in df.to_numpy()]
        # Comma-separated dataframe columns
        cols = ','.join(list(df.columns))
        # SQL query to execute
        print(table)
        query  = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
        cursor = conn.cursor()
        try:
            extras.execute_values(cursor, query, tuples)
            conn.commit()
        except (Exception, sql.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cursor.close()
            conn.close()
            raise error
        print("execute_values() done")
        cursor.close()
        conn.close()
        
    def truncate_table(self,table):
        conn = self.connect()
        cursor = conn.cursor()
        try: 
            query = "TRUNCATE TABLE %s" % table
            cursor.execute(query)
            conn.commit() 
        except (Exception, sql.DatabaseError) as error:
            conn.rollback()
            cursor.close()
            conn.close() 
            raise error
        print("Turncate the Table")
        cursor.close()
        conn.close() 

            
        
