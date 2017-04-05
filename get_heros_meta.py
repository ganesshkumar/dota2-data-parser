import requests, json
from bs4 import BeautifulSoup

hero_class_map = {}

r = requests.get('http://www.dota2.com/heroes/')
html_resource =  r.content

soup = BeautifulSoup(html_resource, 'html.parser')
#print(soup.prettify().encode('utf-8'))

def get_hero_meta(soup_hero):
    return {
        'id': soup_hero.attrs['href'].split('/')[-2].lower(),
        'name': soup_hero.attrs['href'].split('/')[-2].replace('_', ' '),
        'url': soup_hero.attrs['href'],
        'icon_medium': soup_hero.select('img.heroHoverLarge')[0].attrs['src'],
        'icon_small': soup_hero.select('img.heroHoverSmall')[0].attrs['src']
    }

def get_heros(soup_page, css_class_selector):
    heros = []
    for list in soup_page.select('div.{}'.format(css_class_selector)):
        for soup_hero in list.select('a.heroPickerIconLink'):
            heros.append(get_hero_meta(soup_hero))
    return heros

def export_heros_meta(hero_class_map):
    obj = {}
    for hero_class in  hero_class_map.keys():
        heros = hero_class_map[hero_class]
        for hero in heros:
            hero['class'] = hero_class
            obj[hero['id']] = hero

    print len(obj.keys())
    with open('heros_meta.json', 'w') as outfile:
        json.dump(obj, outfile)

# Strength Heros => heroColLeft
hero_class_map['strength'] = get_heros(soup, 'heroColLeft')
hero_class_map['agility'] = get_heros(soup, 'heroColMiddle')
hero_class_map['intelligence'] = get_heros(soup, 'heroColRight')

export_heros_meta(hero_class_map)
