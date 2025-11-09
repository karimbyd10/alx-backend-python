import sqlite3
import functools

#### decorator to log SQL queries
def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query (assuming it's passed as 'query' argument)
        query = kwargs.get('query') if 'query' in kwargs else args[0] if args else None
        print(f"[LOG] Executing SQL Query: {query}")
        
        # Execute the original function
        result = func(*args, **kwargs)
        
        print("[LOG] Query execution completed.")
        return result
    return wrapper


@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
print(users)

