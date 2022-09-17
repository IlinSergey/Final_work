import requests
import config
import json
import os
from tqdm import tqdm


class VkAgent:
    def __init__(self, token: str, id: str):
        self.token = token
        self.id = id

    def get_response(self, url, params):
        return requests.get(url, params=params).json()

    def get_link(self, response, i=int):
        return response['response']['items'][i]['sizes'][-1]['url']

    def get_photo(self, count: int):

        url = 'https://api.vk.com/method/photos.get'
        params = {
            'owner_id': self.id,
            'album_id': 'profile',
            'extended': '1',
            'photo_sizes': '1',
            'rev': '1',
            'access_token': self.token,
            'v': '5.131'
        }
        photo_list = []
        response = self.get_response(url, params)
        for i in range(count):
            file_name = response['response']['items'][i]['likes']['count']
            link = self.get_link(response, i)
            photo_info = {}
            photo_info['file_name'] = file_name
            photo_info['size'] = response['response']['items'][i]['sizes'][-1]['type']
            photo_list.append(photo_info)
            f = open(f'backup\{file_name}.jpg', 'wb')
            ufr = requests.get(link)
            f.write(ufr.content)
            f.close()
        with open(r'backup\files_log.json', 'w') as f:
            f.write(json.dumps(photo_list))
        print('Фото скачаны')

class YaUploader:
    files_url = 'https://cloud-api.yandex.net/v1/disk/resources/files'
    upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
    def __init__(self, token: str):
        self.token = token
    def get_header(self):
        return{'Content-Type': 'application/json',
               'Authorization': f'OAuth {self.token}'}

    def convert_path_to_url(self, path_to_file):
        simbols = {' ': '%20', '"': '%22', '&': '%26', '\\': '%5c', ':': '%5C', '=': '%3D'}
        path_to_file_url = path_to_file
        for k, v in simbols.items():
            if k in path_to_file:
                path_to_file_url = path_to_file_url.replace(k, v)
        return path_to_file_url

    def get_upload_link(self, path_to_file):
        path_to_file_url = self.convert_path_to_url(path_to_file)
        params = {'path': path_to_file_url, 'overwrite': 'True'}
        response = requests.get(self.upload_url, params=params, headers=self.get_header()).json()
        return response
    def upload(self, path_to_file: str):
        """Метод загружает файл на яндекс диск"""
        href = self.get_upload_link(path_to_file).get('href')
        if not href:
            return print(f'Ошибка, ссылка не получена! {self.get_upload_link(path_to_file)["message"]}')

        with open(path_to_file, 'rb') as file:
            try:
                requests.put(href, data=file)
            except KeyError:
                print(f'Файл не загружен, ошибка: {self.get_upload_link(path_to_file)["message"]}')

    def vk_photo_backup(self, cout_photo: int):
        vk.get_photo(cout_photo)
        file_list = os.listdir(r'backup')
        for file in tqdm(file_list):
            path = f'backup\\{file}'
            uploader.upload(path)
        print('Файлы успешно загружены')



uploader = YaUploader(config.yandex_token)
vk = VkAgent(config.vk_token, '11606581')

uploader.vk_photo_backup(10)
