import requests
from bs4 import BeautifulSoup
import pandas as pd


base_url = "http://books.toscrape.com/"
url = base_url


all_books = []

while url:
    print(f"\nScraping: {url}")
    
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    
    
    books = soup.find_all('article', class_='product_pod')
    
    for book in books:
        
        title = book.h3.a['title']
        # Extract price
        price = book.find('p', class_='price_color').text
        # Extract availability
        availability = book.find('p', class_='instock availability').text.strip()
        
        
        all_books.append({
            'Title': title,
            'Price': price,
            'Availability': availability
        })
    
    
    next_button = soup.find('li', class_='next')
    if next_button:
        next_page_url = next_button.find('a')['href']
        if 'catalogue/' not in url and 'catalogue/' in next_page_url:
            url = base_url + next_page_url
        else:
            url = base_url + "catalogue/" + next_page_url
    else:
        url = None


df = pd.DataFrame(all_books)
df.to_csv('books.csv', index=False)

