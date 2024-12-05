import re

# Function to clean text and replace patterns
def clean_product_data(data):
    # Define a mapping of patterns to replace with the generic word or phrase
    replacement_patterns = {
        r"\*\*Benefits of .*?\*\*": "**Benefits**",  # Matches 'Benefits of...' with any product name
        r"\*\*.*?Benefits\*\*": "**Benefits**",  # Matches 'Key Features of ... Benefits', etc.
        r"\*\*BENEFITS OF.*?\*\*": "**Benefits**",  # Matches 'BENEFITS OF...' with any product name
        r"\*\*Key Benefits of .*?\*\*": "**Benefits**",  # Specifically matches 'Key Benefits of ...'
        r"\*\*How to Use.*?\*\*": "**How to Use**",  # Matches 'How to Use...' with any suffix
        r"\*\*WHEN AND HOW TO USE\?\*\*": "**How to Use**",  # Matches 'WHEN AND HOW TO USE?'
        r"\*\*.*?Ingredients\*\*": "**Ingredients**",  # Matches 'Ingredients...' with any prefix
        r"\*\*Range of Flavors:.*?\*\*": "**Flavours**",  # Matches 'Range of Flavors...' and suffix
        r"\*\*.*?Flavors.*?\*\*": "**Flavours**",  # Matches 'FLAVOURS OF...' or '... FLAVORS'
        r"\*\*FLAVOURS OF .*?\*\*": "**Flavours**",  # Matches 'FLAVOURS OF...' specifically
        r"\*\*Why Chose .*?\*\*": "**Why Choose**",  # Matches 'Why Chose...' with any product name
        r"\*\*Why Choose .*?\*\*": "**Why Choose**",  # Matches 'Why Choose...' with any product name
        r"\*\*.*?Why Choose.*?\*\*": "**Why Choose**",  # Matches '*Why Choose Our Shilajit?**'
        r"\*\*DIRECTION TO USE.*?\*\*": "**How to Use**",  # Matches 'DIRECTION TO USE...'
        r"\*\*KEY FEATURES OF .*?\*\*": "**Features**",  # Matches 'KEY FEATURES OF ...'
        r"\*\*INGREDIENTS OF .*?\*\*": "**Ingredients**",  # Matches 'INGREDIENTS OF ...'
        r"\*\*USE OF .*?\*\*": "**How to Use**",  # Matches 'USE OF ...'
        r"\*\*DIRECTIONS FOR USING .*?\*\*": "**How to Use**",  # Matches 'DIRECTIONS FOR USING ...'
        r"\*\*HOW TO CONSUME\*\*": "**How to Use**",  # Matches 'HOW TO CONSUME'
        r"\*\*.*?Description.*?\*\*": "**General Description**",  # Matches variations of description
        r"\*\*.*?Warnings.*?\*\*": "**Warnings**",  # Matches variations of warnings
        r"\*\*.*?Nutritional Facts.*?\*\*": "**Nutritional Information**",  # Matches variations of nutritional facts
    }
    # Iterate over the patterns and replace them
    for pattern, replacement in replacement_patterns.items():
        data = re.sub(pattern, replacement, data, flags=re.IGNORECASE)
    
    return data

# Read product data from a text file
file_path = '/Users/sameedahmed/Desktop/NLPPP/scraped_products.txt'  # Make sure to replace with the correct file path
with open(file_path, 'r') as file:
    product_data = file.read()

# Process the product data
cleaned_data = clean_product_data(product_data)

# Output the cleaned data
print(cleaned_data)
# Define the path for the output cleaned data file
output_file_path = '/Users/sameedahmed/Desktop/NLPPP/cleaned_products.txt'  # Replace with the desired output file path

# Write the cleaned data to the output file
with open(output_file_path, 'w') as output_file:
    output_file.write(cleaned_data)

print(f"Cleaned data has been saved to {output_file_path}")


