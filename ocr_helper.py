from PIL import Image
import pytesseract
import re
import os

def extract_expense_from_image(image_path):
    if not os.path.exists(image_path):
        print("Invalid image path.")
        return None

    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)

        lines = text.split("\n")
        total = None
        category = None
        all_numbers = []
        products = []

        skip_keywords = [
            "subtotal", "tax", "charge", "city", "thank", "expires", "store", "manager", "approval", "ref", "terminal", "account", "barcode", "visa", "date", "phone", "please", "copy", "items sold", "cashier", "coupon"
        ]
        for line in lines:
            line = line.strip()
            if not line:
                continue

            if "total" in line.lower():
                numbers = re.findall(r"\d+\.\d{1,2}", line)
                if numbers:
                    total = float(numbers[-1])
                continue

            if any(kw in line.lower() for kw in skip_keywords):
                continue

            numbers = re.findall(r"-?\d+\.\d{1,2}", line)
            if len(numbers) >= 1:
                try:
                    value = float(numbers[-1])
                except:
                    value = None
                name_part = line
                if value is not None:
                   
                    name_part = re.sub(r"-?\d+\.\d{1,2}$", "", line).strip()
                
                name_part = re.sub(r"^[0-9]+\s*", "", name_part)
                
                name_part = re.sub(r"[A-Z]$", "", name_part).strip()
                name = name_part if name_part else "Item"
                if name and value is not None and value != 0:
                    products.append((name, 1, value, value))
                    continue

            all_numbers += [float(n) for n in re.findall(r"\d+\.\d{1,2}", line)]

            if any(word in line.lower() for word in ["grocery", "supermarket", "provision", "store", "target"]):
                category = "Grocery"

        if total is None or total < 1:
            large_numbers = [n for n in all_numbers if n >= 100]
            if large_numbers:
                total = max(large_numbers)
            elif all_numbers:
                total = max(all_numbers)
            else:
                print("[DEBUG] No valid total found.")
                return None

        return {
            "category": category if category else "Other",
            "amount": total,
            "products": products
        }

    except Exception as e:
        print(" OCR Error:", e)
        return None

