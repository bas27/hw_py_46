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
    token = ''
    session_secret_key = ''
        
    def __init__(self):

        self.params = {
            'application_key': '',
            'access_token': self.token,
            'format': 'json',
            }

    def get_photo(self, user_id, n=5):
        
        self.user_id = user_id
        custom_params = {
        'fid': self.user_id,
        'method': 'photos.getPhotos'
        }

        str_sig = f"application_key={self.params['application_key']}fid={custom_params['fid']}format={self.params['format']}method={custom_params['method']}{self.session_secret_key}"

        hash_object = hashlib.md5(str_sig.encode())

        signature = hash_object.hexdigest()

        params_sig = {
            'sig': signature
        }

        response = requests.get(self.URL, params={**self.params, **custom_params, **params_sig}).json()['photos']

        photo_dict = {}
        count_name = 0
        count_n = 0

        for i in response:
            
            count_n += 1
            if count_n <= n:
                if i['mark_count'] in photo_dict:
                    count_name += 1
                    photo_dict[f"{i['mark_count']}_{count_name}"] = [i['pic640x480'],'pic640x480']
                else:
                    photo_dict[i['mark_count']] = [i['pic640x480'],'pic640x480']
            else:
                break
        return photo_dict


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
    token_vk = input('Введите токен VK: ')
    token = input('Введите токен яндекс диска: ')
    user_id = int(input('Введите id пользователя: '))
    
    choise_number = input(
        'Изменить количество сохраняемых фотографий (по-умолчанию 5), Y/N (default-N, press Enter): ')
    if choise_number.lower() == 'y':
        num_photos = int(input('Укажите количество сохраняемых фотографий: '))
    else:
        num_photos = 5
    
    YaDisk(token, user_id).create_ya_dir()
    
    if choise_net == '1':
        upload_photo = VK(token_vk).get_photo(user_id, num_photos)
    elif choise_net == '2':
        upload_photo = OK().get_photo(user_id, num_photos)
    
    YaDisk(token, user_id).ya_upload(upload_photo)