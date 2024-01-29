import csv
import logging
from typing import Dict, List
from cassiopeia import Champions
from cassiopeia import configuration

def get_api_key(filepath: str) -> str:
    '''Read API Key form a file.'''
    try:
        with open(filepath, 'r') as file:
            api_key=file.read().strip()
        return api_key
    except FileNotFoundError as e:
        logging.error(f'Error opening API keyfile {e}')
        return None

def configure_cassiopeia(api_key: str):
    '''Configure cassiopeia with the API key.'''
    configuration.settings.set_riot_api_key(api_key)

def get_champion_data(champions: Champions) -> (List[Dict], List[Dict]):
    '''Get data for all champions'''
    champion_core_data = []
    champion_stats = []

    for champion in champions:
        core_data = {
            'champion_id': champion.id,
            'name': champion.name,
            'title': champion.title,
            'difficulty': champion.info.difficulty,
        }
        champion_core_data.append(core_data)

        stats_data = {
            'champion_id': champion.id,
            'armor': champion.stats.armor,
            'armor_per_level': champion.stats.armor_per_level,
            'attack_damage': champion.stats.attack_damage,
            'attack_damage_per_level': champion.stats.attack_damage_per_level,
            'attack_range': champion.stats.attack_range,
            'attack_speed': champion.stats.attack_speed,
            'critical_strike_chance': champion.stats.critical_strike_chance,
            'critical_strike_chance_per_level': champion.stats.critical_strike_chance_per_level,
            'health': champion.stats.health,
            'health_per_level': champion.stats.health_per_level,
            'health_regen': champion.stats.health_regen,
            'health_regen_per_level': champion.stats.health_regen_per_level,
            'magic_resist': champion.stats.magic_resist,
            'magic_resist_per_level': champion.stats.magic_resist_per_level,
            'mana': champion.stats.mana,
            'mana_per_level': champion.stats.mana_per_level,
            'mana_regen': champion.stats.mana_regen,
            'mana_regen_per_level': champion.stats.mana_regen_per_level,
            'movespeed': champion.stats.movespeed,
            'percent_attack_speed_per_level': champion.stats.percent_attack_speed_per_level
        }
        champion_stats.append(stats_data)

    return champion_core_data, champion_stats

def write_to_csv(data: List[dict], fields: List[str], filename: str) -> None:
    '''Write data to CSV file'''
    try:
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        logging.error(f'Error writing to CSV file: {e}')

def main():
    logging.basicConfig(level=logging.INFO)

    api_key = get_api_key('api_key.txt')
    if not api_key:
        logging.error('No API key found. Exiting...')
        return

    configure_cassiopeia(api_key)

    champions = Champions(region='EUW')
    
    # Get champions data and write to CSV
    champion_core_data, champion_stats_data = get_champion_data(champions)
    
    if not champion_core_data:
        logging.error('No champion core data found. Exiting ...')
        return

    fields_core = list(champion_core_data[0].keys())
    write_to_csv(data=champion_core_data, fields=fields_core, filename='champion_core.csv')

    if not champion_stats_data:
        logging.error('No champion stats data found. Exiting...')
        return
    
    fields_stats = list(champion_stats_data[0].keys())
    write_to_csv(data=champion_stats_data, fields=fields_stats, filename='champion_stats.csv')


if __name__ == '__main__':
    main()