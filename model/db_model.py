import sqlite3

class DBModel:
    def __init__(self, db_name="expense_tracker.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE,
                password TEXT
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                category TEXT,
                amount REAL,
                date TEXT,
                description TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bill_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                expense_id INTEGER,
                product_name TEXT,
                quantity INTEGER,
                rate REAL,
                total_price REAL,
                FOREIGN KEY (expense_id) REFERENCES expenses(id)
            )
        ''')

        self.conn.commit()
    
    def add_expense(self, user_id, category, amount, date, description):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO expenses (user_id, category, amount, date, description) VALUES (?, ?, ?, ?, ?)",
            (user_id, category, amount, date, description)
        )
        conn.commit()


    def get_connection(self):
        return self.conn
