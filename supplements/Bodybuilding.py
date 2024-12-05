import pandas as pd
import re

# Load the CSV file
file_path = '/Users/sameedahmed/Desktop/NLPPP/product_details_with_flavours.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Clean the 'Product Price' column
def clean_price(price):
    if pd.isna(price):  # Handle missing values
        return None
    price = str(price)  # Convert to string
    match = re.search(r'\$\d+\.\d{2}', price)
    return match.group(0) if match else None

df['Product Price'] = df['Product Price'].apply(clean_price)

# Add 'Category' column based on row ranges
def assign_category(index):
    if 1 <= index <= 41:
        return 'whey protein'
    elif 42 <= index <= 59:
        return 'whey protein isolate'
    elif 60 <= index <= 71:
        return 'Plant protein'
    elif 72 <= index <= 77:
        return 'protein bars'
    elif 79 <= index <= 88:
        return 'STIMULANT FREE PRE-WORKOUT'
    elif 89 <= index <= 128:
        return 'AMINO ACIDS & BCAAS'
    elif 129 <= index <= 155:
        return 'hydration'
    elif 156 <= index <= 169:
        return 'Multi vitamins'
    elif 170 <= index <= 188:
        return 'GREENS & SUPER FOODS'
    else:
        return 'Unknown'

# Apply category assignment based on the index (1-based)
df['Category'] = [assign_category(i + 1) for i in range(len(df))]

# Save the cleaned data back to a new CSV file
output_path = 'cleaned_file.csv'  # Replace with your desired output file path
df.to_csv(output_path, index=False)

print("Data cleaned and saved to:", output_path)
