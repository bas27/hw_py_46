import requests
from pprint import pprint

TOKEN = ''


class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_header(self):
        return {
            'Content-Type': 'application/json', 
            'Authorization': f'OAuth {self.token}'
            }

    def get_upload_link(self, ya_path):
        """ya_path - путь к файлу на Ядиске"""
        
        uload_url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        params = {'path': ya_path, 'overwrite': 'true'}
        resp = requests.get(uload_url, params=params, headers=self.get_header()).json()
        # pprint(resp)
        return resp

    def upload(self, ya_path, file_path: str):
        """file_path - путь к файлу на нашем ПК"""
        
        href = self.get_upload_link(ya_path=ya_path).get("href", "")
        resp = requests.put(href, data=open(file_path, 'rb'))
        resp.raise_for_status()
        if resp.status_code == 201:
            print("Скопировали")
       


if __name__ == '__main__':
    uploader = YaUploader(token=TOKEN)

    uploader.upload('/my_test/Провода1.docx', 'C:/Users/baldin.as/Documents/220в провода.docx')