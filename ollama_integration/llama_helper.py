import subprocess

def get_ai_suggestion(expenses):
    if not expenses:
        return "No expenses to analyze."

    
    category_totals = {}
    for expense in expenses:
        category = expense[1] if len(expense) > 1 else "Unknown"
        amount = float(expense[2]) if len(expense) > 2 else 0
        category_totals[category] = category_totals.get(category, 0) + amount

    if not category_totals:
        return "No spending data to analyze."

    top_category = max(category_totals, key=category_totals.get)
    top_amount = category_totals[top_category]
    return f"You spent the most on {top_category} (₹{top_amount:.2f}). Try to set a budget for this category next month!"
