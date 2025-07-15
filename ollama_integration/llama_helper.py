import subprocess

def get_ai_suggestion(expenses):
    if not expenses:
        return "No expenses to analyze."

    prompt = "Analyze this spending and suggest one tip to save money:\nHere are my recent expenses:\n"
    
    for expense in expenses:
        try:
            # Safely extract data with fallback
            category = expense[1] if len(expense) > 1 else "Unknown"
            amount = expense[2] if len(expense) > 2 else "0"
            date = expense[3] if len(expense) > 3 else "Unknown date"
            description = expense[4] if len(expense) > 4 else "No description"
            
            prompt += f"{date} - {category} - ₹{amount}: {description}\n"
        except Exception as e:
            prompt += f"Incomplete record: {expense}\n"

    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Failed to get AI suggestion: {e}"
