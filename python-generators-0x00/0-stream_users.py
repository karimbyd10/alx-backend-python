#!/usr/bin/python3
import mysql.connector

def stream_users():
    """
    Generator function that streams rows from the user_data table
    in the ALX_prodev database one by one using yield.
    """
    try:
        # Connect to the ALX_prodev database
        connection = mysql.connector.connect(
            host="localhost",
            user="root",          # change if your MySQL user is different
            password="",          # add your MySQL password if required
            database="ALX_prodev"
        )

        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        # Yield each row one by one
        for row in cursor:
            yield row

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

