from os import name
from pprint import pprint
from tqdm import tqdm
import requests
import json
import hashlib

class VK:
    url_api_vk = 'https://api.vk.com/method/'
 
    def __init__(self, token, album='profile'):
        '''
        wall — фотографии со стены;
        profile — фотографии профиля;
        //saved — сохраненные фотографии. Возвращается только с ключом доступа пользователя. -пока под вопросом
        '''

        self.album = album
        self.token = token
    
    def get_photo(self, user_id, n):

        params = {
            'owner_id': user_id,
            'access_token': self.token,
            'v': '5.131',
            'album_id': self.album,
            'photo_size': 'True',
            'extended': '1'
        }

        response = requests.get(
            self.url_api_vk + 'photos.get', params=params).json()['response']['items']

        photo_dict = {}
        count = 0

        for i in response:

            count += 1
            if count <= n:
                if i['likes']['count'] in photo_dict:

                    photo_dict[f"{i['likes']['count']}_{i['date']}"] = [
                        i['sizes'][-1]['url'], i['sizes'][-1]['type']]

                else:
                    photo_dict[i['likes']['count']] = [
                        i['sizes'][-1]['url'], i['sizes'][-1]['type']]
            else:
                break

        return photo_dict

class OK:
    URL = 'https://api.ok.ru/fb.do'
        
    def __init__(self, token, session_secret_key, application_key):
        self.token = token
        self.session_secret_key = session_secret_key
        self.application_key = application_key
        self.params = {
            'application_key': self.application_key,
            'access_token': self.token,
            'format': 'json',
            }
        self.sig_tmp = f"application_key={self.params['application_key']}format={self.params['format']}{self.session_secret_key}"

    def get_hash(self, str_for_hash):
        hash_object = hashlib.md5(str_for_hash.encode())
        return hash_object.hexdigest()
    
    def get_photo(self, user_id, albums=None):
        '''
        albums - список идентификаторов альбомов 
        '''
        self.albums = albums
        self.user_id = user_id
        
        custom_params = {
        'fid': self.user_id,
        'method': 'photos.getPhotos'
        }

        
        if self.albums:
            all_photos = []
            for albums_id in self.albums:

                str_sig = f"aid={albums_id}detectTotalCount=truefid={custom_params['fid']}method={custom_params['method']}{self.sig_tmp}"
                
                params = {
                    'sig': self.get_hash(str_sig),
                    'detectTotalCount': 'true',
                    'aid': albums_id
                }

                response = requests.get(self.URL, params={**self.params, **custom_params, **params}).json()

                if response['hasMore'] == 'true':
                    str_sig = f"{self.sig_tmp}aid={albums_id}fid={custom_params['fid']}method={custom_params['method']}count={response['totalCount']}"

                    params = {
                    'sig': self.get_hash(str_sig),
                    'count': response['totalCount'],
                    'aid': albums_id
                    }
                    response = requests.get(self.URL, params={**self.params, **custom_params, **params}).json()['photos']

                    all_photos.append(response) 
                    n = len(all_photos)
                elif response['hasMore'] == 'false':
                    all_photos.append(response['photos'])
                    n = len(all_photos)
        else:
            str_sig = f"{self.sig_tmp}detectTotalCount=truefid={custom_params['fid']}method={custom_params['method']}"
                
            params = {
                'sig': self.get_hash(str_sig),
            }

            all_photos = requests.get(self.URL, params={**self.params, **custom_params, **params}).json()['photos']

        photo_dict = {}
        count_name = 0
        count_n = 0

        for i in all_photos:
            
            count_n += 1
            if count_n <= n:
                if i['mark_count'] in photo_dict:
                    count_name += 1
                    photo_dict[f"{i['mark_count']}_{count_name}"] = [i['pic640x480'],'pic640x480']
                else:
                    photo_dict[i['mark_count']] = [i['pic640x480'],'pic640x480']
            else:
                break
        pprint(photo_dict)

    def getAlbums(self):
        pass
class YaDisk:
    url_api_ya = 'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token, dir):

        self.token = token
        self.headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        self.name_dir = f'photo_{dir}'

    def create_ya_dir(self):

        req = requests.put(self.url_api_ya, params={
                           'path': self.name_dir}, headers=self.headers)

        if req.status_code == 409:
            print(
                f'Каталог {self.name_dir} существует, файлы будут добавлены в него')
        elif req.status_code == 201:
            print(f'Каталог {self.name_dir} создан')
        else:
            print(
                f'Проблемы при создании каталога, код ошибки - {req.status_code}')

    def ya_upload(self, dict_photo):

        log_list = []

        with tqdm(total=len(dict_photo), ascii=True, desc="Copy photo") as pbar:
            for file_name, val in dict_photo.items():

                params = {
                    'path': f'/{self.name_dir}/{file_name}.jpg',
                    'url': val[0],
                    'overwrite': 'true'
                }

                requests.post(f'{self.url_api_ya}/upload/',
                              headers=self.headers, params=params)

                pbar.update()
                tmp_dict = {
                    "file_name": f'{file_name}.jpg',
                    "size": val[1]
                }

                log_list.append(tmp_dict)

        with open('backup_log.json', 'w') as file:
            json.dump(log_list, file)


if __name__ == '__main__':
    choise_net = input('Выберите социальную сеть: 1. ВК, 2. ОК: ')
    access_token = input('Введите access_token: ')
    if choise_net == '2':
        session_sec_key = input('Введите Session_secret_key: ')
        app_key = input('Введите Публичный ключ приложения: ')
    ya_token = input('Введите токен яндекс диска: ')
    user_id = int(input('Введите id пользователя: '))
    
    OK(access_token, session_sec_key, app_key).get_photo(user_id, [864781883252])
    # choise_number = input(
    #     'Изменить количество сохраняемых фотографий (по-умолчанию 5), Y/N (default-N, press Enter): ')
    # if choise_number.lower() == 'y':
    #     num_photos = int(input('Укажите количество сохраняемых фотографий: '))
    # else:
    #     num_photos = 5
    
    # YaDisk(ya_token, user_id).create_ya_dir()
    
    # if choise_net == '1':
    #     upload_photo = VK(access_token).get_photo(user_id, num_photos)
    # elif choise_net == '2':
    #     upload_photo = OK(access_token, session_sec_key, app_key).get_photo(user_id, num_photos)
    
    # YaDisk(ya_token, user_id).ya_upload(upload_photo)
