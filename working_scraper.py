import requests
from bs4 import BeautifulSoup
import pandas as pd
import sqlite3

# Function to scrape player stats from Baseball-Reference
def scrape_player_stats(player_url):
    url = f'https://www.baseball-reference.com{player_url}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find the stats table (this is a common structure in Baseball-Reference pages)
    table = soup.find('table', {'class': 'stats_table'})

    # Extract column headers
    headers = [th.get_text() for th in table.find_all('th')]

    # Remove columns after 'Awards' (extra columns with years as headers)
    try:
        awards_index = headers.index('Awards')  # Find index of 'Awards' column
        headers = headers[:awards_index + 1]  # Keep columns only up to 'Awards'
    except ValueError:
        pass  # If 'Awards' column doesn't exist, keep the full headers

    # Extract player stats
    rows = table.find_all('tr')
    stats = []

    for row in rows[1:]:  # Skip the header row
        columns = row.find_all('td')
        
        if columns:
            # Add the "Season" to the start of each row by using the first column
            season = row.find('th').get_text()  # Get the season from the <th> cell (first column)
            
            # Check for "Yrs" in the row; if found, stop adding rows
            if 'Yrs' in season:
                break  # Stop processing rows once the "Yrs" row is reached
            
            stats.append([season] + [col.get_text() for col in columns])

    # Debugging: Print header and row lengths
    print("Headers:", headers)
    for idx, row in enumerate(stats[:5]):  # Print first 5 rows to inspect
        print(f"Row {idx}: {len(row)} columns")

    # Ensure rows have the same number of columns as headers
    for row in stats:
        if len(row) < len(headers):  # If there are fewer columns, pad with None
            row.extend([None] * (len(headers) - len(row)))

    # Create the DataFrame after ensuring rows match header length
    df = pd.DataFrame(stats, columns=headers)

    return df

# Example player URL for Mike Trout (adjust this URL to scrape different players)
player_url = '/players/t/troutmi01.shtml'
df = scrape_player_stats(player_url)

# Display the DataFrame
print(df)

# Save the DataFrame as a CSV file
df.to_csv('player_stats.csv', index=False)