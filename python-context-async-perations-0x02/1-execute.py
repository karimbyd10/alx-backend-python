import sqlite3

class ExecuteQuery:
    def __init__(self, db_name, query, params=None):
        """Initialize with database name, query, and optional parameters."""
        self.db_name = db_name
        self.query = query
        self.params = params or ()
        self.conn = None
        self.cursor = None
        self.results = None

    def __enter__(self):
        """Open connection, execute query, and return the results."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("[INFO] Database connection opened.")
        try:
            print(f"[INFO] Executing query: {self.query} with params: {self.params}")
            self.cursor.execute(self.query, self.params)
            self.results = self.cursor.fetchall()
            print("[INFO] Query executed successfully.")
        except Exception as e:
            print(f"[ERROR] Query execution failed: {e}")
            self.results = None
        return self.results  # Return query results directly

    def __exit__(self, exc_type, exc_value, traceback):
        """Handle transaction commit/rollback and close connection."""
        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_value}. Rolling back transaction.")
            self.conn.rollback()
        else:
            self.conn.commit()
            print("[INFO] Transaction committed successfully.")
        self.conn.close()
        print("[INFO] Database connection closed.")
        return False  # Don't suppress exceptions


# ✅ Example usage
if __name__ == "__main__":
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    with ExecuteQuery("users.db", query, params) as results:
        if results:
            print("Query Results:", results)
        else:
            print("No results found or query failed.")

