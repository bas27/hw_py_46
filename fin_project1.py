from os import path, write
import requests
import json

from pprint import pprint

TOKEN_VK = ''
class SocialNet:
    url_api_vk = 'https://api.vk.com/method/'
    url_api_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
    token_vk = TOKEN_VK

    def __init__(self, token_ya):
        self.token_ya = token_ya
        self.headers = {
            'Content-Type': 'application/json', 
            'Authorization': f'OAuth {self.token_ya}'
        }
        
    def get_photo(self, user_id):

        params = {
            'owner_id': user_id,
            'access_token': self.token_vk,
            'v': '5.131',
            'album_id': 'profile',
            'photo_size': 'True',
            'extended': '1'
        }
        
        response = requests.get(self.url_api_vk + 'photos.get', params=params).json()['response']['items']

        photo_dict = {}
        
        for i in response:
                            
            if i['likes']['count'] in photo_dict:

                photo_dict[f"{i['likes']['count']}_{i['date']}"] = [i['sizes'][-1]['url'], i['sizes'][-1]['type']]

            else:
                photo_dict[i['likes']['count']] = [i['sizes'][-1]['url'], i['sizes'][-1]['type']]

        return photo_dict

    def create_ya_dir(self, user_id):
        
        req = requests.put(self.url_api_ya, params={'path': f'photo_{user_id}'}, headers=self.headers)
        req.raise_for_status()
        if req.raise_for_status() == 201:
            print(f'Каталог "photo_{user_id}" создан')
            return f'photo_{user_id}'
        else:
            print(f'Проблемы при содании каталога, код ошибки - {req.raise_for_status()}')

    def ya_upload(self, user_id, n=5):
        '''Загрузка файлов на Ядиск
        n - количество фотографий
        '''
        
        count = 0
        
        for file_name, val in self.get_photo(user_id).items():

            count += 1
            params = {
                'path': f'/{self.create_ya_dir(user_id)}/{file_name}.jpg',
                'url': val[0],
                'overwrite': 'true'
                }
            if count <= n:

                r = requests.post(f'{self.url_api_ya}/upload/', headers=self.headers, params=params)
                r.raise_for_status()
                if r.status_code == 202:
                    print(f"Копирование выполнено - {file_name}.jpg")
                
                log_list = [{
                    "file_name": f'{file_name}.jpg',
                    "size": val[1]
                }]

                with open('backup_log.txt', 'a') as file:
                    json.dump(log_list, file)

ya_soc = SocialNet('')
ya_soc.ya_upload(552934290)
