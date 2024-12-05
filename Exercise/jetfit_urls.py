import requests
from bs4 import BeautifulSoup

# Base URL for the exercise pages
base_url = 'https://www.jefit.com/exercises?page='

# List to store all exercise URLs
urls = []

# Loop through pages 1 to 73
for page_num in range(1, 74):
    # Construct the URL for each page
    url = f"{base_url}{page_num}"
    
    # Send a GET request to the webpage
    response = requests.get(url)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all <a> tags and extract the exercise URLs
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            if href.startswith('/exercises/'):  # Filtering URLs related to exercises
                full_url = f"https://www.jefit.com{href}"  # Completing relative URL
                urls.append(full_url)
    else:
        print(f"Failed to retrieve page {page_num}")

# Save the URLs to a text file
with open('exercise_urls.txt', 'w') as file:
    for url in urls:
        file.write(f"{url}\n")

print(f"Extracted {len(urls)} URLs and saved them to exercise_urls.txt")


