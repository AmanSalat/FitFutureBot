import requests
from bs4 import BeautifulSoup

# Read URLs from a file
with open('exercise_urls.txt', 'r') as url_file:
    urls = [line.strip() for line in url_file if line.strip()]  # Read and clean URLs


# List of exercise URLs to scrape


# Open the file in append mode
with open('scraped_data.txt', 'a', encoding='utf-8') as file:
    for url in urls:
        # Fetch the HTML content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # 1. Scrape Exercise Name
        exercise_name = soup.select_one('h1.border-bottom a').text.strip() if soup.select_one('h1.border-bottom a') else "N/A"

        # 2. Scrape Exercise Categories and Names
        exercise_categories = []
        for category in soup.select('li[id^="exerciselefttext"] a'):
            category_name = category.text.strip()
            category_url = category['href']
            exercise_categories.append({"Category": category_name, "URL": category_url})

        # 3. Scrape Muscle Groups
        muscle_groups = []
        for group in soup.select('div[class="d-flex justify-content-start mt-2"] p'):
            muscle_groups.append(group.text.strip())

        # 4. Scrape Exercise Types (e.g., Beginner - Strength - Compound)
        exercise_types = []
        for etype in soup.select('h1.border-bottom div'):
            exercise_types.append(etype.text.strip())

        # 5. Scrape Equipment Details
        equipment = []
        for eq in soup.select('div[class="ml-1 mr-3"] p'):
            equipment.append(eq.text.strip())

        # 6. Scrape How-to Instructions
        how_to = []
        how_to_section = soup.select('h2 + p.p-2')
        if how_to_section:
            how_to_text = how_to_section[0].get_text(separator="\n").strip()
            how_to.append(how_to_text)

        # Write the scraped data for the current URL
        file.write(f"\nData for {url}:\n")
        file.write(f"Exercise Name: {exercise_name}\n")
        
        file.write("Exercise Categories and URLs:\n")
        for category in exercise_categories:
            file.write(f"{category['Category']}: {category['URL']}\n")
        
        file.write("\nMuscle Groups:\n")
        for group in muscle_groups:
            file.write(f"{group}\n")

        file.write("\nExercise Types:\n")
        for etype in exercise_types:
            file.write(f"{etype}\n")

        file.write("\nEquipment:\n")
        for eq in equipment:
            file.write(f"{eq}\n")

        file.write("\nHow-to Instructions:\n")
        for instruction in how_to:
            file.write(f"{instruction}\n")

print("Data appended to scraped_data.txt")
