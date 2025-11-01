#!/usr/bin/python3
import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that fetches rows from user_data table in batches.
    Yields a list of user dictionaries per batch.
    """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",         # change if your MySQL user differs
            password="",         # add password if required
            database="ALX_prodev"
        )
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []

        # yield any remaining rows not filling a full batch
        if batch:
            yield batch

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def batch_processing(batch_size):
    """
    Processes batches of users, filtering those over age 25,
    and prints each user dictionary.
    """
    for batch in stream_users_in_batches(batch_size):
        # filter users older than 25
        processed = [user for user in batch if user['age'] > 25]

        # yield or print processed users
        for user in processed:
            print(user)

