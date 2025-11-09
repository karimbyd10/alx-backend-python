import sqlite3

class DatabaseConnection:
    def __init__(self, db_name):
        """Initialize with the database name."""
        self.db_name = db_name
        self.conn = None
        self.cursor = None

    def __enter__(self):
        """Open the database connection and return a cursor."""
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        print("[INFO] Database connection opened.")
        return self.cursor

    def __exit__(self, exc_type, exc_value, traceback):
        """Close the connection and handle exceptions if any."""
        if exc_type:
            print(f"[ERROR] Exception occurred: {exc_value}. Rolling back transaction.")
            self.conn.rollback()
        else:
            self.conn.commit()
            print("[INFO] Transaction committed successfully.")
        self.conn.close()
        print("[INFO] Database connection closed.")
        return False  # Propagate exceptions if any


# ✅ Example usage
if __name__ == "__main__":
    with DatabaseConnection("users.db") as cursor:
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print("Query Results:", results)

