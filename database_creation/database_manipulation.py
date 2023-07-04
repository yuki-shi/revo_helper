import sqlite3
import pandas as pd

def connect_to_db(func):
    # Connect and close connection to SQLite
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('pro_helper.db')
        func(conn, *args, **kwargs)
        conn.commit()
        conn.close()
    return wrapper

@connect_to_db
def populate_db(conn, table_name: str, df: pd.DataFrame) -> None:
    # Insert DataFrame into the database
    try:
        df.to_sql(name=table_name,
                  con=conn)
        return
    except Exception as error:
        print('Could not create table', error)
