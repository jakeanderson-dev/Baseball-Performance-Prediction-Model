import requests
from bs4 import BeautifulSoup
import pandas as pd

# Function to scrape player stats from Baseball-Reference
def scrape_player_stats(player_url):
    url = f'https://www.baseball-reference.com{player_url}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the player's name from the <h1> tag and its <span> inside
    player_name_tag = soup.find('h1').find('span')
    player_name = player_name_tag.get_text(strip=True) if player_name_tag else None

    # Extract the player's position(s)
    pos_strong = soup.find('strong', string=lambda t: t and ("Position:" in t or "Positions:" in t))
    position = pos_strong.next_sibling.strip() if pos_strong and pos_strong.next_sibling else None

    # Extract the player's batting orientation
    bats_strong = soup.find('strong', string=lambda t: t and "Bats:" in t)
    batting = bats_strong.next_sibling.strip().split()[0] if bats_strong and bats_strong.next_sibling else None

    # Extract the player's throwing orientation
    throws_strong = soup.find('strong', string=lambda t: t and "Throws:" in t)
    throwing = throws_strong.next_sibling.strip().split()[0] if throws_strong and throws_strong.next_sibling else None

    # Extract the player's height and weight from the 3rd <p> tag
    p_tags = soup.find_all('p')
    height, weight = None, None

    if len(p_tags) >= 3:
        spans = p_tags[2].find_all('span')
        if len(spans) >= 2:
            height = spans[0].get_text(strip=True)
            weight = spans[1].get_text(strip=True)

    # Find the stats table
    table = soup.find('table', {'class': 'stats_table'})

    if not table:
        return pd.DataFrame()  # Return empty DataFrame if no stats table is found

    # Extract column headers
    headers = [th.get_text() for th in table.find_all('th')]

    # Remove columns after 'Awards' (extra columns with years as headers)
    try:
        awards_index = headers.index('Awards')
        headers = headers[:awards_index + 1]
    except ValueError:
        pass

    # Extract player stats
    rows = table.find_all('tr')
    stats = []
    for row in rows[1:]:  # Skip the header row
        columns = row.find_all('td')
        if columns:
            # Get the "Season" from the <th> cell (first column)
            season = row.find('th').get_text()
            if 'Yrs' in season:
                break
            stats.append([season] + [col.get_text() for col in columns])

    # Ensure rows have the same number of columns as headers
    for row in stats:
        if len(row) < len(headers):
            row.extend([None] * (len(headers) - len(row)))

    # Create the DataFrame after ensuring rows match header length
    df = pd.DataFrame(stats, columns=headers)

    # Create new rows for player's basic info
    new_row_name = ["Name: " + str(player_name)] + [None] * (len(headers) - 1)
    new_row_position = ["Position(s): " + str(position)] + [None] * (len(headers) - 1)
    new_row_batting = ["Bats: " + str(batting)] + [None] * (len(headers) - 1)
    new_row_throwing = ["Throws: " + str(throwing)] + [None] * (len(headers) - 1)
    new_row_height = ["Height: " + str(height)] + [None] * (len(headers) - 1)
    new_row_weight = ["Weight: " + str(weight)] + [None] * (len(headers) - 1)

    # Append the new rows at the top of the DataFrame
    df.loc[-1] = new_row_weight
    df.loc[-2] = new_row_height
    df.loc[-3] = new_row_throwing
    df.loc[-4] = new_row_batting
    df.loc[-5] = new_row_position
    df.loc[-6] = new_row_name
    df.index = df.index + 6  # Shift index to keep order
    df = df.sort_index()

    return df

# Example player URL for testing
player_url = '/players/t/troutmi01.shtml'
df = scrape_player_stats(player_url)

# Display the DataFrame
print(df)

# Save the DataFrame as a CSV file
df.to_csv('player_stats_with_full_info.csv', index=False)

