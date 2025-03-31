import re
import pandas as pd

def standardize_product_name(name):
    if pd.isna(name):
        return ""

    name = str(name).lower()
    name = re.sub(r'[^a-z0-9.\s]', '', name)  # Remove punctuation
    name = re.sub(r'\s+', ' ', name).strip()  # Collapse multiple spaces

    # Convert lb to oz
    lb_match = re.search(r'(\d+(?:\.\d+)?)\s?lb', name)
    if lb_match:
        lb_value = float(lb_match.group(1))
        name = re.sub(r'(\d+(?:\.\d+)?)\s?lb', f"{round(lb_value * 16, 2)}oz", name)

    # Convert gal to oz
    gal_match = re.search(r'(\d+(?:\.\d+)?)\s?gal', name)
    if gal_match:
        gal_value = float(gal_match.group(1))
        name = re.sub(r'(\d+(?:\.\d+)?)\s?gal', f"{round(gal_value * 128, 2)}oz", name)

    # Ensure there's no space before oz/g/lb/gallon
    name = re.sub(r'(\d+\.?\d*)\s?(oz|g|ml)', r'\1\2', name)

    return name
