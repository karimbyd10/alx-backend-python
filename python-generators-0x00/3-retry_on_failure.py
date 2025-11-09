import time
import sqlite3
import functools

# Reuse the with_db_connection decorator
def with_db_connection(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect('users.db')
        try:
            result = func(conn, *args, **kwargs)
        finally:
            conn.close()
        return result
    return wrapper


# Decorator to retry on failure
def retry_on_failure(retries=3, delay=2):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt < retries:
                try:
                    print(f"[LOG] Attempt {attempt + 1} of {retries}")
                    return func(*args, **kwargs)
                except sqlite3.OperationalError as e:
                    attempt += 1
                    print(f"[WARNING] OperationalError: {e}. Retrying in {delay} seconds...")
                    time.sleep(delay)
                except Exception as e:
                    # If it's not a transient error, don't retry
                    print(f"[ERROR] Non-transient error: {e}")
                    raise
            print("[ERROR] Max retries reached. Operation failed.")
            raise Exception("Database operation failed after retries.")
        return wrapper
    return decorator


@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    return cursor.fetchall()


#### Attempt to fetch users with automatic retry on failure
users = fetch_users_with_retry()
print(users)

