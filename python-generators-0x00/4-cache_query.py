import time
import sqlite3
import functools

# Global query cache dictionary
query_cache = {}

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


# Decorator to cache query results
def cache_query(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Extract the SQL query from arguments
        query = kwargs.get('query') if 'query' in kwargs else args[1] if len(args) > 1 else None
        
        # Check cache first
        if query in query_cache:
            print(f"[CACHE HIT] Returning cached results for query:\n{query}")
            return query_cache[query]
        
        # Execute query if not cached
        print(f"[CACHE MISS] Executing query and caching results:\n{query}")
        result = func(*args, **kwargs)
        
        # Cache the result
        query_cache[query] = result
        return result
    return wrapper


@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()


#### First call will cache the result
users = fetch_users_with_cache(query="SELECT * FROM users")

#### Second call will use the cached result
users_again = fetch_users_with_cache(query="SELECT * FROM users")

