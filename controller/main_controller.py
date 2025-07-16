from model.db_model import DBModel
from model.user import User
from model.expense import Expense
from view.cli_view import CLIView
from ollama_integration.llama_helper import get_ai_suggestion

class ExpenseTrackerController:
    def __init__(self):
        self.db = DBModel()
        self.view = CLIView()
        self.user_model = User(self.db)
        self.expense_model = Expense(self.db)
        self.current_user_id = None

    def run(self):
        while True:
            if not self.current_user_id:
                choice = self.view.display_welcome()
                if choice == "1":
                    username, password = self.view.get_credentials()
                    if self.user_model.register(username, password):
                        self.view.show_message("Registration successful. Please login.")
                    else:
                        self.view.show_message("Username already exists.")
                elif choice == "2":
                    username, password = self.view.get_credentials()
                    user_id = self.user_model.login(username, password)
                    if user_id:
                        self.current_user_id = user_id
                        self.view.show_message("Login successful!")
                    else:
                        self.view.show_message("Invalid credentials.")
                elif choice == "3":
                    break
                else:
                    self.view.show_message("Invalid choice")
            else:
                choice = self.view.display_dashboard()
                if choice == "1":
                    data = self.view.get_expense_data()
                    self.expense_model.add_expense(self.current_user_id, *data)
                    self.view.show_message("Expense added successfully.")
                elif choice == "2":
                    expenses = self.expense_model.get_expenses(self.current_user_id)
                    self.view.display_expenses(expenses)
                elif choice == "3":
                    expenses = self.expense_model.get_expenses(self.current_user_id)
                    suggestion = get_ai_suggestion(expenses)
                    self.view.show_message(f"AI Suggestion: {suggestion}")
                elif choice == "4":
                    from model.bill_item import BillItem
                    expense_id = self.expense_model.get_last_expense_id()
                    items = BillItem(self.db).get_items_by_expense(expense_id)
                    self.view.display_bill_items(items)
                elif choice == '5':
                    image_path = input("Enter full path to bill image: ")
                    from ocr_helper import extract_expense_from_image
                    data = extract_expense_from_image(image_path)

                    if data:
                        date = data.get('date', '2025-07-14')
                        note = data.get('note', 'Auto-extracted via OCR')
                        self.db.add_expense(self.current_user_id, data['category'], data['amount'], date, note)
                        from model.bill_item import BillItem
                        expense_id = self.expense_model.get_last_expense_id()
                        
                        products = data.get('products', [])
                        if products:
                            BillItem(self.db).add_bill_items(expense_id, products)
                        
                        BillItem(self.db).add_item(expense_id, 'TOTAL', '', '', data['amount'])
                        print(f"Added Rs.{data['amount']} to {data['category']} on {date}")
                    else:
                        print("Failed to extract expense from image.")

                elif choice == "6":
                    expenses = self.expense_model.get_expenses(self.current_user_id)
                    self.view.display_expenses(expenses)
                    expense_id = input("Enter Expense ID to delete: ")
                    if self.expense_model.delete_expense(self.current_user_id, int(expense_id)):
                        print(" Expense deleted successfully.")
                    else:
                        print(" Failed to delete. Invalid Expense ID.")
                elif choice == "7":
                    self.current_user_id = None
                    self.view.show_message("Logged out.")
