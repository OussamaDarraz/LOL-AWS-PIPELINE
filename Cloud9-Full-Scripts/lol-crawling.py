import csv
import os
import requests
import time
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO)


def get_names_from_csv(file_path):
    '''Get the list of champion names from the existing CSV file. If the file doesn't exist, return an empty list.'''
    if os.path.exists(file_path):
        names = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            next(reader, None)  # skip the headers
            for row in reader:
                names.append(row[0])
        return names
    else:
        return []


def fetch_and_parse_page(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    return soup


def fetch_champion_data(champion, base_url):
    # Visit the champion's individual page
    champion_url = base_url + champion.lower() + "/" + "build"
    champion_soup = fetch_and_parse_page(champion_url)

    try:
        role_value = champion_soup.find('span', class_='champion-title').text.strip().split('Build for ')[1].split(', ')[0]
        matches_value = champion_soup.find('div', class_='matches').find('div', class_='value').text.strip()
        win_rate_value = champion_soup.find('div', class_='win-rate').find('div', class_='value').text.strip()
        pick_rate_value = champion_soup.find('div', class_='pick-rate').find('div', class_='value').text.strip()
        ban_rate_value = champion_soup.find('div', class_='ban-rate').find('div', class_='value').text.strip()
    except Exception as e:
        logging.error(f'Error fetching data for {champion}: {str(e)}')
        return None

    logging.info(f'{champion} done.')
    time.sleep(2)  # Consider making this configurable
    return [champion, role_value, matches_value, win_rate_value, pick_rate_value, ban_rate_value]


def main():
    names = get_names_from_csv('champion_core.csv')
    base_url = "https://u.gg/lol/champions/"
    soup = fetch_and_parse_page(base_url)

    # Assuming that the champions are in a list
    champions_list = soup.find_all('div', class_='champion-name')

    # Write to CSV
    write_header = not os.path.exists('champions_crawl_stats.csv')
    with open('champions_stats.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow(["Name", "Role", "Matches", "Win Rate", "Pick Rate", "Ban Rate"])  # Header

        for champion in champions_list:
            champion_name = champion.text.strip()
            if champion_name not in names:
                champion_data = fetch_champion_data(champion_name, base_url)
                if champion_data:
                    writer.writerow(champion_data)


if __name__ == '__main__':
    main()