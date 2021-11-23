from tqdm import tqdm
import requests
import json
'''
pip install progress
'''

class SocialNet:
    url_api_vk = 'https://api.vk.com/method/'
    url_api_ya = 'https://cloud-api.yandex.net/v1/disk/resources'
    token_vk = 'dd00edfda7de89db298e70a3ca353a1e7135aa4c5df2d54eaf78aee68f5d2e03a565c04524fd3535eba33'

    def __init__(self, token_ya, album='profile'):
        '''
        wall — фотографии со стены;
        profile — фотографии профиля;
        //saved — сохраненные фотографии. Возвращается только с ключом доступа пользователя. -пока под вопросом
        '''
        self.token_ya = token_ya
        self.headers = {
            'Content-Type': 'application/json', 
            'Authorization': f'OAuth {self.token_ya}'
        }
        self.album = album
    
    def get_photo(self, user_id, n):

        params = {
            'owner_id': user_id,
            'access_token': self.token_vk,
            'v': '5.131',
            'album_id': self.album,
            'photo_size': 'True',
            'extended': '1'
        }
        
        response = requests.get(self.url_api_vk + 'photos.get', params=params).json()['response']['items']

        photo_dict = {}
        count = 0

        for i in response:

            count += 1
            if count <= n:
                if i['likes']['count'] in photo_dict:

                    photo_dict[f"{i['likes']['count']}_{i['date']}"] = [i['sizes'][-1]['url'], i['sizes'][-1]['type']]

                else:
                    photo_dict[i['likes']['count']] = [i['sizes'][-1]['url'], i['sizes'][-1]['type']]
            else:
                break

        return photo_dict

    def create_ya_dir(self, user_id):
        
        req = requests.put(self.url_api_ya, params={'path': f'photo_{user_id}_{self.album}'}, headers=self.headers)
        
        if req.status_code == 409:
            print(f'Каталог "photo_{user_id}_{self.album}" существует, файлы будут добавлены в него')
        elif req.status_code == 201:
            print(f'Каталог "photo_{user_id}_{self.album}" создан')
        else:
            print(f'Проблемы при создании каталога, код ошибки - {req.status_code}')
        
    def ya_upload(self, user_id, n=5):
        '''Загрузка файлов на Ядиск
        n - количество фотографий
        '''
        upload_photo = self.get_photo(user_id, n)
        self.create_ya_dir(user_id)
        ya_dir = f'photo_{user_id}_{self.album}'
        log_list = []

        with tqdm(total=len(upload_photo), ascii=True, desc="Copy photo") as pbar: 
            for file_name, val in upload_photo.items():

                    params = {
                        'path': f'/{ya_dir}/{file_name}.jpg',
                        'url': val[0],
                        'overwrite': 'true'
                        }
                    
                    requests.post(f'{self.url_api_ya}/upload/', headers=self.headers, params=params)

                    pbar.update()
                    tmp_dict = {
                        "file_name": f'{file_name}.jpg', 
                        "size": val[1]
                    }
                    
                    log_list.append(tmp_dict)
        
        with open('backup_log.json', 'w') as file:
            json.dump(log_list, file)


if __name__ == '__main__': 
    token = input('Введите токен яндекс диска: ')
    vk_user_id = int(input('Введите id пользователя VK: '))
    choise_number = input('Изменить количество сохраняемых фотографий (по-умолчанию 5), Y/N: ')
    my_var = SocialNet(token)
    
    if choise_number.lower() == 'y':
        num_photos = int(input('Укажите количество сохраняемых фотографий: '))
        my_var.ya_upload(vk_user_id, num_photos)
    else:
        my_var.ya_upload(vk_user_id)