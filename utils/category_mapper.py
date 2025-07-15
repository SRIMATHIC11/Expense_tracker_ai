def map_to_category(text):
    text = text.lower()
    if any(x in text for x in ['grocery', 'supermarket', 'vegetable', 'provision']):
        return 'Grocery'
    if any(x in text for x in ['pharmacy', 'medical', 'chemist']):
        return 'Medical'
    if any(x in text for x in ['restaurant', 'food', 'dine']):
        return 'Food'
    if any(x in text for x in ['clothing', 'apparel', 'fashion']):
        return 'Shopping'
    return 'Others'
