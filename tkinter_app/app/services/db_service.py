import os
import sqlite3
import tkinter.messagebox as messagebox

class DBService:
    def __init__(self, database="school_db.sqlite"):
        self.database = database
        self.connection = None

    def connect(self):
        """Establish database connection and initialize tables if needed."""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            db_path = os.path.join(base_dir, self.database)
            
            # Connect to SQLite database (creates it if it doesn't exist)
            self.connection = sqlite3.connect(db_path)
            self.connection.row_factory = sqlite3.Row  # To return dict-like objects
            
            self._initialize_tables()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to connect to SQLite database: {e}")
            return False

    def _initialize_tables(self):
        """Reads schema.sql and executes it to ensure tables exist."""
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            schema_path = os.path.join(base_dir, 'db', 'schema.sql')
            
            if os.path.exists(schema_path):
                with open(schema_path, 'r') as f:
                    schema_script = f.read()
                
                # SQLite doesn't support AUTO_INCREMENT or ENUM exactly like MySQL in raw strings,
                # but we will replace common MySQL-isms with SQLite equivalents.
                schema_script = schema_script.replace("AUTO_INCREMENT", "AUTOINCREMENT")
                # SQLite ENUM workaround (it accepts the syntax but ignores it)
                
                cursor = self.connection.cursor()
                cursor.executescript(schema_script)
                self.connection.commit()
                cursor.close()
        except sqlite3.Error as e:
            print(f"Error initializing tables: {e}")
        except Exception as e:
            print(f"File reading error: {e}")

    def get_connection(self):
        if self.connection is None:
            if not self.connect():
                return None
        return self.connection

    def execute_query(self, query, params=None):
        """Execute INSERT/UPDATE/DELETE queries."""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            # SQLite uses ? instead of %s for parameters
            query = query.replace('%s', '?')
            cursor.execute(query, params or ())
            conn.commit()
            cursor.close()
            return True
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Query Execution Error: {e}")
            return False

    def fetch_all(self, query, params=None):
        """Execute SELECT query and return all results."""
        conn = self.get_connection()
        if not conn:
            return []
            
        try:
            cursor = conn.cursor()
            query = query.replace('%s', '?')
            cursor.execute(query, params or ())
            # Convert rows to dicts
            results = [dict(row) for row in cursor.fetchall()]
            cursor.close()
            return results
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Fetch Error: {e}")
            return []

    def fetch_one(self, query, params=None):
        """Execute SELECT query and return a single result."""
        conn = self.get_connection()
        if not conn:
            return None
            
        try:
            cursor = conn.cursor()
            query = query.replace('%s', '?')
            cursor.execute(query, params or ())
            result = cursor.fetchone()
            cursor.close()
            return dict(result) if result else None
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Fetch Error: {e}")
            return None

    def close(self):
        if self.connection:
            self.connection.close()

# Global instance
db = DBService()
