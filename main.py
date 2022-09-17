import requests
import config
from pprint import pprint

class VkAgent:
    def __init__(self, token:str, id:str):
        self.token = token
        self.id = id

    def get_response(self, url, params):
        return requests.get(url, params=params).json()



    def get_link(self,response, i=int):
        return response['response']['items'][i]['sizes'][-1]['url']


    def get_photo(self, count:int):

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
        response = self.get_response(url, params)
        #pprint(response)
        for i in range(count):
            file_name = response['response']['items'][i]['likes']['count']
            link = self.get_link(response, i)
            f = open(f'backup\{file_name}.jpg', 'wb')
            ufr = requests.get(link)
            f.write(ufr.content)
            f.close()
        print('Фото скачены')

token = config.vk_token
vk = VkAgent(token, '11606581')
vk.get_photo(5)


