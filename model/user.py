class User:
    def __init__(self, db):
        self.conn = db.get_connection()

    def register(self, username, password):
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            self.conn.commit()
            return True
        except:
            return False

    def login(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
        result = cursor.fetchone()
        return result[0] if result else None
