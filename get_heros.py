import requests, json
from bs4 import BeautifulSoup
import time

def get_hero_info(hero_meta, incomplete_heros):
    print 'Obtaining information for {}'.format(hero_meta['name'])
    r = requests.get(hero_meta['url'], timeout=None)
    html_resource =  r.content
    soup = BeautifulSoup(html_resource, 'html.parser')

    try:
        hero_bio_roles = soup.select('p#heroBioRoles')[0]
        hero_meta['icon_large'] = soup.select('img#heroTopPortraitIMG')[0].attrs['src']
        hero_meta['attack_type'] = hero_bio_roles.contents[0].contents
        hero_meta['roles'] = filter(None, [attr.strip().lower() for attr in hero_bio_roles.contents[1].split('-')])
        incomplete_heros.remove(hero_meta['id'])
    except IndexError:
        print 'Failed to fetch information for {}'.format(hero_meta['name'])

    return hero_meta

def get_heros_info(heros_meta, incomplete_heros, heros):
    for hero_id in incomplete_heros:
        hero_meta = heros_meta[hero_id]
        hero_info = get_hero_info(hero_meta, incomplete_heros)
        heros[hero_id] = hero_info
        # Let's respect rate limit and wait for a while
        time.sleep(2)
        print '{} to fetch '.format(len(incomplete_heros))
    return heros

with open('heros_meta.json') as data_file:
    heros_meta = json.load(data_file)

incomplete_heros = heros_meta.keys()
heros = get_heros_info(heros_meta, incomplete_heros, {})

while len(incomplete_heros) > 0:
    heros = get_heros_info(heros_meta, incomplete_heros, heros)

with open('heros_info.json', 'w') as outfile:
    json.dump(heros, outfile)
