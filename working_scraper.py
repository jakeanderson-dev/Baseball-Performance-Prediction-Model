import sqlite3
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
    return df.map(lambda x: 'None' if x == '' or x is None else x)

# Function to insert player data into the database
def insert_player_data(player_info, stats, is_pitcher):
    conn = sqlite3.connect("baseball_stats.db")
    cursor = conn.cursor()

    # Insert player info or get existing player_id
    cursor.execute("SELECT id FROM players WHERE name = ?", (player_info['name'],))
    player = cursor.fetchone()

    if player:
        player_id = player[0]
    else:
        cursor.execute('''
            INSERT INTO players (name, position, bats, throws, height_inches, weight_lbs)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (player_info['name'], player_info['position'], player_info['bats'], player_info['throws'], 
              player_info['height_inches'], player_info['weight_lbs']))
        player_id = cursor.lastrowid

    # Insert stats based on player type
    for stat in stats:
        if is_pitcher and len(stat) == 36:
            cursor.execute('''
                INSERT INTO pitching_stats (
                    player_id, season, age, team, league, war, w, l, win_loss_pct, era, g, gs, gf, cg, sho, sv, ip, h, r, er, hr, bb, ibb, so, hbp, bk, wp, bf, era_plus, fip, whip, h9, hr9, bb9, so9, so_bb_ratio, awards
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (player_id, *stat))
        elif not is_pitcher and len(stat) == 33:
            cursor.execute('''
                INSERT INTO batting_stats (
                    player_id, season, age, team, league, war, g, pa, ab, r, h, doubles, triples, hr, rbi, sb, cs, bb, so, ba, obp, slg, ops, ops_plus, roba, rbat_plus, tb, gidp, hbp, sh, sf, ibb, position_played, awards
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (player_id, *stat))

    conn.commit()
    conn.close()

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
    height, weight = None, None
    spans = soup.find_all('span')
    for i in range(len(spans) - 1):
        if spans[i + 1].get_text(strip=True).endswith("lb"):
            height = spans[i].get_text(strip=True)
            weight = spans[i + 1].get_text(strip=True)
            break
    
    height = convert_height(height)
    weight = clean_weight(weight)

    # Prepare player info
    player_info = {
        'name': player_name,
        'position': position,
        'bats': batting,
        'throws': throwing,
        'height_inches': height,
        'weight_lbs': weight
    }

    # Find stats table
    table = soup.find('table', {'class': 'stats_table'})
    if not table:
        return

    # Extract stats headers and data
    headers = [th.get_text(strip=True) for th in table.find_all('th')]
    rows = table.find_all('tr')
    stats = []
    for row in rows[1:]:
        columns = row.find_all('td')
        if columns:
            season = row.find('th').get_text(strip=True)
            stat_row = [season] + [col.get_text(strip=True) for col in columns]

            # Skip rows containing 'Did not play'
            if any('did not play' in col.lower() for col in stat_row):
                continue

            stats.append(stat_row)

    # Replace empty cells with 'None'
    stats = [replace_empty_cells_with_none(pd.Series(stat)).tolist() for stat in stats]

    # Determine if player is a pitcher or batter based on stats headers
    is_pitcher = 'ERA' in headers

    # Insert data into the database
    insert_player_data(player_info, stats, is_pitcher)

# Example player URL (Mike Trout)
player_url = '/players/k/kershcl01.shtml'
scrape_player_stats(player_url)

print("Player data inserted successfully.")

