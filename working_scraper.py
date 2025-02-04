import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to convert height from '6-2' format to inches
def convert_height(height_str):
    if height_str and '-' in height_str:
        feet, inches = height_str.split('-')
        return int(feet) * 12 + int(inches)
    return None

# Function to clean weight
def clean_weight(weight_str):
    if weight_str:
        weight_str = weight_str.replace("lb", "").replace("lbs", "").strip()
        try:
            return int(weight_str)
        except ValueError:
            return None
    return None

# Function to replace empty cells with 'None'
def replace_empty_cells_with_none(df):
    df = df.apply(lambda col: col.apply(lambda x: 'None' if x == '' or x is None else x))
    return df


# Function to scrape player stats from Baseball-Reference
def scrape_player_stats(player_url):
    url = f'https://www.baseball-reference.com{player_url}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract player details
    player_name = soup.find('h1').find('span').get_text(strip=True)
    pos_strong = soup.find('strong', string=lambda t: t and ("Position:" in t or "Positions:" in t))
    position = pos_strong.next_sibling.strip() if pos_strong and pos_strong.next_sibling else None
    
    bats_strong = soup.find('strong', string=lambda t: t and "Bats:" in t)
    batting = bats_strong.next_sibling.strip().split()[0] if bats_strong and bats_strong.next_sibling else None
    
    throws_strong = soup.find('strong', string=lambda t: t and "Throws:" in t)
    throwing = throws_strong.next_sibling.strip().split()[0] if throws_strong and throws_strong.next_sibling else None
    
    # Extract height and weight
    p_tags = soup.find_all('p')
    if len(p_tags) >= 3:
        spans = p_tags[2].find_all('span')
        height = spans[0].get_text(strip=True) if len(spans) > 0 else None
        weight = spans[1].get_text(strip=True) if len(spans) > 1 else None
    else:
        height, weight = None, None
    
    height = convert_height(height)
    weight = clean_weight(weight)
    
    # Find stats table
    table = soup.find('table', {'class': 'stats_table'})
    if not table:
        return pd.DataFrame()
    
    # Extract column headers
    headers = [th.get_text() for th in table.find_all('th')]
    try:
        awards_index = headers.index('Awards')
        headers = headers[:awards_index + 1]
    except ValueError:
        pass
    
    # Extract player stats
    rows = table.find_all('tr')
    stats = []
    for row in rows[1:]:
        columns = row.find_all('td')
        if columns:
            season = row.find('th').get_text()
            if 'Yrs' in season:
                break
            stats.append([season] + [col.get_text() for col in columns])
    
    for row in stats:
        if len(row) < len(headers):
            row.extend([None] * (len(headers) - len(row)))
    
    # Insert general info in first six columns
    full_headers = ['Name', 'Position', 'Bats', 'Throws', 'Height (inches)', 'Weight (lbs)'] + headers
    full_data = [[player_name, position, batting, throwing, height, weight] + row for row in stats]
    
    df = pd.DataFrame(full_data, columns=full_headers)
    
    # Replace empty cells with 'None'
    df = replace_empty_cells_with_none(df)
    
    return df

# Example player URL
player_url = '/players/k/kershcl01.shtml'
df = scrape_player_stats(player_url)
print(df)
df.to_csv('player_stats_with_full_info.csv', index=False)