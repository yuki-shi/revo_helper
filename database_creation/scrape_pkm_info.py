#!/usr/bin/python3

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from tqdm import tqdm

if __name__ == '__main__':
    # Read csv containing all Pokémon names and wiki URL
    df = pd.read_csv('pkm_list.csv')

    # Create an empty list for the aggregate results
    agg_pkm_list = []

    # For each URL
    for url in tqdm(df['wiki_url']):
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        pkm_dict = {}

        # Name
        pkm_dict['name'] = soup.find_all('h1')[0].text

        # Evolution info
        paragraphs = soup.find_all('p')
        for p in paragraphs:
            if re.findall(r'.*[Ee]volve[sd].*', p.text):
              pkm_dict['evolution_info'] = (p.text).strip()

        # Description
        description_table = soup.find_all('table', {'class': 'informational-box'})[0]
        inner_tbodies = description_table.find_all('tbody')

        # Type
        types = (inner_tbodies[0].find_all('p', string='Type(s)')[0].findNext()).find_all('a')

        for p_type in types:
            pkm_dict.setdefault('types', []).append(p_type.text)

        # Abilities
        abilities = ((inner_tbodies[0].find_all('p', string='Abilities')[0].findNext('tr'))).find_all('td')

        for ability in abilities:
            pkm_dict[ability.find_all('b')[0].text] = ability.find_all('a')[0].text

        # Base stats
        base_stats = ((inner_tbodies[0].find_all('span', string='Base stats')[0].findNext('tr'))).find_all('td')
        for stat in base_stats:
            pkm_dict[re.findall(r'.*(?=\n[0-9]+)', stat.text)[0]] = re.findall(r'[0-9]+', stat.text)[0]

        # Catch rate
        pkm_dict['catch_rate'] = re.findall(r'(?<=\().*%(?=\))', (inner_tbodies[0].find_all('span', string='Catch rate')[0].findNext('p')).text)[0]

        # Rarity
        pkm_dict['rarity'] = (inner_tbodies[0].find_all('span', string='Rarity Tier')[0].findNext('p').text).strip()

        # Obtainability info
        # Get table of contents div
        toc = soup.find_all('div', id='toc')[0]

        # Get all items from table of content
        indices = toc.find_all('li')[0]
        obt_methods = []
        for anchor in indices.find_all('a'):
            obt_methods.append(anchor.text)

        # Get only h3 headings
        obt_methods = [re.findall(r'(?<=^[0-9]\.[0-9] ).*', x) for x in obt_methods]

        # Remove empty entries
        obt_methods = [x for x in obt_methods if x != []]

        # Flatten
        obt_methods = [item for sublist in obt_methods for item in sublist]

        # Remove discontinued methods
        obt_methods = [x for x in obt_methods if x != 'Discontinued methods']

        pkm_dict['obtainability'] = obt_methods

        agg_pkm_list.append(pkm_dict)

    df = pd.DataFrame(agg_pkm_list)
    df.to_csv('pkm_info.csv', index=False)
