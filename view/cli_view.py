class CLIView:
    def display_welcome(self):
        from rich.console import Console
        from rich.panel import Panel
        from rich.text import Text
        console = Console()
        console.print(Panel(Text("Expense Tracker", style="bold magenta"), expand=False))
        console.print("[bold cyan]1.[/] Register", justify="left")
        console.print("[bold cyan]2.[/] Login", justify="left")
        console.print("[bold cyan]3.[/] Exit", justify="left")
        return console.input("[bold yellow]Choose an option:[/] ")

    def get_credentials(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        return username, password

    def display_dashboard(self):
        from rich.console import Console
        console = Console()
        options = [
            "Add Expense Manually",
            "View Expenses",
            "Get AI Suggestion",
            "View Bill Items (Rich Table)",
            "Upload Receipt Image (Auto Extract)",
            "Delete Expense",
            "Logout"
        ]
        for idx, opt in enumerate(options, 1):
            console.print(f"[bold cyan]{idx}.[/] {opt}", justify="left")
        return console.input("[bold yellow]Choose an option:[/] ")

    def get_expense_data(self):
        category = input("Enter expense category: ")
        amount = float(input("Enter amount: "))
        date = input("Enter date (YYYY-MM-DD): ")
        note = input("Enter note (optional): ")
        return category, amount, date, note

    def display_expenses(self, expenses):
        from rich.console import Console
        from rich.table import Table
        from rich.text import Text
        console = Console()
        table = Table(title="Expenses", show_lines=True, header_style="bold magenta")
        table.add_column("ID", style="bold yellow", justify="right")
        table.add_column("Category", style="cyan")
        table.add_column("Amount", style="green", justify="right")
        table.add_column("Date", style="white", justify="center")
        table.add_column("Note", style="magenta")
        if not expenses:
            console.print("[bold red]No expenses found.[/]")
            return
        for expense in expenses:
            table.add_row(str(expense[0]), str(expense[1]), f"₹{expense[2]}", str(expense[3]), str(expense[4]))
        console.print(table)

    def show_message(self, message):
        from rich.console import Console
        console = Console()
        console.print(f"[bold green]{message}[/]")

    def get_expense_id(self):
        from rich.console import Console
        console = Console()
        return int(console.input("[bold yellow]Enter Expense ID to delete:[/] "))

    def display_bill_items(self, items):
        from rich.console import Console
        from rich.table import Table
        console = Console()
        table = Table(title="Bill Items", show_lines=True, header_style="bold magenta")
        table.add_column("Product Name", style="bold cyan")
        table.add_column("Qty", style="yellow", justify="right")
        table.add_column("Rate", style="green", justify="right")
        table.add_column("Total", style="magenta", justify="right")
        if not items:
            console.print("[bold red]No bill items found.[/]")
            return
        for name, qty, rate, total in items:
            table.add_row(str(name), str(qty), str(rate), str(total))
        console.print(table)
