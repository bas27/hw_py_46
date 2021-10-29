import requests

heroes = ['Hulk', 'Captain America', 'Thanos']

# class Intelligense:
        
def id_hero(list_hero):
    
    dict_heroes_id = {}
    
    for hero in heroes:
        
        url = 'https://superheroapi.com/api/2619421814940190/search/' + hero
        # print(url)
        r = requests.get(url).json()
        id_h = r['results'][0]['id']
        dict_heroes_id[hero] = id_h
    
    # return dict_heroes_id
    dict_heroes_intel = {}
    
    for name, id in dict_heroes_id.items():
        
        url = 'https://superheroapi.com/api/2619421814940190/' + id + '/powerstats'
        r = requests.get(url).json()
        dict_heroes_intel[name] = int(r['intelligence'])

    
    very_intel = max(dict_heroes_intel, key=dict_heroes_intel.get)
    print(f'Самый умный герой {very_intel}')

id_hero(heroes)

    # def intelligens (dict_heroes_id):
