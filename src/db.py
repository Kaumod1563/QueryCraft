def connect_to_database(db_name):
    import sqlite3
    connection = sqlite3.connect(db_name)
    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        return cursor.fetchall()
    except Exception as e:
        print("An error occurred:", e)
        return None
    finally:
        cursor.close()

def close_connection(connection):
    connection.close()