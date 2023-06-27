from bs4 import BeautifulSoup
import requests
import re
import pandas as pd

BASE_URL = 'https://wiki.pokemonrevolution.net'
# There are all gens on PRO up to VII
GENS = ['I',
        'II',
        'III',
        'IV',
        'V',
        'VI',
        'VII']

if __name__ == '__main__':
    full_pkm_list = []

    for index, gen in enumerate(GENS):
        # Iterate over every gen pokemon index and get their specific page URL 
        url = f'{BASE_URL}/index.php?title=Category:Generation_{gen}_Pok%C3%A9mon'

        response = requests.get(url, 'html.parser')
        soup = BeautifulSoup(response.text)

        pokemon_list = []

        # Find every anchor tag
        urls = soup.find_all('a', href=True)
        for url in urls:
          # If the inner text of the tag is a url, the pokemon list is over
          if re.match(r'^https.*', url.text):
            break
          pokemon_list.append([url.text, f"{BASE_URL}{url['href']}"])

        # Clean entries that aren't pokemon names 
        if index <= 4:
          pokemon_list = pokemon_list[6:]
        else:
          pokemon_list = pokemon_list[5:]

        # Add a "generation" attribute at the end of each list
        append_gen = [x.append(gen) for x in pokemon_list]
        full_pkm_list.extend(pokemon_list)

    # Create a dataframe with the list of lists
    df = pd.DataFrame(full_pkm_list, columns=['name', 'wiki_url', 'gen'])

    # Export to .csv
    df.to_csv('pkm_list.csv', index=False)
