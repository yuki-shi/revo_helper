import sqlite3
import pandas as pd

def connect_to_db(func):
    # Connect and close connection to SQLite
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('pro_helper.db')
        result = func(conn, *args, **kwargs)
        conn.commit()
        conn.close()
        return result
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

@connect_to_db
def get_headers(conn, table_name: str = 'pkm_list') -> list[str]:
    cursor = conn.cursor()
    cursor.execute(f'SELECT * FROM {table_name};')
    headers = [x[0] for x in cursor.description]
    return headers

@connect_to_db
def query_db(conn, query: str, table_name: str = 'pkm_list') -> list:
    # Create a cursor for queries
    cursor = conn.cursor()

    # Run SQL query
    cursor.execute(f"""
        SELECT * FROM {table_name}
        WHERE {query};
    """)

    # Get result rows
    rows = cursor.fetchall()

    # Get table headers
    headers = get_headers()

    # Append the queries rows
    return rows
