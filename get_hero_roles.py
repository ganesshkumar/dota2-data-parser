import json

with open('heros_info.json') as data_file:
    heros = json.load(data_file)

with open('hero_roles.json', 'w') as outfile:
    hero_roles = []
    for hero_id in heros.keys():
        roles = heros[hero_id]['roles']
        for role in roles:
            if role not in hero_roles:
                hero_roles.append(role)
    json.dump(hero_roles, outfile)
