import requests

heroes = ['Hulk', 'Captain America', 'Thanos']

intel = 0

for hero in heroes:
    
    url = 'https://superheroapi.com/api/2619421814940190/search/' + hero
    results = requests.get(url).json()['results']
    
    for dict_hero in results:
        
        if dict_hero['name'] == hero:
            
            if int(dict_hero['powerstats']['intelligence']) > intel:
                
                name = dict_hero['name']
                intel = int(dict_hero['powerstats']['intelligence'])

print(f'Самым умным является {name} со значением интеллекта {intel}')