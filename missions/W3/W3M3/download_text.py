import requests
from bs4 import BeautifulSoup

# URL to fetch
url = 'https://www.gutenberg.org/cache/epub/74139/pg74139-images.html'

# Path to save the text file
save_path = 'mapreduce_example.txt'

# Fetch the URL content
response = requests.get(url)
response.raise_for_status()

# Parse the HTML content
soup = BeautifulSoup(response.content, 'html.parser')

# Extract text from the HTML
text = soup.get_text()

# Save the extracted text to a file
with open(save_path, 'w', encoding='utf-8') as file:
    file.write(text)

print(f'Text successfully saved to {save_path}')
