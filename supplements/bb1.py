import requests
from bs4 import BeautifulSoup
import csv
import os

# List of URLs to scrape
urls = [
    "https://shop.bodybuilding.com/products/bodybuilding-signature-greens",
    "https://shop.bodybuilding.com/products/6am-run-supergreens",
    "https://shop.bodybuilding.com/products/feel-good-maca-root-powder",
    "https://shop.bodybuilding.com/products/feel-good-matcha-tea-powder",
    "https://shop.bodybuilding.com/products/feel-good-spirulina-powder",
    "https://shop.bodybuilding.com/products/performance-inspired-nutrition-better-beet-powder",
    "https://shop.bodybuilding.com/products/feel-good-fortified-turmeric-powder",
    "https://shop.bodybuilding.com/products/nourish-bloom-coffee-mushroom-infusion",
    "https://shop.bodybuilding.com/products/remix-nutrition-shroom-sync",
    "https://shop.bodybuilding.com/products/legion-genesis-green-superfood-powder",
    "https://shop.bodybuilding.com/products/nourish-bloom-greens-detox",
    "https://shop.bodybuilding.com/products/snap-supplements-collagen-super-greens",
    "https://shop.bodybuilding.com/products/codeage-instantfood-easy-veggies-daily-veggie-blend-supplement",
    "https://shop.bodybuilding.com/products/codeage-instantfood-five-a-day-fruits-vegetables-in-1-capsule",
    "https://shop.bodybuilding.com/products/performance-inspired-nutrition-greens-for-life-organic-greens-mushrooms-superfoods",
    "https://shop.bodybuilding.com/products/nourish-bloom-coffee-manuka-honey",
    "https://shop.bodybuilding.com/products/nourish-bloom-organic-mushroom",
    "https://shop.bodybuilding.com/collections/greens-superfoods",
    "https://shop.bodybuilding.com/products/snap-supplements-olive-leaf-extract"
]






# Output CSV filename
filename = "product_details_with_flavours.csv"

# Check if the file already exists to determine if the header should be written
file_exists = os.path.isfile(filename)

# Open the CSV file in append mode
with open(filename, mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Write the header row only if the file does not exist
    if not file_exists:
        writer.writerow(["Product Title", "Product Price", "Product Description", "Directions", "Flavours"])

    # Loop through each URL
    for url in urls:
        # Send HTTP request to fetch the page
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # CSS Selectors for product details
        accordion_selector = "#Product--template--16779144069279__main > div.product__wrapper.product__wrapper--thumbnails > div > div > div > div > div > div.product__block.tabs-wrapper > collapsible-elements > div > details"
        flavour_selector = "#Product--template--16779144069279__main > div.product__wrapper.product__wrapper--thumbnails > div > div > div > div > div > div.product__block.product__block--lines.product__form__holder > div > div > div:nth-child(2) > fieldset > div > div > span > label"

        # Initialize variables to store product details
        product_title = "N/A"
        product_price = "N/A"
        product_description = "N/A"
        directions = "N/A"

        # Extract flavours from radio button labels
        flavours = [label.get_text(strip=True) for label in soup.select(flavour_selector)]

        # Extract product title and price
        product_title_selector = "#Product--template--16779144069279__main > div.product__wrapper.product__wrapper--thumbnails > div > div > div > div > div > div.product__block.product__head > div.product__title"
        product_price_selector = "#Product--template--16779144069279__main > div.product__wrapper.product__wrapper--thumbnails > div > div > div > div > div > div:nth-child(3) > div.price-flex > div:nth-child(1) > div > div.product__price"

        product_title = soup.select_one(product_title_selector).get_text(strip=True) if soup.select_one(product_title_selector) else "N/A"
        product_price = soup.select_one(product_price_selector).get_text(strip=True) if soup.select_one(product_price_selector) else "N/A"

        # Extract Product Description from the first accordion (it will always be in the first one)
        accordions = soup.select(accordion_selector)
        if accordions:
            product_description = accordions[0].select_one("div > div > div.accordion-content__inner > div:nth-child(1)").get_text(strip=True)

        # Check the second and third accordion for Directions
        directions_found = False
        for i, accordion in enumerate(accordions[1:3], 2):  # Check only the second and third accordion
            summary_text = accordion.select_one("summary").get_text(strip=True)
            
            if "Directions" in summary_text:  # If "Directions" is in the summary of the accordion
                directions = accordion.select_one("div > div > p > span").get_text(strip=True) if accordion.select_one("div > div > p > span") else "N/A"
                directions_found = True
                break  # Stop once we find the Directions section

        # If Directions were not found in the expected accordions, set as "N/A"
        if not directions_found:
            directions = "N/A"

        # Write the product details to the CSV file
        writer.writerow([product_title, product_price, product_description, directions, ", ".join(flavours)])

print(f"Data from all URLs has been appended to {filename}")
