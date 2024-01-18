import mysql.connector

# def create_table(cursor):
#     create_table_query = '''
#     CREATE TABLE IF NOT EXISTS users (
#         id INT AUTO_INCREMENT PRIMARY KEY,
#         username VARCHAR(255) UNIQUE,
#         password VARCHAR(255)
#     )
#     '''
#     cursor.execute(create_table_query)

def create_connection(host, user, password, database):
    connection = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
    return connection

def initialize_database(host, user, password, database):
    connection = create_connection(host, user, password, database)
    cursor = connection.cursor()

    # Create the database if it doesn't exist
    create_database_query = f'CREATE DATABASE IF NOT EXISTS {database}'
    cursor.execute(create_database_query)
    connection.commit()

    # Switch to the created database
    cursor.execute(f'USE {database}')

    # Create the users table if it doesn't exist
    # create_table(cursor)
    connection.commit()

    # return connection, cursor
