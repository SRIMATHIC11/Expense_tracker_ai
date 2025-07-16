from rich.console import Console
from rich.table import Table

class BillItem:
    def add_item(self, expense_id, name, qty, rate, value):
        """
        Add a single bill item to the database.
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO bill_items (expense_id, product_name, quantity, rate, total_price)
            VALUES (?, ?, ?, ?, ?)
        ''', (expense_id, name, qty, rate, value))
        self.conn.commit()
    def __init__(self, db):
        self.conn = db.get_connection()

    def add_bill_items(self, expense_id, items):
        """
        Add extracted bill items to the database.
        Each item should be a tuple: (product_name, quantity, rate, total_price)
        """
        cursor = self.conn.cursor()
        for name, qty, rate, value in items:
            cursor.execute('''
                INSERT INTO bill_items (expense_id, product_name, quantity, rate, total_price)
                VALUES (?, ?, ?, ?, ?)
            ''', (expense_id, name, qty, rate, value))
        self.conn.commit()

    def get_items_by_expense(self, expense_id):
        """
        Fetch all product items for a given expense ID.
        Returns a list of tuples: (product_name, quantity, rate, total_price)
        """
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT product_name, quantity, rate, total_price
            FROM bill_items
            WHERE expense_id = ?
        ''', (expense_id,))
        return cursor.fetchall()

    def display_items_rich(self, expense_id):
        """
        Display product items beautifully using rich 🧁
        """
        console = Console()
        items = self.get_items_by_expense(expense_id)

        if not items:
            console.print(" No items found for this expense.", style="bold red")
            return

        table = Table(title=f" Items for Expense ID: {expense_id}", show_lines=True)

        table.add_column("Product Name", style="cyan", justify="left")
        table.add_column("Qty", style="magenta", justify="center")
        table.add_column("Rate", style="green", justify="center")
        table.add_column("₹Val", style="bold yellow", justify="center")

        for name, qty, rate, value in items:
            table.add_row(name, str(qty), str(rate), str(value))

        console.print(table)
