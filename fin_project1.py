from os import path, write
import requests

from pprint import pprint

with open('../secret/vk.txt', 'r') as secret_file_object, open('../secret/yandex_disk.txt', 'r') as secret_file_ya:
    token_vk = secret_file_object.read().strip()
    token_ya = secret_file_ya.read().strip()

URL = 'https://api.vk.com/method/'
URL_YA = 'https://cloud-api.yandex.net/v1/disk/resources'
# = 65466460
def get_photo(user_id):

    params = {
        'owner_id': user_id,
        'access_token': token_vk,
        'v': '5.131',
        'album_id': 'profile',
        'photo_size': 'True',
        'extended': '1'
    }
    
    response = requests.get(URL + 'photos.get', params=params).json()['response']['items']

    photo_dict = {}
    
    n = 0
    for i in response:
                        
        if i['likes']['count'] in photo_dict.keys():
            
            n += 1
            photo_dict[f"{i['likes']['count']}_{n}"] = [i['sizes'][-1]['url'], i['sizes'][-1]['type']]

        else:
            photo_dict[i['likes']['count']] = [i['sizes'][-1]['url'], i['sizes'][-1]['type']]

    return photo_dict

def get_headers():
    return {
        'Content-Type': 'application/json', 
        'Authorization': f'OAuth {token_ya}'
        }

def create_ya_dir(user_id):
    
    requests.put(URL_YA, params={'path': f'photo_{user_id}'}, headers=get_headers())
    return f'photo_{user_id}'

def ya_upload(user_id, n=5):
    '''Загрузка файлов на Ядиск
    n - количество фотографий
    '''
    headers = get_headers()
    
    count = 0
    
    for file_name, val in get_photo(user_id).items():
        log_list = []
        count += 1
        params = {
            'path': f'/{create_ya_dir(user_id)}/{file_name}.jpg',
            'url': val[0],
            'overwrite': 'true'
            }
        if count <= n:

            r = requests.post(f'{URL_YA}/upload/', headers=headers, params=params)
            r.raise_for_status()
            if r.status_code == 202:
                print(f"Копирование выполнено - {file_name}.jpg")
            
            log_list = [{
                "file_name": f'{file_name}.jpg',
                "size": val[1]
            }]

            with open('backup_log.txt', 'a') as file:
                file.writelines(str(log_list))

            # /for i in range(100):
        # time.sleep(1)
        # sys.stdout.write("\r%d%%" % n)
        # sys.stdout.flush()

ya_upload(552934290, 20)
# get_photo()