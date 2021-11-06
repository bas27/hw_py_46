import requests

from pprint import pprint

with open('../secret/vk.txt', 'r') as file_object:
    token = file_object.read().strip()

URL = 'https://api.vk.com/method/'

def get_photo():

    params = {
        'owner_id': '65466460',
        'access_token': token,
        'v': '5.131',
        'album_id': 'profile',
        'photo_size': 'True',
        'extended': '1'
    }
    
    response = requests.get(URL + 'photos.get', params=params).json()['response']['items']
    # pprint(response)

    photo_dict = {}
    
    n = 0
    for i in response:
                        
        if i['likes']['count'] in photo_dict.keys():
            
            n += 1
            photo_dict[f"{i['likes']['count']}_{n}"] = [i['sizes'][-1]['url'], i['sizes'][-1]['type']]

        else:
            photo_dict[i['likes']['count']] = [i['sizes'][-1]['url'], i['sizes'][-1]['type']]
          

        # lst_dict.append(photo_dict)
     
      
    pprint(photo_dict)
    # pprint(lst_dict)
    return photo_dict

def ya_upload():
    

get_photo()