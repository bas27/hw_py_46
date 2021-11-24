from tqdm import tqdm
import requests
import json

class VK:
    url_api_vk = 'https://api.vk.com/method/'
    token_vk = ''

    def __init__(self, album='profile'):
        '''
        wall — фотографии со стены;
        profile — фотографии профиля;
        //saved — сохраненные фотографии. Возвращается только с ключом доступа пользователя. -пока под вопросом
        '''

        self.album = album

    def get_photo(self, user_id, n=5):

        params = {
            'owner_id': user_id,
            'access_token': self.token_vk,
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
    token = input('Введите токен яндекс диска: ')
    vk_user_id = int(input('Введите id пользователя VK: '))
    YaDisk(token, vk_user_id).create_ya_dir()
    choise_number = input(
        'Изменить количество сохраняемых фотографий (по-умолчанию 5), Y/N (default-N, press Enter): ')

    if choise_number.lower() == 'y':
        num_photos = int(input('Укажите количество сохраняемых фотографий: '))
        upload_photo = VK().get_photo(vk_user_id, num_photos)
        YaDisk(token, vk_user_id).ya_upload(upload_photo)

    else:
        upload_photo = VK().get_photo(vk_user_id)
        YaDisk(token, vk_user_id).ya_upload(upload_photo)