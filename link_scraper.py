import requests
from bs4 import BeautifulSoup
import re
import sqlite3

def save_urls_to_db(urls, db_path="baseball_stats.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS player_urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE
        )
    """)
    
    for url in urls:
        cursor.execute("INSERT OR IGNORE INTO player_urls (url) VALUES (?)", (url,))
    
    conn.commit()
    conn.close()

def get_player_urls(base_url, letter, min_year=2004):
    player_urls = []
    
    url = f"{base_url}{letter}/"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Failed to fetch {url}")
        return player_urls
    
    soup = BeautifulSoup(response.text, 'html.parser')
    player_entries = soup.find_all('p')  # Players are listed in <p> tags
    
    for entry in player_entries:
        link = entry.find('a')
        if not link:
            continue
        
        player_url = link.get('href')
        years_active_text = entry.get_text()
        
        # Extract years from the text using regex
        years_match = re.search(r'\((\d{4})-(\d{4})\)', years_active_text)
        if years_match:
            first_year = int(years_match.group(1))
            
            if first_year >= min_year:
                player_urls.append(player_url)
                print(player_url)  # Print to terminal
    
    save_urls_to_db(player_urls)
    return player_urls

if __name__ == "__main__":
    base_index_url = "https://www.baseball-reference.com/players/"
    letter = "a"  # Set to 'a' to check only 'A' players
    get_player_urls(base_index_url, letter)









