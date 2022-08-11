import sqlite3
import pandas as pd
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def get_all(col, table_name):
    database = r"DOGE_DATABASE.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        data = pd.read_sql_query("SELECT "+col+" FROM "+table_name, conn)
        return data

def get_by_date(col, table_name, date):
    database = r"DOGE_DATABASE.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        data = pd.read_sql_query("SELECT "+col+" FROM "+table_name+" WHERE Date ='"+date+"'", conn)
        return data

def get_by_range(col, table_name, start, end):
    print("connected.")
    database = r"DOGE_DATABASE.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        data = pd.read_sql_query("SELECT "+col+" FROM "+table_name+" WHERE Date BETWEEN '"+start+"' AND '"+end+"'", conn)
        return data

def add_row(values):
    database = r"DOGE_DATABASE.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO doge_realtime(date,time,day_price,day_open,day_high,day_low,market_cap,volume,total_supply) VALUES (?,?,?,?,?,?,?,?,?)",values)
        conn.commit()
        print("Record inserted successfully", cur.rowcount)
        cur.close()

def add_pred(values):
    database = r"DOGE_DATABASE.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO doge_pred(Date, Predicted_Price, Predicted_High, Predicted_Low) VALUES (?,?,?,?)",values)
        conn.commit()
        #print("Prediction Data inserted successfully", cur.rowcount)
        cur.close()

def add_analysis(values):
    database = r"DOGE_DATABASE.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO doge_model_analysis(Date, Model, R2, MSE, RMSE) VALUES (?,?,?,?,?)",values)
        conn.commit()
        #print("Prediction Data inserted successfully", cur.rowcount)
        cur.close()

def add_histo(values):
    database = r"DOGE_DATABASE.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO doge_histo(Date, Close, Open, High, Low) VALUES (?,?,?,?,?)",values)
        conn.commit()
        print("Historical Data inserted successfully", cur.rowcount)
        cur.close()

def add_des(values):
    database = r"DOGE_DATABASE.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("INSERT INTO doge_decide(Date, MACD, RSI, SO, PRED, Decision) VALUES (?,?,?,?,?,?)",values)
        conn.commit()
        print("Decision Data inserted successfully", cur.rowcount)
        cur.close()

def delete_row(table_name):
    database = r"DOGE_DATABASE.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM "+table_name+";")
        conn.commit()
        print('We have deleted', cur.rowcount, 'records from the table.')
        cur.close()