class Expense:

    def delete_expense(self, user_id, expense_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM expenses WHERE user_id=? AND id=?", (user_id, expense_id))
        self.conn.commit()
        return cursor.rowcount > 0
    def __init__(self, db):
        self.conn = db.get_connection()

    def add_expense(self, user_id, category, amount, date, description):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO expenses (user_id, category, amount, date, description)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, category, amount, date, description))
        self.conn.commit()

    def get_expenses(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, category, amount, date, description FROM expenses WHERE user_id=?", (user_id,))
        return cursor.fetchall()

    def get_last_expense_id(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM expenses ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        return result[0] if result else None

